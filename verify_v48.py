import sys
import os
import time

# Mocking modules to avoid GUI dependency if needed, but we can just test the Engine logic
from system_engine import SystemEngine

def test_v48_synesthesia_loop():
    print("--- Verifying Version 4.8: Synesthesia-Fusion ---")
    engine = SystemEngine()
    
    initial_bias = engine.synesthesia_bias
    print(f"Initial Synesthesia Bias: {initial_bias}")
    
    # Simulate high metabolism visual feedback (Pulse > 0.8)
    print("Simulating High-Metabolism Feedback (Hyper-Divergence trigger)...")
    engine.analyze_visual_metabolism({"pulse": 0.9})
    high_bias = engine.synesthesia_bias
    print(f"Bias after High Pulse: {high_bias:.4f}")
    
    # Simulate low metabolism visual feedback (Pulse < 0.3)
    print("Simulating Low-Metabolism Feedback (Architectural-Silence trigger)...")
    engine.analyze_visual_metabolism({"pulse": 0.1})
    low_bias = engine.synesthesia_bias
    print(f"Bias after Low Pulse: {low_bias:.4f}")
    
    # Check stats integration
    stats = engine.get_system_stats()
    print(f"Engine Stats Synesthesia: {stats.get('synesthesia')}")
    
    success = high_bias > initial_bias and low_bias < high_bias
    
    if success:
        print("\n[SUCCESS] Visual-metabolic feedback loop is operational.")
        return True
    else:
        print("\n[FAILURE] Synesthesia bias did not respond as expected.")
        return False

if __name__ == "__main__":
    if test_v48_synesthesia_loop():
        sys.exit(0)
    else:
        sys.exit(1)
