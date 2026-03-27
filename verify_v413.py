import time
from system_engine import SystemEngine

def test_v413():
    print("--- Verifying Version 4.13: Neural-Sync Refinement ---")
    engine = SystemEngine()
    
    # Test 1: sync_token presence and rotation
    stats1 = engine.get_system_stats()
    token1 = stats1.get("sync_token")
    print(f"Token 1: {token1}")
    
    time.sleep(0.1)
    stats2 = engine.get_system_stats()
    token2 = stats2.get("sync_token")
    print(f"Token 2: {token2}")
    
    if token1 and token2 and token1 != token2:
        print("[SUCCESS] Neural-Sync token rotation verified.")
    else:
        print("[FAILURE] Neural-Sync token missing or static.")
    
    # Test 2: merge_cluster_results safety
    print("Testing swarm merge with zero sandboxes...")
    engine.active_sandboxes = []
    try:
        res = engine.merge_cluster_results()
        print(f"Empty merge result: {res}")
        print("[SUCCESS] Swarm merge stabilized (no AttributeError).")
    except Exception as e:
        print(f"[FAILURE] Swarm merge failed: {e}")

    print("--- v4.13 Verification Complete ---")

if __name__ == "__main__":
    test_v413()
