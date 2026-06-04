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
    print(f"\n=================== SUBAGENT JSON: {name} ({conv_id}) ===================")
    if not log_file.exists():
        print("Log file does not exist.")
        continue
    
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            step = json.loads(line)
            content = step.get("content", "")
            
            # Find JSON code blocks in content
            if step.get("source") == "MODEL" and content:
                json_blocks = re.findall(r"```json\s*(.*?)\s*```", content, re.DOTALL)
                for jb in json_blocks:
                    if "http" in jb and ("{" in jb or "[" in jb):
                        # Clean it up and try to see if it's a mapping
                        try:
                            data = json.loads(jb)
                            # If it's a dict, let's print keys and some values or check if it's our target mapping
                            if isinstance(data, dict):
                                # If it's article_specific_mappings, print it
                                if "article_specific_mappings" in data or any("|" in k for k in data.keys()) or any("http" in k for k in data.keys()):
                                    print("Valid Mapping Dict Found:")
                                    print(json.dumps(data, indent=2))
                            elif isinstance(data, list):
                                # Print first few items
                                print("Valid List Found:")
                                print(json.dumps(data[:3], indent=2))
                        except Exception:
                            # If not valid JSON, just print it as text
                            print("Text block:")
                            print(jb[:1000])
                            print("...")
