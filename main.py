import time
import random
from src.inference import MedGuardInference

# Initialize the Brain
engine = MedGuardInference()

def run_system():
    print("🚀 Med-Guard Edge System Active...")
    print("Monitoring Vitals (Ctrl+C to stop)\n")
    
    try:
        while True:
            # 1. Simulate a Heart Rate reading
            # Normal range 60-100; occasionally spike to 140
            if random.random() > 0.9:
                hr = random.randint(130, 150) # The anomaly
            else:
                hr = random.randint(70, 85)   # The normal state

            # 2. Run Inference
            is_anomaly, score = engine.analyze(hr)

            # 3. Output results
            status = "⚠️ ANOMALY" if is_anomaly else "✅ NORMAL"
            print(f"Reading: {hr} BPM | Status: {status} | Z-Score: {score:.2f}")

            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping System...")

if __name__ == "__main__":
    run_system()