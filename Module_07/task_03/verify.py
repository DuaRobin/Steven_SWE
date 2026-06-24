from pathlib import Path
import json, hashlib, uuid, datetime, os

MODULE_DIR: Path = Path(__file__).resolve().parents[1]
INPUT_DIR: Path = Path(MODULE_DIR, "task_01", "starter_outputs")
EVIDENCE_DIR: Path = Path(MODULE_DIR, "evidence")
LOG = f"{EVIDENCE_DIR}/audit_log.jsonl"


def verify_chain(path):
    prev = "GENESIS"
    for i, line in enumerate(l for l in open(path) if l.strip()):
        rec = json.loads(line)
        if rec["prev_hash"] != prev:
            return False, f"chain break at record {i}"
        body = {k: v for k, v in rec.items() if k != "record_hash"}
        if (
            hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
            != rec["record_hash"]
        ):
            return False, f"record {i} was altered"
        prev = rec["record_hash"]
    return True, "chain intact"


if __name__ == "__main__":
    print(verify_chain(LOG))
