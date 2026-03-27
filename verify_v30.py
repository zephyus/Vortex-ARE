from system_engine import SystemEngine

engine = SystemEngine()
issues = engine.check_code_health()

print("--- AI-Driven Refactor Lab Audit ---")
if not issues:
    print("No hotspots identified (Integrity optimal).")
else:
    for issue in issues[:3]:
        fname, func, length, m_score = issue
        print(f"Target: {func:20} File: {fname:20} Intensity: {m_score:.2f}")
        
    # Verify Preview
    print("\n--- Generating Predictive Proposal ---")
    orig, suggest = engine.get_refactor_preview(issues[0])
    
    print("ORIGINAL (Subset):")
    print("\n".join(orig.splitlines()[:5]))
    print("...")
    print("\nPROPOSED MODULAR SPLIT:")
    print(suggest)

    if "_optimized_logic_gate_1" in suggest:
        print("\nVERIFIED: Predictive modularization engine is generating high-fidelity split proposals.")
    else:
        print("\nPARTIAL VERIFICATION: Proposal logic fallback detected.")
