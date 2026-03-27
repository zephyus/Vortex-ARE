import sys
import os
import time

# Mocking modules if necessary, but here we assume direct access to local files
sys.path.append(os.getcwd())

try:
    from system_engine import SystemEngine
    print("[SUCCESS] SystemEngine imported.")
except ImportError as e:
    print(f"[FAILURE] Could not import SystemEngine: {e}")
    sys.exit(1)

def verify_v411():
    print("--- Verifying Version 4.11: Structural-Consciousness ---")
    engine = SystemEngine()
    
    # 1. Test Architectural Auditor
    print("Running Architectural Audit...")
    audit_score = engine.architectural_auditor()
    print(f"Structural Consciousness Index: {audit_score:.4f}")
    
    if audit_score > 0:
        print("[SUCCESS] ArchitecturalAuditor correctly analyzed the codebase.")
    else:
        print("[FAILURE] ArchitecturalAuditor returned invalid score.")
        sys.exit(1)
    
    # 2. Test Swarm Stats
    print("Simulating Decentralized Swarm...")
    engine.spawn_evolution_cluster(count=2)
    stats = engine.get_system_stats()
    print(f"Active Swarm Nodes: {stats.get('active_nodes')}")
    
    if stats.get('active_nodes', 0) == 2:
        print("[SUCCESS] Swarm node tracking validated.")
    else:
        print(f"[FAILURE] Expected 2 swarm nodes, got {stats.get('active_nodes')}")
        sys.exit(1)
        
    engine.merge_cluster_results() # Cleanup threads
    print("[SUCCESS] v4.11 Verification Complete.")

if __name__ == "__main__":
    verify_v411()
