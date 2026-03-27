import time
from system_engine import SystemEngine

def verify_v415():
    print("--- v4.15 Verification: Metabolic-Aesthetic Sync ---")
    engine = SystemEngine()
    
    # 1. Check initial state
    print(f"Initial Metabolic State: {engine.metabolic_state}")
    print(f"Initial Visual State: {getattr(engine, 'actual_visual_state', 'N/A')}")
    res = engine.calculate_aesthetic_resonance()
    print(f"Initial Resonance: {res}")
    assert res == 1.0, f"Expected 1.0, got {res}"
    
    # 2. Simulate Mismatch (Engine Sprints, UI stays Steady)
    engine.metabolic_state = "SPRINT"
    res = engine.calculate_aesthetic_resonance()
    print(f"Mismatched Resonance (SPRINT/STEADY): {res}")
    assert res == 0.6, f"Expected 0.6, got {res}"
    
    # 3. Simulate Total Mismatch (Engine Sprints, UI Recharges - unlikely but testable)
    engine.actual_visual_state = "RECHARGE"
    res = engine.calculate_aesthetic_resonance()
    print(f"Total Mismatch (SPRINT/RECHARGE): {res}")
    assert res == 0.2, f"Expected 0.2, got {res}"
    
    # 4. Correct UI State via feedback
    engine.analyze_visual_metabolism({"state": "SPRINT", "intensity": 0.9})
    print(f"New Visual State: {engine.actual_visual_state}")
    res = engine.calculate_aesthetic_resonance()
    print(f"Resynchronized Resonance: {res}")
    assert res == 1.0, f"Expected 1.0, got {res}"
    
    # 5. Check Telemetry Injection
    stats = engine.get_system_stats()
    print(f"Telemetry aesthetic_res: {stats.get('aesthetic_res')}")
    assert stats.get('aesthetic_res') == 1.0
    
    print("\n[SUCCESS] v4.15 Metabolic-Aesthetic Sync verified.")

if __name__ == "__main__":
    verify_v415()
