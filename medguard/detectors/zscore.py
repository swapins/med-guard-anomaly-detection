from typing import Tuple, Deque
from collections import deque
import math
import logging

from medguard.base import BaseDetector


class ZScoreDetector(BaseDetector):
    """
    Sliding-window Z-score detector using incremental statistics.
    """

    def __init__(self, window_size: int, threshold: float):
        self.window_size = window_size
        self.threshold = threshold
        self.window: Deque[float] = deque(maxlen=window_size)

        self.logger = logging.getLogger(__name__)

    def update(self, value: float) -> None:
        self.window.append(value)

    def _compute_stats(self) -> Tuple[float, float]:
        n = len(self.window)
        if n == 0:
            return 0.0, 0.0

        mean = sum(self.window) / n
        variance = sum((x - mean) ** 2 for x in self.window) / n
        std = math.sqrt(variance)

        return mean, std

    def analyze(self, value: float) -> Tuple[bool, float]:
        if len(self.window) < self.window_size:
            self.update(value)
            return False, 0.0

        mean, std = self._compute_stats()

        if std == 0:
            self.logger.debug("Zero standard deviation detected.")
            self.update(value)
            return False, 0.0

        z_score = (value - mean) / std
        is_anomaly = abs(z_score) > self.threshold

        self.update(value)
        return is_anomaly, z_score
