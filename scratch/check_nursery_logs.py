import json
from pathlib import Path

log_file = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain\71730ed9-f117-4b0b-8c98-01469c547bff\.system_generated\logs\transcript.jsonl")

if not log_file.exists():
    print("Does not exist")
    exit()

with open(log_file, "r", encoding="utf-8") as f:
    steps = [json.loads(line) for line in f if line.strip()]

print(f"Total steps: {len(steps)}")
for i, s in enumerate(steps):
    content = s.get("content", "")
    if s.get("source") == "MODEL" and "BisphenolA_FactSheet" in content:
        print(f"\n=================== STEP {i} ===================")
        # print first 1000 chars of content
        print(content[:1500])
        print("...")
