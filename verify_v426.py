
import os
import json
import time
from system_engine import SystemEngine

def test_v426_governor():
    print("--- NEURAL-SYNC LOGIC HARDENING VERIFICATION (v4.26) ---")
    engine = SystemEngine()
    
    # 1. Verify Checkpoint Existence
    print("[Phase 1: Checkpoint Integrity]")
    if os.path.exists(engine.checkpoint_path):
        print(f"  Checkpoint found at: {engine.checkpoint_path}")
        print("  Validation: PASS")
    else:
        print("  Validation: FAIL (Checkpoint missing)")
        return

    # 2. Simulate "Unstable" Evolution (Modify config in memory and trigger smells)
    print("\n[Phase 2: Alert Triggering]")
    engine.consensus_strength = 15.0 # Should trigger ALERT
    state = engine.apply_meta_governance()
    print(f"  Low Consensus State: {state}")
    if state == "ALERT":
        print("  Validation: PASS (Alert active)")
    else:
        print("  Validation: FAIL")

    # 3. Simulate "Smell Overflow" Rollback
    print("\n[Phase 3: Automated Rollback]")
    # Backup current valid config
    with open(engine.config_path, "r") as f:
        original_dna = json.load(f)
    
    # Corrupt config with dummy data
    corrupt_data = {"corrupted": True, "window_size": "BROKEN"}
    with open(engine.config_path, "w") as f:
        json.dump(corrupt_data, f)
    
    print("  Triggering Smell Overflow (Mocking 51 smells)...")
    # Mock check_code_health to return 51 smells
    engine.check_code_health = lambda: ["smell"] * 51 
    
    engine.apply_meta_governance()
    print(f"  Governor State during rollback: {engine.governor_state}")
    
    # Verify restoration
    engine.load_config()
    with open(engine.config_path, "r") as f:
        restored_dna = json.load(f)
        
    if "corrupted" not in restored_dna and "window_size" in restored_dna:
        print("  Rollback Restoration: PASS")
    else:
        print("  Rollback Restoration: FAIL (DNA remains corrupted)")

    print("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    test_v426_governor()
