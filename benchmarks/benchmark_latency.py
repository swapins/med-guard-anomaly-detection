import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from medguard.config import MedGuardConfig, SignalConfig
from medguard.inference import MultiVitalInference

# Configure multi-vital detection
config = MedGuardConfig(
    heart_rate=SignalConfig(window_size=15, threshold=2.0),
    spo2=SignalConfig(window_size=15, threshold=2.0),
    respiratory_rate=SignalConfig(window_size=15, threshold=2.0),
    systolic_bp=SignalConfig(window_size=15, threshold=2.0),
    temperature=SignalConfig(window_size=15, threshold=2.0),
)

engine = MultiVitalInference(config)

# Warm-up
for _ in range(100):
    engine.analyze({
        'heart_rate': 75.0,
        'spo2': 97.0,
        'respiratory_rate': 16.0,
        'systolic_bp': 120.0,
        'temperature': 36.8,
    })

# Benchmark 10,000 samples
num_samples = 10000
test_vitals = {
    'heart_rate': 75.0,
    'spo2': 97.0,
    'respiratory_rate': 16.0,
    'systolic_bp': 120.0,
    'temperature': 36.8,
}

start = time.perf_counter()
for _ in range(num_samples):
    engine.analyze(test_vitals)
end = time.perf_counter()

elapsed = end - start
throughput = num_samples / elapsed if elapsed > 0 else 0

print(f"\n=== Latency Benchmark ===")
print(f"Processed {num_samples:,} samples in {elapsed:.4f} seconds")
print(f"Throughput: {throughput:,.0f} samples/sec")
print(f"Per-sample latency: {(elapsed/num_samples)*1000:.4f} ms")
