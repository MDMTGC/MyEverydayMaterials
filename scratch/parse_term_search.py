import os

file_path = r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials\scratch\term_search_results.txt"
if not os.path.exists(file_path):
    print("File does not exist")
    exit()

with open(file_path, "rb") as f:
    raw = f.read()

try:
    content = raw.decode("utf-16")
except Exception:
    content = raw.decode("utf-8")

lines = content.split("\n")
print(f"Total lines: {len(lines)}")

# Let's print out lines containing "http" and one of the terms, or lines that show a mapping
for idx, line in enumerate(lines):
    if "Found term" in line:
        print(line)
    elif "http" in line and ("->" in line or "=>" in line or "replace" in line.lower() or "to" in line.lower() or "dossier" in line.lower()):
        # Print this line and the surrounding 2 lines if it contains any of the target terms
        if any(term in line.lower() for term in ["paraben", "formaldehyde", "aoec", "turf", "soda", "baking"]):
            print(f"Line {idx}: {line.strip()}")
