from pathlib import Path

root = Path(__file__).resolve().parents[2]
bad = []
for p in root.rglob("*"):
    if not p.is_file():
        continue
    if "submission" in p.parts:
        continue
    if p.suffix.lower() not in {".md", ".csv", ".json", ".html", ".py", ".ps1", ".sh", ".txt"}:
        continue
    try:
        p.read_text(encoding="utf-8")
    except Exception as e:
        bad.append((str(p.relative_to(root)), type(e).__name__, str(e)[:160]))
print("BAD", len(bad))
for b in bad:
    print(b)
