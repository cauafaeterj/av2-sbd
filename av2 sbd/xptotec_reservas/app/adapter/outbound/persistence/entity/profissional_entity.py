from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class ProfissionalEntity(Base):

    __tablename__ = "profissionais"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    especialidades: Mapped[str] = mapped_column(String(255), nullable=False)
