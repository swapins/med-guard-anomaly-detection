# Med-Guard: Lightweight Statistical Anomaly Detection for Edge Research

Abstract
-------

Med-Guard is a research prototype implementing a computationally lightweight, statistically grounded anomaly detection pipeline for time-series monitoring on resource-constrained edge hardware. The project focuses on methods that prioritize interpretability, deterministic behavior, and low resource consumption over deep-learning complexity.

Motivation
----------

Edge and embedded environments impose constraints that affect algorithm design: limited memory, reduced CPU performance, energy budgets, and intermittent connectivity. This repository investigates whether sliding-window statistical techniques (rolling mean/std and Z-score rules) provide an effective baseline for anomaly detection in such settings.

Scope and disclaimer
--------------------

This codebase is a research tool and experimental prototype. It is not validated for clinical use and must not be used for patient care or medical decision-making.

System overview
---------------

Signal Source → Sliding-window Buffer → Statistical Engine → Z-score Computation → Local Alert

Core components

- Signal Input Layer — accepts sequential numeric observations (synthetic or recorded signals).
- Sliding-window Buffer — fixed-size buffer of recent samples.
- Statistical Engine — computes rolling mean (μ) and standard deviation (σ) for the active window.
- Z-score Detector — standardizes incoming samples: z = (x − μ) / σ and flags samples where |z| exceeds a configured threshold.
- Local Alerting — interface for raising local events; no cloud dependency required by the baseline.

Design constraints and target hardware
-------------------------------------

Design targets for the baseline implementation:

- Memory: minimal footprint (target < 5 MB for Python runtime + dependencies).
- Latency: designed for low per-sample processing overhead suitable for SBC-class CPUs.
- No GPU or heavy ML frameworks required.
- Offline operation and deterministic behavior.

Target evaluation platforms include Raspberry Pi and other ARM-based SBCs.

Implementation details
----------------------

- Language: Python 3.9+
- Dependencies: NumPy (for efficient numeric ops)
- Module: a single inference component (`MedGuardInference`) exposes `analyze()` which accepts a scalar observation and returns (is_anomaly: bool, z_score: float).

Example usage
-------------

```python
from medguard import MedGuardInference

engine = MedGuardInference(window_size=15, threshold=2.0)
is_anomaly, z = engine.analyze(heart_rate=85)
if is_anomaly:
    print('Anomaly detected', z)
```

Installation and running
------------------------

Prerequisites: Python 3.9+, virtual environment recommended, pip.

Setup (example):

```bash
git clone <repository-url>
cd med-guard-anomaly-detection
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
python main.py
```

Evaluation and limitations
--------------------------

Current repository uses synthetic signals for controlled experiments. Known limitations:

- No empirical benchmark vs learned anomaly detectors in this release.
- No clinical dataset validation included.
- Thresholds are heuristic; no adaptive thresholding implemented.

Research directions
-------------------

Potential extensions:

- Quantitative benchmarking vs lightweight learned models (e.g., small autoencoders).
- Adaptive threshold mechanisms and online calibration.
- Robust statistics (e.g., MAD-based detectors) and outlier-resistant estimators.
- Multi-signal fusion and correlation-aware detection.

Authors and acknowledgements
----------------------------

Author: Swapin Vidya

License
-------

MIT License

License & Patent Notice
----------------------

- **License:** This repository is provided under the MIT License. See the `LICENSE` file for full terms and conditions.
- **Patent notice & usage limitation:** Patent Notice
Certain architectural concepts referenced in this repository are related to intellectual property associated with the PeachBot Med AI platform, including issued patents and/or pending patent applications.

This repository itself is released under the MIT License. The MIT License applies solely to the code contained herein and does not grant rights to practice or commercialize any separate patented systems beyond the scope of this specific implementation. For inquiries related to intellectual property beyond this repository’s open-source scope, please contact the project maintainer.




