from src.core.entities.branches import Branch
from src.domain.branches.branches_dal import BranchesDAL
from src.utils.result import Result


class BranchesBL:
    @staticmethod
    async def add_branches(branches: list[Branch]) -> Result[bool, str]:
        return await BranchesDAL.add_branches(branches)