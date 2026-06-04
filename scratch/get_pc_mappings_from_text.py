import json
from pathlib import Path

conv_id = "6c919d5f-e04f-474e-a60f-706d4ff23cd1"
log_file = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain") / conv_id / ".system_generated" / "logs" / "transcript.jsonl"

if not log_file.exists():
    print("Does not exist")
    exit()

with open(log_file, "r", encoding="utf-8") as f:
    steps = [json.loads(line) for line in f if line.strip()]

# Search for any markdown tables or mapping text in the model's responses
for i, s in enumerate(steps):
    if s.get("source") == "MODEL":
        content = s.get("content", "")
        if content:
            # Check if it has markdown tables with URLs or mapping indicator ->
            lines = content.split("\n")
            table_lines = [l for l in lines if "|" in l and "http" in l]
            arrow_lines = [l for l in lines if ("->" in l or "=>" in l or "replace" in l.lower()) and "http" in l]
            
            if len(table_lines) > 2 or len(arrow_lines) > 2:
                print(f"\n=================== STEP {i} ===================")
                print(f"Found {len(table_lines)} table lines and {len(arrow_lines)} arrow/replace lines.")
                # Print the whole step content if it's not too long, or first 2000 chars
                print(content[:2500])
                if len(content) > 2500:
                    print("... [TRUNCATED] ...")
                print("-" * 50)
