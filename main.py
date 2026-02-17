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
    Occasional anomaly spikes are introduced probabilistically.
    """

    def spike(prob, normal_range, anomaly_range):
        if random.random() < prob:
            return random.randint(*anomaly_range)
        return random.randint(*normal_range)

    return {
        "heart_rate": spike(0.05, (70, 85), (130, 150)),
        "spo2": spike(0.05, (95, 99), (85, 90)),
        "respiratory_rate": spike(0.05, (14, 18), (25, 35)),
        "systolic_bp": spike(0.05, (110, 125), (160, 180)),
        "temperature": round(
            spike(0.05, (36, 37), (39, 40)) + random.random(), 1
        ),
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
