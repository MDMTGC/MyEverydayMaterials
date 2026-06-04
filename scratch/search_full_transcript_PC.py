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

for idx in range(240, len(steps)):
    step = steps[idx]
    content = step.get("content", "")
    if step.get("source") == "MODEL" and content:
        # Check if content looks like it has code changes, file updates, or JSON mapping
        if "replace" in content or "update" in content or "mapping" in content or "SUCCESS" in content or "http" in content:
            print(f"\n=================== STEP {idx} ({step.get('source')}) ===================")
            lines = content.split("\n")
            print(f"Total lines: {len(lines)}")
            # Search for print of file path, code blocks or mappings
            mapping_lines = []
            for i, l in enumerate(lines):
                if "http" in l or "articles/" in l or "replace" in l:
                    mapping_lines.append((i, l))
            
            print(f"Found {len(mapping_lines)} interesting lines. Showing first 30:")
            for i, l in mapping_lines[:30]:
                print(f"  {i}: {l.strip()}")
            
            # Print the first 2000 characters if there are code blocks or JSON
            if "```" in content:
                print("--- Code/JSON block present. First 1000 chars of step content: ---")
                print(content[:1000])
