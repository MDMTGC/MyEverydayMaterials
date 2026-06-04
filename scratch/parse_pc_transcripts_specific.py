import json
import re
from pathlib import Path

conv_id = "6c919d5f-e04f-474e-a60f-706d4ff23cd1"
log_file = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain") / conv_id / ".system_generated" / "logs" / "transcript.jsonl"

if not log_file.exists():
    print("Does not exist")
    exit()

urls = [
    "formaldehyde-releasers",
    "formaldehyde-cosmetics-what-you-should-know",
    "the-toxic-twenty/parabens",
    "synthetic-turf-pfas"
]

steps = []
with open(log_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            steps.append(json.loads(line))

for idx, step in enumerate(steps):
    content = step.get("content", "")
    if not content:
        continue
    for url in urls:
        if url in content:
            print(f"Step {idx} ({step.get('source')}): Found reference to '{url}'")
            # Let's search for lines containing 'http' near the reference
            lines = content.split("\n")
            for i, l in enumerate(lines):
                if url in l:
                    start = max(0, i - 4)
                    end = min(len(lines), i + 15)
                    print(f"--- Context (Step {idx}): ---")
                    print("\n".join(lines[start:end]))
                    print("-" * 50)
                    break
            break
