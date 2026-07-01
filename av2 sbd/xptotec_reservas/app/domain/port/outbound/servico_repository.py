from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.domain.model.servico import Servico


class ServicoRepository(ABC):

    @abstractmethod
    def buscar_por_ids(self, ids: List[UUID]) -> List[Servico]:
        ...
