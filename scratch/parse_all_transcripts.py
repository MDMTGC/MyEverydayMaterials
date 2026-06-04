import json
import re
from pathlib import Path

subagents = {
    "Kitchen_Nursery": "71730ed9-f117-4b0b-8c98-01469c547bff",
    "PersonalCare_Cleaning": "6c919d5f-e04f-474e-a60f-706d4ff23cd1",
    "Household_PetCare": "b904725a-cefe-4bc9-b7cd-867ac94b7dec",
    "Tech_Outdoor": "be3fdaf6-a958-477a-9e0c-2cc4ee1e31ec",
}

brain_dir = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain")

for name, conv_id in subagents.items():
    log_file = brain_dir / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
    print(f"\n=================== PARSING LOGS: {name} ({conv_id}) ===================")
    if not log_file.exists():
        print("Log file does not exist.")
        continue
    
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            step = json.loads(line)
            content = step.get("content", "")
            
            # Search for JSON blocks in content
            if step.get("source") == "MODEL" and content:
                # Find JSON block
                json_blocks = re.findall(r"```json\s*(.*?)\s*```", content, re.DOTALL)
                for jb in json_blocks:
                    if "http" in jb and ("mapping" in jb or "{" in jb):
                        print("--- Found JSON Block ---")
                        # Try parsing or printing first 500 chars
                        print(jb[:1500])
                        print("...")
                
                # Also print any markdown lines containing "http" and "->"
                lines = content.split("\n")
                mappings_found = []
                for l in lines:
                    if "http" in l and ("->" in l or "=>" in l or "to" in l):
                        mappings_found.append(l)
                if len(mappings_found) > 5:
                    print(f"--- Found {len(mappings_found)} potential mapping lines. Showing first few: ---")
                    for ml in mappings_found[:15]:
                        print("  ", ml)
