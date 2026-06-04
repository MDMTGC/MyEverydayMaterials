import json
from pathlib import Path

conv_id = "6c919d5f-e04f-474e-a60f-706d4ff23cd1"
log_file = Path(r"C:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials\scratch\term_search_results.txt")

# Let's read term_search_results.txt instead, since we already dumped matches there!
# We can decode it and search for relevant lines.
if not log_file.exists():
    print("Does not exist")
    exit()

with open(log_file, "rb") as f:
    raw = f.read()

try:
    content = raw.decode("utf-16")
except Exception:
    content = raw.decode("utf-8")

lines = content.split("\n")
print(f"Total lines in search results: {len(lines)}")

# Let's search for "PersonalCare_Cleaning" and show lines near it containing http
pc_section = False
for idx, line in enumerate(lines):
    if "PersonalCare_Cleaning" in line:
        pc_section = True
        print(f"\n=================== {line} ===================")
    elif "===================" in line and pc_section:
        # If another section starts, we don't stop, but we know it's a new subagent
        pc_section = False
        
    if pc_section:
        if "http" in line or "step" in line.lower() or "found" in line.lower():
            print(f"{idx}: {line.strip()}")
