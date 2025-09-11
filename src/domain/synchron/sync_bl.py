from __future__ import annotations

from typing import Dict, Set

from src.utils import easyclinic
from src.domain.synchron.sync_dal import SyncDAL


class SyncBL:

    @staticmethod
    async def sync_all() -> dict:
        """
        Полный синк: филиалы -> все спец-сти -> связи филиал-спец -> врачи (+связи).
        """
        result: dict = {}

        # 1) branches
        branches_resp = await easyclinic.get_branches()
        filials = branches_resp.get("filials", []) if isinstance(branches_resp, dict) else branches_resp
        res_br = await SyncDAL.upsert_branches(filials)
        result.update(res_br)

        # 2) global specialties (без filial_id)
        specs_resp = await easyclinic.get_specialties()
        all_specs = specs_resp.get("specialities", []) if isinstance(specs_resp, dict) else specs_resp
        res_sp = await SyncDAL.upsert_specialities(all_specs)
        result.update(res_sp)

        # 3) filial_speciality для каждого филиала
        for f in filials:
            fid = int(f["id"])
            one_resp = await easyclinic.get_specialties(filial_id=fid)
            names = one_resp.get("specialities", []) if isinstance(one_resp, dict) else one_resp
            res_fs = await SyncDAL.replace_filial_specialities(fid, names)
            # можно копить метрики по каждому филиалу, но для краткости пропустим

        # 4) doctors (идём по филиалам и агрегируем)
        aggregated: Dict[int, dict] = {}
        for f in filials:
            fid = int(f["id"])
            docs_resp = await easyclinic.get_doctors(filial_id=fid)
            docs_arr = docs_resp.get("doctors", []) if isinstance(docs_resp, dict) else docs_resp

            for row in docs_arr:
                did = int(row["id"])
                full_name = row.get("fio") or ""
                # "34,84" -> берём первую как ты просил
                filials_str = (row.get("filials") or "").strip()
                primary_filial_id = None
                if filials_str:
                    first = filials_str.split(",")[0].strip()
                    if first.isdigit():
                        primary_filial_id = int(first)

                spec_name = row.get("speciality") or ""

                agg = aggregated.get(did)
                if not agg:
                    aggregated[did] = {
                        "full_name": full_name,
                        "primary_filial_id": primary_filial_id,
                        "spec_names": set([spec_name]) if spec_name else set(),
                    }
                else:
                    # слить спецы и не затирать ранее выбранный primary_filial_id
                    if spec_name:
                        cast_set: Set[str] = agg["spec_names"]
                        cast_set.add(spec_name)
                    # первичный филиал уже выбран из первой встречи
                    # если вдруг ранее None, можем проставить
                    if agg.get("primary_filial_id") is None and primary_filial_id is not None:
                        agg["primary_filial_id"] = primary_filial_id

        res_docs = await SyncDAL.upsert_doctors_with_specialities(aggregated)
        result.update(res_docs)

        return result
