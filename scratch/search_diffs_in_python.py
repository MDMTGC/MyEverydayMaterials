import os

diffs_path = r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials\scratch\all_subagent_diffs.txt"
if not os.path.exists(diffs_path):
    print("File does not exist")
    exit()

with open(diffs_path, "rb") as f:
    raw = f.read()

try:
    content = raw.decode("utf-16")
except Exception:
    content = raw.decode("utf-8")

lines = content.split("\n")
print(f"Total lines in diff file: {len(lines)}")

# Find target terms
targets = ["the-toxic-twenty", "formaldehyde-releasers", "parabens", "aoec", "sodium-bicarbonate", "bakingsoda", "cir-safety.org"]

for idx, line in enumerate(lines):
    for term in targets:
        if term in line:
            print(f"\n=================== FOUND '{term}' at line {idx} ===================")
            # Print 10 lines before and 20 lines after
            start = max(0, idx - 10)
            end = min(len(lines), idx + 20)
            for j in range(start, end):
                prefix = ">>>" if j == idx else "   "
                print(f"{prefix} {j}: {lines[j]}")
            break
