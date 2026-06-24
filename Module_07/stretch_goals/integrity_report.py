# Strech Goal - 2

from pathlib import Path
import json, os, sys

# Add Module Dir to Sys Path For Imports
MODULE_DIR: Path = Path(__file__).resolve().parents[1]
sys.path.append(f"{MODULE_DIR}")
EVIDENCE_DIR: Path = Path(MODULE_DIR, "evidence")

# Import audit and verify from task_03
from task_03.audit import append_audit
from task_03.verify import verify_chain

# Ensure this exactly matches the LOG path in audit.py
LOG = f"{EVIDENCE_DIR}/Task3_Audit_Log.jsonl"


def run_integrity_report():
    # 1. Clear the log for a fresh test
    if os.path.exists(LOG):
        os.remove(LOG)

    # 2. Write 5 clean records
    print("--- GENERATING 5 CLEAN RECORDS ---")
    for i in range(5):
        append_audit(
            decision="approve" if i % 2 == 0 else "route-to-adjuster",
            slice_attrs="age_band=36-50",
            model_input_vector={"DrivAge": 40 + i, "BonusMalus": 50, "VehAge": 5},
        )

    # 3. Verify clean log
    print("\n--- RUNNING VERIFIER ON CLEAN LOG ---")
    is_clean, msg = verify_chain(LOG)
    print(f"[{'PASS' if is_clean else 'FAIL'}] {msg}")

    # 4. Tamper with the log (Simulate Insider Threat)
    print("\n--- SIMULATING INSIDER THREAT ---")
    print("Malicious actor changes record index 2 decision to 'deny'...")
    with open(LOG, "r") as f:
        lines = f.readlines()

    # Parse record at index 2, change a field, and put it back into the list
    tampered_record = json.loads(lines[2])
    tampered_record["decision"] = "deny"
    lines[2] = json.dumps(tampered_record) + "\n"

    # Overwrite the file with the tampered line
    with open(LOG, "w") as f:
        f.writelines(lines)
    print("Tampered log saved.")

    # 5. Verify tampered log
    print("\n--- RUNNING VERIFIER ON TAMPERED LOG ---")
    is_clean, msg = verify_chain(LOG)
    print(f"[{'PASS' if is_clean else 'FAIL'}] {msg}")


if __name__ == "__main__":
    run_integrity_report()
