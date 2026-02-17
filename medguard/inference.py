from typing import Dict, Tuple
from medguard.config import MedGuardConfig
from medguard.detectors.zscore import ZScoreDetector
from medguard.detectors.mad import MADDetector


class MultiVitalInference:

    def __init__(self, config: MedGuardConfig):
        self.detectors = {
            "heart_rate": self._build_detector(config.heart_rate),
            "spo2": self._build_detector(config.spo2),
            "respiratory_rate": self._build_detector(config.respiratory_rate),
            "systolic_bp": self._build_detector(config.systolic_bp),
            "temperature": self._build_detector(config.temperature),
        }

    def _build_detector(self, signal_config):
        if signal_config.detector_type == "mad":
            return MADDetector(signal_config.window_size, signal_config.threshold)
        return ZScoreDetector(signal_config.window_size, signal_config.threshold)

    def analyze(self, vitals: Dict[str, float]) -> Dict[str, Tuple[bool, float]]:
        results = {}

        for key, value in vitals.items():
            detector = self.detectors.get(key)
            if detector:
                results[key] = detector.analyze(value)

        return results
