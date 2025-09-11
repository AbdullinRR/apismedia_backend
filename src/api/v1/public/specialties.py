from fastapi import APIRouter, Query

router = APIRouter(prefix="/public/specialties", tags=["public: specialties"])

@router.get("")
async def list_specialties(filial_id: int | None = Query(default=None)):
    # заглушка
    base = [
        {"id": 1, "name": "cardiology", "correct_name": "Кардиология"},
        {"id": 2, "name": "ophthalmology", "correct_name": "Офтальмология"},
    ]
    if filial_id:
        return base[:1]
    return base