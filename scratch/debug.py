with open('articles/kitchen.py', 'r', encoding='utf-8') as f:
    content = f.read()

slug = 'bamboo-fiber-plates'
slug_pos = content.find(f'"slug": "{slug}"')
next_slug_pos = content.find('"slug":', slug_pos + 10)
if next_slug_pos == -1:
    next_slug_pos = len(content)

block = content[slug_pos:next_slug_pos]

import re
matches = re.findall(r'https?://[^\s"\']+', block)
print("All URLs in block:")
for m in matches:
    if 'bfr' in m:
        print("FOUND BFR URL:", repr(m))
