from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class ClienteEntity(Base):

    __tablename__ = "clientes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    telefone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    credito_disponivel: Mapped[Numeric] = mapped_column(
        Numeric(12, 2), nullable=False, default=0
    )
