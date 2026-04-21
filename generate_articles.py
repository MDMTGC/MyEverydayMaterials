#!/usr/bin/env python3
"""Universal static site generator for MyEverydayMaterials."""

import argparse
import hashlib
import html
import importlib
import json
import re
import shutil
import urllib.parse
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

SITE_NAME = "Everyday Materials"
SITE_URL = "https://myeverydaymaterials.com"
AFFILIATE_TAG = "myeverydaymat-20"
CSS_VERSION = "13"

# Stable launch date — articles get deterministic publication dates spread over
# the weeks following launch so Google sees organic publishing cadence.
SITE_LAUNCH_DATE = date(2026, 2, 1)

AUTHOR_NAME = "Melecio"
AUTHOR_EMAIL = "myeverydaymaterials@gmail.com"
AUTHOR_PHOTO = "/images/Melecio.png"
AUTHOR_URL = f"{SITE_URL}/about"
AUTHOR_ID = f"{SITE_URL}/about#author"
REVIEW_DATE = "2026-04-19"  # DEFAULT_REVIEW_DATE from prompt


def stable_publish_date(slug):
    """Return a deterministic publication date based on the article slug.

    Spreads articles across ~8 weeks after SITE_LAUNCH_DATE so that each
    article has a unique, stable datePublished that doesn't change on rebuild.
    """
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    offset_days = h % 56  # spread over 8 weeks
    return (SITE_LAUNCH_DATE + timedelta(days=offset_days)).isoformat()

# Inline script to prevent Flash of Default Theme — runs before CSS is parsed
THEME_INIT_SCRIPT = '<script>!function(){var t=localStorage.getItem("mem-theme")||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light");document.documentElement.setAttribute("data-theme",t)}()</script>'
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


_NAV_CHEVRON = '<svg class="nav-chevron" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>'
_HAMBURGER_ICON = '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="4" y1="6" x2="20" y2="6"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="18" x2="20" y2="18"/></svg>'


def build_site_header():
    """Build the site-wide navigation header used on every page."""
    dropdown_links = "\n".join(
        f'        <a href="/{slug}/">{cat["name"].replace("&amp;", "&")}</a>'
        for slug, cat in CATEGORIES.items()
    )
    return f"""  <header>
    <a href="/" class="brand">{SITE_NAME}</a>
    <nav class="site-nav" id="site-nav">
      <a href="/" class="site-nav-link">Home</a>
      <div class="site-nav-dropdown" id="nav-dropdown">
        <button class="site-nav-link site-nav-dropdown-toggle" type="button" aria-expanded="false">Articles {_NAV_CHEVRON}</button>
        <div class="site-nav-dropdown-menu">
{dropdown_links}
        </div>
      </div>
      <a href="/methodology" class="site-nav-link">Methodology</a>
      <a href="/about" class="site-nav-link">About</a>
      <a href="/about#contact" class="site-nav-link">Contact</a>
    </nav>
    <div class="header-right"></div>
    <button class="nav-toggle" type="button" aria-label="Open menu" aria-controls="site-nav" aria-expanded="false">{_HAMBURGER_ICON}</button>
  </header>"""


def _fmt_date_long(iso_date):
    """Convert ISO date string (YYYY-MM-DD) to 'Month D, YYYY'."""
    try:
        d = date.fromisoformat(iso_date)
        return d.strftime("%B %-d, %Y")
    except (ValueError, AttributeError):
        return iso_date


def build_byline(pub_date, reviewed_date=None):
    """Render author byline: photo, name/link, published date, reviewed date."""
    pub_long = _fmt_date_long(pub_date)
    if reviewed_date and reviewed_date != pub_date:
        date_line = f'Published {pub_long} &middot; Last reviewed {_fmt_date_long(reviewed_date)}'
    else:
        date_line = f'Published {pub_long}'
    return (
        f'<div class="byline">'
        f'<img class="byline-photo" src="{AUTHOR_PHOTO}" alt="{AUTHOR_NAME}" width="48" height="48" />'
        f'<div class="byline-text">'
        f'<span class="byline-name">By <a href="/about">{AUTHOR_NAME}</a></span>'
        f'<span class="byline-dates">{date_line}</span>'
        f'</div>'
        f'</div>'
    )


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
            f"""        <a href="../{target_category}/{target_slug}" class="connect-link">
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
    canonical = f"{SITE_URL}/{category_slug}/{article['slug']}"
    plain_title = html.escape(html.unescape(article["title"]), quote=True)
    plain_desc = html.escape(article["meta_description"], quote=True)
    pub_date = article.get("published") or stable_publish_date(article["slug"])
    reviewed_date = article.get("reviewed") or REVIEW_DATE
    mod_date = reviewed_date

    # Estimate word count from section content (strip tags for rough count)
    raw_text = " ".join(s.get("content", "") for s in article["sections"])
    word_count = len(re.sub(r"<[^>]+>", " ", raw_text).split())

    # Derive the simple SAFE / CAUTION / AVOID badge label from verdict_level
    _badge_label_map = {"verdict-safe": "SAFE", "verdict-caution": "CAUTION", "verdict-avoid": "AVOID"}
    v_bubble = _badge_label_map.get(article.get("verdict_level", ""), "CAUTION")

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
  <meta property="article:published_time" content="{pub_date}" />
  <meta property="article:modified_time" content="{mod_date}" />
  <meta property="article:section" content="{cat['name'].replace('&amp;', '&')}" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{plain_title}" />
  <meta name="twitter:description" content="{plain_desc}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" />
  <link rel="icon" href="../favicon.svg" type="image/svg+xml" />
  <meta property="og:image" content="{SITE_URL}/images/hero.jpg" />
  {THEME_INIT_SCRIPT}
  <link rel="stylesheet" href="../css/style.css?v={CSS_VERSION}" />
  <script type="application/ld+json">
  {json.dumps({
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": html.unescape(article["title"]),
      "description": article["meta_description"],
      "url": canonical,
      "datePublished": pub_date,
      "dateModified": reviewed_date,
      "wordCount": word_count,
      "author": {"@id": AUTHOR_ID},
      "publisher": {
          "@type": "Organization",
          "name": SITE_NAME,
          "url": SITE_URL,
      },
      "mainEntityOfPage": canonical,
  }, indent=4, ensure_ascii=False)}
  </script>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to content</a>
{build_site_header()}
  <main id="main-content">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../">Home</a>
      <span class="breadcrumb-sep" aria-hidden="true">/</span>
      <a href="./">{CATEGORIES.get(category_slug, {}).get("name", category_slug.title()).replace("&amp;", "&")}</a>
    </nav>
    <article>
    <h1>{article['title']}</h1>
    {build_byline(pub_date, reviewed_date)}
    {'<div class="callout callout-personal"><strong>A note from Melecio</strong>' + html.escape(article["personal_note"]) + '</div>' if article.get("personal_note") else ''}
    <p class="title-dek">{plain_desc}</p>
    <div class="editors-note">{EDITORS_NOTE}</div>
    <div class="verdict-card {article['verdict_level']}">
      <div class="verdict-header">
        <span class="verdict-bubble">{v_bubble}</span>
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
  <footer class="site-footer"><nav><a href="../">Home</a><a href="../about">About</a><a href="../methodology">Methodology</a><a href="../privacy">Privacy Policy</a></nav><p class="copyright">&copy; {date.today().year} {SITE_NAME}</p></footer>
  <script src="../js/main.js" defer></script>
</body>
</html>
"""


def generate_category_index(category_slug, generated_articles, target_count):
    cat = CATEGORIES[category_slug]
    cat_name = cat["name"].replace("&amp;", "&")
    cat_title = f"{cat_name} &mdash; {SITE_NAME}"
    cat_canonical = f"{SITE_URL}/{category_slug}/"

    _status_badge_map = {
        "verdict-safe": ("safe", "Safe"),
        "verdict-caution": ("caution", "Caution"),
        "verdict-avoid": ("avoid", "Avoid"),
    }

    link_parts = []
    for entry in generated_articles:
        slug, title = entry[0], entry[1]
        vlevel = entry[2] if len(entry) > 2 else ""
        badge_cls, badge_txt = _status_badge_map.get(vlevel, ("", ""))
        badge_html = f' <span class="status-badge status-badge--{badge_cls}">{badge_txt}</span>' if badge_cls else ""
        data_attr = f' data-status="{vlevel}"' if vlevel else ""
        link_parts.append(
            f'        <a href="{slug}" class="connect-link"{data_attr}>\n'
            f'          <div class="connect-type">{badge_html.strip() if badge_html else "Guide"}</div>\n'
            f'          <div class="connect-title">{title} <span>&rarr;</span></div>\n'
            f'        </a>'
        )
    links_html = "\n".join(link_parts)

    # ld+json: CollectionPage with article list
    cat_items = [
        {
            "@type": "ListItem",
            "position": i,
            "name": html.unescape(entry[1]),
            "url": f"{SITE_URL}/{category_slug}/{entry[0]}",
        }
        for i, entry in enumerate(generated_articles, 1)
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
  <meta property="og:image" content="{SITE_URL}/images/hero.jpg" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{cat_title}" />
  <meta name="twitter:description" content="{cat['description']}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" />
  {THEME_INIT_SCRIPT}
  <link rel="stylesheet" href="../css/style.css?v={CSS_VERSION}" />
  <link rel="icon" href="../favicon.svg" type="image/svg+xml" />
  <script type="application/ld+json">
  {cat_ld}
  </script>
</head><body>
{build_site_header()}
  <main>
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../">Home</a>
      <span class="breadcrumb-sep" aria-hidden="true">/</span>
      <span aria-current="page">{cat_name}</span>
    </nav>
    <h1>{cat_name}</h1>
    <p class="title-dek">{cat['tagline']}</p>
    <div class="alt-type alt-type--spaced">{len(generated_articles)} published guides &middot; {target_count} materials catalog</div>
    <div class="connection-hub connection-hub--transparent">
      <div class="connection-grid">
{links_html}
      </div>
    </div>
  </main>
  <footer class="site-footer"><nav><a href="../">Home</a><a href="../about">About</a><a href="../methodology">Methodology</a><a href="../privacy">Privacy Policy</a></nav><p class="copyright">&copy; {date.today().year} {SITE_NAME}</p></footer>
  <script src="../js/main.js" defer></script>
</body></html>
"""


def generate_homepage(catalog_by_category, generated_counts, all_generated=None):
    sections = []
    for cat_slug, cat in CATEGORIES.items():
        published = generated_counts.get(cat_slug, 0)
        href = f"{cat_slug}/" if published else "#"

        sections.append(f"""        <a href="{href}" class="connect-link connect-link--has-img">
          <img class="connect-img" src="images/categories/{cat_slug}.webp" alt="{cat['name'].replace("&amp;", "&")}" width="400" height="250" loading="lazy" />
          <div class="connect-body">
            <div class="connect-title">{cat['name'].replace("&amp;", "&")} <span>&rarr;</span></div>
            <p class="alt-desc hero-tagline">{cat['tagline']}</p>
          </div>
        </a>""")

    home_desc = "Science-backed guides to the materials in your home — what they&rsquo;re made of, whether they&rsquo;re safe, and what to do about it."
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

    # Featured guide: first article with featured=True across all generated articles,
    # checking kitchen first, then personal-care, then cleaning per Phase 4 spec.
    featured_html = ""
    if all_generated:
        _badge_label_map = {"verdict-safe": "SAFE", "verdict-caution": "CAUTION", "verdict-avoid": "AVOID"}
        _preferred_cats = ["kitchen", "personal-care", "cleaning"]
        _search_order = _preferred_cats + [c for c in all_generated if c not in _preferred_cats]
        for _cat_slug in _search_order:
            for _art in all_generated.get(_cat_slug, []):
                if _art.get("featured"):
                    _badge = _badge_label_map.get(_art.get("verdict_level", ""), "CAUTION")
                    _badge_cls = _art.get("verdict_level", "verdict-caution").replace("verdict-", "")
                    featured_html = (
                        f'<div class="featured-guide">'
                        f'<div class="featured-guide-label">Featured Guide</div>'
                        f'<a href="{_cat_slug}/{_art["slug"]}" class="connect-link">'
                        f'<div class="connect-type"><span class="status-badge status-badge--{_badge_cls}">{_badge}</span> {CATEGORIES[_cat_slug]["name"].replace("&amp;", "&")}</div>'
                        f'<div class="connect-title">{_art["title"]} <span>&rarr;</span></div>'
                        f'</a>'
                        f'</div>'
                    )
                    break
            if featured_html:
                break

    # Recently reviewed strip: 3 articles with the latest reviewed date.
    recently_reviewed_html = ""
    if all_generated:
        _all_arts = []
        for _cat_slug, _arts in all_generated.items():
            for _art in _arts:
                _all_arts.append((_cat_slug, _art))
        _all_arts.sort(key=lambda x: x[1].get("reviewed", REVIEW_DATE), reverse=True)
        _recent_links = []
        for _cat_slug, _art in _all_arts[:3]:
            _reviewed = _art.get("reviewed", REVIEW_DATE)
            _recent_links.append(
                f'<a href="{_cat_slug}/{_art["slug"]}" class="connect-link">'
                f'<div class="connect-type">Reviewed {_fmt_date_long(_reviewed)}</div>'
                f'<div class="connect-title">{_art["title"]} <span>&rarr;</span></div>'
                f'</a>'
            )
        if _recent_links:
            recently_reviewed_html = (
                f'<div class="connection-hub connection-hub--transparent">'
                f'<h2>Recently Reviewed</h2>'
                f'<div class="connection-grid">{"".join(_recent_links)}</div>'
                f'</div>'
            )

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
  <meta property="og:image" content="{SITE_URL}/images/hero.jpg" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{home_title}" />
  <meta name="twitter:description" content="{home_desc}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" />
  {THEME_INIT_SCRIPT}
  <link rel="stylesheet" href="css/style.css?v={CSS_VERSION}" />
  <link rel="icon" href="favicon.svg" type="image/svg+xml" />
  <script type="application/ld+json">
  {homepage_ld}
  </script>
</head><body>
  <a href="#main-content" class="skip-link">Skip to content</a>
{build_site_header()}
  <div class="hero">
    <div class="site-mark">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-label="{SITE_NAME} logo" role="img"><path d="M12 2L2 7l10 5 10-5-10-5Z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
    </div>
    <h1>{SITE_NAME}</h1>
    <p class="hero-subtitle">The Science of Your Home, Simplified.</p>
    <p class="hero-intro">Every guide here is a plain-English translation of what peer-reviewed research, regulatory agencies, and independent testing say about a material in your home. Each lands on one of three verdicts &mdash; Safe, Caution, or Avoid &mdash; with sources cited. Written by {AUTHOR_NAME}, updated as evidence changes.</p>
  </div>
  <main id="main-content">
    {featured_html}
    <div class="connection-hub connection-hub--transparent">
      <h2>Browse guides by category</h2>
      <div class="connection-grid">\n{chr(10).join(sections)}\n      </div>
    </div>
    {recently_reviewed_html}
  </main>
  <footer class="site-footer"><nav><a href="about">About</a><a href="methodology">Methodology</a><a href="privacy">Privacy Policy</a></nav><p class="copyright">&copy; {date.today().year} {SITE_NAME}</p></footer>
  <script src="js/main.js" defer></script>
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
  <link rel="canonical" href="{SITE_URL}/{{pagename}}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" />
  <link rel="icon" href="favicon.svg" type="image/svg+xml" />
  {THEME_INIT_SCRIPT}
  <link rel="stylesheet" href="css/style.css?v={CSS_VERSION}" />
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to content</a>
{build_site_header()}
  <main id="main-content" class="prose">
{{body}}
  </main>
  <footer class="site-footer"><nav><a href="./">Home</a><a href="about">About</a><a href="methodology">Methodology</a><a href="privacy">Privacy Policy</a></nav><p class="copyright">&copy; {date.today().year} {SITE_NAME}</p></footer>
  <script src="js/main.js" defer></script>
</body>
</html>"""

    _person_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": AUTHOR_ID,
        "name": AUTHOR_NAME,
        "url": AUTHOR_URL,
        "image": SITE_URL + AUTHOR_PHOTO,
        "email": AUTHOR_EMAIL,
    }, indent=4, ensure_ascii=False)

    about_body = f"""    {build_byline(REVIEW_DATE)}
    <h1>About {SITE_NAME}</h1>

    <p>I&rsquo;m {AUTHOR_NAME}, and I started this site because the internet is terrible at answering a specific kind of question.</p>

    <p>Is the plastic in my kid&rsquo;s sippy cup safe? Does that non-stick pan leach something when I overheat it? Is bamboo dinnerware actually eco-friendly, or is it a scam? What&rsquo;s in the fire retardant on my couch?</p>

    <p>Google these questions and you get two extremes: alarmist blogs selling you a $60 &ldquo;clean&rdquo; alternative, or industry pages quietly reassuring you everything is fine. Neither shows its work. Neither tells you which specific conditions matter. Neither updates when new research comes out.</p>

    <p>I got frustrated enough to start doing my own research. Download the actual studies. Read the methodology sections. Check what regulatory agencies &mdash; the EPA, FDA, European Chemicals Agency, WHO &mdash; had actually published, versus what a blog claimed they&rsquo;d published. Over a few years of this, I got reasonably good at it.</p>

    <p>{SITE_NAME} is what that process looks like when I write it down.</p>

    <h2>What this site is</h2>

    <p>A growing library of evidence-based guides on household materials &mdash; what they&rsquo;re made of, what&rsquo;s known about their safety, and what a reasonable person should actually do about it. Every guide lands on one of three verdicts: <strong>Safe</strong>, <strong>Caution</strong>, or <strong>Avoid</strong>, based on the weight of current research. Every claim links to a source. Every verdict explains its reasoning. When research is genuinely mixed, I say so.</p>

    <h2>What I&rsquo;m not</h2>

    <p>I&rsquo;m not a toxicologist, chemist, materials scientist, or medical professional. I don&rsquo;t have a degree in any relevant field. I have no financial relationship with any manufacturer covered on this site and no brand partnerships that influence verdicts. Amazon affiliate links fund this site &mdash; those are disclosed on every guide.</p>

    <p>What I <em>am</em> is a careful researcher who decided the internet needed fewer opinion pieces and more synthesis. If you want credentialed medical advice, see a doctor. If you want to understand the research landscape around the plastic in your kitchen before you buy the $40 alternative, this site is for you.</p>

    <h2 id="contact">Reach me</h2>

    <p>Email: <a href="mailto:{AUTHOR_EMAIL}">{AUTHOR_EMAIL}</a>. If you spot an error, find a newer study I should incorporate, or have a material you&rsquo;d like me to research, I want to hear about it.</p>

    <p><a href="methodology">Read my research methodology &rarr;</a></p>"""

    methodology_body = f"""    {build_byline(REVIEW_DATE)}
    <h1>Methodology</h1>

    <p>Every guide on {SITE_NAME} follows the same research and writing process. This page documents that process so you can evaluate the work on its merits.</p>

    <h2>How topics are selected</h2>

    <p>Topics come from three sources: (1) direct reader questions, (2) materials that appear in common consumer products where safety claims are contested or confusing, and (3) emerging chemicals of regulatory interest &mdash; the EPA&rsquo;s TSCA work plan, ECHA&rsquo;s SVHC candidate list, Proposition 65 listings. Topics are prioritized by how often real people need to make decisions about them and how confusing the existing information landscape is.</p>

    <h2>Source hierarchy</h2>

    <p>Not all sources are equal. Guides prioritize in this order:</p>

    <p><strong>Tier 1 &mdash; Primary research and official regulatory documents.</strong> Peer-reviewed studies, systematic reviews and meta-analyses, government agency technical reports (EPA, FDA, CDC, WHO, EFSA, ECHA, NIOSH), and the testing standards they reference.</p>

    <p><strong>Tier 2 &mdash; Secondary synthesis from authoritative bodies.</strong> Position statements from established medical and scientific organizations (American Academy of Pediatrics, ACS, Consumer Reports independent testing), regulatory fact sheets, well-cited review articles.</p>

    <p><strong>Tier 3 &mdash; Reliable journalism.</strong> Investigative reporting from outlets with demonstrated science-reporting track records, when they&rsquo;re citing Tier 1 sources I can verify independently.</p>

    <p>Blog posts, industry marketing, and single-study claims without replication are not accepted as evidence. Industry-funded research is cited only when it&rsquo;s the available evidence &mdash; and the funding source is always disclosed.</p>

    <h2>How verdicts are assigned</h2>

    <p>Each guide lands on one of three verdicts:</p>

    <p><strong>Safe</strong> &mdash; The weight of current evidence supports normal, common-sense use. No credible mechanism of harm at realistic exposure levels. Any narrow conditions under which the material should still be avoided are specified (e.g., kidney-impaired individuals, extreme temperatures).</p>

    <p><strong>Caution</strong> &mdash; Evidence suggests harm is possible under specific conditions (heat, acidity, damage, prolonged exposure). The material is usable if those conditions are avoided. Guides specify what to do and not do.</p>

    <p><strong>Avoid</strong> &mdash; Either clear evidence of harm at realistic exposure levels, or a recognized regulatory action (ban, restriction, SVHC listing) that supports removal from normal use. Alternatives are always provided.</p>

    <p>These verdicts reflect research weight, not personal risk tolerance. A &ldquo;Caution&rdquo; rating means <em>be thoughtful</em>, not <em>this will hurt you</em>.</p>

    <h2>Update policy</h2>

    <p>Guides are reviewed on a rolling basis when a new peer-reviewed study or meta-analysis is published, a regulatory body issues new guidance, a reader flags a missed source, or twelve months have passed since the last review. Each guide displays its publish date and most recent review date. Substantive changes are logged in a visible change note on the guide.</p>

    <h2>Conflicts of interest</h2>

    <p>{SITE_NAME} earns commissions on qualifying Amazon purchases made through links in the &ldquo;Better Alternatives&rdquo; section of guides. These affiliate relationships do not influence which products are recommended &mdash; recommendations are selected before affiliate availability is checked, and products without affiliate options are included when they&rsquo;re the right call. No sponsored content, no brand partnerships, no paid placements.</p>

    <h2>Limitations</h2>

    <p>This site is not medical advice. It does not substitute for consultation with a physician, toxicologist, or other credentialed professional regarding your specific situation. Guides cover material safety at the population level based on published research &mdash; individual risk factors (pregnancy, pre-existing conditions, occupational exposure, children) may warrant different thresholds than the general guidance here.</p>

    <h2>Corrections</h2>

    <p>If you find an error &mdash; a misquoted source, an outdated study, a missed update, a logical mistake &mdash; email <a href="mailto:{AUTHOR_EMAIL}">{AUTHOR_EMAIL}</a> with specifics. Every correction submitted is acted on. Substantive corrections are logged with a dated changelog on the guide.</p>

    <p><em>Maintained by {AUTHOR_NAME}. <a href="about">About &rarr;</a></em></p>"""

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
            '<title>About {author} &mdash; {site}</title>\n  <meta name="description" content="{author} started {site} to translate peer-reviewed household material research into plain-English verdicts. Learn about the research process and methodology." />\n  <script type="application/ld+json">\n  {ld}\n  </script>'.format(
                author=AUTHOR_NAME, site=SITE_NAME, ld=_person_ld
            ),
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
        pagename = filename.replace(".html", "")
        page_html = _prose_head.replace("{title_meta}", title_meta).replace("{pagename}", pagename).replace("{body}", body)
        Path(f"public/{filename}").write_text(page_html, encoding="utf-8")


def generate_sitemap(urls):
    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc in urls:
        if loc.endswith("/") and loc.count("/") == 3:
            priority = "1.0"   # homepage
            freq = "weekly"
            lastmod = today
        elif loc.endswith("/"):
            priority = "0.8"   # category index
            freq = "weekly"
            lastmod = today
        elif loc.endswith("/about") or loc.endswith("/methodology"):
            priority = "0.5"   # static info pages
            freq = "monthly"
            lastmod = today
        else:
            priority = "0.9"   # article
            freq = "monthly"
            # Extract slug from URL for stable lastmod
            slug = loc.rsplit("/", 1)[-1]
            lastmod = stable_publish_date(slug)
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod><changefreq>{freq}</changefreq><priority>{priority}</priority></url>")
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

    js_dir = public_dir / "js"
    js_dir.mkdir(exist_ok=True)
    if Path("js/main.js").exists():
        shutil.copy("js/main.js", js_dir / "main.js")

    overall = grouped_material_rows()
    all_generated = defaultdict(list)
    all_generated_articles = defaultdict(list)  # full article dicts for homepage
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
            # Ensure stable date fields are set on the dict for homepage use
            art.setdefault("published", stable_publish_date(art["slug"]))
            art.setdefault("reviewed", REVIEW_DATE)
            target = cat_dir / f"{art['slug']}.html"
            html_code = generate_article(art, all_articles_map, cat_slug, related_map, slug_to_category)
            target.write_text(html_code, encoding="utf-8")
            print(f"  Generated: public/{cat_slug}/{art['slug']}.html")
            gen_list.append((art['slug'], art['title'], art.get('verdict_level', 'verdict-neutral')))
            all_generated_articles[cat_slug].append(art)

        all_generated[cat_slug] = gen_list
        counts[cat_slug] = len(gen_list)

        if gen_list:
            idx_html = generate_category_index(cat_slug, gen_list, total_in_catalog)
            idx_target = cat_dir / "index.html"
            idx_target.write_text(idx_html, encoding="utf-8")
            print(f"  Generated: public/{cat_slug}/index.html (category page)")

        print(f"  Done: {counts[cat_slug]} pages in public/{cat_slug}/")

    if args.all:
        generate_homepage(overall, counts, all_generated_articles)
        # Gather URLs for sitemap
        sitemap_urls = [SITE_URL + "/"]
        sitemap_urls.append(f"{SITE_URL}/about")
        sitemap_urls.append(f"{SITE_URL}/methodology")
        for cat_slug, articles in all_generated.items():
            if not articles: continue
            sitemap_urls.append(f"{SITE_URL}/{cat_slug}/")
            for slug, *_ in articles:
                sitemap_urls.append(f"{SITE_URL}/{cat_slug}/{slug}")
        generate_sitemap(sitemap_urls)
        print(f"\n  Total generated pages: {sum(counts.values())} across {len([c for c in counts.values() if c > 0])} categories in public/")

if __name__ == "__main__":
    main()
