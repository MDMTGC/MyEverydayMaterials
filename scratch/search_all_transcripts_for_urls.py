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

urls_to_find = [
    "formaldehyde-releasers",
    "formaldehyde-cosmetics-what-you-should-know",
    "the-toxic-twenty/parabens",
    "synthetic-turf-pfas",
    "https://www.epa.gov/",
    "https://www.atsdr.cdc.gov/toxprofiledocs/index.html",
    "https://cir-safety.org/sites/default/files/SLS.pdf"
]

for name, conv_id in subagents.items():
    log_file = brain_dir / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
    if not log_file.exists():
        continue
    
    steps = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                steps.append(json.loads(line))
                
    for idx, step in enumerate(steps):
        content = step.get("content", "")
        if not content:
            continue
        for url in urls_to_find:
            if url in content:
                # Print the matching paragraph or block of text containing the url
                # Let's split content by paragraphs and print the one matching the url
                paragraphs = content.split("\n\n")
                for p in paragraphs:
                    if url in p:
                        print(f"[{name}] Step {idx} | Found '{url}':")
                        print(p.strip())
                        print("-" * 50)
                        break
