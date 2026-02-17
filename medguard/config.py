from dataclasses import dataclass


@dataclass
class SignalConfig:
    window_size: int
    threshold: float
    detector_type: str = "zscore"


@dataclass
class MedGuardConfig:
    heart_rate: SignalConfig
    spo2: SignalConfig
    respiratory_rate: SignalConfig
    systolic_bp: SignalConfig
    temperature: SignalConfig
