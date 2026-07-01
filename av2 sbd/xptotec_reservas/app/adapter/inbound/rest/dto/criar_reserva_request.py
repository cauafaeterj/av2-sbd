from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CriarReservaRequest(BaseModel):

    cliente_id: UUID = Field(..., alias="clienteId", description="clienteId é obrigatório")
    profissional_id: Optional[UUID] = Field(default=None, alias="profissionalId")
    servico_ids: List[UUID] = Field(
        ...,
        alias="servicoIds",
        min_length=1,
        description="Pelo menos um serviço deve ser informado",
    )
    horario_inicio: datetime = Field(..., alias="horarioInicio")

    model_config = {"populate_by_name": True}
