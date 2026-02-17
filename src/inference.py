import numpy as np

class MedGuardInference:
    def __init__(self, window_size=15):
        self.history = []
        self.window_size = window_size

    def analyze(self, heart_rate):
        self.history.append(heart_rate)
        
        # Keep only the last 15 readings for a "sliding window"
        if len(self.history) > self.window_size:
            self.history.pop(0)

        if len(self.history) < 5:
            return False, 0.0

        # Calculate Mean and Standard Deviation
        mean = np.mean(self.history)
        std = np.std(self.history)
        
        # Calculate Z-Score (how many deviations from normal)
        z_score = (heart_rate - mean) / std if std > 0 else 0
        
        # Threshold: > 2.0 is statistically significant (Anomaly)
        is_anomaly = abs(z_score) > 2.0
        return is_anomaly, z_score