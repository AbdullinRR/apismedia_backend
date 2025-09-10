from sqlalchemy.orm import Mapped, mapped_column, relationship


from .database import Base


class DoctorBase(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)