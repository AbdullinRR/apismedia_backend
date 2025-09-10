from typing import Optional
from pydantic import BaseModel, ConfigDict


class DoctorDocument(BaseModel):
    """
    Pydantic модель для документа врача
    """
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    doctor_id: int
    file_url: Optional[str]
    description: Optional[str] = None