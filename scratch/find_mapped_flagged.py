import json
import os

WORKSPACE_DIR = r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials"
MAPPINGS_FILE = os.path.join(WORKSPACE_DIR, "scratch", "extracted_wt_mappings.json")
REVIEW_FILE = os.path.join(WORKSPACE_DIR, "sources-needing-review.md")

# Load extracted mappings
with open(MAPPINGS_FILE, "r", encoding="utf-8") as f:
    wt_mappings = json.load(f)

# Group wt_mappings by file and old_url
wt_map = {}
for item in wt_mappings:
    # item has 'file', 'old_url', 'new_url'
    # We want to map old_url -> new_url, but since diff direction was main -> wt,
    # let's look at the mapping direction.
    # If the main branch has the old URL and wt has the new URL, then:
    # old_url (main) -> new_url (wt)
    # If main has the new URL and wt has the old URL, then it is:
    # new_url (wt) -> old_url (main) (which we don't want)
    # Let's see: we know that the flagged URLs are the ones in sources-needing-review.md.
    # So if old_url or new_url in wt_mappings matches a flagged URL, we can map it to the other!
    wt_map[(item["file"], item["old_url"])] = item["new_url"]
    wt_map[(item["file"], item["new_url"])] = item["old_url"]

# Parse flagged URLs from sources-needing-review.md
flagged = []
with open(REVIEW_FILE, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("|") and not line.startswith("| ---") and not line.startswith("| Article Slug"):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 3:
                slug = parts[0]
                idx = parts[1]
                url = parts[2]
                flagged.append({"slug": slug, "idx": idx, "url": url})

print(f"Total flagged URLs: {len(flagged)}")

resolved_count = 0
for entry in flagged:
    url = entry["url"]
    slug = entry["slug"]
    
    # Find matching files for this slug
    # We will search in wt_map keys
    found_mapping = None
    for (f_name, old_u), new_u in wt_map.items():
        # Check if the url matches one of the endpoints of the mapping
        # and if the file name is relevant (could be kitchen.py, nursery.py, etc.)
        if old_u == url:
            # Let's verify if the slug is associated with this file
            # (Just print it out for verification)
            found_mapping = new_u
            break
            
    if found_mapping:
        resolved_count += 1
        print(f"Resolved from WT: {slug} (source {entry['idx']}) | {url} -> {found_mapping}")
    else:
        print(f"NOT resolved: {slug} (source {entry['idx']}) | {url}")

print(f"Total resolved: {resolved_count} / {len(flagged)}")
