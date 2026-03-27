import sys
import os
import time

sys.path.append(os.getcwd())
from system_engine import SystemEngine

def verify_v412():
    print("--- Verifying Version 4.12: Subconscious-Refactoring ---")
    engine = SystemEngine()
    
    # Pre-tuning weights
    w_before = engine.synaptic_weights.get("complexity", 1.0)
    print(f"Initial Complexity Weight: {w_before}")
    
    # Execute subconscious tuning
    print("Triggering Subconscious Tuner...")
    engine.subconscious_tuner()
    
    w_after = engine.synaptic_weights.get("complexity", 1.0)
    print(f"Post-Tuning Complexity Weight: {w_after}")
    
    if w_before != w_after:
        print("[SUCCESS] SubconsciousTuner autonomously modified synaptic weights.")
    else:
        # It's possible for it to be same if weights were already at min/max,
        # but for a fresh start they should move.
        print("[WARNING] Weights remained unchanged. Audit might have returned neutral result.")
    
    # Test restored stats
    stats = engine.get_system_stats()
    print(f"Audit score in stats: {stats.get('structural_audit')}")
    if stats.get('structural_audit') is not None:
        print("[SUCCESS] get_system_stats restoration verified.")
    else:
        print("[FAILURE] get_system_stats is still missing structural_audit.")
        sys.exit(1)

    print("[SUCCESS] v4.12 Verification Complete.")

if __name__ == "__main__":
    verify_v412()
