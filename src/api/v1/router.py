from fastapi import APIRouter

# public
from src.api.v1.public import branches as pub_branches
from src.api.v1.public import specialties as pub_specialties
from src.api.v1.public import doctors as pub_doctors
from src.api.v1.public import slots as pub_slots

# admin
from src.api.v1.admin import easyclinic as adm_easyclinic
from src.api.v1.admin import sync as sync_easyclinic


router = APIRouter()

# v1/public
router.include_router(pub_branches.router, prefix="/api/v1")
router.include_router(pub_specialties.router, prefix="/api/v1")
router.include_router(pub_doctors.router, prefix="/api/v1")
router.include_router(pub_slots.router, prefix="/api/v1")

# v1/admin
router.include_router(adm_easyclinic.router, prefix="/api/v1")
router.include_router(sync_easyclinic.router, prefix="/api/v1")
