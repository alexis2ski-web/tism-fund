"""Build data.json for the tism fund app from an ArtifactData dump.

Usage: python3 -I tools/build_data.py <dump_dir> <output data.json>

<dump_dir> holds the folders nights/, nflDays/, news/ and fantasyWeeks/, each with one
JSON file per document, as written by ArtifactData list/query with out_dir.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LIMITS = {"nights": 60, "nflDays": 60, "news": 7, "fantasyWeeks": 20}


def load(folder: Path, collection: str):
    docs = []
    for f in sorted((folder / collection).glob("*.json")):
        raw = json.loads(f.read_text(encoding="utf-8"))
        doc = raw.get("data", raw) if isinstance(raw, dict) else None
        if not isinstance(doc, dict):
            continue
        if collection == "fantasyWeeks":
            doc = {"_id": f.stem, **doc}
        docs.append(doc)
    key = (lambda d: d.get("week", 0)) if collection == "fantasyWeeks" else (lambda d: d.get("date", ""))
    docs.sort(key=key, reverse=True)
    return docs[: LIMITS[collection]]


def main():
    dump, out = Path(sys.argv[1]), Path(sys.argv[2])
    data = {c: load(dump, c) for c in LIMITS}
    data["synced"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {out}: " + ", ".join(f"{len(data[c])} {c}" for c in LIMITS))


if __name__ == "__main__":
    main()
