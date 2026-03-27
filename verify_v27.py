from system_engine import SystemEngine
import os

engine = SystemEngine()
old_pos = engine.node_positions.copy()
print(f"Pre-Optimization positions: {len(old_pos)}")

success = engine.optimize_visual_layout()
new_pos = engine.node_positions

print(f"Post-Optimization positions: {len(new_pos)}")
if success and len(new_pos) >= len(old_pos):
    print("VERIFIED: Visual Layout Optimizer is operational.")
    # Show a few moves
    for nid in list(new_pos.keys())[:3]:
        old = old_pos.get(nid, (0,0))
        curr = new_pos[nid]
        print(f"  Node {nid:15} | Old: {old} -> New: {curr}")
else:
    print("FAILED: Layout optimization regression detected.")
