from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class NoShowResponse(BaseModel):

    reserva_id: UUID = Field(..., alias="reservaId")
    status: str
    valor_retido: Decimal = Field(..., alias="valorRetido")
    credito_gerado: Decimal = Field(..., alias="creditoGerado")
    credito_total_cliente: Decimal = Field(..., alias="creditoTotalCliente")
    mensagem: str

    model_config = {"populate_by_name": True}
