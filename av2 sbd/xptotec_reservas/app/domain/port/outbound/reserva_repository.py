from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.domain.model.reserva import Reserva
from app.domain.model.slot_horario import SlotHorario


class ReservaRepository(ABC):

    @abstractmethod
    def salvar(self, reserva: Reserva) -> Reserva:
        ...

    @abstractmethod
    def buscar_por_id(self, id: UUID) -> Optional[Reserva]:
        ...

    @abstractmethod
    def buscar_slots_por_profissional_e_periodo(
        self, profissional_id: UUID, inicio: datetime, fim: datetime
    ) -> List[SlotHorario]:
        ...
