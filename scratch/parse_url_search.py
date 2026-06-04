import os

file_path = r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials\scratch\url_search_results.txt"
if not os.path.exists(file_path):
    print("File does not exist")
    exit()

with open(file_path, "rb") as f:
    raw = f.read()

try:
    content = raw.decode("utf-16")
except Exception:
    content = raw.decode("utf-8")

paragraphs = content.split("--------------------------------------------------")
print(f"Total entries: {len(paragraphs)}")

targets = ["formaldehyde-releasers", "formaldehyde-cosmetics", "the-toxic-twenty/parabens", "synthetic-turf-pfas"]

for idx, p in enumerate(paragraphs):
    found = False
    for t in targets:
        if t in p:
            found = True
            break
    if found:
        # Check if the paragraph has a new URL that looks like a replacement
        print(f"\n=================== ENTRY {idx} ===================")
        print(p.strip())
        print("=" * 50)
