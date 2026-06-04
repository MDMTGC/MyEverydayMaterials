import json
import re
from pathlib import Path

subagents = {
    "PersonalCare_Cleaning": "6c919d5f-e04f-474e-a60f-706d4ff23cd1",
    "Household_PetCare": "b904725a-cefe-4bc9-b7cd-867ac94b7dec",
}

brain_dir = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain")

# Slugs we are interested in for Personal Care & Cleaning:
pc_slugs = [
    "methylene-glycol-hair", "microbeads-exfoliants", "nail-polish-toxic-trio", 
    "parabens-preservatives", "pfas-dental-floss", "phthalates-cosmetics", 
    "quats-disinfectants", "sodium-bicarbonate", "sodium-lauryl-sulfate", 
    "talc-asbestos-risk", "titanium-dioxide-toothpaste", "triclosan-antibacterial"
]

# Slugs we are interested in for Household & Pet Care:
hh_slugs = [
    "aerosol-propellants", "air-freshener-phthalates", "fiberglass-mattress-covers", 
    "flame-retardants-foam", "formaldehyde-mdf-furniture", "hidden-fragrance-pet-wipes", 
    "melamine-pet-bowls", "microplastics-synthetic-laundry", "perchloroethylene-dry-cleaning", 
    "plastic-water-fountains", "polyurethane-foam-offgassing", "polyurethane-pet-beds", 
    "pvc-vinyl-flooring", "pvc-vinyl-pet-toys", "vocs-paint-carpet", "chemical-flea-collars",
    "essential-oil-diffusers"
]

def search_logs(name, conv_id, slugs):
    log_file = brain_dir / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
    print(f"\n=================== SEARCHING {name} LOGS ===================")
    if not log_file.exists():
        print("Log file does not exist.")
        return
        
    steps = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                steps.append(json.loads(line))
                
    # Search for occurrences of target slugs in model messages
    for idx, step in enumerate(steps):
        content = step.get("content", "")
        if step.get("source") != "MODEL" or not content:
            continue
            
        # If the content matches one of our slugs and contains "http"
        for slug in slugs:
            if slug in content and "http" in content:
                # Look for a mapping, list, or JSON dictionary around the match
                lines = content.split("\n")
                matched_lines = []
                for i, l in enumerate(lines):
                    if slug in l or (i > 0 and slug in lines[i-1]) or (i < len(lines)-1 and slug in lines[i+1]):
                        matched_lines.append((i, l))
                
                if matched_lines:
                    print(f"Step {idx}: Found slug '{slug}' reference:")
                    # Print 10 lines before and after the first match
                    first_match_idx = matched_lines[0][0]
                    start = max(0, first_match_idx - 5)
                    end = min(len(lines), first_match_idx + 10)
                    print("\n".join(lines[start:end]))
                    print("-" * 50)
                    break

search_logs("PersonalCare_Cleaning", "6c919d5f-e04f-474e-a60f-706d4ff23cd1", pc_slugs)
search_logs("Household_PetCare", "b904725a-cefe-4bc9-b7cd-867ac94b7dec", hh_slugs)
