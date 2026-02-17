import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class VitalDashboard(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Med-Guard Research Dashboard")
        self.setGeometry(0, 0, 1024, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.labels = {}

        for vital in ["heart_rate", "spo2", "respiratory_rate", "systolic_bp", "temperature"]:
            label = QLabel(f"{vital}: --")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 28px;")
            self.layout.addWidget(label)
            self.labels[vital] = label

    def update_vitals(self, results):
        for vital, (is_anomaly, score) in results.items():
            color = "red" if is_anomaly else "green"
            self.labels[vital].setText(f"{vital}: {score:.2f}")
            self.labels[vital].setStyleSheet(f"font-size: 28px; color: {color};")
