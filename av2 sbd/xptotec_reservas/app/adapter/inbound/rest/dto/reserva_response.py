from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ReservaResponse(BaseModel):

    id: UUID
    cliente_nome: str = Field(..., alias="clienteNome")
    profissional_nome: Optional[str] = Field(default=None, alias="profissionalNome")
    servicos: List[str]
    horario_inicio: datetime = Field(..., alias="horarioInicio")
    horario_fim: datetime = Field(..., alias="horarioFim")
    valor_total: Decimal = Field(..., alias="valorTotal")
    status: str

    model_config = {"populate_by_name": True}
