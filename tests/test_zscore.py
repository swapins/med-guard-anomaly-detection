from medguard.config import MedGuardConfig
from medguard.inference import MedGuardInference


def test_basic_anomaly_detection():
    config = MedGuardConfig(window_size=5, threshold=2.0)
    engine = MedGuardInference(config)

    normal_values = [70, 72, 71, 73, 74]
    for v in normal_values:
        engine.analyze(v)

    is_anomaly, _ = engine.analyze(150)
    assert is_anomaly is True
