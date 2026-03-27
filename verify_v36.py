import os
import time
from system_engine import SystemEngine

def test_proactive_hardening():
    print("Testing Proactive Logic Hardening (Version 3.6 Audit)...")
    engine = SystemEngine()
    
    # 1. Ensure at least one snapshot exists for comparison
    print("Creating baseline snapshot...")
    engine.save_ui_snapshot(0,0,100,100)
    time.sleep(1.1) # Ensure mtime difference
    
    # 2. Simulate a code change in main_app.py
    target_file = "main_app.py"
    print(f"Simulating change in {target_file}...")
    with open(target_file, "a") as f:
        f.write("\ndef proactive_test_func():\n    pass # Proactive Audit Marker\n")
    
    try:
        # 3. Trigger hardening
        print("Triggering Proactive Logic Hardening...")
        success, msg = engine.proactive_logic_hardening()
        
        print(f"Result: {success}, Message: {msg}")
        
        if success and "Hardened" in msg:
            print("✅ SUCCESS: Proactive hardening correctly identified and targeted the modification.")
        elif success and "No proactive hardening required" in msg:
            print("❌ FAILURE: System failed to detect the modification.")
        else:
            print(f"⚠️ VERIFICATION INCOMPLETE: {msg}")
            
    finally:
        # Cleanup: Remove the test function
        print("Cleaning up simulated changes...")
        with open(target_file, "r") as f:
            lines = f.readlines()
        with open(target_file, "w") as f:
            f.writelines([l for l in lines if "proactive_test_func" not in l and "Proactive Audit Marker" not in l])

if __name__ == "__main__":
    test_proactive_hardening()
