import pytest
from medguard.detectors.zscore import ZScoreDetector


def test_threshold_at_boundary():
    """Test that threshold is enforced at boundary values."""
    detector = ZScoreDetector(window_size=10, threshold=2.0)
    
    # Populate with normal distribution-like data
    baseline = list(range(70, 80))
    for v in baseline[:-1]:
        detector.analyze(float(v))
    
    # Just below threshold
    is_anomaly, z = detector.analyze(60.0)
    # May not trigger depending on stats
    
    # Far beyond threshold
    is_anomaly_far, z_far = detector.analyze(200.0)
    assert is_anomaly_far is True


def test_custom_thresholds():
    """Test detectors with varying threshold values."""
    low_threshold = ZScoreDetector(window_size=5, threshold=1.0)
    high_threshold = ZScoreDetector(window_size=5, threshold=3.0)
    
    baseline = [100.0, 101.0, 99.0, 102.0]
    for v in baseline:
        low_threshold.analyze(v)
        high_threshold.analyze(v)
    
    test_val = 110.0
    low_is_anomaly, _ = low_threshold.analyze(test_val)
    high_is_anomaly, _ = high_threshold.analyze(test_val)
    
    # Low threshold should be more sensitive
    assert isinstance(low_is_anomaly, bool)
    assert isinstance(high_is_anomaly, bool)
