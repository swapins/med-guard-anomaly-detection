from medguard.config import MedGuardConfig, SignalConfig
from medguard.inference import MultiVitalInference
from medguard.detectors.zscore import ZScoreDetector


def test_zscore_detector_basic():
    """Test basic Z-score detection on single vital."""
    detector = ZScoreDetector(window_size=5, threshold=2.0)
    
    # Normal values - fill window completely
    normal_values = [70, 72, 71, 73, 74]
    for v in normal_values:
        detector.analyze(v)
    
    # Anomaly (far from baseline) - now window is full
    is_anomaly, z_score = detector.analyze(150)
    assert is_anomaly is True
    assert z_score > 2.0


def test_multi_vital_inference():
    """Test multi-vital inference engine."""
    config = MedGuardConfig(
        heart_rate=SignalConfig(window_size=15, threshold=2.0),
        spo2=SignalConfig(window_size=15, threshold=2.0),
        respiratory_rate=SignalConfig(window_size=15, threshold=2.0),
        systolic_bp=SignalConfig(window_size=15, threshold=2.0),
        temperature=SignalConfig(window_size=15, threshold=2.0),
    )
    
    engine = MultiVitalInference(config)
    
    # Normal vitals
    results = engine.analyze({
        'heart_rate': 75,
        'spo2': 98,
        'respiratory_rate': 16,
        'systolic_bp': 120,
        'temperature': 36.8,
    })
    
    assert len(results) == 5
    for vital, (is_anomaly, score) in results.items():
        assert isinstance(is_anomaly, bool)
        assert isinstance(score, float)


def test_zero_variance_handling():
    """Test detector behavior with constant values (zero variance)."""
    detector = ZScoreDetector(window_size=5, threshold=2.0)
    
    # Feed constant values
    constant = [100.0] * 5
    for v in constant[:-1]:
        detector.analyze(v)
    
    is_anomaly, z_score = detector.analyze(100.0)
    # With zero variance, z-score should be 0.0
    assert z_score == 0.0
    assert is_anomaly is False
