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

terms = ["formaldehyde-releasers", "parabens", "synthetic-turf-pfas", "formaldehyde-cosmetics", "aoec"]

for name, conv_id in subagents.items():
    log_file = brain_dir / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
    if not log_file.exists():
        continue
    
    with open(log_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            step = json.loads(line)
            content = step.get("content", "")
            if not content:
                continue
            for term in terms:
                if term in content:
                    print(f"Found term '{term}' in subagent {name} at step {step.get('step_index') or line_num}")
                    # Print matches
                    lines = content.split("\n")
                    for idx, l in enumerate(lines):
                        if term in l:
                            start = max(0, idx - 3)
                            end = min(len(lines), idx + 8)
                            print(f"  --- Snippet: ---")
                            print("\n".join(lines[start:end]))
                            print("-" * 40)
                            break
