from typing import Tuple, Deque
from collections import deque
import statistics

from medguard.base import BaseDetector


class MADDetector(BaseDetector):
    """
    Median Absolute Deviation based anomaly detector.
    More robust to outliers than Z-score.
    """

    def __init__(self, window_size: int, threshold: float):
        self.window_size = window_size
        self.threshold = threshold
        self.window: Deque[float] = deque(maxlen=window_size)

    def update(self, value: float) -> None:
        self.window.append(value)

    def analyze(self, value: float) -> Tuple[bool, float]:
        if len(self.window) < self.window_size:
            self.update(value)
            return False, 0.0

        median = statistics.median(self.window)
        deviations = [abs(x - median) for x in self.window]
        mad = statistics.median(deviations)

        if mad == 0:
            self.update(value)
            return False, 0.0

        modified_z = 0.6745 * (value - median) / mad
        is_anomaly = abs(modified_z) > self.threshold

        self.update(value)
        return is_anomaly, modified_z
