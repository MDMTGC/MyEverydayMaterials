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
    print(f"Checking logs for: {name}")
    if not log_file.exists():
        continue
        
    steps = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                steps.append(json.loads(line))
                
    # We will search for steps by MODEL that contain a lot of "http" links (>= 5) and write them to scratch/summary_<name>.txt
    for idx, step in enumerate(steps):
        content = step.get("content", "")
        if step.get("source") == "MODEL" and content:
            urls = re.findall(r"https?://[^\s\"'<>|]+", content)
            if len(urls) >= 5 and ("mapping" in content.lower() or "replace" in content.lower() or "resolved" in content.lower() or "|" in content or "updated" in content.lower()):
                output_path = Path(r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials\scratch") / f"summary_{name}_{idx}.txt"
                output_path.write_text(content, encoding="utf-8")
                print(f"  Wrote step {idx} ({len(urls)} URLs) to {output_path.name}")
