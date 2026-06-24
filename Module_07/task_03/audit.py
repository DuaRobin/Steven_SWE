from pathlib import Path
import json, hashlib, uuid, datetime, os

MODULE_DIR: Path = Path(__file__).resolve().parents[1]
INPUT_DIR: Path = Path(MODULE_DIR, "task_01", "starter_outputs")
EVIDENCE_DIR: Path = Path(MODULE_DIR, "evidence")
LOG = f"{EVIDENCE_DIR}/Task3_Audit_Log.jsonl"


def last_hash(path):
    if not os.path.exists(path):
        return "GENESIS"
    lines = [l for l in open(path) if l.strip()]
    return json.loads(lines[-1])["record_hash"] if lines else "GENESIS"


def append_audit(decision, slice_attrs, model_input_vector):
    # input_hash: a sha256 of the input vector, hashed with sort_keys=True for stability
    input_hash = hashlib.sha256(
        json.dumps(model_input_vector, sort_keys=True).encode()
    ).hexdigest()
    rec = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "request_id": str(uuid.uuid4()),
        "input_hash": input_hash,
        "model_version": "claims_triage:production",
        "decision": decision,  # approve / route-to-adjuster / deny
        "slice_attrs": slice_attrs,  # the proxy slice from Task 1
        # prev_hash: link this record to the previous one to make the log tamper-evident
        "prev_hash": last_hash(LOG),
    }
    rec["record_hash"] = hashlib.sha256(
        json.dumps(rec, sort_keys=True).encode()
    ).hexdigest()
    with open(LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


if __name__ == "__main__":
    append_audit(
        "route-to-adjuster",
        "age_band=18-25",
        {"DrivAge": 23, "BonusMalus": 90, "VehAge": 2},
    )
    append_audit(
        "approve", "age_band=36-50", {"DrivAge": 44, "BonusMalus": 50, "VehAge": 7}
    )
    print("wrote", LOG)
