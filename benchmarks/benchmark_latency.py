import time
from medguard.config import MedGuardConfig
from medguard.inference import MedGuardInference

config = MedGuardConfig()
engine = MedGuardInference(config)

samples = [70] * 10000

start = time.time()
for s in samples:
    engine.analyze(s)

end = time.time()

print(f"Processed 10,000 samples in {end - start:.4f} seconds")
