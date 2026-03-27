import time
from system_engine import SystemEngine

def verify_v416():
    print("--- v4.16 Verification: Neural-Energy Harvesting ---")
    engine = SystemEngine()
    
    # 1. Test STEADY (Default)
    engine.metabolic_state = "STEADY"
    eff = engine.calculate_neural_harvesting()
    throttle = engine.task_throttle
    print(f"STEADY -> Efficiency: {eff}, Throttle: {throttle}")
    assert eff == 1.0
    assert throttle == 1.0
    
    # 2. Test RECHARGE
    engine.metabolic_state = "RECHARGE"
    eff = engine.calculate_neural_harvesting()
    throttle = engine.task_throttle
    print(f"RECHARGE -> Efficiency: {eff}, Throttle: {throttle}")
    assert eff == 1.5
    assert throttle == 2.0
    
    # 3. Test SPRINT
    engine.metabolic_state = "SPRINT"
    eff = engine.calculate_neural_harvesting()
    throttle = engine.task_throttle
    print(f"SPRINT -> Efficiency: {eff}, Throttle: {throttle}")
    assert eff == 0.5
    assert throttle == 0.5
    
    # 4. Check Telemetry
    stats = engine.get_system_stats()
    print(f"Telemetry harvest_efficiency: {stats.get('harvest_efficiency')}")
    assert stats.get('harvest_efficiency') == 0.5
    
    print("\n[SUCCESS] v4.16 Neural-Energy Harvesting verified.")

if __name__ == "__main__":
    verify_v416()
