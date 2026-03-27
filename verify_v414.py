import time
from system_engine import SystemEngine

def test_v414():
    print("--- Verifying Version 4.14: Structural-Resonance Engine ---")
    engine = SystemEngine()
    
    # Test 1: Resonance Calculation
    print("Testing resonance calculation with stable history...")
    engine.resonance_history = [0.9, 0.9, 0.9, 0.9, 0.9] # Perfectly stable
    res = engine.calculate_structural_resonance()
    print(f"Stable Resonance: {res}")
    
    print("Testing resonance calculation with unstable history...")
    engine.resonance_history = [0.9, 0.1, 0.9, 0.1, 0.9] # Highly unstable
    res = engine.calculate_structural_resonance()
    print(f"Unstable Resonance: {res}")
    
    if res < engine.resonance_threshold:
        print("[SUCCESS] Resonance correctly drops on instability.")
    else:
        print("[FAILURE] Resonance failed to detect instability.")

    # Test 2: Engine Trigger
    print("Testing autonomous repair trigger...")
    engine.resonance_wave = 0.5 # Force low resonance
    engine.active_sandboxes = []
    triggered = engine.structural_resonance_engine()
    
    if triggered and len(engine.active_sandboxes) > 0:
        print("[SUCCESS] Structural-Resonance Engine triggered emergency evolution.")
    else:
        print("[FAILURE] Engine failed to trigger repair.")

    print("--- v4.14 Verification Complete ---")

if __name__ == "__main__":
    test_v414()
