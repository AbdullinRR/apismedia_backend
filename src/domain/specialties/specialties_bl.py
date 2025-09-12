from src.core.entities.specialties import Speciality
from src.domain.specialties.specialties_dal import SpecialityDAL
from src.utils.result import Result


class SpecialityBL:
    @staticmethod
    async def add_specialties(specialties: list[Speciality]) -> Result[bool, str]:
        return await SpecialityDAL.add_specialties(specialties)