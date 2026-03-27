import os
import time
from system_engine import SystemEngine

def test_neural_resonance():
    print("Testing Neural-Resonance (Version 3.9 Audit)...")
    engine = SystemEngine()
    target = "resonance_test_target.py"
    
    def setup_target():
        with open(target, "w", encoding="utf-8") as f:
            f.write("def dummy(): pass\n")

    try:
        # 1. Test Performance Bias
        print("\n--- Phase 1: Performance Bias Audit ---")
        engine.config["personality"] = "Performance"
        engine.save_config(engine.config)
        setup_target()
        engine.simulate_logic_divergence(target)
        with open(target, "r") as f:
            content = f.read()
            if "PERFORMANCE_BIAS" in content:
                print("✅ SUCCESS: Logic synthesis correctly prioritized Performance constructs.")
            else:
                print("❌ FAILURE: Performance bias not detected in evolved logic.")

        # 2. Test Safety Bias
        print("\n--- Phase 2: Safety Bias Audit ---")
        engine.config["personality"] = "Safety"
        engine.save_config(engine.config)
        setup_target()
        engine.simulate_logic_divergence(target)
        with open(target, "r") as f:
            content = f.read()
            if "SAFETY_BIAS" in content:
                print("✅ SUCCESS: Logic synthesis correctly prioritized Safety constructs.")
            else:
                print("❌ FAILURE: Safety bias not detected in evolved logic.")

        # 3. Test Aesthetic Bias
        print("\n--- Phase 3: Aesthetic Bias Audit ---")
        engine.config["personality"] = "Aesthetic"
        engine.save_config(engine.config)
        setup_target()
        engine.simulate_logic_divergence(target)
        with open(target, "r") as f:
            content = f.read()
            if "AESTHETIC_BIAS" in content:
                print("✅ SUCCESS: Logic synthesis correctly prioritized Aesthetic constructs.")
            else:
                print("❌ FAILURE: Aesthetic bias not detected in evolved logic.")

    finally:
        if os.path.exists(target): os.remove(target)

if __name__ == "__main__":
    test_neural_resonance()
