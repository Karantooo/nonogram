from abc import ABC, abstractmethod

class InterfazAnimacionVD(ABC):
    @abstractmethod
    def imprimir(self) -> None:
        pass
