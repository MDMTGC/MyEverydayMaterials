import os
import re
from pathlib import Path

# Load URLs from sources-needing-review.md
flagged_urls = []
with open("sources-needing-review.md", "r", encoding="utf-8") as f:
    for line in f:
        # Match table rows: | Article Slug | Source # | Current URL | Reason Flagged |
        m = re.match(r'^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|', line)
        if m:
            slug = m.group(1).strip()
            src_num = m.group(2).strip()
            url = m.group(3).strip()
            reason = m.group(4).strip()
            if slug != "Article Slug" and not slug.startswith("---"):
                flagged_urls.append((slug, url))

print(f"Loaded {len(flagged_urls)} flagged URLs from sources-needing-review.md")

articles_dir = Path("articles")
found_count = 0
not_found_count = 0

for slug, url in flagged_urls:
    found_in_any = False
    for py_file in articles_dir.glob("*.py"):
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()
        if url in content:
            found_in_any = True
            # Find line number
            lines = content.splitlines()
            for line_idx, line_content in enumerate(lines, 1):
                if url in line_content:
                    print(f"FOUND: articles/{py_file.name}:{line_idx} - {slug} -> {url}")
    # Also check generate_articles.py
    with open("generate_articles.py", "r", encoding="utf-8") as f:
        content = f.read()
    if url in content:
        found_in_any = True
        lines = content.splitlines()
        for line_idx, line_content in enumerate(lines, 1):
            if url in line_content:
                print(f"FOUND: generate_articles.py:{line_idx} - {slug} -> {url}")
                
    if found_in_any:
        found_count += 1
    else:
        print(f"NOT FOUND in articles/*.py: {slug} -> {url}")
        not_found_count += 1

print(f"\nTotal found in main: {found_count}, not found: {not_found_count}")
