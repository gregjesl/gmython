from abc import ABC, abstractmethod

class Resource(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def to_gmat_script(self) -> str:
        pass