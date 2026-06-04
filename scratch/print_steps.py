import json
from pathlib import Path

conv_id = "6c919d5f-e04f-474e-a60f-706d4ff23cd1"
log_file = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain") / conv_id / ".system_generated" / "logs" / "transcript.jsonl"

if not log_file.exists():
    print("Does not exist")
    exit()

steps = []
with open(log_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            steps.append(json.loads(line))

for idx in range(220, 240):
    if idx < len(steps):
        step = steps[idx]
        print(f"\n=================== STEP {idx} ({step.get('source')}) ===================")
        content = step.get("content", "")
        # Print content, up to 2000 chars
        print(content[:2000])
        if len(content) > 2000:
            print("...")
