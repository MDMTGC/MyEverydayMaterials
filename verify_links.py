import os
import re
import urllib.request
import urllib.error
from pathlib import Path

def check_amazon_links():
    base_dir = Path(r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials")
    categories = ['kitchen', 'nursery', 'pet_care', 'household', 'personal_care', 'cleaning', 'tech_office', 'outdoor', 'surfaces_fabrics']
    
    link_pattern = re.compile(r'href="(https://www\.amazon\.com/[^"]+)"')
    all_links = set()
    link_to_files = {}

    print("Scanning HTML files for Amazon links...")
    for cat in categories:
        cat_dir = base_dir / cat
        if not cat_dir.exists():
            continue
        for html_file in cat_dir.glob("*.html"):
            content = html_file.read_text(encoding="utf-8")
            matches = link_pattern.findall(content)
            for match in matches:
                all_links.add(match)
                if match not in link_to_files:
                    link_to_files[match] = []
                link_to_files[match].append(str(html_file))

    print(f"Found {len(all_links)} unique Amazon links. Verifying...")
    
    broken_links = {}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    import time
    for i, link in enumerate(list(all_links)):
        if "s?k=" in link: # Search links rarely 404, skip or check? Let's check them too just in case but they usually return 200 even if no results.
            # actually checking search links is fine
            pass
            
        print(f"[{i+1}/{len(all_links)}] Checking {link}")
        req = urllib.request.Request(link, headers=headers)
        try:
            # Amazon often blocks scripted requests with 503, but 404 is what we care about
            with urllib.request.urlopen(req, timeout=10) as response:
                pass # 200 OK
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"  -> 404 Not Found!")
                broken_links[link] = link_to_files[link]
            elif e.code == 503:
                # Amazon bot protection, usually means the page exists but we're blocked
                pass
            else:
                print(f"  -> HTTP Error: {e.code}")
        except urllib.error.URLError as e:
            print(f"  -> URL Error: {e.reason}")
        except Exception as e:
            print(f"  -> Error: {e}")
        
        time.sleep(1) # Be gentle
        
    print("\n--- Summary ---")
    if not broken_links:
        print("No broken 404 links found!")
    else:
        print(f"Found {len(broken_links)} broken links:")
        for link, files in broken_links.items():
            print(f"- {link}")
            for f in set(files):
                print(f"  in {f}")

if __name__ == "__main__":
    check_amazon_links()
