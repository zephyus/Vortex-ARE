
import sys
import os
import time
import hashlib
from system_engine import SystemEngine

def verify_v419():
    print("--- NEURAL-SYNC CONSENSUS VERIFICATION (v4.19) ---")
    engine = SystemEngine()
    
    # 1. Verify Metabolic SHA256 Handshake
    print("\n[Phase 1: Sync Handshake]")
    token1 = engine.get_sync_token()
    print(f"Token 1: {token1}")
    time.sleep(0.1)
    token2 = engine.get_sync_token()
    print(f"Token 2: {token2}")
    
    if token1 != token2:
        print("PASS: Sync tokens are metabolic (evolve each call).")
    else:
        print("FAIL: Sync tokens are static.")
        
    # 2. Verify Consensus Healing Gate
    print("\n[Phase 2: Consensus Gate]")
    # We need to manually stabilize the resonance history to pass the gate
    # calculate_structural_resonance appends a new audit each time.
    # To keep resonance high, we'll mock the history with very similar values.
    # We'll use a value close to what architectural_auditor() returns (likely ~0.2)
    audit = engine.architectural_auditor()
    print(f"Current Audit: {audit:.4f}")
    engine.resonance_history = [audit] * 5 
    
    engine.energy = 50.0
    res = engine.calculate_structural_resonance()
    print(f"Engine Resonance: {res:.4f}")
    
    candidate = {"node": "system_engine", "type": "AUTO_REPAIR"}
    approved = engine.apply_consensus_healing(candidate)
    print(f"Approval (Stable/High Energy): {approved}")
    
    # Force failure via energy
    engine.energy = 10.0
    rejected = engine.apply_consensus_healing(candidate)
    print(f"Approval (Low Energy): {rejected}")
    
    # Force failure via resonance
    engine.energy = 50.0
    engine.resonance_history = [1.0, 0.0, 1.0, 0.0] # Unstable
    res_unstable = engine.calculate_structural_resonance()
    print(f"Unstable Resonance: {res_unstable:.4f}")
    rejected_res = engine.apply_consensus_healing(candidate)
    print(f"Approval (Unstable): {rejected_res}")
    
    if approved and not rejected and not rejected_res:
        print("PASS: Consensus protocol correctly validates/rejects healing candidates.")
    else:
        print("FAIL: Consensus protocol logic mismatch.")
        
    # 3. Verify Dashboard Telemetry
    print("\n[Phase 3: Telemetry]")
    stats = engine.get_system_stats()
    print(f"Consensus Active Stat: {stats.get('consensus_active')}")
    print(f"Resonance Stat: {stats.get('resonance_wave')}")
    print(f"Iteration Index: {engine.iteration}")
    
    if "consensus_active" in stats and "sync_token" in stats:
        print("PASS: Telemetry HUD updated with v4.19 tokens.")
    else:
        print("FAIL: Telemetry missing v4.19 keys.")

    print("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    verify_v419()
