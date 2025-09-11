from fastapi import APIRouter

router = APIRouter(prefix="/public/branches", tags=["public: branches"])

@router.get("")
async def list_branches():
    return [
        {"id": 1, "title": "Главный филиал", "address": "г. Казань, ул. Пример, 1"},
        {"id": 2, "title": "Филиал №2", "address": "г. Казань, ул. Вторая, 2"},
    ]