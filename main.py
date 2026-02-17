import sys
import random
import logging
from typing import Dict

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from medguard.config import MedGuardConfig, SignalConfig
from medguard.inference import MultiVitalInference
from medguard.ui.dashboard import VitalDashboard


# ----------------------------
# Simulated Multi-Vital Stream
# ----------------------------

def simulated_vitals() -> Dict[str, float]:
    """
    Generates synthetic physiological signals for research simulation.
    Uses realistic ranges for each vital sign.
    Occasional anomaly spikes are introduced probabilistically.
    """

    def spike(prob, normal_range, anomaly_range):
        """Generate normal or anomalous value with given probability."""
        if random.random() < prob:
            return random.uniform(*anomaly_range)
        return random.uniform(*normal_range)

    return {
        "heart_rate": spike(0.05, (60, 100), (120, 160)),           # Normal: 60-100 bpm
        "spo2": spike(0.05, (95, 99), (85, 92)),                    # Normal: 95-99 %
        "respiratory_rate": spike(0.05, (12, 20), (28, 40)),        # Normal: 12-20 /min
        "systolic_bp": spike(0.05, (110, 130), (160, 200)),         # Normal: 110-130 mmHg
        "temperature": round(spike(0.05, (36.5, 37.5), (38.5, 40.5)), 1),  # Normal: 36.5-37.5 °C
    }


# ----------------------------
# Main Application
# ----------------------------

class MedGuardApp:

    def __init__(self):

        logging.info("Initializing Med-Guard Multi-Vital Research System")

        # Configure multi-signal detectors
        config = MedGuardConfig(
            heart_rate=SignalConfig(window_size=15, threshold=2.0),
            spo2=SignalConfig(window_size=15, threshold=2.0),
            respiratory_rate=SignalConfig(window_size=15, threshold=2.0),
            systolic_bp=SignalConfig(window_size=15, threshold=2.0),
            temperature=SignalConfig(window_size=15, threshold=2.0),
        )

        self.engine = MultiVitalInference(config)

        self.app = QApplication(sys.argv)
        self.dashboard = VitalDashboard()
        self.dashboard.show()

        # QTimer for non-blocking update loop (1 second interval)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loop)
        self.timer.start(1000)

    def update_loop(self):
        """
        Periodic update loop triggered by QTimer.
        Simulates incoming vitals and updates inference + UI.
        """

        vitals = simulated_vitals()
        results = self.engine.analyze(vitals)

        self.dashboard.update_vitals(results)

        for vital, (is_anomaly, score) in results.items():
            if is_anomaly:
                logging.info(
                    f"[ANOMALY] {vital} | score={score:.3f}"
                )

    def run(self):
        sys.exit(self.app.exec_())


# ----------------------------
# Entry Point
# ----------------------------

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    application = MedGuardApp()
    application.run()
