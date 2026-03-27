from system_engine import SystemEngine
import os

engine = SystemEngine()
activity = engine.get_module_activity()

print("--- Neural Path Activity Audit ---")
for mod, level in activity.items():
    print(f"Module: {mod:20} Pulse Intensity: {level:.2f}")

# Verify engine/main_app are prioritized
if activity.get("system_engine", 0) > 0.1 and activity.get("main_app", 0) > 0.1:
    print("\nVERIFIED: Core modules have active neural pulses.")
else:
    print("\nPARTIAL VERIFICATION: Check metabolic weights.")

# Force an event and check bonus
engine.add_event("REFACTOR", "Simulating activity in dashboard_gui")
activity_revised = engine.get_module_activity()
if activity_revised.get("dashboard_gui", 0) > activity.get("dashboard_gui", 0):
    print("VERIFIED: Activity bonus correctly applied for recent evolutionary events.")
else:
    print(f"PARTIAL VERIFICATION: Event bonus did not spike (Before: {activity.get('dashboard_gui', 0):.2f}, After: {activity_revised.get('dashboard_gui', 0):.2f})")
