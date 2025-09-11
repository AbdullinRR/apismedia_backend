import httpx

from src.config import settings

HEADERS = {
    "Authorization": f"Bearer {settings.EASYCLINIC_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


async def get_branches():
    async with httpx.AsyncClient(base_url=settings.EASYCLINIC_BASE_URL) as client:
        r = await client.get("/appointment_book/branches", headers=HEADERS)
        r.raise_for_status()
        return r.json()


async def get_specialties(filial_id: int | None = None):
    params = {"filial_id": filial_id} if filial_id else None
    async with httpx.AsyncClient(base_url=settings.EASYCLINIC_BASE_URL) as client:
        r = await client.get("/appointment_book/specialties", headers=HEADERS, params=params)
        r.raise_for_status()
        return r.json()


async def get_doctors(speciality: str | None = None, filial_id: int | None = None):
    params = {}
    if speciality:
        params["speciality"] = speciality
    if filial_id:
        params["filial_id"] = filial_id
    async with httpx.AsyncClient(base_url=settings.EASYCLINIC_BASE_URL) as client:
        r = await client.get("/appointment_book/doctors", headers=HEADERS, params=params or None)
        r.raise_for_status()
        return r.json()


async def get_available_times(
    doctor_id: int | None = None,
    speciality: str | None = None,
    filial_id: int | None = None,
    services: bool = False,
    months: int = 1,
):
    params = {"services": services, "months": months}
    if doctor_id:
        params["doctor_id"] = doctor_id
    if speciality:
        params["speciality"] = speciality
    if filial_id:
        params["filial_id"] = filial_id
    async with httpx.AsyncClient(base_url=settings.EASYCLINIC_BASE_URL) as client:
        r = await client.get("/appointment_book/available-times", headers=HEADERS, params=params)
        r.raise_for_status()
        return r.json()