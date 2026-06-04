import re
from pathlib import Path

diffs_path = Path(r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials\scratch\all_subagent_diffs.txt")
raw_data = diffs_path.read_bytes()
try:
    content = raw_data.decode("utf-16")
except UnicodeDecodeError:
    content = raw_data.decode("utf-8")


# Let's split by file diffs
file_sections = content.split("--- Diff in ")
mappings = {}

for section in file_sections:
    if not section.strip():
        continue
    
    lines = section.split("\n")
    filename = lines[0].strip()
    
    # We will look for pairs of - and + lines containing http URLs
    # Since diffs are line-by-line, we can search for a block of '-' lines and then a block of '+' lines
    # Let's parse blocks of lines.
    # An easy way: we track lines that start with '-' and lines that start with '+'
    # For a given change hunk, we look at lines with '-' and lines with '+'
    # Let's do a sliding window or a simple hunk-based match.
    # Since we only want to map URLs, we can parse out lines with 'https://' or 'http://'
    # and find matching title/url pairs.
    
    # Let's find all chunks
    hunks = []
    current_hunk = []
    for line in lines[1:]:
        if line.startswith("@@"):
            if current_hunk:
                hunks.append(current_hunk)
                current_hunk = []
        elif line.startswith("-") or line.startswith("+"):
            current_hunk.append(line)
    if current_hunk:
        hunks.append(current_hunk)
        
    for hunk in hunks:
        minus_lines = [l[1:].strip() for l in hunk if l.startswith("-")]
        plus_lines = [l[1:].strip() for l in hunk if l.startswith("+")]
        
        # Extract URLs
        minus_urls = []
        for ml in minus_lines:
            match = re.search(r'"(https?://[^"]+)"', ml)
            if match:
                minus_urls.append(match.group(1))
                
        plus_urls = []
        for pl in plus_lines:
            match = re.search(r'"(https?://[^"]+)"', pl)
            if match:
                plus_urls.append(match.group(1))
                
        # If we have same number of minus and plus URLs, we map them!
        if len(minus_urls) == len(plus_urls) and len(minus_urls) > 0:
            for m_url, p_url in zip(minus_urls, plus_urls):
                if m_url != p_url:
                    key = (filename, m_url)
                    mappings[key] = p_url
        elif len(minus_urls) == 1 and len(plus_urls) == 1:
            key = (filename, minus_urls[0])
            mappings[key] = plus_urls[0]

print(f"Extracted {len(mappings)} mappings:")
for (filename, old_url), new_url in sorted(mappings.items()):
    print(f"  {filename} | {old_url} -> {new_url}")

# Let's save this as a JSON dict
import json
output_mappings = []
for (filename, old_url), new_url in sorted(mappings.items()):
    output_mappings.append({
        "file": filename,
        "old_url": old_url,
        "new_url": new_url
    })
    
with open(r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials\scratch\extracted_wt_mappings.json", "w", encoding="utf-8") as f:
    json.dump(output_mappings, f, indent=2)
