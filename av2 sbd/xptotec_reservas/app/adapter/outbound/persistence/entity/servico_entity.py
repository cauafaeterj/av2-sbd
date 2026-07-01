from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class ServicoEntity(Base):

    __tablename__ = "servicos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    especialidade: Mapped[str] = mapped_column(String(50), nullable=False)
    duracao_minutos: Mapped[int] = mapped_column(Integer, nullable=False)
    preco: Mapped[Numeric] = mapped_column(Numeric(12, 2), nullable=False)
