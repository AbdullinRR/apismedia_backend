from pydantic import BaseModel, ConfigDict


class Speciality(BaseModel):
    """
    Pydantic модель для специальности
    """
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    name: str
    # "красивое" поле для показа на сайте
    correct_name: str = None
