from __future__ import annotations

from typing import Iterable

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import (
    BranchBase,
    SpecialityBase,
    DoctorBase,
    DoctorSpecialityBase,
    FilialSpecialityBase,
)
from src.core.database import connection
from src.utils.normalize import norm_spec_name


class SyncDAL:
    @staticmethod
    async def _fetch_all_branches_map(session: AsyncSession) -> dict[int, BranchBase]:
        rows = (await session.execute(sa.select(BranchBase))).scalars().all()
        return {b.id: b for b in rows}

    @staticmethod
    @connection
    async def upsert_branches(filials: list[dict], session: AsyncSession) -> dict:
        """
        filials: [{"id": int, "title": str}, ...]
        """
        existing = await SyncDAL._fetch_all_branches_map(session)
        created = 0
        updated = 0

        for item in filials or []:
            bid = int(item["id"])
            title = item.get("title") or ""
            obj = existing.get(bid)
            if obj is None:
                session.add(BranchBase(id=bid, title=title))
                created += 1
            else:
                if obj.title != title:
                    obj.title = title
                    updated += 1

        await session.commit()
        return {"branches_created": created, "branches_updated": updated}

    @staticmethod
    async def _fetch_all_specialities_map(session: AsyncSession) -> dict[str, SpecialityBase]:
        """
        Ключ = нормализованное имя (norm_spec_name(existing.name)).
        """
        rows = (await session.execute(sa.select(SpecialityBase))).scalars().all()
        return {norm_spec_name(s.name): s for s in rows}

    @staticmethod
    @connection
    async def upsert_specialities(all_specs: Iterable[str], session: AsyncSession) -> dict:
        """
        all_specs: ["Врач-кардиолог", ...] — «грязные» названия из EC (без филиала)
        """
        existing = await SyncDAL._fetch_all_specialities_map(session)
        created = 0

        for raw in all_specs or []:
            key = norm_spec_name(raw)
            if not key:
                continue
            if key in existing:
                continue
            # пока correct_name = как пришло; админ позже отредактирует
            obj = SpecialityBase(name=raw, correct_name=raw)
            session.add(obj)
            created += 1

        await session.commit()
        return {"specialities_created": created}


    @staticmethod
    @connection
    async def replace_filial_specialities(
        filial_id: int,
        spec_names: Iterable[str],
        session: AsyncSession,
    ) -> dict:
        """
        Полная пересборка связей филиала по текущему списку из EC.
        """
        # текущие спец-объекты
        all_specs = await SyncDAL._fetch_all_specialities_map(session)

        # нормализуем входные имена → ищем id
        spec_ids: set[int] = set()
        for raw in spec_names or []:
            key = norm_spec_name(raw)
            if not key:
                continue
            spec = all_specs.get(key)
            if spec:
                spec_ids.add(spec.id)

        # сносим старые
        await session.execute(
            sa.delete(FilialSpecialityBase).where(FilialSpecialityBase.filial_id == filial_id)
        )
        # вставляем новые
        for sid in spec_ids:
            session.add(FilialSpecialityBase(filial_id=filial_id, speciality_id=sid))

        await session.commit()
        return {"filial_id": filial_id, "filial_specialities": len(spec_ids)}

    @staticmethod
    async def _fetch_all_doctors_ids(session: AsyncSession) -> set[int]:
        rows = (await session.execute(sa.select(DoctorBase.id))).scalars().all()
        return set(int(x) for x in rows)

    @staticmethod
    @connection
    async def upsert_doctors_with_specialities(
        aggregated: dict[int, dict],  # doctor_id -> {"full_name", "primary_filial_id", "spec_names": set[str]}
        session: AsyncSession,
    ) -> dict:
        """
        Агрегированный словарь по всем филиалам и специям.
        """
        # карты для быстрых операций
        existing_ids = await SyncDAL._fetch_all_doctors_ids(session)
        specs_map = await SyncDAL._fetch_all_specialities_map(session)

        created = 0
        updated = 0
        links_rebuilt = 0

        # upsert doctors
        for did, payload in aggregated.items():
            full_name: str = payload["full_name"]
            primary_filial_id: int | None = payload.get("primary_filial_id")
            spec_names: set[str] = payload.get("spec_names", set())

            if did not in existing_ids:
                session.add(
                    DoctorBase(
                        id=did,
                        full_name=full_name,
                        filial_id=primary_filial_id,
                        is_active=True,
                        # наши поля не трогаем: photo_url / education / about остаются NULL
                    )
                )
                created += 1
            else:
                # обновим только если есть изменения
                obj: DoctorBase = await session.get(DoctorBase, did)
                changed = False
                if obj.full_name != full_name:
                    obj.full_name = full_name
                    changed = True
                if primary_filial_id is not None and obj.filial_id != primary_filial_id:
                    obj.filial_id = primary_filial_id
                    changed = True
                if obj.is_active is False:
                    obj.is_active = True
                    changed = True
                if changed:
                    updated += 1

            await session.execute(sa.delete(DoctorSpecialityBase).where(DoctorSpecialityBase.doctor_id == did))
            cnt = 0
            for raw in sorted(spec_names):  # стабильный порядок не обязателен, просто «красиво»
                key = norm_spec_name(raw)
                spec = specs_map.get(key)
                if not spec:
                    continue
                session.add(DoctorSpecialityBase(doctor_id=did, speciality_id=spec.id))
                cnt += 1
            if cnt:
                links_rebuilt += 1

        # деактивация тех, кого EC не вернул
        seen_ids = set(aggregated.keys())
        gone_ids = list(existing_ids - seen_ids)
        if gone_ids:
            await session.execute(
                sa.update(DoctorBase).where(DoctorBase.id.in_(gone_ids)).values(is_active=False)
            )

        await session.commit()
        return {
            "doctors_created": created,
            "doctors_updated": updated,
            "doctors_deactivated": len(gone_ids),
            "doctor_spec_links_rebuilt": links_rebuilt,
        }
