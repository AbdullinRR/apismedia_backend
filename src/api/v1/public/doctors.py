from fastapi import APIRouter, Query

router = APIRouter(prefix="/public/doctors", tags=["public: doctors"])

@router.get("")
async def list_doctors(
    filial_id: int | None = Query(default=None),
    speciality_id: int | None = Query(default=None),
):
    # заглушка
    doctors = [
        {
            "id": 1001,
            "full_name": "Иванов Иван Иванович",
            "filial_id": 1,
            "is_active": True,
            "photo_url": None,
            "education": "КГМУ",
            "about": "Опыт 10 лет",
            "specialities": [{"id": 1, "name": "cardiology", "correct_name": "Кардиология"}],
            "documents": [],
        },
        {
            "id": 1002,
            "full_name": "Петров Петр Петрович",
            "filial_id": 2,
            "is_active": True,
            "photo_url": None,
            "education": "КГМУ",
            "about": "Опыт 5 лет",
            "specialities": [{"id": 2, "name": "ophthalmology", "correct_name": "Офтальмология"}],
            "documents": [],
        },
    ]
    if filial_id is not None:
        doctors = [d for d in doctors if d["filial_id"] == filial_id]
    if speciality_id is not None:
        doctors = [d for d in doctors if any(s["id"] == speciality_id for s in d["specialities"])]
    return doctors

@router.get("/{doctor_id}")
async def get_doctor(doctor_id: int):
    # заглушка
    return {
        "id": doctor_id,
        "full_name": "Иванов Иван Иванович",
        "filial_id": 1,
        "is_active": True,
        "photo_url": None,
        "education": "КГМУ",
        "about": "Опыт 10 лет",
        "specialities": [{"id": 1, "name": "cardiology", "correct_name": "Кардиология"}],
        "documents": [
            {"id": 1, "doctor_id": doctor_id, "file_url": "https://example.com/cert1.jpg", "description": "Сертификат"},
        ],
    }
