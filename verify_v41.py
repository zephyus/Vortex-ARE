import os
import time
from system_engine import SystemEngine

def test_architectural_healing():
    print("Testing Architectural-Immunity (Version 4.1 Audit)...")
    engine = SystemEngine()
    
    # Target file for corruption
    target = "healing_test_subject.py"
    
    # 0. Preparation: Create and Snapshot
    print("\n--- Phase 0: Preparation & DNA Snapshot ---")
    healthy_original = "def stable_logic():\n    return 'HEALTHY'\n"
    with open(target, "w", encoding="utf-8") as f:
        f.write(healthy_original)
    
    # Manually create a dna snapshot for this test (since save_dna_snapshot is periodic)
    # We'll just put it in the snapshot dir with the right prefix
    snap_path = os.path.join(engine.snapshot_dir, f"dna_test_{int(time.time())}.py")
    with open(snap_path, "w", encoding="utf-8") as f:
        f.write(healthy_original)
        
    try:
        # 1. Corrupt the target
        print("\n--- Phase 1: Injection of Corrupt Logic ---")
        with open(target, "w", encoding="utf-8") as f:
            f.write("def broken_logic():\n    ERROR!! syntax error here")
        print("Target file intentionally corrupted.")
        
        # 2. Trigger Autonomous Healing
        print("\n--- Phase 2: Autonomous Healing Trigger ---")
        success, msg = engine.automated_regression_healing(target)
        print(f"Result: {success}, Message: {msg}")
        
        # 3. Verify Restoration
        print("\n--- Phase 3: Integrity Restoration Audit ---")
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()
            if "stable_logic" in content and "HEALED_FROM_SNAPSHOT_V41" in content:
                print("✅ SUCCESS: Architectural integrity autonomously restored via snapshot merge.")
            else:
                print("❌ FAILURE: Restoration failed or incomplete.")
                print(f"Current content:\n{content}")

    finally:
        # Cleanup
        if os.path.exists(target): os.remove(target)
        if os.path.exists(snap_path): os.remove(snap_path)

if __name__ == "__main__":
    test_architectural_healing()
