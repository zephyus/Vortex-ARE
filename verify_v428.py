
import os
import json
from system_engine import SystemEngine

def test_v428_adaptation():
    print("--- NEURAL-SYNC FEEDBACK LOOP VERIFICATION (v4.28) ---")
    engine = SystemEngine()
    
    # Reset memory for clean test
    engine.semantic_memory = {tag: {"success": 0, "fail": 0} for tag in engine.semantic_memory}
    
    print("[Phase 1: Recording Failures]")
    # Simulate 3 UI failures (rollbacks)
    for _ in range(3):
        engine.record_semantic_outcome("UI", success=False)
    
    # Simulate 2 LOGIC successes
    for _ in range(2):
        engine.record_semantic_outcome("LOGIC", success=True)
        
    print(f"  Memory Stats: UI={engine.semantic_memory['UI']}, LOGIC={engine.semantic_memory['LOGIC']}")

    print("\n[Phase 2: Adaptive Weighting Verification]")
    engine.calculate_thermal_score = lambda: 30.0 # Low thermal to isolate adaptation
    engine.get_resonance_score = lambda: 0.9      # Same resonance for both
    
    # Candidate 1: UI (Success Rate: 0/3 = 0.0) -> Adaptive Weight: (0.5 + 0.0) = 0.5
    ui_cand = {"code": "self.ui_update()", "semantic_tag": "UI"}
    # Candidate 2: LOGIC (Success Rate: 2/2 = 1.0) -> Adaptive Weight: (0.5 + 1.0) = 1.5
    logic_cand = {"code": "def business_logic(): pass", "semantic_tag": "LOGIC"}
    
    # 0.9 resonance * 100 = 90 base score
    # UI Weighted: 90 * 1.0 (base weight) * 0.5 (adaptive) = 45
    # LOGIC Weighted: 90 * 1.2 (base logic weight) * 1.5 (adaptive) = 162
    
    winner = engine.evaluate_consensus([ui_cand, logic_cand])
    print(f"  Winner Tag (After UI Failures): {winner.get('semantic_tag')}")
    
    if winner.get("semantic_tag") == "LOGIC":
        print("  Adaptation Bias: PASS")
    else:
        print("  Adaptation Bias: FAIL")

    # 3. Verify Refactoring Trigger logic (mocked)
    print("\n[Phase 3: Persistence Check]")
    engine.save_config(engine.config)
    with open(engine.config_path, "r") as f:
        conf = json.load(f)
        if "semantic_memory" in conf and conf["semantic_memory"]["UI"]["fail"] == 3:
            print("  Persistence: PASS")
        else:
            print(f"  Persistence: FAIL (Found: {conf.get('semantic_memory')})")

    print("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    test_v428_adaptation()
