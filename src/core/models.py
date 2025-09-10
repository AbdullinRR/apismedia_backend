from __future__ import annotations

from sqlalchemy import (
    String,
    BigInteger,
    ForeignKey,
    Boolean,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy

from src.core.database import Base


class DoctorSpecialityBase(Base):
    """
    Связь врач - специальность.
    """
    __tablename__ = "doctor_speciality"

    doctor_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("doctors.id", ondelete="CASCADE"), primary_key=True
    )
    speciality_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("specialities.id", ondelete="CASCADE"), primary_key=True
    )

    doctor: Mapped["DoctorBase"] = relationship(back_populates="speciality_links")
    speciality: Mapped["SpecialityBase"] = relationship(back_populates="doctor_links")


class FilialSpecialityBase(Base):
    """
    Связь филиал - специальность.
    """
    __tablename__ = "filial_speciality"

    filial_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("branches.id", ondelete="CASCADE"), primary_key=True
    )
    speciality_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("specialities.id", ondelete="CASCADE"), primary_key=True
    )

    branch: Mapped["BranchBase"] = relationship(back_populates="speciality_links")
    speciality: Mapped["SpecialityBase"] = relationship(back_populates="branch_links")


class BranchBase(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    # "красивое" поле для показа на сайте
    address: Mapped[str] = mapped_column(String, nullable=True)

    doctors: Mapped[list["DoctorBase"]] = relationship(
        back_populates="branch",
        cascade="all,delete",
        passive_deletes=True,
    )

    speciality_links: Mapped[list["FilialSpecialityBase"]] = relationship(
        back_populates="branch",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    specialities = association_proxy("speciality_links", "speciality")


class SpecialityBase(Base):
    __tablename__ = "specialities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    # "красивое" поле для показа на сайте
    correct_name: Mapped[str] = mapped_column(String, nullable=False)

    doctor_links: Mapped[list["DoctorSpecialityBase"]] = relationship(
        back_populates="speciality",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    branch_links: Mapped[list["FilialSpecialityBase"]] = relationship(
        back_populates="speciality",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    doctors = association_proxy("doctor_links", "doctor")
    branches = association_proxy("branch_links", "branch")


class DoctorBase(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    filial_id: Mapped[int] = mapped_column(ForeignKey("branches.id", ondelete="SET NULL"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="True", nullable=False)

    photo_url: Mapped[str] = mapped_column(String, nullable=True)
    education: Mapped[str] = mapped_column(String, nullable=True)
    about: Mapped[str] = mapped_column(Text, nullable=True)

    branch: Mapped["BranchBase"] = relationship(back_populates="doctors")

    speciality_links: Mapped[list["DoctorSpecialityBase"]] = relationship(
        back_populates="doctor",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    specialities = association_proxy("speciality_links", "speciality")
    documents: Mapped[list["DoctorDocumentBase"]] = relationship(
        back_populates="doctor",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class DoctorDocumentBase(Base):
    """
    Класс для хранения информации о документах доктора
    """
    __tablename__ = "doctor_documents"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id", ondelete="CASCADE"), index=True)
    file_url: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    doctor: Mapped["DoctorBase"] = relationship(back_populates="documents")



