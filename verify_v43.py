import time
import threading
from system_engine import SystemEngine

def test_neural_conduction():
    print("Testing Neural-Conduction (Version 4.3 Audit)...")
    engine = SystemEngine()
    
    received_count = 0
    received_payloads = []
    lock = threading.Lock()

    def mock_subscriber_1(payload):
        nonlocal received_count
        with lock:
            received_count += 1
            received_payloads.append(f"Sub1: {payload}")

    def mock_subscriber_2(payload):
        nonlocal received_count
        with lock:
            received_count += 1
            received_payloads.append(f"Sub2: {payload}")

    # 1. Test Subscription
    print("\n--- Phase 1: Subscription Registry Audit ---")
    engine.subscribe_to_signals("test_topic", mock_subscriber_1)
    engine.subscribe_to_signals("test_topic", mock_subscriber_2)
    print("Two subscribers registered to 'test_topic'.")

    # 2. Test Emission
    print("\n--- Phase 2: Signal Propagation Audit ---")
    test_payload = {"status": "ACTIVE", "frequency": 4.2}
    engine.broadcast_signal("test_topic", test_payload)
    
    # Wait for propagation (though it's synchronous callbacks in this impl, 
    # the hub is designed for thread-safe emission)
    time.sleep(0.1)
    
    with lock:
        if received_count == 2:
            print(f"✅ SUCCESS: Signal propagated to all subscribers. Payloads: {received_payloads}")
        else:
            print(f"❌ FAILURE: Signal propagation incomplete. Received count: {received_count}")

    # 3. Test Non-Blocking Concurrency
    print("\n--- Phase 3: Concurrency Audit ---")
    # Reset
    received_count = 0
    
    def emit_loop():
        for i in range(10):
            engine.broadcast_signal("test_topic", i)
            time.sleep(0.01)

    t = threading.Thread(target=emit_loop)
    t.start()
    t.join()
    
    with lock:
        if received_count == 20: # 10 emits * 2 subs
            print(f"✅ SUCCESS: High-frequency concurrent emission verified. Total signals handled: {received_count}")
        else:
            print(f"❌ FAILURE: Concurrent signal loss detected. Received: {received_count}")

if __name__ == "__main__":
    test_neural_conduction()
