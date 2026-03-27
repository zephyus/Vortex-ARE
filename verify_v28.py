from system_engine import SystemEngine
import time
import os

engine = SystemEngine()
engine.energy = 30.0 # Force low energy
engine.save_config(engine.config)

print(f"Starting Energy: {engine.energy}%")
interval = engine.get_metabolic_interval()
print(f"Adaptive Interval at 30% Energy: {interval} mins (Expected: 10.0)")

# Test Harvesting (Simulate idle)
engine.last_energy_regen = time.time() - 300 # 5 mins ago
engine.regenerate_energy()
print(f"Energy after 5m idle regen: {engine.energy:.2f}% (Expected > Baseline because of Idle Bonus)")

# Test Performance Burst
engine.energy = 95.0
engine.config["personality"] = "Performance"
interval = engine.get_metabolic_interval()
print(f"Adaptive Interval at 95% Energy (Performance): {interval} mins (Expected: 2.0)")

if interval == 2.0 and engine.energy > 95.0:
    print("VERIFIED: Version 2.8 Metabolic Harvesting and Adaptive Heartbeat are operational.")
else:
    print(f"PARTIAL VERIFICATION: Check logic (Energy: {engine.energy:.2f}, Interval: {interval})")
