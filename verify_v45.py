import time
from system_engine import SystemEngine

def test_neural_feedback():
    print("Testing Neural-Feedback (Version 4.5 Audit)...")
    engine = SystemEngine()
    
    # Initial state
    initial_weight = engine.synaptic_weights["complexity"]
    print(f"Initial complexity weight: {initial_weight}")
    
    # 1. Simulate a series of failures for 'complexity'
    print("\n--- Phase 1: Negative Feedback Loop Audit ---")
    borderline_candidate = "print('line')\n" * 450 # Standard threshold is 500
    
    # Should be accepted initially (450 < 500*1.0)
    if engine.synaptic_filter(borderline_candidate):
        print("Initial: Borderline candidate accepted (Correct).")
    else:
        print("Initial: Borderline candidate rejected (Unexpected).")
        
    print("Simulating 5 consecutive verification failures for high-complexity code...")
    for i in range(5):
        engine.apply_synaptic_feedback(success=False, rules_triggered=["complexity"])
        
    final_weight = engine.synaptic_weights["complexity"]
    print(f"Final complexity weight after feedback: {final_weight:.2f}")
    
    # Threshold should now be 500 * final_weight
    # Adjustment was 0.05 * 2 = 0.1 per failure. 5 failures = -0.5. 1.0 - 0.5 = 0.5.
    # New threshold ~ 250.
    
    if not engine.synaptic_filter(borderline_candidate):
        print(f"✅ SUCCESS: Synapse learned. Candidate (450 lines) now suppressed by tightened threshold.")
    else:
        print(f"❌ FAILURE: Synapse failed to learn. Candidate still accepted.")

    # 2. Simulate Positive Feedback
    print("\n--- Phase 2: Positive Feedback Loop Audit ---")
    print("Simulating 5 consecutive verification successes...")
    for i in range(5):
        engine.apply_synaptic_feedback(success=True)
        
    restored_weight = engine.synaptic_weights["complexity"]
    print(f"Restored complexity weight: {restored_weight:.2f}")
    
    if engine.synaptic_filter(borderline_candidate):
        print("✅ SUCCESS: High-resonance state restored. Candidate accepted again.")
    else:
        print("❌ FAILURE: Positive feedback failed to relax thresholds.")

if __name__ == "__main__":
    test_neural_feedback()
