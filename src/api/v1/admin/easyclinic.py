from fastapi import APIRouter, Query, HTTPException
from src.utils import easyclinic

router = APIRouter(prefix="/admin/easyclinic", tags=["admin: easyclinic"])


@router.get("/branches")
async def branches():
    return await easyclinic.get_branches()


@router.get("/specialties")
async def specialties(filial_id: int | None = Query(default=None)):
    return await easyclinic.get_specialties(filial_id)


@router.get("/doctors")
async def doctors(
    speciality: str | None = Query(default=None),
    filial_id: int | None = Query(default=None),
):
    return await easyclinic.get_doctors(speciality=speciality, filial_id=filial_id)


@router.get("/available-times")
async def available_times(
    doctor_id: int | None = Query(default=None),
    speciality: str | None = Query(default=None),
    filial_id: int | None = Query(default=None),
    services: bool = Query(default=False),
    months: int = Query(default=1, ge=1, le=6),
):
    if bool(doctor_id) == bool(speciality):
        raise HTTPException(status_code=400, detail="укажите либо doctor_id, либо speciality")

    return await easyclinic.get_available_times(
        doctor_id=doctor_id,
        speciality=speciality,
        filial_id=filial_id,
        services=services,
        months=months,
    )
