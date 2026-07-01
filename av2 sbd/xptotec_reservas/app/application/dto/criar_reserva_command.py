from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID


@dataclass(frozen=True)
class CriarReservaCommand:

    cliente_id: UUID
    profissional_id: Optional[UUID]
    servico_ids: List[UUID] = field(default_factory=list)
    horario_inicio: Optional[datetime] = None

    def __post_init__(self):
        if self.cliente_id is None:
            raise ValueError("clienteId é obrigatório.")
        if not self.servico_ids:
            raise ValueError("Pelo menos um serviço deve ser informado.")
        if self.horario_inicio is None:
            raise ValueError("horarioInicio é obrigatório.")
