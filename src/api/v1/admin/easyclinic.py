from fastapi import APIRouter, Query, HTTPException

from src.core.entities.branches import Branch
from src.core.entities.specialties import Speciality
from src.domain.branches.branshes_bl import BranchesBL
from src.domain.specialties.specialties_bl import SpecialityBL
from src.domain.specialties.specialties_dal import SpecialityDAL
from src.utils import easyclinic
from src.utils.result import Result

router = APIRouter(prefix="/admin/easyclinic", tags=["admin: easyclinic"])


@router.get("/branches")
async def branches():
    branches_data = await easyclinic.get_branches()

    branches_orm = []
    for branch in branches_data:
        branches_orm.append(Branch(
            id=branch["id"],
            title=branch["title"]
        ))

    result = await BranchesBL.add_branches(branches_orm)
    if not result.ok:
        return {
            "success": False,
        }

    return {
        "success": True,
    }


@router.post("/specialties")
async def add_specialties():
    specialties_data = await easyclinic.get_specialties()

    specialties_orm = []
    for speciality in specialties_data:
        specialties_orm.append(Speciality(
            name=speciality["name"],
        ))

    result = await SpecialityBL.add_specialties(specialties_orm)
    if not result.ok:
        return {
            "success": False,
        }

    return {
        "success": True,
    }



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
