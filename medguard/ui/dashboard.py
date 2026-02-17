import sys
from collections import deque
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import QPointF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class WaveformCanvas(FigureCanvasQTAgg):
    """Matplotlib canvas for waveform visualization."""
    
    def __init__(self, parent=None, vital_name="", buffer_size=100):
        self.vital_name = vital_name
        self.buffer_size = buffer_size
        self.data_buffer = deque(maxlen=buffer_size)
        self.time_buffer = deque(maxlen=buffer_size)
        self.time_counter = 0
        
        fig = Figure(figsize=(3, 1.5), dpi=100, facecolor='#1a1a2e')
        self.ax = fig.add_subplot(111, facecolor='#0f3460')
        self.ax.set_ylim(0, 100)
        self.ax.tick_params(colors='white', labelsize=8)
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.line, = self.ax.plot([], [], lw=2, color='#00d4ff')
        
        super().__init__(fig)
        self.setParent(parent)
    
    def update_data(self, value, is_anomaly=False):
        """Add new data point and update plot."""
        self.data_buffer.append(value)
        self.time_buffer.append(self.time_counter)
        self.time_counter += 1
        
        color = '#ff4444' if is_anomaly else '#00d4ff'  # Red for anomaly, cyan for normal
        self.line.set_color(color)
        self.line.set_data(list(self.time_buffer), list(self.data_buffer))
        
        if self.data_buffer:
            self.ax.set_ylim(min(self.data_buffer) - 5, max(self.data_buffer) + 5)
        
        self.draw_idle()


class VitalDashboard(QWidget):
    """Medical-grade dashboard for 8-inch touchscreen with waveforms."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Med-Guard | Clinical Monitoring System")
        
        # Optimize for 8-inch touchscreen (1024x768 typical)
        self.setGeometry(0, 0, 1024, 768)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
                color: white;
            }
            QLabel {
                color: white;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)
        
        # Header
        header = QLabel("Med-Guard Patient Monitor")
        header_font = QFont("Segoe UI", 18, QFont.Bold)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("background-color: #0f3460; padding: 10px; border-radius: 5px;")
        main_layout.addWidget(header)
        
        # Vitals Grid (2 columns x 3 rows for 5 vitals + status)
        grid = QGridLayout()
        grid.setSpacing(6)
        
        self.vital_cards = {}
        self.waveform_canvases = {}
        
        vitals_info = [
            ("heart_rate", "HR", "bpm", 0),
            ("spo2", "SpO₂", "%", 1),
            ("respiratory_rate", "RR", "/min", 2),
            ("systolic_bp", "SBP", "mmHg", 3),
            ("temperature", "Temp", "°C", 4),
        ]
        
        for vital, short_name, unit, idx in vitals_info:
            card = self._create_vital_card(vital, short_name, unit)
            self.vital_cards[vital] = card
            row = idx // 3
            col = idx % 3
            grid.addWidget(card, row, col)
        
        main_layout.addLayout(grid, 1)
        
        # Status bar
        status_layout = QHBoxLayout()
        self.status_label = QLabel("● MONITORING")
        self.status_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.status_label.setStyleSheet("color: #00ff00; padding: 8px;")
        status_layout.addWidget(self.status_label)
        
        self.alert_label = QLabel("No Alerts")
        self.alert_label.setFont(QFont("Segoe UI", 12))
        self.alert_label.setStyleSheet("color: #ffaa00;")
        status_layout.addWidget(self.alert_label)
        
        status_layout.addStretch()
        main_layout.addLayout(status_layout)
        
        self.setLayout(main_layout)
        self.alerts = []

    def _create_vital_card(self, vital_name, short_name, unit):
        """Create a vital sign card with waveform."""
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: #0f3460;
                border: 2px solid #16213e;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)
        
        # Vital name + value
        header_layout = QHBoxLayout()
        
        name_label = QLabel(short_name)
        name_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        name_label.setStyleSheet("color: #00d4ff;")
        header_layout.addWidget(name_label)
        
        value_label = QLabel("--")
        value_label.setFont(QFont("Courier", 14, QFont.Bold))
        value_label.setAlignment(Qt.AlignRight)
        value_label.setStyleSheet("color: #ffffff;")
        header_layout.addWidget(value_label)
        
        unit_label = QLabel(unit)
        unit_label.setFont(QFont("Segoe UI", 9))
        unit_label.setStyleSheet("color: #888888;")
        header_layout.addWidget(unit_label)
        
        layout.addLayout(header_layout)
        
        # Waveform canvas
        canvas = WaveformCanvas(card, vital_name, buffer_size=80)
        self.waveform_canvases[vital_name] = canvas
        layout.addWidget(canvas)
        
        # Status indicator (normal/anomaly)
        status = QLabel("✓ NORMAL")
        status.setFont(QFont("Segoe UI", 9, QFont.Bold))
        status.setAlignment(Qt.AlignCenter)
        status.setStyleSheet("color: #00ff00; padding: 4px;")
        layout.addWidget(status)
        
        card.setLayout(layout)
        
        # Store references for updates
        card.value_label = value_label
        card.status_label = status
        card.vital_name = vital_name
        
        return card

    def update_vitals(self, results):
        """Update all vital cards with new analysis results."""
        alerts_count = 0
        
        for vital, (is_anomaly, score) in results.items():
            if vital not in self.vital_cards:
                continue
            
            card = self.vital_cards[vital]
            
            # Update value display
            card.value_label.setText(f"{score:.1f}")
            
            # Update waveform
            if vital in self.waveform_canvases:
                self.waveform_canvases[vital].update_data(score, is_anomaly)
            
            # Update status
            if is_anomaly:
                card.status_label.setText("⚠ ANOMALY")
                card.status_label.setStyleSheet("color: #ff4444; padding: 4px; font-weight: bold;")
                alerts_count += 1
                if vital not in self.alerts:
                    self.alerts.append(vital)
            else:
                card.status_label.setText("✓ NORMAL")
                card.status_label.setStyleSheet("color: #00ff00; padding: 4px;")
                if vital in self.alerts:
                    self.alerts.remove(vital)
        
        # Update header alert status
        if alerts_count > 0:
            alert_text = f"⚠ {alerts_count} ALERT{'S' if alerts_count > 1 else ''}"
            self.alert_label.setText(alert_text)
            self.alert_label.setStyleSheet("color: #ff4444; font-weight: bold;")
        else:
            self.alert_label.setText("✓ All Normal")
            self.alert_label.setStyleSheet("color: #00ff00;")

