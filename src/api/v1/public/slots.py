from fastapi import APIRouter, Query

router = APIRouter(prefix="/public/doctors", tags=["public: slots"])

@router.get("/{doctor_id}/slots")
async def doctor_slots(
    doctor_id: int,
    months: int = Query(default=1, ge=1, le=6),
    filial_id: int | None = Query(default=None),
):
    # заглушка расписания (как будто EasyClinic)
    return {
        "doctor_id": doctor_id,
        "days": [
            {"date": "2025-09-12", "filial": {"id": filial_id or 1, "title": "Главный филиал"}, "times": ["10:00", "10:30"]},
            {"date": "2025-09-13", "filial": {"id": filial_id or 1, "title": "Главный филиал"}, "times": ["11:00"]},
        ],
        "services": [],
    }
