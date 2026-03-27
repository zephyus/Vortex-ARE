import time
import subprocess
import json
from system_engine import SystemEngine

engine = SystemEngine()
# Ensure we have the right secret in config for the test
engine.config["telemetry_secret"] = "SYSTEM_CORE_BETA_2026"
engine.save_config(engine.config)

print("--- Version 3.3: Neural-Sync (Phase 2) Verification ---")

# 1. Start Mock Command Server in background
print("Spawning mock command server...")
server_proc = subprocess.Popen(["python", "mock_command_server.py"])
time.sleep(2) # Wait for server to bind

# 2. Trigger Pulse-Pull
print("\nTriggering Pulse-Pull from localhost:8081...")
success, msg = engine.poll_remote_commands(endpoint="http://localhost:8081")

if success:
    print(f"SUCCESS: {msg}")
    # Verify effect
    with open("config.json", "r") as f:
        conf = json.load(f)
    if conf.get("personality") == "Performance":
        print("VERIFIED: Personality shifted to Performance.")
    else:
        print(f"FAILED: Personality is {conf.get('personality')}, expected Performance.")
        success = False
else:
    print(f"FAILED: {msg}")

# Cleanup
server_proc.wait(timeout=10)
print("\n--- Verification Cycle Complete ---")
if success:
    exit(0)
else:
    exit(1)
