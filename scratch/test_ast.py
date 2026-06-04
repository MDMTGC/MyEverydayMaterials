import re
import ast
import os

filepath = r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials\articles\kitchen.py"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Try to find ARTICLES =
m = re.search(r'ARTICLES\s*=\s*(?:\\?\s*)(\[.*\])', content, re.DOTALL)
if m:
    print("Found ARTICLES match!")
    # Let's print the first 200 chars of match
    print(m.group(1)[:200])
    try:
        articles = ast.literal_eval(m.group(1))
        print(f"Successfully evaluated ARTICLES list! Found {len(articles)} articles.")
    except Exception as e:
        print("literal_eval failed:", e)
else:
    print("No ARTICLES match found.")
