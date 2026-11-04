"""Turn the app's current data.json back into a dump folder for build_data.py.

Usage: python3 -I tools/seed_dump.py <data.json> <dump_dir>

Writes <dump_dir>/<collection>/<doc_id>.json for every document already in the app:
nights, nflDays and news are named by their "date", fantasyWeeks by their "_id".
A sync run then overwrites only the documents that may have changed (fetched fresh
from the artifact) and rebuilds data.json with build_data.py.
"""
import json
import sys
from pathlib import Path

COLLECTIONS = ("nights", "nflDays", "news", "fantasyWeeks")


def main():
    src, dump = Path(sys.argv[1]), Path(sys.argv[2])
    data = json.loads(src.read_text(encoding="utf-8"))
    counts = {}
    for c in COLLECTIONS:
        folder = dump / c
        folder.mkdir(parents=True, exist_ok=True)
        n = 0
        for doc in data.get(c, []):
            doc = dict(doc)
            doc_id = doc.pop("_id", None) if c == "fantasyWeeks" else doc.get("date")
            if not doc_id:
                continue
            (folder / f"{doc_id}.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
            n += 1
        counts[c] = n
    print("seeded " + ", ".join(f"{counts[c]} {c}" for c in COLLECTIONS))


if __name__ == "__main__":
    main()
