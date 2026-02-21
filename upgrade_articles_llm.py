import os
import sys
import importlib
import json
from pathlib import Path
from google import genai
from google.genai import types

def get_gold_standard_example():
    return """
    {
        "slug": "pfas-forever-chemicals",
        "title": "PFAS in Your Kitchen: What &ldquo;Forever Chemicals&rdquo; Really Mean for Your Health",
        "meta_description": "Science-backed guide to PFAS forever chemicals in cookware and food packaging. Learn the real risks and discover safer alternatives.",
        "verdict_level": "verdict-avoid",
        "verdict_rating": "Avoid Where Possible &mdash; These chemicals never break down",
        "verdict_summary": "PFAS (per- and polyfluoroalkyl substances) are linked to cancer, thyroid disease, and immune suppression. They persist indefinitely in the body and environment. The EPA set a near-zero limit (4 ppt) for drinking water in 2024, signaling serious concern. Replace PFAS-coated cookware and avoid microwave popcorn bags.",
        "sections": [
            {
                "id": "what-are-pfas",
                "heading": "What Are PFAS?",
                "content": "<p>PFAS stands for per- and polyfluoroalkyl substances...</p>"
            },
            {
                "id": "health-risks",
                "heading": "The Health Risks",
                "content": "<p>The scientific consensus on PFAS has shifted dramatically...</p>\\n<ul class=\\"key-facts\\">\\n  <li><span class=\\"fact-label\\">Cancer</span> PFOA classified as a Group 2B carcinogen...</li>\\n</ul>\\n<div class=\\"callout callout-danger\\">\\n  <strong>Key fact:</strong> A 2023 study found...\\n</div>"
            },
            {
                "id": "what-to-do",
                "heading": "What You Can Do Right Now",
                "content": "<p>You don&rsquo;t need to panic, but you should reduce exposure where practical...</p>"
            }
        ],
        "alternatives": [
            {
                "name": "Lodge 12-Inch Cast Iron Skillet",
                "type": "Cast Iron",
                "description": "Pre-seasoned, PFAS-free, and virtually indestructible.",
                "pros": "Lasts a lifetime, zero chemical coatings",
                "cons": "Heavy, requires seasoning maintenance",
                "asin": "B00006JSUA"
            }
        ],
        "sources": [
            ("EPA PFAS National Primary Drinking Water Regulation (2024)", "https://www.epa.gov/")
        ]
    }
    """

def generate_new_article(client, slug, old_data):
    # This function is no longer used directly in the loop as we baked it in to handle retries properly.
    pass

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY environment variable required.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    
    categories_to_upgrade = ['pet_care', 'surfaces_fabrics', 'personal_care', 'cleaning', 'tech_office']
    base_dir = Path(r"c:\\Users\\MDMTGC\\Desktop\\MyEverydayMaterials\\MyEverydayMaterials\\articles")
    
    for target_category in categories_to_upgrade:
        file_path = base_dir / f"{target_category}.py"
        
        if not file_path.exists():
            print(f"File {file_path} not found. Skipping.")
            continue
            
        sys.path.append(str(base_dir.parent))
        try:
            # Need to reload the module if we are looping
            if f"articles.{target_category}" in sys.modules:
                sys.modules.pop(f"articles.{target_category}", None)
            module = importlib.import_module(f"articles.{target_category}")
        except ModuleNotFoundError:
            print(f"Module articles.{target_category} not found. Skipping.")
            continue
            
        old_articles = getattr(module, "articles", None)
        
        # If it's already a list (ARTICLES), it means it was previously upgraded (partially or fully)
        is_already_upgraded = False
        if getattr(module, "ARTICLES", None):
             print(f"\\n--- Found ARTICLES list in {target_category}. Checking for incomplete entries... ---")
             old_articles_list = getattr(module, "ARTICLES")
             old_articles = {art['slug']: art for art in old_articles_list}
             is_already_upgraded = True
             
        if not old_articles or not isinstance(old_articles, dict):
            print(f"Could not find 'articles' dictionary or list in {file_path}. Skipping.")
            continue
            
        if not is_already_upgraded:
             print(f"\\n--- Found {len(old_articles)} articles in {target_category} (Dict Format). Translating... ---")
        
        new_articles_list = []
        
        for i, (slug, old_data) in enumerate(old_articles.items()):
            # Check if it was already successfully generated previously
            if is_already_upgraded and old_data.get('verdict_summary') != 'Failed to generate.':
                 print(f"[{i+1}/{len(old_articles)}] Skipping {slug} (Already Upgraded)")
                 new_articles_list.append(old_data)
                 continue
                 
            print(f"[{i+1}/{len(old_articles)}] Upgrading {slug}...")
            import time
            time.sleep(4) # Protect against the 15 RPM rate limit
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    prompt = f"""You are a World-Class Senior Scientific Writer for "Everyday Materials". 
Your task is to rewrite a basic, short article into our Kitchen "Gold Standard" format.

Input Data for '{slug}':
{json.dumps(old_data, indent=2)}

Requirements:
1. Return purely valid Python code (a single Python dictionary) matching the exact schema of our Gold Standard.
2. The output must NOT be wrapped in markdown code blocks like ```python. Just the dictionary starting with {{}} and ending with {{}}.
3. Create a compelling `title` (Topic: Problem & Solution format).
4. `verdict_level` must be one of: 'verdict-avoid', 'verdict-caution', 'verdict-safe'.
5. `verdict_summary` must be a deeply researched, 4-5 sentence summary of the specific chemical risk and mechanism of action.
6. Generate exactly 3 well-written `sections` using proper HTML (`<p>`, `<ul>`, `<strong>`, etc.). Include a `<ul class="key-facts">` list with `<span class="fact-label">` tags in the Health Risks section, and a `<div class="callout callout-warning">` (or info/safe/danger) somewhere in the text.
7. Generate EXACTLY 3-4 specific Amazon product recommendations in `alternatives`. You must provide realistic, real-world `asin` values for these products (e.g. B00006JSUA type strings, not generic).
8. `sources` should be a list of tuples containing (Title, URL) of real scientific references (e.g. FDA, EPA, WHO, specific journals).

Gold Standard Schema Reference:
{get_gold_standard_example()}

Do not output anything except the evaluated Python dictionary.
"""
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    text = response.text.strip()
                    if text.startswith("```python"):
                        text = text[9:]
                    elif text.startswith("```json"):
                        text = text[7:]
                    if text.startswith("```"):
                        text = text[3:]
                    if text.endswith("```"):
                        text = text[:-3]
                    
                    # Check for json/dict syntax issues
                    new_data = eval(text.strip())
                    new_data['slug'] = slug
                    new_articles_list.append(new_data)
                    break
                except Exception as e:
                    print(f"   Failed to generate {slug} (Attempt {attempt+1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(65)
            else:
                print(f"   Using fallback for {slug}")
                new_articles_list.append({"slug": slug, "title": old_data.get("title", slug), "verdict_level": "verdict-caution", "verdict_summary": "Failed to generate.", "sections": [], "alternatives": [], "sources": []})
                
        # Write the new file
        output_code = f'\"\"\"Upgraded {target_category} article data.\"\"\"\\n\\n'
        output_code += "ARTICLES = [\\n"
        for art in new_articles_list:
            output_code += "    " + json.dumps(art, indent=4) + ",\\n"
        output_code += "]\\n"
        
        # Backup original
        import shutil
        shutil.copy(file_path, base_dir / f"{target_category}.py.bak")
        
        file_path.write_text(output_code, encoding="utf-8")
        print(f"Successfully wrote {len(new_articles_list)} articles to {file_path}")

if __name__ == "__main__":
    main()
