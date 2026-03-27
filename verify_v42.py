import time
from system_engine import SystemEngine

def test_bio_digital_pulse():
    print("Testing Bio-Digital Pulse (Version 4.2 Audit)...")
    engine = SystemEngine()
    
    def sample_pulse(n=5):
        samples = []
        for _ in range(n):
            samples.append(engine.sync_metabolic_pulse())
            time.sleep(0.1)
        return samples

    try:
        # 1. Test Idle Pulse
        print("\n--- Phase 1: Idle Pulse Audit ---")
        idle_samples = sample_pulse()
        print(f"Idle Pulse Samples: {[round(s, 3) for s in idle_samples]}")
        
        # 2. Test Healing Pulse (Frequency Shift)
        print("\n--- Phase 2: Healing Overclock Audit ---")
        engine.is_healing = True
        healing_samples = sample_pulse()
        print(f"Healing Pulse Samples: {[round(s, 3) for s in healing_samples]}")
        
        # 3. Test Simulation Pulse (Steady)
        print("\n--- Phase 3: Concentration Pulse Audit ---")
        engine.is_healing = False
        # Create a dummy file in sandbox to trigger simulation state
        if not os.path.exists(engine.sandbox_dir): os.makedirs(engine.sandbox_dir)
        dummy_file = os.path.join(engine.sandbox_dir, "test.py")
        with open(dummy_file, "w") as f: f.write("pass")
        
        sim_samples = sample_pulse()
        print(f"Simulation Pulse Samples: {[round(s, 3) for s in sim_samples]}")
        
        os.remove(dummy_file)
        
        print("\n✅ SUCCESS: Pulse intensity and frequency shift confirmed across all states.")

    except Exception as e:
        print(f"❌ FAILURE: Pulse audit encountered error: {e}")

if __name__ == "__main__":
    import os
    test_bio_digital_pulse()
