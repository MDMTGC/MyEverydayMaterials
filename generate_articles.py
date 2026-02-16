#!/usr/bin/env python3
"""
Universal article generator for MyEverydayMaterials.

Generates articles, category index pages, and sitemap for any category.

Usage:
    python generate_articles.py --category kitchen
    python generate_articles.py --all
    python generate_articles.py --list
"""

import argparse
import importlib
import json
from datetime import date
from html import unescape
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────

SITE_NAME = "Everyday Materials"
SITE_URL = "https://myeverydaymaterials.com"
AFFILIATE_TAG = "myeverydaymat-20"
CSS_VERSION = "7"

EDITORS_NOTE = (
    "<strong>Note from the Editor:</strong> At Everyday Materials, our goal is "
    "to help you navigate the science of your home. We only recommend "
    "&ldquo;Better Alternatives&rdquo; that we&rsquo;ve researched extensively "
    "and would feel safe using in our own kitchens and lives. If you purchase "
    "through one of our links, we may earn a small commission from Amazon at "
    "no extra cost to you. This helps us keep the lights on and the research "
    "coming. Thank you for trusting us."
)

# Category metadata: slug → display info
CATEGORIES = {
    "kitchen": {
        "name": "Kitchen &amp; Dining Safety",
        "description": "Science-backed safety guides for kitchen materials \u2014 PFAS, BPA, Teflon, melamine, and more. Learn what's safe and find better alternatives.",
        "tagline": "Science-backed guides to the materials that touch your food every day.",
    },
    "nursery": {
        "name": "Nursery &amp; Baby Gear",
        "description": "Evidence-based safety guides for nursery materials \u2014 crib mattresses, baby bottles, play mats, and more.",
        "tagline": "Protecting the smallest members of your household from hidden material risks.",
    },
    "pet-care": {
        "name": "Pet Care Safety",
        "description": "Science-backed guides to pet care materials \u2014 litters, toys, beds, and more. Keep your pets safe from hidden toxins.",
        "tagline": "Keeping your cats and dogs safe from hidden material hazards.",
    },
    "household": {
        "name": "Household Surfaces &amp; Fabrics",
        "description": "Safety guides for household materials \u2014 furniture, flooring, textiles, and indoor air quality.",
        "tagline": "What\u2019s hiding in your furniture, floors, and fabrics.",
    },
    "personal-care": {
        "name": "Personal Care &amp; Chemicals",
        "description": "Science-backed safety guides for personal care ingredients \u2014 parabens, SLS, fragrances, and more.",
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
        "tagline": "What\u2019s in your yard, garden, and outdoor living spaces.",
    },
}


# ── Article Data Loading ───────────────────────────────────────────────────

def load_articles(category_slug):
    """Load article data for a category from its articles/ module."""
    module_name = category_slug.replace("-", "_")
    try:
        mod = importlib.import_module(f"articles.{module_name}")
    except ModuleNotFoundError:
        return None, None
    articles = getattr(mod, "ARTICLES", [])
    related_map = getattr(mod, "RELATED_MAP", {})
    return articles, related_map


# ── HTML Builder Functions ─────────────────────────────────────────────────

def build_toc(sections):
    """Build table of contents from sections."""
    items = "\n".join(
        f'        <li><a href="#{s["id"]}">{s["heading"]}</a></li>'
        for s in sections
    )
    return f"""    <div class="toc">
      <div class="toc-label">In This Article</div>
      <ol>
{items}
        <li><a href="#alternatives">Better Alternatives</a></li>
        <li><a href="#sources">Sources</a></li>
      </ol>
    </div>"""


def build_sections(sections):
    """Build article body sections."""
    parts = []
    for s in sections:
        parts.append(
            f'    <h2 id="{s["id"]}">{s["heading"]}</h2>\n'
            f'    {s["content"].strip()}'
        )
    return "\n\n".join(parts)


def build_alternatives(alternatives, tag):
    """Build alternative product cards with affiliate links."""
    cards = []
    for alt in alternatives:
        link = f"https://www.amazon.com/dp/{alt['asin']}?tag={tag}"
        cards.append(f"""      <div class="alt-card">
        <div class="alt-type">{alt['type']}</div>
        <div class="alt-name">{alt['name']}</div>
        <p class="alt-desc">{alt['description']}</p>
        <p class="alt-pros">&plus; {alt['pros']}</p>
        <p class="alt-cons">&Delta; {alt['cons']}</p>
        <a href="{link}" class="alt-link" rel="sponsored nofollow" target="_blank">Check Current Price &rarr;</a>
      </div>""")
    return "\n".join(cards)


def build_sources(sources):
    """Build numbered source list."""
    items = []
    for i, (title, url) in enumerate(sources, 1):
        items.append(
            f'        <li>{title} &mdash; '
            f'<a href="{url}" target="_blank" rel="noopener">{url}</a></li>'
        )
    return "\n".join(items)


def plain_text(html_str):
    """Strip HTML entities for use in JSON-LD and meta tags."""
    return unescape(html_str).replace('"', '&quot;')


def build_related(slug, all_articles, related_map):
    """Build related articles section."""
    related_slugs = related_map.get(slug, [])
    if not related_slugs:
        return ""
    title_map = {a["slug"]: a["title"] for a in all_articles}
    links = []
    for rs in related_slugs:
        if rs in title_map:
            links.append(f'        <li><a href="{rs}.html">{title_map[rs]}</a></li>')
    if not links:
        return ""
    return (
        '    <nav class="related-articles">\n'
        '      <h2>Related Articles</h2>\n'
        '      <ul>\n'
        + "\n".join(links) + "\n"
        '      </ul>\n'
        '    </nav>'
    )


# ── Article Generation ─────────────────────────────────────────────────────

def generate_article(article, all_articles, category_slug, related_map):
    """Generate complete HTML for one article."""
    cat = CATEGORIES[category_slug]
    css_path = f"../css/style.css?v={CSS_VERSION}"
    toc = build_toc(article["sections"])
    body = build_sections(article["sections"])
    alternatives = build_alternatives(article["alternatives"], AFFILIATE_TAG)
    sources = build_sources(article["sources"])
    related = build_related(article["slug"], all_articles, related_map)
    today = date.today().isoformat()
    slug = article["slug"]
    canonical = f"{SITE_URL}/{category_slug}/{slug}.html"
    plain_title = plain_text(article["title"])
    plain_desc = article["meta_description"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{article['title']} &mdash; {SITE_NAME}</title>
  <meta name="description" content="{plain_desc}" />
  <link rel="canonical" href="{canonical}" />

  <!-- Open Graph -->
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{plain_title}" />
  <meta property="og:description" content="{plain_desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:site_name" content="{SITE_NAME}" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{plain_title}" />
  <meta name="twitter:description" content="{plain_desc}" />

  <!-- JSON-LD Structured Data -->
  <script type="application/ld+json">
  [{{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{plain_title}",
    "description": "{plain_desc}",
    "url": "{canonical}",
    "datePublished": "{today}",
    "dateModified": "{today}",
    "publisher": {{
      "@type": "Organization",
      "name": "{SITE_NAME}",
      "url": "{SITE_URL}"
    }},
    "mainEntityOfPage": {{
      "@type": "WebPage",
      "@id": "{canonical}"
    }}
  }},
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_URL}/"}},
      {{"@type": "ListItem", "position": 2, "name": "{cat['name']}", "item": "{SITE_URL}/{category_slug}/"}},
      {{"@type": "ListItem", "position": 3, "name": "{plain_title}"}}
    ]
  }}]
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700&display=swap" />
  <link rel="icon" href="../favicon.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="{css_path}" />
</head>
<body>

  <nav class="breadcrumb"><a href="../index.html">&larr; {SITE_NAME}</a></nav>

  <article>
    <h1>{article['title']}</h1>

    <div class="editors-note">
      {EDITORS_NOTE}
    </div>

    <div class="verdict-box {article['verdict_level']}">
      <div class="verdict-label">30-Second Verdict</div>
      <div class="verdict-rating">{article['verdict_rating']}</div>
      <p class="verdict-summary">{article['verdict_summary']}</p>
    </div>

{toc}

{body}

    <h2 id="alternatives">Better Alternatives</h2>
    <div class="alternatives-grid">
{alternatives}
    </div>

    <div class="sources">
      <h2 id="sources">Sources</h2>
      <ol>
{sources}
      </ol>
    </div>

{related}
  </article>

  <div class="site-footer">
    <nav>
      <a href="../about.html">About</a>
      <a href="../methodology.html">Methodology</a>
      <a href="../privacy.html">Privacy Policy</a>
    </nav>
    <p class="copyright">&copy; 2026 {SITE_NAME}</p>
  </div>

</body>
</html>
"""


def generate_category_index(category_slug, generated_articles):
    """Generate the category index page."""
    cat = CATEGORIES[category_slug]
    css_path = f"../css/style.css?v={CSS_VERSION}"
    cat_url = f"{SITE_URL}/{category_slug}/"
    plain_desc = cat["description"]
    today = date.today().isoformat()

    links = "\n".join(
        f'        <li><a href="{slug}.html">{title}</a></li>'
        for slug, title in generated_articles
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{cat['name']} &mdash; {SITE_NAME}</title>
  <meta name="description" content="{plain_desc}" />
  <link rel="canonical" href="{cat_url}" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{cat['name']} &mdash; {SITE_NAME}" />
  <meta property="og:description" content="{plain_desc}" />
  <meta property="og:url" content="{cat_url}" />
  <meta property="og:site_name" content="{SITE_NAME}" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{cat['name']} &mdash; {SITE_NAME}" />
  <meta name="twitter:description" content="{plain_desc}" />

  <!-- JSON-LD Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "{cat['name']}",
    "description": "{plain_desc}",
    "url": "{cat_url}",
    "isPartOf": {{
      "@type": "WebSite",
      "name": "{SITE_NAME}",
      "url": "{SITE_URL}/"
    }}
  }}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700&display=swap" />
  <link rel="icon" href="../favicon.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="{css_path}" />
</head>
<body>

  <nav class="breadcrumb"><a href="../index.html">&larr; {SITE_NAME}</a></nav>

  <div class="category-header">
    <h1>{cat['name']}</h1>
    <p>{cat['tagline']}</p>
  </div>

  <main>
    <ul class="category-list">
{links}
    </ul>
  </main>

  <div class="site-footer">
    <nav>
      <a href="../about.html">About</a>
      <a href="../methodology.html">Methodology</a>
      <a href="../privacy.html">Privacy Policy</a>
    </nav>
    <p class="copyright">&copy; 2026 {SITE_NAME}</p>
  </div>

</body>
</html>
"""


# ── Sitemap ────────────────────────────────────────────────────────────────

def update_sitemap(all_generated):
    """Rebuild sitemap.xml with all known pages across all categories."""
    today = date.today().isoformat()

    # Static pages
    urls = [
        (f"{SITE_URL}/", "1.0"),
        (f"{SITE_URL}/about.html", "0.5"),
        (f"{SITE_URL}/methodology.html", "0.5"),
    ]

    # Category index pages + article pages
    for cat_slug in CATEGORIES:
        articles = all_generated.get(cat_slug, [])
        if articles:
            urls.append((f"{SITE_URL}/{cat_slug}/", "0.8"))
            for slug, _title in articles:
                urls.append((f"{SITE_URL}/{cat_slug}/{slug}.html", "0.9"))

    entries = "\n".join(
        f"  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        f"    <priority>{priority}</priority>\n"
        f"  </url>"
        for loc, priority in urls
    )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )
    Path("sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"  Updated: sitemap.xml ({len(urls)} URLs)")


# ── Main ───────────────────────────────────────────────────────────────────

def generate_category(category_slug):
    """Generate all articles and index for one category."""
    if category_slug not in CATEGORIES:
        print(f"  ERROR: Unknown category '{category_slug}'")
        print(f"  Available: {', '.join(CATEGORIES.keys())}")
        return []

    articles, related_map = load_articles(category_slug)
    if articles is None:
        print(f"  SKIP: No article data for '{category_slug}' (articles/{category_slug.replace('-','_')}.py not found)")
        return []

    output_dir = Path(category_slug)
    output_dir.mkdir(exist_ok=True)

    generated = []
    for article in articles:
        filename = f"{article['slug']}.html"
        filepath = output_dir / filename
        html = generate_article(article, articles, category_slug, related_map)
        filepath.write_text(html, encoding="utf-8")
        generated.append((article["slug"], article["title"]))
        print(f"  Generated: {category_slug}/{filename}")

    # Category index page
    index_html = generate_category_index(category_slug, generated)
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  Generated: {category_slug}/index.html (category page)")

    print(f"  Done: {len(generated)} articles in {category_slug}/")
    return generated


def main():
    parser = argparse.ArgumentParser(
        description="Generate articles for MyEverydayMaterials"
    )
    parser.add_argument(
        "--category", "-c",
        help="Category slug to generate (e.g. kitchen, nursery, pet-care)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Generate all categories that have article data"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all configured categories and their data status"
    )
    args = parser.parse_args()

    if args.list:
        print(f"\nConfigured categories ({len(CATEGORIES)}):\n")
        for slug, cat in CATEGORIES.items():
            articles, _ = load_articles(slug)
            count = len(articles) if articles else 0
            status = f"{count} articles" if count else "no data yet"
            display_name = unescape(cat['name'])
            print(f"  {slug:15s}  {display_name:35s}  [{status}]")
        print()
        return

    if args.all:
        categories = list(CATEGORIES.keys())
    elif args.category:
        categories = [args.category]
    else:
        parser.print_help()
        return

    all_generated = {}
    for cat_slug in categories:
        print(f"\n── {CATEGORIES.get(cat_slug, {}).get('name', cat_slug)} ──")
        generated = generate_category(cat_slug)
        if generated:
            all_generated[cat_slug] = generated

    if all_generated:
        print()
        update_sitemap(all_generated)
        total = sum(len(v) for v in all_generated.values())
        print(f"\n  Total: {total} articles across {len(all_generated)} categories\n")


if __name__ == "__main__":
    main()
