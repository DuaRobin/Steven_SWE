from pathlib import Path
import json

MODULE_DIR: Path = Path(__file__).resolve().parents[1]
INPUT_DIR: Path = Path(MODULE_DIR, "task_01", "starter_outputs")
EVIDENCE_DIR: Path = Path(MODULE_DIR, "evidence")
LOG = f"{EVIDENCE_DIR}/audit_log.jsonl"

latest = json.loads([l for l in open(LOG) if l.strip()][-1])
print(json.dumps(latest, indent=2))
assert len(latest["input_hash"]) == 64
