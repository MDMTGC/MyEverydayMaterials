import os
import json
from jinja2 import Environment, FileSystemLoader
# Ensure all category modules are imported
from articles import kitchen, cleaning, nursery, pet_care, outdoor

# Configuration
DATA_FILE = "materials_data.json"
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "."  # Root directory for category folders

# Mapping slugs in JSON to article data in Python modules
category_articles = {
    "kitchen": kitchen.articles,
    "cleaning": cleaning.articles,
    "nursery": nursery.articles,
    "pet-care": pet_care.articles,
    "outdoor": outdoor.articles
}

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
article_template = env.get_template("article_template.html")
category_template = env.get_template("category_template.html")

def generate_site():
    # Load registry data
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    for category in data.get("categories", []):
        category_slug = category["slug"]
        category_name = category["name"]
        materials = category.get("materials", [])

        # Create category directory if it doesn't exist
        category_dir = os.path.join(OUTPUT_DIR, category_slug)
        os.makedirs(category_dir, exist_ok=True)

        # Get the article data for this category
        articles_data = category_articles.get(category_slug, {})

        if not articles_data:
            print(f"Skipping {category_name}: No article data found in module.")
            continue

        print(f"Processing category: {category_name}...")

        # 1. Generate Individual Article Pages
        for material in materials:
            material_slug = material["slug"]
            
            # Match JSON slug to the data in our Python modules
            article_info = articles_data.get(material_slug)

            if article_info:
                # Set the output path to match your JSON links (e.g., nursery/slug.html)
                file_path = os.path.join(category_dir, f"{material_slug}.html")
                
                html_content = article_template.render(
                    title=article_info["title"],
                    verdict=article_info["verdict"],
                    content=article_info["content"],
                    sources=article_info.get("sources", []),
                    category_name=category_name,
                    category_slug=category_slug
                )

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"  Generated article: {file_path}")
            else:
                print(f"  Warning: No content found for slug '{material_slug}' in {category_slug}.py")

        # 2. Generate Category Index Page (index.html)
        index_path = os.path.join(category_dir, "index.html")
        index_content = category_template.render(
            category_name=category_name,
            materials=materials
        )
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)
        print(f"  Generated category index: {index_path}")

if __name__ == "__main__":
    generate_site()
    print("\nBuild complete! All synchronized categories have been generated.")
