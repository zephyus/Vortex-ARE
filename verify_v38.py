import os
import time
from system_engine import SystemEngine

def test_evolutionary_divergence():
    print("Testing Evolutionary Divergence (Version 3.8 Audit)...")
    engine = SystemEngine()
    
    # 0. Preparation: Create a dummy target file
    target = "divergence_test_target.py"
    with open(target, "w", encoding="utf-8") as f:
        f.write("def dummy_function():\n    return 'original'\n")
    
    try:
        # 1. Trigger Simulation
        print("\n--- Phase 1: Simulation Trigger ---")
        success, msg = engine.simulate_logic_divergence(target)
        print(f"Result: {success}, Message: {msg}")
        
        # 2. Verify Sandbox Contents
        print("\n--- Phase 2: Sandbox Audit ---")
        if os.path.exists(engine.sandbox_dir):
            files = os.listdir(engine.sandbox_dir)
            print(f"Sandbox files: {files}")
            if len(files) >= 3:
                print(f"✅ SUCCESS: Divergence sandbox contains {len(files)} candidates.")
            else:
                print(f"❌ FAILURE: Sandbox under-populated: {len(files)} files.")
        else:
            print("❌ FAILURE: Sandbox directory missing.")
            
        # 3. Verify Selection Commit
        print("\n--- Phase 3: Selection Audit ---")
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()
            if "DIVERGENCE_MARKER_" in content:
                print("✅ SUCCESS: Target file successfully evolved with a selected candidate marker.")
            else:
                print("❌ FAILURE: Target file does not contain a divergence marker.")
                
    finally:
        # Cleanup
        if os.path.exists(target): os.remove(target)
        # Sandbox is persistent for now as per design

if __name__ == "__main__":
    test_evolutionary_divergence()
