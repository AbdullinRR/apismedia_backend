import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import connection
from src.core.entities.specialties import Speciality
from src.core.models import SpecialityBase
from src.utils.result import Result


logger = logging.getLogger(__name__)


class SpecialityDAL:
    @staticmethod
    @connection
    async def add_specialties(specialties: list[Speciality], session: AsyncSession) -> Result[bool, str]:
        try:
            specialties_db = await session.execute(
                select(SpecialityBase)
            )

            specialties_names = [speciality.name for speciality in specialties_db]

            for speciality_orm in specialties:
                if speciality_orm.name not in specialties_names:
                    session.add(speciality_orm)

            await session.commit()

            return Result.success(True)

        except Exception as e:
            logger.info(f"SpecialtyDAL.add_specialties({e})")
            return Result.failure(str(e))

