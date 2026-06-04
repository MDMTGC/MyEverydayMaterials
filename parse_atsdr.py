import os

content_path = r"C:\Users\MDMTGC\.gemini\antigravity\brain\7e96b97a-cc07-41c4-91f7-a1f9fdb6f7fa\.system_generated\steps\625\content.md"

if not os.path.exists(content_path):
    print("File does not exist")
else:
    size = os.path.getsize(content_path)
    print(f"File size: {size} bytes")
    with open(content_path, "r", encoding="utf-8") as f:
        text = f.read()
    print("First 500 chars:")
    print(repr(text[:500]))
    
    # Let's search case insensitively for "http" to see if there are links
    links = [line for line in text.split("\n") if "http" in line]
    print(f"Lines containing http: {len(links)}")
    for l in links[:20]:
        print(l.strip()[:150])
