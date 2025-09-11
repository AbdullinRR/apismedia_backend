from fastapi import APIRouter
from src.domain.synchron.sync_bl import SyncBL


router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/sync")
async def run_sync():
    """
    Полный синк из EasyClinic в БД.
    """
    res = await SyncBL.sync_all()
    return {"status": "ok", "details": res}