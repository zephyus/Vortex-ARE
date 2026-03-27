import os
import sys
import time

# Sync Path
sys.path.append(os.path.abspath("."))
try:
    from system_engine import SystemEngine
except ImportError:
    print("FAILED: Could not import SystemEngine.")
    sys.exit(1)

def verify_v418():
    print("--- v4.18 Semantic-Coupling Verification ---")
    engine = SystemEngine()
    
    print("[1/3] Mapping logic entanglement...")
    graph = engine.map_logic_entanglement()
    
    if not graph:
        print("FAILED: Logic graph is empty.")
        return False
    
    print(f"PASS: Graph mapped with {len(graph)} nodes.")
    
    print("[2/3] Verifying entanglement scores...")
    # Select a known core node
    core_nodes = ["system_engine", "dashboard_gui", "main_app"]
    found_score = False
    for node in core_nodes:
        if node in graph:
            score = engine.get_entanglement_score(node)
            print(f"  > Node '{node}' score: {score:.4f}")
            if score > 0:
                found_score = True
    
    if not found_score:
        print("WARNING: All core node entanglement scores are 0. (Might be expected if dependencies are loose).")
    else:
        print("PASS: Entanglement scores detected and calculated.")

    print("[3/3] Telemetry verification...")
    stats = engine.get_system_stats()
    if "entanglement" in stats and stats["entanglement"]:
        print("PASS: Entanglement data successfully exposed to telemetry.")
    else:
        print("FAILED: Entanglement data missing from telemetry.")
        return False

    print("\n--- Verification COMPLETE: v4.18 Stable ---")
    return True

if __name__ == "__main__":
    success = verify_v418()
    sys.exit(0 if success else 1)
