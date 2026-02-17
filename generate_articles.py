#!/usr/bin/env python3
"""Universal static site generator for MyEverydayMaterials."""

import argparse
import html
import importlib
import json
from collections import defaultdict
from datetime import date
from html import unescape
from pathlib import Path

SITE_NAME = "Everyday Materials"
SITE_URL = "https://myeverydaymaterials.com"
AFFILIATE_TAG = "myeverydaymat-20"
CSS_VERSION = "7"
MATERIALS_DATA_FILE = Path("materials_data.json")

EDITORS_NOTE = (
    "<strong>Note from the Editor:</strong> At Everyday Materials, our goal is "
    "to help you navigate the science of your home. We only recommend "
    "&ldquo;Better Alternatives&rdquo; that we&rsquo;ve researched extensively "
    "and would feel safe using in our own kitchens and lives. If you purchase "
    "through one of our links, we may earn a small commission from Amazon at "
    "no extra cost to you. This helps us keep the lights on and the research "
    "coming. Thank you for trusting us."
)

CATEGORIES = {
    "kitchen": {
        "name": "Kitchen &amp; Dining Safety",
        "description": "Science-backed safety guides for kitchen materials — PFAS, BPA, Teflon, melamine, and more. Learn what's safe and find better alternatives.",
        "tagline": "Science-backed guides to the materials that touch your food every day.",
    },
    "nursery": {
        "name": "Nursery &amp; Baby Gear",
        "description": "Evidence-based safety guides for nursery materials — crib mattresses, baby bottles, play mats, and more.",
        "tagline": "Protecting the smallest members of your household from hidden material risks.",
    },
    "pet-care": {
        "name": "Pet Care Safety",
        "description": "Science-backed guides to pet care materials — litters, toys, beds, and more. Keep your pets safe from hidden toxins.",
        "tagline": "Keeping your cats and dogs safe from hidden material hazards.",
    },
    "household": {
        "name": "Household Surfaces &amp; Fabrics",
        "description": "Safety guides for household materials — furniture, flooring, textiles, and indoor air quality.",
        "tagline": "What’s hiding in your furniture, floors, and fabrics.",
    },
    "personal-care": {
        "name": "Personal Care &amp; Chemicals",
        "description": "Science-backed safety guides for personal care ingredients — parabens, SLS, fragrances, and more.",
        "tagline": "The science behind what you put on your skin every day.",
    },
    "cleaning": {
        "name": "Cleaning &amp; Maintenance",
        "description": "Safety guides for household cleaners, laundry products, water filtration, and solvents.",
        "tagline": "Safer ways to keep your home clean without toxic tradeoffs.",
    },
    "tech": {
        "name": "Tech &amp; Home Office",
        "description": "Safety guides for electronics, 3D printing materials, and home office equipment.",
        "tagline": "The materials in your devices, cables, and workspace.",
    },
    "outdoor": {
        "name": "Outdoor &amp; Garden",
        "description": "Safety guides for pesticides, treated wood, garden hoses, synthetic turf, and lawn equipment.",
        "tagline": "What’s in your yard, garden, and outdoor living spaces.",
    },
}


def load_material_rows():
    if not MATERIALS_DATA_FILE.exists():
        return []
    rows = json.loads(MATERIALS_DATA_FILE.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        return []
    return rows


def grouped_material_rows():
    grouped = defaultdict(list)
    for row in load_material_rows():
        grouped[row.get("category", "")].append(row)
    for slug in grouped:
        grouped[slug].sort(key=lambda r: r.get("material_name", ""))
    return grouped


def load_articles_module(category_slug):
    module_name = category_slug.replace("-", "_")
    try:
        mod = importlib.import_module(f"articles.{module_name}")
    except ModuleNotFoundError:
        return None, {}
    except (ImportError, SyntaxError) as exc:
        print(f"  WARN: Could not load 'articles/{module_name}.py' ({exc.__class__.__name__}: {exc})")
        return None, {}
    return getattr(mod, "ARTICLES", None), getattr(mod, "RELATED_MAP", {})


def verdict_level(status):
    return {
        "AVOID": "verdict-avoid",
        "CAUTION": "verdict-caution",
        "SAFE": "verdict-safe",
    }.get((status or "").upper(), "verdict-neutral")


def normalize_basic_article(row):
    material_name = row.get("material_name", row.get("slug", "Material")).strip()
    verdict = row.get("verdict", "See material profile for details.").strip()
    alternative = row.get("alternative", "Use lower-toxicity alternatives where practical.").strip()
    status = (row.get("status") or "CAUTION").upper()
    return {
        "slug": row.get("slug", "untitled"),
        "title": material_name,
        "meta_description": f"{material_name}: {verdict[:130]}",
        "verdict_level": verdict_level(status),
        "verdict_rating": f"{status.title()} — Quick Safety Verdict",
        "verdict_summary": verdict,
        "sections": [
            {
                "id": "what-it-is",
                "heading": "What This Material Is",
                "content": f"<p>{html.escape(material_name)} is tracked in our household materials registry. This page summarizes the current high-level safety stance while the long-form deep-dive article is in progress.</p>",
            },
            {
                "id": "what-to-do",
                "heading": "What You Can Do Right Now",
                "content": f"<p>{html.escape(verdict)}</p><p><strong>Better direction:</strong> {html.escape(alternative)}</p>",
            },
        ],
        "alternatives": [
            {
                "name": alternative,
                "type": "Suggested Alternative",
                "description": "Practical lower-risk option from our normalized catalog.",
                "pros": "Easy immediate risk reduction",
                "cons": "Full brand-level comparisons coming in expanded guides",
            }
        ],
        "sources": [],
    }


def merge_articles(category_slug):
    rows_by_category = grouped_material_rows()
    rows = rows_by_category.get(category_slug, [])
    row_slugs = {r.get("slug") for r in rows if r.get("slug")}

    module_articles, related_map = load_articles_module(category_slug)
    module_articles = module_articles or []

    by_slug = {}
    # If catalog exists for this category, only keep module articles that match catalog slugs.
    for article in module_articles:
        slug = article.get("slug")
        if not slug:
            continue
        if row_slugs and slug not in row_slugs:
            continue
        by_slug[slug] = article

    for row in rows:
        slug = row.get("slug")
        if slug and slug not in by_slug:
            by_slug[slug] = normalize_basic_article(row)

    articles = list(by_slug.values())
    articles.sort(key=lambda a: a.get("title", ""))
    return articles, related_map, len(rows)


def build_toc(sections):
    items = "\n".join(f'        <li><a href="#{s["id"]}">{s["heading"]}</a></li>' for s in sections)
    return f"""    <div class=\"toc\">\n      <div class=\"toc-label\">In This Article</div>\n      <ol>\n{items}\n        <li><a href=\"#alternatives\">Better Alternatives</a></li>\n        <li><a href=\"#sources\">Sources</a></li>\n      </ol>\n    </div>"""


def build_alternatives(alternatives):
    cards = []
    for alt in alternatives:
        link = ""
        if alt.get("asin"):
            href = f"https://www.amazon.com/dp/{alt['asin']}?tag={AFFILIATE_TAG}"
            link = f'\n        <a href="{href}" class="alt-link" rel="sponsored nofollow" target="_blank">Check Current Price &rarr;</a>'
        cards.append(
            f"""      <div class=\"alt-card\">\n        <div class=\"alt-type\">{alt.get('type','Alternative')}</div>\n        <div class=\"alt-name\">{alt.get('name','Alternative')}</div>\n        <p class=\"alt-desc\">{alt.get('description','')}</p>\n        <p class=\"alt-pros\">&plus; {alt.get('pros','')}</p>\n        <p class=\"alt-cons\">&Delta; {alt.get('cons','')}</p>{link}\n      </div>"""
        )
    return "\n".join(cards)


def build_sources(sources):
    if not sources:
        return "        <li>Detailed source references will be added in the full article update.</li>"
    return "\n".join(
        f'        <li>{title} &mdash; <a href="{url}" target="_blank" rel="noopener">{url}</a></li>' for title, url in sources
    )


def build_related(slug, all_articles, related_map):
    related_slugs = related_map.get(slug, [])
    if not related_slugs:
        return ""
    title_map = {a["slug"]: a["title"] for a in all_articles}
    links = [f'        <li><a href="{rs}.html">{title_map[rs]}</a></li>' for rs in related_slugs if rs in title_map]
    if not links:
        return ""
    return "    <nav class=\"related-articles\">\n      <h2>Related Articles</h2>\n      <ul>\n" + "\n".join(links) + "\n      </ul>\n    </nav>"


def generate_article(article, all_articles, category_slug, related_map):
    cat = CATEGORIES[category_slug]
    canonical = f"{SITE_URL}/{category_slug}/{article['slug']}.html"
    plain_title = html.escape(unescape(article["title"]), quote=True)
    plain_desc = html.escape(article["meta_description"], quote=True)
    today = date.today().isoformat()
    sections_html = "\n\n".join(f'    <h2 id="{s["id"]}">{s["heading"]}</h2>\n    {s["content"].strip()}' for s in article["sections"])

    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{article['title']} &mdash; {SITE_NAME}</title>
  <meta name=\"description\" content=\"{plain_desc}\" />
  <link rel=\"canonical\" href=\"{canonical}\" />
  <meta property=\"og:type\" content=\"article\" />
  <meta property=\"og:title\" content=\"{plain_title}\" />
  <meta property=\"og:description\" content=\"{plain_desc}\" />
  <meta property=\"og:url\" content=\"{canonical}\" />
  <meta property=\"og:site_name\" content=\"{SITE_NAME}\" />
  <meta name=\"twitter:card\" content=\"summary\" />
  <meta name=\"twitter:title\" content=\"{plain_title}\" />
  <meta name=\"twitter:description\" content=\"{plain_desc}\" />
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />
  <link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700&display=swap\" />
  <link rel=\"icon\" href=\"../favicon.svg\" type=\"image/svg+xml\" />
  <link rel=\"stylesheet\" href=\"../css/style.css?v={CSS_VERSION}\" />
</head>
<body>
  <nav class=\"breadcrumb\"><a href=\"../index.html\">&larr; {SITE_NAME}</a></nav>
  <article>
    <h1>{article['title']}</h1>
    <div class=\"editors-note\">{EDITORS_NOTE}</div>
    <div class=\"verdict-box {article['verdict_level']}\">
      <div class=\"verdict-label\">30-Second Verdict</div>
      <div class=\"verdict-rating\">{article['verdict_rating']}</div>
      <p class=\"verdict-summary\">{article['verdict_summary']}</p>
    </div>
{build_toc(article['sections'])}
{sections_html}
    <h2 id=\"alternatives\">Better Alternatives</h2>
    <div class=\"alternatives-grid\">{build_alternatives(article['alternatives'])}
    </div>
    <div class=\"sources\">
      <h2 id=\"sources\">Sources</h2>
      <ol>
{build_sources(article['sources'])}
      </ol>
    </div>
{build_related(article['slug'], all_articles, related_map)}
  </article>
  <div class=\"site-footer\"><nav><a href=\"../about.html\">About</a><a href=\"../methodology.html\">Methodology</a><a href=\"../privacy.html\">Privacy Policy</a></nav><p class=\"copyright\">&copy; {today[:4]} {SITE_NAME}</p></div>
</body>
</html>
"""


def generate_category_index(category_slug, generated_articles, target_count):
    cat = CATEGORIES[category_slug]
    links = "\n".join(f'        <li><a href="{slug}.html">{title}</a></li>' for slug, title in generated_articles)
    return f"""<!DOCTYPE html>
<html lang=\"en\"><head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{cat['name']} &mdash; {SITE_NAME}</title>
  <meta name=\"description\" content=\"{cat['description']}\" />
  <link rel=\"canonical\" href=\"{SITE_URL}/{category_slug}/\" />
  <link rel=\"stylesheet\" href=\"../css/style.css?v={CSS_VERSION}\" />
  <link rel=\"icon\" href=\"../favicon.svg\" type=\"image/svg+xml\" />
</head><body>
  <nav class=\"breadcrumb\"><a href=\"../index.html\">&larr; {SITE_NAME}</a></nav>
  <div class=\"category-header\"><h1>{cat['name']}</h1><p>{cat['tagline']}</p></div>
  <p class=\"registry-meta\">{len(generated_articles)} published guides • {target_count} materials in catalog</p>
  <main><ul class=\"category-list\">{links}
    </ul></main>
  <div class=\"site-footer\"><nav><a href=\"../about.html\">About</a><a href=\"../methodology.html\">Methodology</a><a href=\"../privacy.html\">Privacy Policy</a></nav><p class=\"copyright\">&copy; {date.today().year} {SITE_NAME}</p></div>
</body></html>
"""


def generate_homepage(catalog_by_category, generated_counts):
    sections = []
    for cat_slug, cat in CATEGORIES.items():
        total = len(catalog_by_category.get(cat_slug, []))
        published = generated_counts.get(cat_slug, 0)
        href = f"{cat_slug}/index.html" if published else "#"
        state = "Live" if published else "In Progress"
        cta = "Browse guides" if published else "Catalog preview"
        sections.append(
            f"""      <li class=\"material-row\"><a href=\"{href}\">\n        <div class=\"row-name\">{cat['name']}<span class=\"row-sub\">{cat['tagline']}</span></div>\n        <div class=\"row-status\"><span class=\"badge {'badge-safe' if published else 'badge-caution'}\">{state}</span></div>\n        <div class=\"row-alt\">{published}/{total} published &middot; {cta}</div>\n      </a></li>"""
        )

    html_out = f"""<!DOCTYPE html>
<html lang=\"en\"><head>
  <meta charset=\"UTF-8\" /><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{SITE_NAME} — Science-Backed Safety Guides for Your Home</title>
  <meta name=\"description\" content=\"Browse 100 household material safety entries across 8 categories.\" />
  <link rel=\"canonical\" href=\"{SITE_URL}/\" />
  <link rel=\"stylesheet\" href=\"css/style.css?v={CSS_VERSION}\" />
  <link rel=\"icon\" href=\"favicon.svg\" type=\"image/svg+xml\" />
</head><body>
  <div class=\"hero\"><h1>{SITE_NAME}</h1><p class=\"tagline\">The Science of Your Home, Simplified.</p></div>
  <main>
    <div class=\"section-label\"><h2>Safety Guide Categories</h2></div>
    <p class=\"registry-meta\">Catalog: {sum(len(v) for v in catalog_by_category.values())} materials across 8 categories</p>
    <div class=\"registry-header\"><span>Category</span><span style=\"text-align:center\">Status</span><span class=\"col-alt\">Coverage</span></div>
    <ul class=\"material-grid\">\n{''.join(sections)}\n    </ul>
  </main>
  <div class=\"site-footer\"><nav><a href=\"about.html\">About</a><a href=\"methodology.html\">Methodology</a><a href=\"privacy.html\">Privacy Policy</a></nav><p class=\"copyright\">&copy; {date.today().year} {SITE_NAME}</p></div>
</body></html>
"""
    Path("index.html").write_text(html_out, encoding="utf-8")
    print("  Generated: index.html (category gateway homepage)")


def update_sitemap(all_generated):
    today = date.today().isoformat()
    urls = [(f"{SITE_URL}/", "1.0"), (f"{SITE_URL}/about.html", "0.5"), (f"{SITE_URL}/methodology.html", "0.5")]
    for cat_slug, articles in all_generated.items():
        if not articles:
            continue
        urls.append((f"{SITE_URL}/{cat_slug}/", "0.8"))
        for slug, _ in articles:
            urls.append((f"{SITE_URL}/{cat_slug}/{slug}.html", "0.9"))
    entries = "\n".join(
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{priority}</priority>\n  </url>" for loc, priority in urls
    )
    Path("sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries + '\n</urlset>\n', encoding="utf-8")
    print(f"  Updated: sitemap.xml ({len(urls)} URLs)")


def generate_category(category_slug):
    if category_slug not in CATEGORIES:
        print(f"  ERROR: Unknown category '{category_slug}'")
        return []

    articles, related_map, total_in_catalog = merge_articles(category_slug)
    if not articles:
        print(f"  SKIP: No entries found for '{category_slug}'")
        return []

    output_dir = Path(category_slug)
    output_dir.mkdir(exist_ok=True)
    generated = []

    expected_files = set()
    for article in articles:
        filename = f"{article['slug']}.html"
        expected_files.add(filename)
        outfile = output_dir / filename
        outfile.write_text(generate_article(article, articles, category_slug, related_map), encoding="utf-8")
        generated.append((article["slug"], article["title"]))
        print(f"  Generated: {category_slug}/{filename}")

    # Remove stale generated article pages that no longer exist in the catalog/module merge.
    for stale in output_dir.glob("*.html"):
        if stale.name == "index.html":
            continue
        if stale.name not in expected_files:
            stale.unlink()
            print(f"  Removed stale: {category_slug}/{stale.name}")

    (output_dir / "index.html").write_text(generate_category_index(category_slug, generated, total_in_catalog), encoding="utf-8")
    print(f"  Generated: {category_slug}/index.html (category page)")
    print(f"  Done: {len(generated)} pages in {category_slug}/")
    return generated


def main():
    parser = argparse.ArgumentParser(description="Generate articles for MyEverydayMaterials")
    parser.add_argument("--category", "-c", help="Category slug to generate")
    parser.add_argument("--all", "-a", action="store_true", help="Generate all categories")
    parser.add_argument("--list", "-l", action="store_true", help="List all category counts from materials_data.json")
    args = parser.parse_args()

    catalog_by_category = grouped_material_rows()

    if args.list:
        print(f"\nConfigured categories ({len(CATEGORIES)}):\n")
        for slug, cat in CATEGORIES.items():
            count = len(catalog_by_category.get(slug, []))
            print(f"  {slug:15s}  {unescape(cat['name']):35s}  [{count} catalog entries]")
        print()
        return

    categories = list(CATEGORIES.keys()) if args.all else ([args.category] if args.category else [])
    if not categories:
        parser.print_help()
        return

    all_generated = {}
    for cat_slug in categories:
        print(f"\n── {CATEGORIES.get(cat_slug, {}).get('name', cat_slug)} ──")
        generated = generate_category(cat_slug)
        all_generated[cat_slug] = generated

    print()
    update_sitemap(all_generated)
    generated_counts = {k: len(v) for k, v in all_generated.items()}
    generate_homepage(catalog_by_category, generated_counts)
    total = sum(len(v) for v in all_generated.values())
    print(f"\n  Total generated pages: {total} across {sum(1 for v in all_generated.values() if v)} categories\n")


if __name__ == "__main__":
    main()
