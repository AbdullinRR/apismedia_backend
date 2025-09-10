from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from src.core.entities.specialties import Speciality
from src.core.entities.doctor_documents import DoctorDocument


class Doctor(BaseModel):
    """
    Pydantic модель для врача
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    filial_id: int
    is_active: bool = True

    photo_url: Optional[str] = None
    education: Optional[str] = None
    about: Optional[str] = None

    specialities: List[Speciality] = []
    documents: List[DoctorDocument] = []
