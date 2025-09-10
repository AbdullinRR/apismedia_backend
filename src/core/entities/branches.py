from typing import Optional
from pydantic import BaseModel, ConfigDict


class Branch(BaseModel):
    """
    Pydantic модель для филиала
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    # "красивое" поле для показа на сайте
    address: Optional[str] = None