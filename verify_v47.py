import os
from system_engine import SystemEngine

def test_neural_entropy():
    print("Testing Neural-Entropy (Version 4.7 Audit)...")
    engine = SystemEngine()
    test_dna = "test_dna_blob.py"
    
    # 1. Inject Bloat
    print("\n--- Phase 1: Bloat Injection ---")
    bloated_content = [
        "def main():\n",
        "    print('Normal Logic')\n",
        "    # DIVERGENCE_CANDIDATE_1: Bloat line 1\n",
        "    # SANDBOX_SEED: Bloat line 2\n",
        "    return True\n"
    ]
    with open(test_dna, "w", encoding="utf-8") as f:
        f.writelines(bloated_content)
    
    initial_entropy = engine.get_entropy_score(test_dna)
    print(f"Initial Entropy: {initial_entropy:.4f}")

    # 2. Run Refactoring
    print("\n--- Phase 2: Refactoring Execution ---")
    success = engine.refactor_neutral_logic(test_dna)
    
    if success:
        print("✅ SUCCESS: Refactoring engine executed.")
    else:
        print("❌ FAILURE: Refactoring engine failed to execute.")

    # 3. Verify Cleanup
    with open(test_dna, "r", encoding="utf-8") as f:
        clean_content = f.read()
    
    markers = ["DIVERGENCE_CANDIDATE", "SANDBOX_SEED"]
    still_bloated = any(m in clean_content for m in markers)
    
    if not still_bloated:
        print("✅ SUCCESS: Redundant markers successfully pruned.")
    else:
        print("❌ FAILURE: Bloat markers still present in DNA.")
        print(f"Residual content:\n{clean_content}")

    final_entropy = engine.get_entropy_score(test_dna)
    print(f"Final Entropy: {final_entropy:.4f}")
    
    # Cleanup test file
    if os.path.exists(test_dna):
        os.remove(test_dna)

if __name__ == "__main__":
    test_neural_entropy()
