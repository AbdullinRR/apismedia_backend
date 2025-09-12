from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import connection
from src.core.entities.branches import Branch
from src.core.models import BranchBase
from src.utils.result import Result


class BranchesDAL:
    @staticmethod
    @connection
    async def add_branches(branches: list[Branch], session: AsyncSession) -> Result[bool, str]:
        try:
            branches_bd = await session.execute(select(BranchBase))

            branches_id = [branch.id for branch in branches_bd]

            for branch in branches:
                if branch.id not in branches_id:
                    session.add(branch)

            await session.commit()

            return Result.success(True)

        except Exception as e:
            return Result.error(e)