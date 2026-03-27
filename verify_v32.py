import time
import subprocess
from system_engine import SystemEngine

engine = SystemEngine()

print("--- Version 3.2: Neural-Sync (Phase 1) Verification ---")

# 1. Start Mock Server in background
print("Spawning mock server...")
server_proc = subprocess.Popen(["python", "mock_telemetry_server.py"])
time.sleep(2) # Wait for server to bind

# 2. Trigger Broadcast
print("\nTriggering DNA Broadcast to localhost:8080...")
success, msg = engine.broadcast_evolution_state(endpoint="http://localhost:8080")

if success:
    print(f"SUCCESS: {msg}")
else:
    print(f"FAILED: {msg}")

# Cleanup
server_proc.wait(timeout=10)
print("\n--- Verification Cycle Complete ---")
if success:
    exit(0)
else:
    exit(1)
