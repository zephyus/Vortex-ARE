import os
import json
import time
from system_engine import SystemEngine

def test_roadmap_evolution():
    print("Testing Bio-Digital Synthesis (Version 4.0 Audit)...")
    engine = SystemEngine()
    
    # 0. Preparation: Ensure roadmap.json exists
    if os.path.exists(engine.roadmap_path):
        os.remove(engine.roadmap_path)
    
    # Re-init to create fresh roadmap
    engine = SystemEngine()
    
    try:
        # 1. Trigger Roadmap Evolution (Default/Steady)
        print("\n--- Phase 1: Default Strategy Audit ---")
        success, vision = engine.evolve_roadmap()
        print(f"Result: {success}, Vision: {vision}")
        
        with open(engine.roadmap_path, "r") as f:
            data = json.load(f)
            if data["vision"] == vision and len(data["milestones"]) > 0:
                print(f"✅ SUCCESS: Roadmap persisted vision '{vision}' and created a milestone.")
            else:
                print("❌ FAILURE: Roadmap persistence mismatch or missing milestones.")

        # 2. Test Aggressive Vision (Performance + High Energy)
        print("\n--- Phase 2: Aggressive Strategy Audit ---")
        engine.energy = 95.0
        engine.config["personality"] = "Performance"
        success, vision = engine.evolve_roadmap()
        print(f"Result: {success}, Vision: {vision}")
        if vision == "Aggressive Throughput Optimization":
            print("✅ SUCCESS: System correctly projected an Aggressive vision for high performance.")
        else:
            print(f"❌ FAILURE: Unexpected vision projection: {vision}")

        # 3. Test Recharge Vision (Low Energy)
        print("\n--- Phase 3: Recharge Strategy Audit ---")
        engine.energy = 20.0
        success, vision = engine.evolve_roadmap()
        print(f"Result: {success}, Vision: {vision}")
        if vision == "Deep Architectural Recharge":
            print("✅ SUCCESS: System correctly projected a Defensive vision for low energy.")
        else:
            print(f"❌ FAILURE: Unexpected vision projection: {vision}")

    finally:
        # We'll leave roadmap.json for the real system to use
        pass

if __name__ == "__main__":
    test_roadmap_evolution()
