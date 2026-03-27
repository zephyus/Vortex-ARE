from system_engine import SystemEngine
import os

engine = SystemEngine()
# Simulate an anomaly in the engine itself to trigger self-hardening
engine.current_anomalies = ["system_engine"]
print(f"Triggering evolution for: {engine.current_anomalies}")

success = engine.evolve_test_suite()
print(f"Evolution success: {success}")

if success:
    with open("test_engine_logic.py", "r") as f:
        content = f.read()
        if "Logic Mirroring" in content:
            print("VERIFIED: Deep Logic Mirroring detected in test suite.")
        else:
            print("FAILED: Logic Mirroring missing from test suite.")
