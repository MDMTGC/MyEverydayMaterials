import json
from pathlib import Path

log_file = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain\6c919d5f-e04f-474e-a60f-706d4ff23cd1\.system_generated\logs\transcript.jsonl")

if log_file.exists():
    with open(log_file, "r", encoding="utf-8") as f:
        steps = [json.loads(line) for line in f if line.strip()]
        
    print(f"Total steps: {len(steps)}")
    
    # We will search steps in reverse order for any text content containing "http" or "www" and print them.
    for i in range(len(steps) - 1, -1, -1):
        step = steps[i]
        if step.get("source") == "MODEL":
            content = step.get("content", "")
            if content and ("http" in content or "www" in content or "mapping" in content or "replace" in content):
                # Print step index and content snippet
                print(f"\n--- STEP {i} ({step.get('type')}) ---")
                print(content[:1500])
                print("..." if len(content) > 1500 else "")
                print("-" * 60)
                # Keep printing up to 5 steps
                if i < len(steps) - 10:
                    break
else:
    print("Log file does not exist")
