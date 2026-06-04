import json
from pathlib import Path

conv_id = "6c919d5f-e04f-474e-a60f-706d4ff23cd1"
log_file = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain") / conv_id / ".system_generated" / "logs" / "transcript.jsonl"

if not log_file.exists():
    print("Does not exist")
    exit()

flagged_urls = [
    "https://www.ewg.org/the-toxic-twenty/formaldehyde-releasers",
    "https://www.fda.gov/cosmetics/cosmetic-ingredients/formaldehyde-cosmetics-what-you-should-know",
    "https://www.ewg.org/the-toxic-twenty/parabens"
]

steps = []
with open(log_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            steps.append(json.loads(line))

for idx, step in enumerate(steps):
    content = step.get("content", "")
    if not content:
        continue
    
    # Check if this step has any of the flagged URLs
    for furl in flagged_urls:
        if furl in content:
            print(f"\nFound URL '{furl}' in step {idx} (source: {step.get('source')}):")
            # If the source is MODEL, let's print the entire model message or search for replacements in it
            # We look for lines containing "http" and check if there are new URLs
            lines = content.split("\n")
            for i, l in enumerate(lines):
                if furl in l:
                    # Print 5 lines before and 15 lines after
                    start = max(0, i - 3)
                    end = min(len(lines), i + 12)
                    print(f"--- Context (Line {i}): ---")
                    for j in range(start, end):
                        print(f"  {j}: {lines[j]}")
                    print("-" * 50)
