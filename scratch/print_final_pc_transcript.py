import json
from pathlib import Path

conv_id = "6c919d5f-e04f-474e-a60f-706d4ff23cd1"
log_file = Path(r"C:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials\scratch\term_search_results.txt") # wait, we can read the raw file directly
log_file = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain") / conv_id / ".system_generated" / "logs" / "transcript.jsonl"

if not log_file.exists():
    print("Does not exist")
    exit()

steps = []
with open(log_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            steps.append(json.loads(line))

print(f"Total steps: {len(steps)}")
for idx in range(len(steps) - 6, len(steps)):
    step = steps[idx]
    print(f"\n=================== STEP {idx} ({step.get('source')}) ===================")
    print(step.get("content", ""))
