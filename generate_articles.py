#!/usr/bin/env python3
"""Universal static site generator for MyEverydayMaterials."""

import argparse
import html
import importlib
import json
import re
import urllib.parse
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
        items.append(f'        <li>{title} &mdash; <a href="{url}" target="_blank" rel="noopener">{url}</a></li>')
    return "\n".join(items)


def build_related(slug, all_articles, related_map):
    related_slugs = related_map.get(slug, [])
    if not related_slugs:
        return ""
    
    # all_articles is already a dict mapping {slug: title}
    title_map = all_articles
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
            
        # Discover category of target_slug by searching the overall catalog
        # Since this runs inside build_related we can import overall dict from generation scope
        target_category = ""
        for cat_key, arts in grouped_material_rows().items():
            if any(a.get("slug") == target_slug for a in arts):
                target_category = cat_key
                break
        
        # Fallback to the first word of the slug if category isn't found
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
      <h2 style="font-family: var(--serif); font-size: 1.75rem; color: var(--text-main); margin-bottom: 0.5rem; border: none; margin-top: 0;">Explore Connections</h2>
      <p style="color: var(--text-muted); margin-bottom: 2rem;">Dive deeper into related hazards, similar chemical profiles, or safe material equivalents.</p>
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

def generate_article(article, all_articles, category_slug, related_map):
    cat = CATEGORIES[category_slug]
    canonical = f"{SITE_URL}/{category_slug}/{article['slug']}.html"
    plain_title = html.escape(unescape(article["title"]), quote=True)
    plain_desc = html.escape(article["meta_description"], quote=True)
    today = date.today().isoformat()
    
    v_raw = unescape(article.get('verdict_rating', 'Caution'))
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
  <link rel="stylesheet" href="../css/style.css?v={CSS_VERSION}" />
</head>
<body>
  <header>
    <a href="../" class="brand">{SITE_NAME}</a>
    <span class="category-pill">{CATEGORIES.get(category_slug, {}).get("name", category_slug.title()).replace("&amp;", "&")}</span>
  </header>
  <main>
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
{build_related(article['slug'], all_articles, related_map)}
  </main>
  <div class="site-footer"><nav><a href="../about.html">About</a><a href="../methodology.html">Methodology</a><a href="../privacy.html">Privacy Policy</a></nav><p class="copyright">&copy; {today[:4]} {SITE_NAME}</p></div>
</body>
</html>
"""


def generate_category_index(category_slug, generated_articles, target_count):
    cat = CATEGORIES[category_slug]
    
    links_html = "\n".join(
        f"""        <a href="{slug}.html" class="connect-link">
          <div class="connect-type">Guide</div>
          <div class="connect-title">{title} <span>&rarr;</span></div>
        </a>"""
        for slug, title in generated_articles
    )

    return f"""<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{cat['name'].replace('&amp;', '&')} &mdash; {SITE_NAME}</title>
  <meta name="description" content="{cat['description']}" />
  <link rel="canonical" href="{SITE_URL}/{category_slug}/" />
  <link rel="stylesheet" href="../css/style.css?v={CSS_VERSION}" />
  <link rel="icon" href="../favicon.svg" type="image/svg+xml" />
</head><body>
  <header>
    <a href="../" class="brand">{SITE_NAME}</a>
    <span class="category-pill">{cat['name'].replace("&amp;", "&")}</span>
  </header>
  <main>
    <h1>{cat['name'].replace('&amp;', '&')}</h1>
    <p class="title-dek">{cat['tagline']}</p>
    <div class="alt-type" style="margin-bottom: 2rem;">{len(generated_articles)} published guides • {target_count} materials catalog</div>
    <div class="connection-hub" style="margin-top: 0; border-top: none; padding-top: 0; background: transparent;">
      <div class="connection-grid">
{links_html}
      </div>
    </div>
  </main>
  <div class="site-footer"><nav><a href="../about.html">About</a><a href="../methodology.html">Methodology</a><a href="../privacy.html">Privacy Policy</a></nav><p class="copyright">&copy; {date.today().year} {SITE_NAME}</p></div>
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
          <div class="connect-title">{cat['name']} <span>&rarr;</span></div>
          <p class="alt-desc" style="margin-top: 0.75rem; margin-bottom: 0;">{cat['tagline']}</p>
        </a>""")

    html_out = f"""<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{SITE_NAME} — Science-Backed Safety Guides for Your Home</title>
  <meta name="description" content="Browse 100 household material safety entries across 8 categories." />
  <link rel="canonical" href="{SITE_URL}/" />
  <link rel="stylesheet" href="css/style.css?v={CSS_VERSION}" />
  <link rel="icon" href="favicon.svg" type="image/svg+xml" />
</head><body>
  <div class="hero">
    <div class="site-mark">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5Z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
    </div>
    <h1>{SITE_NAME}</h1>
    <p class="tagline" style="margin-bottom: 0; color: rgba(255,255,255,0.9);">The Science of Your Home, Simplified.</p>
  </div>
  <main>
    <div class="connection-hub" style="margin-top: 0; border-top: none; padding-top: 0; background: transparent;">
      <h2 style="font-family: var(--serif); font-size: 2rem; margin-bottom: 0.5rem; color: var(--text-main);">Safety Guide Categories</h2>
      <p class="title-dek">Browse {sum(len(v) for v in catalog_by_category.values())} household material safety entries across 8 categories.</p>
      <div class="connection-grid">\n{chr(10).join(sections)}\n      </div>
    </div>
  </main>
  <div class="site-footer"><nav><a href="about.html">About</a><a href="methodology.html">Methodology</a><a href="privacy.html">Privacy Policy</a></nav><p class="copyright">&copy; {date.today().year} {SITE_NAME}</p></div>
</body></html>
"""
    Path("public/index.html").write_text(html_out, encoding="utf-8")
    
    # Generate About/Privacy/Methodology boilerplate text directly into public/
    nav_html = f"""<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>About Us — {SITE_NAME}</title>
  <link rel="stylesheet" href="css/style.css?v={CSS_VERSION}" />
  <link rel="icon" href="favicon.svg" type="image/svg+xml" />
</head><body>
  <header>
    <a href="/" class="brand">{SITE_NAME}</a>
  </header>
  <main>
    <h1>Coming Soon</h1>
    <p class="title-dek">This page is currently under construction.</p>
  </main>
  <div class="site-footer"><nav><a href="about.html">About</a><a href="methodology.html">Methodology</a><a href="privacy.html">Privacy Policy</a></nav><p class="copyright">&copy; {date.today().year} {SITE_NAME}</p></div>
</body></html>"""
    
    Path("public/about.html").write_text(nav_html, encoding="utf-8")
    Path("public/methodology.html").write_text(nav_html, encoding="utf-8")
    Path("public/privacy.html").write_text(nav_html, encoding="utf-8")


def generate_sitemap(urls):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc in urls:
        lines.append(f"  <url><loc>{loc}</loc></url>")
    lines.append('</urlset>')
    Path("public/sitemap.xml").write_text("\n".join(lines), encoding="utf-8")


# The generate_category function is no longer used as its logic is integrated into main.
# It can be removed or kept if there's an external call to it.
# For this change, we'll keep it but it won't be called by the new main.
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
    
    import shutil
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
            html_code = generate_article(art, all_articles_map, cat_slug, related_map)
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
        for cat_slug, articles in all_generated.items():
            if not articles: continue
            sitemap_urls.append(f"{SITE_URL}/{cat_slug}/")
            for slug, _ in articles:
                sitemap_urls.append(f"{SITE_URL}/{cat_slug}/{slug}.html")
        generate_sitemap(sitemap_urls)
        print(f"\n  Total generated pages: {sum(counts.values())} across {len([c for c in counts.values() if c > 0])} categories in public/")

if __name__ == "__main__":
    main()
