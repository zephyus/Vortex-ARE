from system_engine import SystemEngine

engine = SystemEngine()
scores = {}
hotspots = engine.check_code_health()

print("--- Metabolic Efficiency Audit ---")
for fname, func, length, m_score in hotspots:
    print(f"File: {fname:20} | Score: {m_score:5} | Lines: {length:3} | Func: {func}")

if len(hotspots) > 0:
    print("VERIFIED: Metabolic Scoring engine is generating heatmap data.")
else:
    print("FAILED: No metabolic hotspots identified.")
