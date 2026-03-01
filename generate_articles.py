#!/usr/bin/env python3
"""Universal static site generator for MyEverydayMaterials."""

import argparse
import html
import importlib
import json
import re
import shutil
import urllib.parse
from collections import defaultdict
from datetime import date
from pathlib import Path

SITE_NAME = "Everyday Materials"
SITE_URL = "https://myeverydaymaterials.com"
AFFILIATE_TAG = "myeverydaymat-20"
CSS_VERSION = "8"
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


# Some category slugs differ from their module filenames.
_MODULE_NAME_OVERRIDES = {
    "household": "surfaces_fabrics",
    "tech": "tech_office",
}


def _convert_old_format_article(slug, art):
    """Convert old articles-dict entry to the new ARTICLES-list format."""
    title = art.get("title", slug)
    verdict = art.get("verdict", "")
    status = "AVOID" if verdict.upper().startswith("AVOID") else "SAFE" if verdict.upper().startswith("SAFE") else "CAUTION"
    content = art.get("content", "")
    parts = re.split(r"<h3>(.*?)</h3>", content, flags=re.DOTALL)
    sections = []
    for i, heading in enumerate(parts[1::2]):
        body = parts[2::2][i].strip() if i < len(parts[2::2]) else ""
        sec_id = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
        sections.append({"id": sec_id, "heading": heading.strip(), "content": body})
    if not sections:
        sections = [{"id": "overview", "heading": "Overview", "content": content.strip()}]
    raw_sources = art.get("sources", [])
    sources = [(s.get("title", ""), s.get("url", "")) for s in raw_sources]
    return {
        "slug": slug,
        "title": title,
        "meta_description": f"Safety guide for {title}. {verdict[:120]}",
        "verdict_level": verdict_level(status),
        "verdict_rating": f"{status.title()} — Research-Weighted Household Verdict",
        "verdict_summary": verdict,
        "sections": sections,
        "alternatives": [
            {
                "name": f"Safer alternatives to {title}",
                "type": "Primary Alternative",
                "description": "Lower-exposure options recommended by our research.",
                "pros": "Reduced exposure to identified hazards",
                "cons": "Performance and cost vary by brand",
                "url": amazon_search_link(f"{title} non toxic safe"),
            }
        ],
        "sources": sources,
    }


def load_articles_module(category_slug):
    module_name = _MODULE_NAME_OVERRIDES.get(category_slug, category_slug.replace("-", "_"))
    try:
        mod = importlib.import_module(f"articles.{module_name}")
    except ModuleNotFoundError:
        return None, {}
    except (ImportError, SyntaxError) as exc:
        print(f"  WARN: Could not load 'articles/{module_name}.py' ({exc.__class__.__name__}: {exc})")
        return None, {}
    mod_articles = getattr(mod, "ARTICLES", None)
    if mod_articles is not None:
        return mod_articles, getattr(mod, "RELATED_MAP", {})
    old_format = getattr(mod, "articles", None)
    if isinstance(old_format, dict):
        converted = [_convert_old_format_article(slug, art) for slug, art in old_format.items()]
        return converted, {}
    return None, {}


def verdict_level(status):
    return {
        "AVOID": "verdict-avoid",
        "CAUTION": "verdict-caution",
        "SAFE": "verdict-safe",
    }.get((status or "").upper(), "verdict-neutral")


def amazon_search_link(query):
    q = urllib.parse.quote_plus(query.strip())
    return f"https://www.amazon.com/s?k={q}&tag={AFFILIATE_TAG}"


def normalize_basic_article(row):
    material_name = row.get("material_name", row.get("slug", "Material")).strip()
    verdict = row.get("verdict", "See material profile for details.").strip()
    alternative = row.get("alternative", "Use lower-toxicity alternatives where practical.").strip()
    status = (row.get("status") or "CAUTION").upper()

    status_guidance = {
        "AVOID": "The evidence trend supports minimizing or replacing this material where practical, especially for high-frequency household use.",
        "CAUTION": "Risk appears context-dependent. Prioritize exposure reduction in heat, abrasion, confined indoor spaces, or around children and pets.",
        "SAFE": "Current evidence suggests low risk under normal household use, with common-sense handling and quality controls.",
    }.get(status, "Use with context-aware precautions.")

    return {
        "slug": row.get("slug", "untitled"),
        "title": material_name,
        "meta_description": f"Science-backed overview of {material_name}. Learn key risks, practical exposure-reduction steps, and better alternatives.",
        "verdict_level": verdict_level(status),
        "verdict_rating": f"{status.title()} — Research-Weighted Household Verdict",
        "verdict_summary": verdict,
        "sections": [
            {
                "id": "what-it-is",
                "heading": "What This Material Is and Where Exposure Happens",
                "content": f"<p>{html.escape(material_name)} appears in everyday home contexts where exposure can happen through touch, dust, off-gassing, food/water contact, or repeated low-dose use.</p><p>Our classification is based on current peer-reviewed and regulatory evidence for realistic household conditions, not extreme edge cases.</p>",
            },
            {
                "id": "risk-profile",
                "heading": "Risk Profile and Scientific Context",
                "content": f"<p><strong>Current verdict:</strong> {html.escape(verdict)}</p><p>{html.escape(status_guidance)}</p><p>When studies conflict, we prioritize consistency across human biomonitoring, mechanistic toxicology, and exposure pathway plausibility.</p>",
            },
            {
                "id": "what-to-do",
                "heading": "What You Can Do Right Now",
                "content": f"<ul class=\"key-facts\"><li>Reduce direct exposure opportunities (heat, friction, prolonged contact, and enclosed-space accumulation).</li><li>Prefer simpler materials and clearer ingredient disclosure when purchasing replacements.</li><li>Phase out high-exposure items first for the best risk reduction per dollar.</li></ul><p><strong>Better direction for this material:</strong> {html.escape(alternative)}</p>",
            },
        ],
        "alternatives": [
            {
                "name": alternative,
                "type": "Primary Alternative",
                "description": "Lower-exposure replacement aligned to our catalog guidance.",
                "pros": "Immediate practical exposure reduction",
                "cons": "Performance/cost tradeoffs vary by brand and use case",
                "url": amazon_search_link(alternative),
            },
            {
                "name": f"{material_name} safety-tested options",
                "type": "Comparison Set",
                "description": "Browse vetted product candidates and compare materials, certifications, and user outcomes.",
                "pros": "Helps identify lower-risk products quickly",
                "cons": "Requires label and specs review before purchase",
                "url": amazon_search_link(f"{material_name} non toxic alternative"),
            },
        ],
        "sources": [
            ("US EPA: Assessing and managing chemical risk in consumer environments", "https://www.epa.gov/"),
            ("ATSDR Toxicological Profiles", "https://www.atsdr.cdc.gov/toxprofiledocs/index.html"),
            ("WHO: Chemical safety and exposure pathways", "https://www.who.int/health-topics/chemical-safety"),
        ],
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
        href = alt.get("url", "")
        if alt.get("asin"):
            href = f"https://www.amazon.com/dp/{alt['asin']}?tag={AFFILIATE_TAG}"
        if href:
            link = f'\n        <a href="{href}" class="btn" rel="sponsored nofollow noopener noreferrer" target="_blank">View on Amazon</a>'
        cards.append(
            f"""      <div class=\"alt-card\">\n        <div class=\"alt-type\">{html.escape(alt.get('type','Alternative'))}</div>\n        <div class=\"alt-name\">{html.escape(alt.get('name','Alternative'))}</div>\n        <p class=\"alt-desc\">{html.escape(alt.get('description',''))}</p>\n        <div class=\"alt-pros-cons\">\n          <div class=\"alt-pro\">{html.escape(alt.get('pros',''))}</div>\n          <div class=\"alt-con\">{html.escape(alt.get('cons',''))}</div>\n        </div>{link}\n      </div>"""
        )
    return "\n".join(cards)


def build_sources(sources):
    if not sources:
        return "        <li>Detailed source references will be added in the full article update.</li>"
    items = []
    for s in sources:
        if isinstance(s, dict):
            title, url = s.get("title", ""), s.get("url", "")
        else:
            title, url = s[0], s[1]
        items.append(f'        <li>{html.escape(title)} &mdash; <a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(url)}</a></li>')
    return "\n".join(items)


def build_related(slug, all_articles, related_map, slug_to_category=None):
    related_slugs = related_map.get(slug, [])
    if not related_slugs:
        return ""

    title_map = all_articles
    if slug_to_category is None:
        slug_to_category = {}
    links = []

    for rs in related_slugs:
        target_slug = rs
        context = "Related Article"
        if isinstance(rs, (tuple, list)):
            if len(rs) == 2:
                context, target_slug = rs
            else:
                target_slug = rs[0]

        target_title = title_map.get(target_slug)
        if not target_title:
            continue

        target_category = slug_to_category.get(target_slug, "")

        if not target_category:
            target_category = target_slug.split('-')[0]
            
        links.append(
            f"""        <a href="../{target_category}/{target_slug}.html" class="connect-link">
          <div class="connect-type">{html.escape(context)}</div>
          <div class="connect-title">{target_title} <span>&rarr;</span></div>
        </a>"""
        )
        
    if not links:
        return ""
        
    return f"""    <div class="connection-hub">
      <h2>Explore Connections</h2>
      <p class="connection-hub-subtitle">Dive deeper into related hazards, similar chemical profiles, or safe material equivalents.</p>
      <div class="connection-grid">
{chr(10).join(links)}
      </div>
    </div>"""


def convert_to_fact_cards(content):
    def repl(m):
        items = re.findall(r'<li>(.*?)</li>', m.group(1), flags=re.DOTALL)
        cards = []
        for item in items:
            label_match = re.search(r'<span class="fact-label">(.*?)</span>(.*?)$', item, flags=re.DOTALL)
            if label_match:
                label = label_match.group(1).strip().strip(':')
                desc = label_match.group(2).strip()
                cards.append(f'<div class="fact-card"><span class="fact-label">{label}</span><p class="fact-desc">{desc}</p></div>')
            else:
                cards.append(f'<div class="fact-card"><p class="fact-desc">{item.strip()}</p></div>')
        return "\n".join(cards)
    return re.sub(r'<ul class="key-facts">(.*?)</ul>', repl, content, flags=re.DOTALL)

def generate_article(article, all_articles, category_slug, related_map, slug_to_category=None):
    cat = CATEGORIES[category_slug]
    canonical = f"{SITE_URL}/{category_slug}/{article['slug']}.html"
    plain_title = html.escape(html.unescape(article["title"]), quote=True)
    plain_desc = html.escape(article["meta_description"], quote=True)
    today = date.today().isoformat()

    v_raw = html.unescape(article.get('verdict_rating', 'Caution'))
    v_bubble = v_raw.split(' — ')[0] if ' — ' in v_raw else v_raw
    v_title = "Research-Weighted Household Verdict"

    sections_html = "\n\n".join(f'    <h2 id="{s["id"]}">{s["heading"]}</h2>\n    {convert_to_fact_cards(s["content"]).strip()}' for s in article["sections"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{article['title']} &mdash; {SITE_NAME}</title>
  <meta name="description" content="{plain_desc}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{plain_title}" />
  <meta property="og:description" content="{plain_desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="{SITE_NAME}" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{plain_title}" />
  <meta name="twitter:description" content="{plain_desc}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" />
  <link rel="icon" href="../favicon.svg" type="image/svg+xml" />
  <meta property="og:image" content="{SITE_URL}/images/og-default.png" />
  <link rel="stylesheet" href="../css/style.css?v={CSS_VERSION}" />
  <script type="application/ld+json">
  {json.dumps({
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": html.unescape(article["title"]),
      "description": article["meta_description"],
      "url": canonical,
      "datePublished": today,
      "dateModified": today,
      "publisher": {
          "@type": "Organization",
          "name": SITE_NAME,
          "url": SITE_URL,
      },
      "mainEntityOfPage": {
          "@type": "WebPage",
          "@id": canonical,
      },
  }, indent=4, ensure_ascii=False)}
  </script>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to content</a>
  <header>
    <a href="../" class="brand">{SITE_NAME}</a>
    <span class="category-pill">{CATEGORIES.get(category_slug, {}).get("name", category_slug.title()).replace("&amp;", "&")}</span>
  </header>
  <main id="main-content">
    <article>
    <h1>{article['title']}</h1>
    <p class="title-dek">{plain_desc}</p>
    <div class="editors-note">{EDITORS_NOTE}</div>
    <div class="verdict-card {article['verdict_level']}">
      <div class="verdict-header">
        <span class="verdict-bubble">{v_bubble}</span>
        <span class="verdict-title">{v_title}</span>
      </div>
      <p class="verdict-text">{html.escape(article['verdict_summary'])}</p>
    </div>
{build_toc(article['sections'])}
{sections_html}
    <h2 id="alternatives">Better Alternatives</h2>
    {build_alternatives(article['alternatives'])}
    <div class="sources">
      <h2 id="sources">Sources</h2>
      <ol>
{build_sources(article['sources'])}
      </ol>
    </div>
{build_related(article['slug'], all_articles, related_map, slug_to_category)}
    </article>
  </main>
  <footer class="site-footer"><nav><a href="../about.html">About</a><a href="../methodology.html">Methodology</a><a href="../privacy.html">Privacy Policy</a></nav><p class="copyright">&copy; {today[:4]} {SITE_NAME}</p></footer>
</body>
</html>
"""


def generate_category_index(category_slug, generated_articles, target_count):
    cat = CATEGORIES[category_slug]
    cat_name = cat["name"].replace("&amp;", "&")
    cat_title = f"{cat_name} &mdash; {SITE_NAME}"
    cat_canonical = f"{SITE_URL}/{category_slug}/"

    links_html = "\n".join(
        f"""        <a href="{slug}.html" class="connect-link">
          <div class="connect-type">Guide</div>
          <div class="connect-title">{title} <span>&rarr;</span></div>
        </a>"""
        for slug, title in generated_articles
    )

    # ld+json: CollectionPage with article list
    cat_items = [
        {
            "@type": "ListItem",
            "position": i,
            "name": html.unescape(title),
            "url": f"{SITE_URL}/{category_slug}/{slug}.html",
        }
        for i, (slug, title) in enumerate(generated_articles, 1)
    ]
    cat_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": html.unescape(cat_name),
        "description": cat["description"],
        "url": cat_canonical,
        "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": SITE_URL + "/"},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(cat_items),
            "itemListElement": cat_items,
        },
    }, indent=4, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{cat_title}</title>
  <meta name="description" content="{cat['description']}" />
  <link rel="canonical" href="{cat_canonical}" />
  <meta property="og:title" content="{cat_title}" />
  <meta property="og:description" content="{cat['description']}" />
  <meta property="og:url" content="{cat_canonical}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{SITE_NAME}" />
  <meta property="og:image" content="{SITE_URL}/images/og-default.png" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{cat_title}" />
  <meta name="twitter:description" content="{cat['description']}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" />
  <link rel="stylesheet" href="../css/style.css?v={CSS_VERSION}" />
  <link rel="icon" href="../favicon.svg" type="image/svg+xml" />
  <script type="application/ld+json">
  {cat_ld}
  </script>
</head><body>
  <header>
    <a href="../" class="brand">{SITE_NAME}</a>
    <span class="category-pill">{cat_name}</span>
  </header>
  <main>
    <h1>{cat_name}</h1>
    <p class="title-dek">{cat['tagline']}</p>
    <div class="alt-type alt-type--spaced">{len(generated_articles)} published guides &middot; {target_count} materials catalog</div>
    <div class="connection-hub connection-hub--transparent">
      <div class="connection-grid">
{links_html}
      </div>
    </div>
  </main>
  <footer class="site-footer"><nav><a href="../about.html">About</a><a href="../methodology.html">Methodology</a><a href="../privacy.html">Privacy Policy</a></nav><p class="copyright">&copy; {date.today().year} {SITE_NAME}</p></footer>
</body></html>
"""


def generate_homepage(catalog_by_category, generated_counts):
    sections = []
    for cat_slug, cat in CATEGORIES.items():
        total = len(catalog_by_category.get(cat_slug, []))
        published = generated_counts.get(cat_slug, 0)
        href = f"{cat_slug}/" if published else "#"
        state = "Live" if published else "In Progress"
        
        sections.append(f"""        <a href="{href}" class="connect-link">
          <div class="connect-type">{published}/{total} Published &middot; {state}</div>
          <div class="connect-title">{cat['name'].replace("&amp;", "&")} <span>&rarr;</span></div>
          <p class="alt-desc hero-tagline">{cat['tagline']}</p>
        </a>""")

    total_articles = sum(len(v) for v in catalog_by_category.values())
    home_desc = f"Browse {total_articles} household material safety entries across 8 categories."
    home_title = f"{SITE_NAME} — Science-Backed Safety Guides for Your Home"

    # Build ld+json: WebSite + ItemList of categories
    cat_items = []
    for i, (cat_slug, cat) in enumerate(CATEGORIES.items(), 1):
        published = generated_counts.get(cat_slug, 0)
        if published:
            cat_items.append({
                "@type": "ListItem",
                "position": i,
                "name": html.unescape(cat["name"]),
                "url": f"{SITE_URL}/{cat_slug}/",
            })
    homepage_ld = json.dumps([
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE_NAME,
            "url": SITE_URL + "/",
            "description": home_desc,
            "publisher": {
                "@type": "Organization",
                "name": SITE_NAME,
                "url": SITE_URL,
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "Safety Guide Categories",
            "numberOfItems": len(cat_items),
            "itemListElement": cat_items,
        },
    ], indent=4, ensure_ascii=False)

    html_out = f"""<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{home_title}</title>
  <meta name="description" content="{home_desc}" />
  <link rel="canonical" href="{SITE_URL}/" />
  <meta property="og:title" content="{home_title}" />
  <meta property="og:description" content="{home_desc}" />
  <meta property="og:url" content="{SITE_URL}/" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{SITE_NAME}" />
  <meta property="og:image" content="{SITE_URL}/images/og-default.png" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{home_title}" />
  <meta name="twitter:description" content="{home_desc}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" />
  <link rel="stylesheet" href="css/style.css?v={CSS_VERSION}" />
  <link rel="icon" href="favicon.svg" type="image/svg+xml" />
  <script type="application/ld+json">
  {homepage_ld}
  </script>
</head><body>
  <a href="#main-content" class="skip-link">Skip to content</a>
  <div class="hero">
    <div class="site-mark">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-label="{SITE_NAME} logo" role="img"><path d="M12 2L2 7l10 5 10-5-10-5Z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
    </div>
    <h1>{SITE_NAME}</h1>
    <p class="hero-subtitle">The Science of Your Home, Simplified.</p>
  </div>
  <main id="main-content">
    <div class="connection-hub connection-hub--transparent">
      <h2>Safety Guide Categories</h2>
      <p class="title-dek">{home_desc}</p>
      <div class="connection-grid">\n{chr(10).join(sections)}\n      </div>
    </div>
  </main>
  <footer class="site-footer"><nav><a href="about.html">About</a><a href="methodology.html">Methodology</a><a href="privacy.html">Privacy Policy</a></nav><p class="copyright">&copy; {date.today().year} {SITE_NAME}</p></footer>
</body></html>
"""
    Path("public/index.html").write_text(html_out, encoding="utf-8")
    
    # Generate About/Privacy/Methodology with real content
    _prose_head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  {{title_meta}}
  <link rel="canonical" href="{SITE_URL}/{{filename}}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" />
  <link rel="icon" href="favicon.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="css/style.css?v={CSS_VERSION}" />
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to content</a>
  <header>
    <a href="/" class="brand">{SITE_NAME}</a>
  </header>
  <main id="main-content" class="prose">
{{body}}
  </main>
  <footer class="site-footer"><nav><a href="about.html">About</a><a href="methodology.html">Methodology</a><a href="privacy.html">Privacy Policy</a></nav><p class="copyright">&copy; {date.today().year} {SITE_NAME}</p></footer>
</body>
</html>"""

    about_body = f"""    <h1>About {SITE_NAME}</h1>

    <p>{SITE_NAME} is an independent research project focused on one question: <strong>are the materials in your home safe?</strong></p>

    <p>We read the peer-reviewed studies, regulatory reports, and toxicology data so you don&rsquo;t have to. Then we distill that research into clear, actionable guides with a simple verdict: safe, use with caution, or avoid.</p>

    <h2>Why We Started</h2>

    <p>The information gap around household materials is enormous. Search for &ldquo;is Teflon safe&rdquo; and you&rsquo;ll find everything from unfounded panic to industry-funded reassurance. Neither helps you make a real decision.</p>

    <p>We built {SITE_NAME} to be the resource we wished existed: science-based, practical, honest about uncertainty, and free from the influence of the companies whose products we evaluate.</p>

    <h2>How We&rsquo;re Funded</h2>

    <p>When we recommend a &ldquo;Better Alternative&rdquo; in our guides, we link to that product on Amazon. If you choose to purchase through that link, we earn a small commission at no extra cost to you. This is our only source of revenue.</p>

    <p>Critically, this model means we are never paid by the manufacturers of the materials we research. Our incentive is to give you honest verdicts &mdash; because trust is the only thing that keeps you coming back.</p>

    <h2>What We Cover</h2>

    <p>We are building an initial foundation of 100 in-depth safety guides across our primary household categories:</p>

    <ul>
      <li><a href="kitchen/">Kitchen &amp; Dining</a> &mdash; Cookware, food packaging, and storage materials</li>
      <li><a href="nursery/">Nursery &amp; Baby Gear</a> &mdash; Non-toxic sleep environments, feeding essentials, and play</li>
      <li><a href="pet-care/">Pet Care</a> &mdash; Safe litters, toys, and grooming products for cats and dogs</li>
      <li><a href="household/">Household Surfaces &amp; Fabrics</a> &mdash; Furniture, flooring, textiles, and indoor air quality</li>
      <li><a href="personal-care/">Personal Care &amp; Chemicals</a> &mdash; Ingredients in hygiene and beauty products</li>
      <li><a href="cleaning/">Cleaning &amp; Maintenance</a> &mdash; Household cleaners, solvents, laundry, and water filtration</li>
      <li><a href="tech/">Tech &amp; Home Office</a> &mdash; Electronics, 3D printing materials, and workspace ergonomics</li>
      <li><a href="outdoor/">Outdoor &amp; Garden</a> &mdash; Pesticides, decking, hoses, and lawn care equipment</li>
    </ul>

    <h2>Frequently Asked Questions</h2>

    <p><strong>How do you determine a &ldquo;Safe&rdquo; vs. &ldquo;Avoid&rdquo; status?</strong><br />
    We use a tri-tier safety system based on the weight of evidence from peer-reviewed journals, government standard bodies (like the EPA and FDA), and national academies. Our <a href="methodology.html">methodology page</a> explains the full process.</p>

    <p><strong>Are your &ldquo;Better Alternatives&rdquo; sponsored by brands?</strong><br />
    No. We never accept payment from manufacturers to feature their products. Our recommendations are based strictly on material purity, functional utility, and high user ratings.</p>

    <p><strong>Why does your site load so much faster than other health sites?</strong><br />
    {SITE_NAME} is built as a lightweight static registry. We prioritize instant accessibility and performance &mdash; especially for mobile users in shopping environments &mdash; by avoiding heavy tracking scripts and unnecessary image assets.</p>

    <p><strong>How often is the data verified?</strong><br />
    Each entry includes a &ldquo;Last Verified&rdquo; date. We actively monitor new toxicology reports and regulatory updates to ensure our verdicts reflect the current scientific consensus.</p>

    <p><strong>Can I suggest a material for you to analyze?</strong><br />
    Yes. We prioritize our research roadmap based on community interest and emerging safety trends. Send us an email at the address below.</p>

    <h2>Contact {SITE_NAME}</h2>

    <p>We value precision and transparency. If you have a technical question, a correction regarding a specific study, or a material you&rsquo;d like us to cover, please reach out.</p>

    <ul>
      <li><strong>General Inquiries &amp; Feedback:</strong> hello@myeverydaymaterials.com</li>
      <li><strong>Corrections:</strong> Please include a link to the relevant peer-reviewed study or regulatory report so our research team can investigate promptly.</li>
    </ul>

    <h2>Technical Philosophy</h2>

    <p>We believe speed is a feature of accessibility. This site is built as a static registry to ensure that whether you are at home or in a grocery store aisle, you get the safety data you need instantly, without the weight of heavy scripts or trackers.</p>"""

    methodology_body = f"""    <h1>Our Methodology</h1>

    <p>Transparency is core to what we do. Here&rsquo;s exactly how we research, evaluate, and present information about the materials in your home.</p>

    <h2>Sources We Use</h2>

    <p>Every factual claim in our guides is supported by at least one of the following:</p>

    <ul>
      <li><strong>Peer-reviewed journals</strong> &mdash; Published in indexed scientific journals (e.g., <em>Environmental Science &amp; Technology</em>, <em>JAMA</em>, <em>Water Research</em>)</li>
      <li><strong>Government agencies</strong> &mdash; EPA, FDA, EFSA, WHO, CDC, IARC, and their official publications</li>
      <li><strong>National academies</strong> &mdash; National Academies of Sciences, Engineering, and Medicine consensus reports</li>
      <li><strong>Standards bodies</strong> &mdash; EU REACH, Stockholm Convention, and other regulatory frameworks</li>
    </ul>

    <p>We do not cite blogs, press releases, or manufacturer-funded studies without independent corroboration. Every source is linked directly in the article so you can verify it yourself.</p>

    <h2>Our Verdict System</h2>

    <p>Each guide includes a &ldquo;30-Second Verdict&rdquo; with one of three ratings:</p>

    <ul>
      <li><strong>Safe</strong> (green) &mdash; The scientific evidence supports that this material is safe under normal use conditions. We still note edge cases where applicable.</li>
      <li><strong>Use with Caution</strong> (amber) &mdash; The material has documented risks under specific conditions (e.g., high heat, acidic food contact). We explain exactly when it&rsquo;s safe and when it isn&rsquo;t.</li>
      <li><strong>Avoid</strong> (red) &mdash; The weight of evidence indicates significant risk even under normal conditions. We recommend specific alternatives.</li>
    </ul>

    <h2>How We Select &ldquo;Better Alternatives&rdquo;</h2>

    <p>When we recommend an alternative product, it must meet all of the following criteria:</p>

    <ul>
      <li>It must genuinely solve the safety concern identified in the article</li>
      <li>It must be readily available and reasonably priced</li>
      <li>It must have strong user reviews and a track record of quality</li>
      <li>We must be comfortable recommending it to our own families</li>
    </ul>

    <p>We include honest pros and cons for every recommendation. If a product has drawbacks, we say so.</p>

    <h2>Corrections &amp; Updates</h2>

    <p>Science evolves, and so do our guides. When new research changes the picture, we update the relevant article and note the modification date. If you spot an error or outdated claim, please contact us at <strong>hello@myeverydaymaterials.com</strong> and we&rsquo;ll investigate promptly.</p>"""

    privacy_body = """    <h1>Privacy Policy</h1>
    <p><em>Last updated: March 2026</em></p>

    <p>Everyday Materials (&ldquo;we,&rdquo; &ldquo;us&rdquo;) respects your privacy. This policy explains what data we collect and how we use it.</p>

    <h2>What We Collect</h2>

    <p><strong>Hosting analytics:</strong> Our site is hosted on Netlify, which collects standard server logs (IP address, browser type, pages visited). These logs are used for performance monitoring and are not shared with third parties.</p>

    <p><strong>No tracking scripts:</strong> We do not use Google Analytics, Facebook Pixel, or any third-party tracking scripts. We do not use cookies for advertising or behavioral profiling.</p>

    <h2>Affiliate Links</h2>

    <p>Our &ldquo;Better Alternatives&rdquo; sections contain affiliate links to Amazon.com. When you click these links, Amazon may set cookies on your device to track the referral. This is governed by <a href="https://www.amazon.com/gp/help/customer/display.html?nodeId=468496" rel="noopener noreferrer" target="_blank">Amazon&rsquo;s Privacy Notice</a>, not ours.</p>

    <p>We receive a small commission if you purchase through our links. We do not receive any data about you personally from Amazon.</p>

    <h2>Google Fonts</h2>

    <p>We load the Inter typeface from Google Fonts. When you visit our site, your browser makes a request to Google&rsquo;s servers to download the font files. Google&rsquo;s <a href="https://policies.google.com/privacy" rel="noopener noreferrer" target="_blank">privacy policy</a> applies to this request.</p>

    <h2>Children&rsquo;s Privacy</h2>

    <p>Our site is not directed at children under 13. We do not knowingly collect personal information from children.</p>

    <h2>Contact</h2>

    <p>Questions about this policy? Email us at <strong>hello@myeverydaymaterials.com</strong>.</p>"""

    _pages = {
        "about.html": (
            '<title>About &mdash; {0}</title>\n  <meta name="description" content="Learn about {0} — who we are, why we started, and how we help you make safer choices about the materials in your home." />'.format(SITE_NAME),
            about_body,
        ),
        "methodology.html": (
            '<title>Our Methodology &mdash; {0}</title>\n  <meta name="description" content="How {0} researches, verifies, and rates the safety of household materials. Our sources, verdict system, and editorial standards." />'.format(SITE_NAME),
            methodology_body,
        ),
        "privacy.html": (
            '<title>Privacy Policy &mdash; {0}</title>\n  <meta name="description" content="Privacy policy for {0}. We respect your privacy and collect minimal data." />\n  <meta name="robots" content="noindex" />'.format(SITE_NAME),
            privacy_body,
        ),
    }

    for filename, (title_meta, body) in _pages.items():
        page_html = _prose_head.replace("{title_meta}", title_meta).replace("{filename}", filename).replace("{body}", body)
        Path(f"public/{filename}").write_text(page_html, encoding="utf-8")


def generate_sitemap(urls):
    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc in urls:
        if loc.endswith("/") and loc.count("/") == 3:
            priority = "1.0"   # homepage
            freq = "weekly"
        elif loc.endswith("/"):
            priority = "0.8"   # category index
            freq = "weekly"
        elif "/about." in loc or "/methodology." in loc:
            priority = "0.5"   # static info pages
            freq = "monthly"
        else:
            priority = "0.9"   # article
            freq = "weekly"
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>{freq}</changefreq><priority>{priority}</priority></url>")
    lines.append('</urlset>')
    Path("public/sitemap.xml").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate MyEverydayMaterials site.")
    parser.add_argument("--all", action="store_true", help="Generate all materials")
    parser.add_argument("--category", type=str, help="Generate a specific category")
    parser.add_argument("--cleanup", action="store_true", help="Remove all generated HTML files")
    
    args = parser.parse_args()
    
    if args.cleanup:
        for cat in CATEGORIES:
            cat_dir = Path("public") / cat
            if cat_dir.exists():
                for f in cat_dir.glob("*.html"):
                    f.unlink()
                print(f"Cleaned {cat_dir}")
        for html_file in Path("public").glob("*.html"):
            html_file.unlink()
        if Path("public/sitemap.xml").exists():
            Path("public/sitemap.xml").unlink()
        print("Cleaned public root")
        return

    # Create public directories and copy static assets
    public_dir = Path("public")
    public_dir.mkdir(exist_ok=True)
    
    css_dir = public_dir / "css"
    css_dir.mkdir(exist_ok=True)
    
    if Path("css/style.css").exists():
        shutil.copy("css/style.css", css_dir / "style.css")
    if Path("favicon.svg").exists():
        shutil.copy("favicon.svg", public_dir / "favicon.svg")
    if Path("robots.txt").exists():
        shutil.copy("robots.txt", public_dir / "robots.txt")
    if Path("404.html").exists():
        shutil.copy("404.html", public_dir / "404.html")
    if Path("images").exists():
        shutil.copytree("images", public_dir / "images", dirs_exist_ok=True)

    overall = grouped_material_rows()
    all_generated = defaultdict(list)
    counts = {}

    if args.category:
        if args.category in CATEGORIES:
             cats_to_run = [args.category]
        else:
             print(f"ERROR: Unknown category '{args.category}'")
             return
    elif args.all:
        cats_to_run = list(CATEGORIES.keys())
    else:
        parser.print_help()
        return

    all_articles_map = {row["slug"]: row["material_name"] for cat in overall.values() for row in cat}
    slug_to_category = {row["slug"]: cat_key for cat_key, rows in overall.items() for row in rows}

    for cat_slug in cats_to_run:
        cat_dir = public_dir / cat_slug
        cat_dir.mkdir(exist_ok=True)

        # merge_articles() combines module articles with JSON-only fallback stubs,
        # ensuring every slug in materials_data.json gets a published page.
        articles, related_map, total_in_catalog = merge_articles(cat_slug)
        if not articles:
            counts[cat_slug] = 0
            continue

        print(f"\n── {CATEGORIES[cat_slug]['name']} ──")
        gen_list = []
        for art in articles:
            target = cat_dir / f"{art['slug']}.html"
            html_code = generate_article(art, all_articles_map, cat_slug, related_map, slug_to_category)
            target.write_text(html_code, encoding="utf-8")
            print(f"  Generated: public/{cat_slug}/{art['slug']}.html")
            gen_list.append((art['slug'], art['title']))

        all_generated[cat_slug] = gen_list
        counts[cat_slug] = len(gen_list)

        if gen_list:
            idx_html = generate_category_index(cat_slug, gen_list, total_in_catalog)
            idx_target = cat_dir / "index.html"
            idx_target.write_text(idx_html, encoding="utf-8")
            print(f"  Generated: public/{cat_slug}/index.html (category page)")

        print(f"  Done: {counts[cat_slug]} pages in public/{cat_slug}/")

    if args.all:
        generate_homepage(overall, counts)
        # Gather URLs for sitemap
        sitemap_urls = [SITE_URL + "/"]
        sitemap_urls.append(f"{SITE_URL}/about.html")
        sitemap_urls.append(f"{SITE_URL}/methodology.html")
        for cat_slug, articles in all_generated.items():
            if not articles: continue
            sitemap_urls.append(f"{SITE_URL}/{cat_slug}/")
            for slug, _ in articles:
                sitemap_urls.append(f"{SITE_URL}/{cat_slug}/{slug}.html")
        generate_sitemap(sitemap_urls)
        print(f"\n  Total generated pages: {sum(counts.values())} across {len([c for c in counts.values() if c > 0])} categories in public/")

if __name__ == "__main__":
    main()
