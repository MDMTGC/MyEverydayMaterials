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
    print(f"\n=================== SUBAGENT LOG TRANSCRIPT: {name} ===================")
    if not log_file.exists():
        print("Does not exist")
        continue
        
    steps = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                steps.append(json.loads(line))
                
    # Search backwards for any step that contains a JSON or table mapping of URLs
    # or look for "http" mappings in user/model messages.
    found_count = 0
    for idx in range(len(steps)-1, -1, -1):
        step = steps[idx]
        content = step.get("content", "")
        if not content:
            continue
            
        # Check if content has many http links (e.g. >= 5) and looks like a summary
        urls = re.findall(r"https?://[^\s\"'<>|]+", content)
        if len(urls) >= 5 and ("mapping" in content.lower() or "replace" in content.lower() or "resolved" in content.lower() or "|" in content):
            print(f"Step {idx} ({step.get('source')}): Found large mapping message ({len(urls)} URLs)")
            # Print the content
            print(content[:3000])
            print("\n... [TRUNCATED] ...\n")
            found_count += 1
            if found_count >= 2: # Show at most 2 messages
                break
