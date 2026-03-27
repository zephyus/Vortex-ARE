from system_engine import SystemEngine
import os

def verify_v417():
    print("--- v4.17 Verification: Cognitive-Snapshotting ---")
    engine = SystemEngine()
    
    node_name = "test_function"
    original_logic = "def test_function():\n    return 'original'"
    
    # 1. Capture Snapshot
    print(f"Capturing snapshot for {node_name}...")
    snapshot_id = engine.capture_node_snapshot(node_name, original_logic)
    print(f"Captured: {snapshot_id}")
    
    snapshot_path = os.path.join(engine.node_snapshot_dir, f"{snapshot_id}.log")
    assert os.path.exists(snapshot_path), "Snapshot file not found!"
    
    with open(snapshot_path, "r") as f:
        content = f.read()
    assert content == original_logic, "Snapshot content mismatch!"
    
    # 2. Rollback
    print(f"Triggering rollback for {snapshot_id}...")
    success = engine.rollback_node(node_name, snapshot_id)
    assert success is True, "Rollback failed!"
    
    print("\n[SUCCESS] v4.17 Cognitive-Snapshotting verified.")

if __name__ == "__main__":
    verify_v417()
