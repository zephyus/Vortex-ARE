import time
import threading
from system_engine import SystemEngine

def test_parallel_evolution():
    print("Testing Parallel-Evolution (Version 4.6 Audit)...")
    engine = SystemEngine()
    
    # 1. Spawn Cluster
    print("\n--- Phase 1: Cluster Spawning Audit ---")
    sandboxes = engine.spawn_evolution_cluster(count=3)
    print(f"Spawned {len(sandboxes)} evolution sandboxes.")
    
    if len(sandboxes) == 3:
        print("✅ SUCCESS: Cluster size verified.")
    else:
        print(f"❌ FAILURE: Expected 3 sandboxes, got {len(sandboxes)}.")

    # 2. Monitor and Merging
    print("\n--- Phase 2: Merging and Fitness Audit ---")
    print("Waiting for sandboxes to complete (simulated workload)...")
    
    # The sandboxes should complete and broadcast signals
    # We join them in merge_cluster_results()
    result = engine.merge_cluster_results()
    
    if result:
        print("✅ SUCCESS: Best candidate successfully merged from cluster.")
        print(f"Merged Result Snippet: {result[:50]}...")
    else:
        print("❌ FAILURE: No candidate merged from cluster.")

    # 3. Thread Safety Check
    print("\n--- Phase 3: Resource Cleanup Audit ---")
    if len(engine.active_sandboxes) == 0:
        print("✅ SUCCESS: Active sandboxes correctly cleared after merging.")
    else:
        print("❌ FAILURE: Sandbox references still leaking.")

if __name__ == "__main__":
    test_parallel_evolution()
