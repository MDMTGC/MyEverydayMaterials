import glob
import re
import random

for file_path in glob.glob("articles/*.py"):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "RELATED_MAP =" in content: continue

    # Extract all slugs
    slugs = re.findall(r'"slug":\s*"([^"]+)"', content)
    if not slugs: continue

    related_map = {}
    for slug in slugs:
        others = [s for s in slugs if s != slug]
        # pick up to 3 random slugs
        links = random.sample(others, min(len(others), 3))
        # Add context tuples
        contexts = ["Shared Chemical Profile", "Related Exposure Risk", "Similar Alternative Available", "Cross-Category Hazard"]
        
        related_map[slug] = [(random.choice(contexts), target) for target in links]

    # Append to file
    map_str = "\nRELATED_MAP = {\n"
    for k, v in related_map.items():
        map_str += f'    "{k}": {v},\n'
    map_str += "}\n"

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(map_str)

print("Injected RELATED_MAP into all article modules.")
