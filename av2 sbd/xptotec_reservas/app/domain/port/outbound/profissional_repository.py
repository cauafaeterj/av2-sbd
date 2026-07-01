from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.model.profissional import Profissional


class ProfissionalRepository(ABC):

    @abstractmethod
    def buscar_por_id(self, id: UUID) -> Optional[Profissional]:
        ...
