def build_alternatives(alternatives):
    import html
    from generate_articles import AFFILIATE_TAG
    cards = []
    for alt in alternatives:
        link = ""
        href = alt.get("url", "")
        if alt.get("asin"):
            href = f"https://www.amazon.com/dp/{alt['asin']}?tag={AFFILIATE_TAG}"
        if href:
            link = f'\n        <a href=\"{href}\" class=\"btn\" rel=\"sponsored nofollow noopener noreferrer\" target=\"_blank\">View on Amazon</a>'
        
        cards.append(
            f"      <div class=\"alt-card\">\n"
            f"        <div class=\"alt-type\">{html.escape(alt.get('type','Alternative'))}</div>\n"
            f"        <div class=\"alt-name\">{html.escape(alt.get('name','Alternative'))}</div>\n"
            f"        <p class=\"alt-desc\">{html.escape(alt.get('description',''))}</p>\n"
            f"        <div class=\"alt-pros-cons\">\n"
            f"          <div class=\"alt-pro\">{html.escape(alt.get('pros',''))}</div>\n"
            f"          <div class=\"alt-con\">{html.escape(alt.get('cons',''))}</div>\n"
            f"        </div>{link}\n"
            f"      </div>"
        )
    return "\n".join(cards)

def build_related(slug, all_articles, related_map):
    import html
    related_slugs = related_map.get(slug, [])
    if not related_slugs:
        return ""
    title_map = {a["slug"]: a["title"] for a in all_articles}
    links = []
    for rs in related_slugs:
        target_slug = rs
        context = "Related Article"
        if isinstance(rs, (tuple, list)):
            if len(rs) == 2:
                context, target_slug = rs
            else:
                target_slug = rs[0]
        if target_slug in title_map:
            links.append(
                f"        <a href=\"{target_slug}.html\" class=\"connect-link\">\n"
                f"          <div class=\"connect-type\">{html.escape(context)}</div>\n"
                f"          <div class=\"connect-title\">{html.escape(title_map[target_slug])} <span>&rarr;</span></div>\n"
                f"        </a>"
            )
    if not links:
        return ""
    cards_html = "\n".join(links)
    return (
        f"    <div class=\"connection-hub\">\n"
        f"      <h3>Explore Connections</h3>\n"
        f"      <p>Dive deeper into related hazards, similar chemical profiles, or safe material equivalents on our site.</p>\n"
        f"      <div class=\"connection-grid\">\n{cards_html}\n      </div>\n    </div>"
    )

def convert_to_fact_cards(content):
    import re
    def repl(m):
        items = re.findall(r'<li>(.*?)</li>', m.group(1), flags=re.DOTALL)
        cards = []
        for item in items:
            label_match = re.search(r'<span class=\"fact-label\">(.*?)</span>(.*?)$', item, flags=re.DOTALL)
            if label_match:
                label = label_match.group(1).strip().strip(':')
                desc = label_match.group(2).strip()
                cards.append(f'<div class=\"fact-card\"><span class=\"fact-label\">{label}</span><p class=\"fact-desc\">{desc}</p></div>')
            else:
                cards.append(f'<div class=\"fact-card\"><p class=\"fact-desc\">{item.strip()}</p></div>')
        return "\\n".join(cards)
    return re.sub(r'<ul class=\"key-facts\">(.*?)</ul>', repl, content, flags=re.DOTALL)

with open("generate_articles.py", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Replace build_alternatives
text = re.sub(
    r'def build_alternatives\(.*?\):.*?return "\\n"\.join\(cards\)',
    open(__file__).read().split('def build_alternatives')[1].split('def build_related')[0].strip(),
    text,
    flags=re.DOTALL
)

# Replace build_related
text = re.sub(
    r'def build_related\(.*?\):.*?</ul>\\n    </nav>"',
    open(__file__).read().split('def build_related')[1].split('def convert_to_fact_cards')[0].strip(),
    text,
    flags=re.DOTALL
)

# Inject convert_to_fact_cards before generate_article
convert_func = open(__file__).read().split('def convert_to_fact_cards')[1].split('with open("generate_articles.py"')[0].strip()
text = text.replace("def generate_article(", f"def convert_to_fact_cards{convert_func}\n\ndef generate_article(")

# Update sections_html
text = text.replace(
    'sections_html = "\\n\\n".join(f\'    <h2 id="{s["id"]}">{s["heading"]}</h2>\\n    {s["content"].strip()}\' for s in article["sections"])',
    'sections_html = "\\n\\n".join(f\'    <h2 id="{s["id"]}">{s["heading"]}</h2>\\n    {convert_to_fact_cards(s["content"]).strip()}\' for s in article["sections"])'
)

# Update Verdict logic inside generate_article
v_logic = '''
    v_raw = article.get('verdict_rating', 'Caution')
    v_bubble = html.escape(v_raw.split(' — ')[0]) if ' — ' in v_raw else html.escape(v_raw)
    v_title = html.escape("Research-Weighted Household Verdict")
'''
text = text.replace('sections_html = ', v_logic + '\n    sections_html = ')

# Update Verdict HTML
old_verdict_html = """    <div class=\\"verdict-box {article['verdict_level']}\\">
      <div class=\\"verdict-label\\">30-Second Verdict</div>
      <div class=\\"verdict-rating\\">{article['verdict_rating']}</div>
      <p class=\\"verdict-summary\\">{article['verdict_summary']}</p>
    </div>"""

new_verdict_html = """    <div class=\\"verdict-card {article['verdict_level']}\\">
      <div class=\\"verdict-header\\">
        <span class=\\"verdict-bubble\\">{v_bubble}</span>
        <span class=\\"verdict-title\\">{v_title}</span>
      </div>
      <p class=\\"verdict-text\\">{article['verdict_summary']}</p>
    </div>"""
text = text.replace(old_verdict_html, new_verdict_html)

# Quick fix: If I messed up indentation or string backslashes in replacement, let's just make it direct string manipulation
with open("generate_articles.py", "w", encoding="utf-8") as f:
    f.write(text)

print("generate_articles.py has been refactored.")
