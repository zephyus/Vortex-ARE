import sys
import os
import time
from system_engine import SystemEngine

def test_v49_predictive_regen():
    print("--- Verifying Version 4.9: Predictive-Regeneration ---")
    engine = SystemEngine()
    
    # 1. Populate some history with a downward trend
    print("Simulating Energy Decay...")
    engine.history["energy"] = [100.0, 95.0, 90.0, 85.0, 80.0]
    engine.energy = 75.0
    
    # 2. Check prediction
    pred = engine.predict_energy_metabolism()
    print(f"Current Energy: {engine.energy}, Predicted (10 cycles): {pred:.2f}")
    
    # 3. Trigger regulation
    engine.auto_regulate_metabolism()
    print(f"Metabolic State after prediction: {engine.metabolic_state}")
    
    # 4. Simulate fast crash
    print("\nSimulating Fast Decay (Pre-emptive recharge check)...")
    engine.history["energy"] = [80.0, 70.0, 60.0, 50.0, 40.0]
    engine.energy = 35.0
    # Decay is -10 per cycle. Predicted in 10 cycles = 35 - 100 = -65.
    
    engine.auto_regulate_metabolism()
    print(f"Current Energy: {engine.energy}, Predicted: {engine.predict_energy_metabolism():.2f}")
    print(f"Metabolic State: {engine.metabolic_state}")
    
    success = (engine.metabolic_state == "RECHARGE")
    
    if success:
        print("\n[SUCCESS] Predictive-Regeneration proactively triggered RECHARGE mode.")
        return True
    else:
        print("\n[FAILURE] Proactive recharge failed to trigger.")
        return False

if __name__ == "__main__":
    if test_v49_predictive_regen():
        sys.exit(0)
    else:
        sys.exit(1)
