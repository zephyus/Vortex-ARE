import os
from system_engine import SystemEngine

def test_digital_synapse():
    print("Testing Digital-Synapse (Version 4.4 Audit)...")
    engine = SystemEngine()
    
    # Force personality for testing
    engine.config["personality"] = "Safety"
    
    # 1. Test Complexity Pruning
    print("\n--- Phase 1: Complexity Gating Audit ---")
    long_candidate = "print('line')\n" * 600
    if not engine.synaptic_filter(long_candidate):
        print("✅ SUCCESS: Candidate exceeding complexity threshold correctly suppressed.")
    else:
        print("❌ FAILURE: Complexity gating failed.")

    # 2. Test Personality Pruning (Safety)
    print("\n--- Phase 2: Personality Resonance Audit (Safety) ---")
    risky_candidate = "def unsafe():\n    os.system('rm -rf /')"
    if not engine.synaptic_filter(risky_candidate):
        print("✅ SUCCESS: Risky candidate correctly suppressed in Safety mode.")
    else:
        print("❌ FAILURE: Safety gating failed.")

    # 3. Test Structural Integrity Pruning
    print("\n--- Phase 3: Structural Integrity Audit ---")
    corrupt_candidate = "class SystemEngine:\n    # Corrupting engine without def markers"
    if not engine.synaptic_filter(corrupt_candidate):
        print("✅ SUCCESS: Corrupt structural candidate correctly suppressed.")
    else:
        print("❌ FAILURE: Structural integrity gating failed.")

    # 4. Test Acceptance
    print("\n--- Phase 4: Acceptance Audit ---")
    valid_candidate = "def new_feature():\n    return 'VALID'"
    if engine.synaptic_filter(valid_candidate):
        print("✅ SUCCESS: High-resonance logic correctly accepted.")
    else:
        print("❌ FAILURE: Valid candidate was suppressed.")

if __name__ == "__main__":
    test_digital_synapse()
