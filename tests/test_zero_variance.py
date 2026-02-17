import pytest
from medguard.detectors.zscore import ZScoreDetector
from medguard.detectors.mad import MADDetector


def test_zscore_zero_variance():
    """Test Z-score detector with zero variance (all identical values)."""
    detector = ZScoreDetector(window_size=5, threshold=2.0)
    
    # Feed identical values
    for _ in range(4):
        detector.analyze(100.0)
    
    # Test with same value (should not be anomaly)
    is_anomaly, z = detector.analyze(100.0)
    assert is_anomaly is False
    assert z == 0.0  # z-score is 0 when value equals mean and std is 0


def test_mad_zero_variance():
    """Test MAD detector with zero variance."""
    detector = MADDetector(window_size=5, threshold=2.0)
    
    # Feed identical values
    for _ in range(4):
        detector.analyze(100.0)
    
    # Test with same value
    is_anomaly, score = detector.analyze(100.0)
    assert is_anomaly is False
    # MAD should handle zero variance gracefully


def test_window_filling_behavior():
    """Test detector behavior as window fills."""
    detector = ZScoreDetector(window_size=3, threshold=2.0)
    
    # First call (window not full)
    is_anomaly1, z1 = detector.analyze(10.0)
    assert is_anomaly1 is False
    
    # Second call
    is_anomaly2, z2 = detector.analyze(11.0)
    assert is_anomaly2 is False
    
    # Window now full, subsequent calls use stats
    is_anomaly3, z3 = detector.analyze(12.0)
    assert isinstance(is_anomaly3, bool)
