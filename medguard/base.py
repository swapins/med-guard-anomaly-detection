from abc import ABC, abstractmethod
from typing import Tuple


class BaseDetector(ABC):
    """
    Abstract base class for anomaly detection strategies.
    """

    @abstractmethod
    def update(self, value: float) -> None:
        pass

    @abstractmethod
    def analyze(self, value: float) -> Tuple[bool, float]:
        pass
