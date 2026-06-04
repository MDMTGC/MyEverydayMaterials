import os
import re
from pathlib import Path

WORKSPACE_DIR = r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials"
ARTICLES_DIR = os.path.join(WORKSPACE_DIR, "articles")
REVIEW_FILE = os.path.join(WORKSPACE_DIR, "sources-needing-review.md")

# Parse flagged URLs from sources-needing-review.md
# Format of line: | Article Slug | Source # | Current URL | Reason Flagged |
flagged = []
with open(REVIEW_FILE, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("|") and not line.startswith("| ---") and not line.startswith("| Article Slug"):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 3:
                slug = parts[0]
                idx = parts[1]
                url = parts[2]
                reason = parts[3] if len(parts) > 3 else ""
                flagged.append({"slug": slug, "idx": idx, "url": url, "reason": reason})

print(f"Parsed {len(flagged)} flagged entries from report.")

# Search files
files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith(".py")]

still_present = []
for entry in flagged:
    url = entry["url"]
    slug = entry["slug"]
    found = False
    for f in files:
        fpath = os.path.join(ARTICLES_DIR, f)
        with open(fpath, "r", encoding="utf-8") as file_obj:
            content = file_obj.read()
        if f'"{url}"' in content or f"'{url}'" in content:
            # Check if this slug is in this file (some files contain multiple slugs)
            # A crude check: does the file contain "slug": "slug" or similar?
            if f'"{slug}"' in content or f"'{slug}'" in content:
                still_present.append((f, slug, entry["idx"], url))
                found = True
                break

print(f"Found {len(still_present)} URLs still present in article source files:")
for f, slug, idx, url in still_present:
    print(f"  {f} | {slug} (source {idx}) | {url}")
