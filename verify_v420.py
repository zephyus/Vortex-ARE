
import os
import sys
import json
import psutil
from system_engine import SystemEngine
from unittest.mock import patch, MagicMock

def test_v420_evolution():
    print("--- NEURAL-SYNC META-GOVERNOR VERIFICATION (v4.20) ---")
    engine = SystemEngine()
    
    # Phase 1: Meta-Governance Invariants
    print("[Phase 1: Meta-Governance]")
    
    # Mock CPU > 70
    with patch('psutil.cpu_percent', return_value=85.0):
        is_safe = engine.apply_meta_governance()
        status = "PASS" if not is_safe else "FAIL"
        print(f"  CPU Invariant (>70%): {status} (Blocked={not is_safe})")

    # Mock Disk Usage > 90
    mock_disk = MagicMock()
    mock_disk.percent = 95.0
    with patch('psutil.disk_usage', return_value=mock_disk):
        is_safe = engine.apply_meta_governance()
        status = "PASS" if not is_safe else "FAIL"
        print(f"  Disk Invariant (>90%): {status} (Blocked={not is_safe})")

    # Mock Safe System
    with patch('psutil.cpu_percent', return_value=10.0), \
         patch('psutil.disk_usage', return_value=MagicMock(percent=30.0)):
        is_safe = engine.apply_meta_governance()
        status = "PASS" if is_safe else "FAIL"
        print(f"  Safe Invariants (10% CPU, 30% Disk): {status} (Allowed={is_safe})")

    # Phase 2: DNA Integrity Manifest
    print("[Phase 2: Hardened-DNA Manifest]")
    success, backup_path = engine.perform_backup(reason="v4.20-Verification")
    if success and os.path.exists(backup_path):
        manifest_path = backup_path + ".manifest.json"
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            integrity = manifest.get("integrity", "")
            if integrity.startswith("sha3-256:"):
                print(f"  SHA3-256 Manifest: PASS (Integrity: {integrity[:25]}...)")
            else:
                print(f"  SHA3-256 Manifest: FAIL (Invalid hash format: {integrity})")
            
            print(f"  Governor Version: {'PASS' if manifest.get('governor_v') == '4.20' else 'FAIL'}")
        else:
            print("  Manifest File: FAIL (Missing .manifest.json)")
    else:
        print("  Backup Generation: FAIL")

    # Phase 3: Telemetry Handshake
    print("[Phase 3: Telemetry Update]")
    stats = engine.get_system_stats()
    gov_status = stats.get("governor_status", "Missing")
    print(f"  Governor Telemetry: {'PASS' if isinstance(gov_status, bool) else 'FAIL'} (Status: {gov_status})")

    print("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    test_v420_evolution()
