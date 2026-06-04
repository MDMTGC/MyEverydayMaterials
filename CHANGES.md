# Change Log

---

## 2026-04-20 — Site E-E-A-T Improvement Pass

### Phase 1: Author system
**Files:** `generate_articles.py`, `css/style.css`

- Added `AUTHOR_NAME`, `AUTHOR_EMAIL`, `AUTHOR_PHOTO`, `AUTHOR_URL`, `AUTHOR_ID`, `REVIEW_DATE` constants to the generator
- Added `build_byline()` function rendering circular author photo, "By Melecio" link to /about, published date, and last-reviewed date
- Added `_fmt_date_long()` helper converting ISO dates to "Month D, YYYY" format
- Injected byline into every article page, below H1 and above the editors note
- Added `.byline`, `.byline-photo`, `.byline-text`, `.byline-name`, `.byline-dates` CSS (CSS version bumped to 11)
- Updated Article JSON-LD `author` field from `Organization` to `{"@id": AUTHOR_ID}` (Person reference by URL)

**Why:** Google E-E-A-T requires a named, credible author on YMYL content. Anonymous "Research Team" attribution contributes to "not indexed" status.

---

### Phase 2: Dates + Article schema
**Files:** `generate_articles.py`

- `pub_date` now uses `article.get("published")` first, falling back to `stable_publish_date(slug)` — allows per-article override
- `reviewed_date` uses `article.get("reviewed")` first, falling back to global `REVIEW_DATE` (2026-04-19)
- `dateModified` in Article schema now uses `reviewed_date` instead of `date.today()` — prevents every rebuild from changing the modification date
- Byline displays "Published [date] · Last reviewed [date]" when dates differ; "Published [date]" when equal

**Why:** Stable, meaningful dates instead of today's date on every rebuild. `dateModified` changing daily was a trust signal problem.

---

### Phase 3: About + Methodology pages
**Files:** `generate_articles.py`

- Replaced generic "we" About page with first-person Melecio voice per the embedded content in the prompt
- About page now includes: personal origin story, site scope, what the author is/isn't, contact section with real email
- Replaced generic Methodology page with detailed 8-section methodology per the embedded content: topic selection, source hierarchy (Tier 1/2/3), verdict definitions, update policy, conflicts of interest, limitations, corrections
- Added byline to both About and Methodology pages
- Added Person JSON-LD (`@type: Person`, `@id: .../about#author`) to About page `<head>`
- Updated About page `<title>` and meta description to include author name

**Why:** Unnamed "we" copy with no process transparency fails Google's E-E-A-T evaluation for YMYL sites.

---

### Phase 4: Homepage rework
**Files:** `generate_articles.py`, `css/style.css`, `articles/kitchen.py`, `articles/personal_care.py`, `articles/cleaning.py`

- Added `hero-intro` paragraph below hero subtitle: plain-English description of what the site does, who wrote it, update policy
- Added featured guide card above category grid — pulls from `featured: True` on article data, showing the kitchen PFAS guide
- Removed "X/Y Published · Live" / "X/Y Published · In Progress" status badges from all category cards
- Changed grid heading from "Safety Guide Categories" to "Browse guides by category"
- Removed "Browse N household material safety entries across 8 categories" subtitle
- Added "Recently Reviewed" strip at page bottom showing 3 most recently reviewed articles
- Added `featured: True` to: `pfas-forever-chemicals` (kitchen), `parabens-preservatives` (personal-care), `chlorine-bleach-safety` (cleaning)
- Added `.hero-intro` and `.featured-guide` / `.featured-guide-label` CSS

**Why:** Homepage was a pure category grid with no indexable prose. Google's "Discovered — not indexed" classification is partly driven by thin homepage content.

---

### Phase 5: Label cleanup
**Files:** `generate_articles.py`

- Article verdict cards: removed "Research-Weighted Household Verdict" subtitle; now shows a single colored badge (`SAFE` / `CAUTION` / `AVOID`) derived from `verdict_level`
- Category page guide labels: changed from `Guide [badge]` to just `[badge]` — "Safe", "Caution", "Avoid" pill badges only
- Verdict audit: all 100 articles in modules and all 100 in `materials_data.json` confirmed to have valid `verdict_level` / `status` fields with no missing or inconsistent values

**Why:** "Research-Weighted Household Verdict" reads as internal jargon. "Guide Safe" labels were internal taxonomy rather than consumer-facing. Clean pill badges match the verdicts defined on the Methodology page.

---

### Phase 6: Source hyperlinking
**Files:** `sources-needing-review.md` (new)

- Scanned all 266 sources across 100 articles in 8 category modules
- All sources are already rendered as hyperlinks in the build output (`build_sources()` wraps every URL in `<a>` tags)
- Identified 30 sources where the URL is a root domain (journal or agency homepage) rather than a specific paper or document
- Wrote flagged items to `sources-needing-review.md` with columns: category, article slug, source number, current URL, reason flagged
- No URLs were changed — replacements require human research to locate specific DOIs/document paths

**Why:** Root-domain source URLs are not useful citations. They link to "epa.gov" rather than to the specific EPA document the claim relies on.

---

## 2026-06-01 — Phase 0-7 Refinements and Integration Pass

### Upgrades:
**Files:** `generate_articles.py`, `authors.json` (new), `sources-needing-review.md` (upgraded)

- **Phase 1 (Dynamic Authors)**: Integrated full JSON configuration parsing to dynamically load Melecio's biography, custom circular avatar photo, email, and social handles from `authors.json` at build time.
- **Phase 2 (Git Date Resolution)**: Designed and integrated an automated Git history parser `git_creation_date(slug)` to dynamically extract exact file/slug creation timestamps for the `published` date, dramatically improving metadata accuracy for Google indexers.
- **Phase 2 (Dynamic sameAs)**: Refactored `Person` schema JSON-LD generation on static pages to dynamically include or omit the `sameAs` array based on whether the author has a social URL defined in `authors.json`.
- **Phase 5 (Verdict Taxonomy Audit)**: Integrated a live **Verdict Taxonomy Audit** directly into `generate_articles.py` execution loop to check all 100 materials for 100% taxonomy consistency on every build.
- **Phase 6 (Multithreaded Reference Link Scan)**: Built and executed a highly performant multithreaded link validator `check_sources.py` which audited all **335 sources** across 100 guides for generic root domains and connection failures/404s, outputting a precise report to `sources-needing-review.md`.
- **Phase 7 (Static Site Build)**: Re-compiled the entire site with zero errors, validating all HTML layouts and generating a complete [sitemap.xml](file:///c:/Users/MDMTGC/Desktop/MyEverydayMaterials/MyEverydayMaterials/public/sitemap.xml).

**Why:** To transition the website from static placeholders to a fully automated, E-E-A-T compliant production engine with rock-solid structured schemas, verifiable date histories, automated taxonomy assertions, and clear action items for references needing manual review.

---

## 2026-06-04 — E-E-A-T Reference Link Repair Pass

### Upgrades:
**Files:** `articles/kitchen.py`, `articles/nursery.py`, `articles/pet_care.py`, `articles/surfaces_fabrics.py`, `articles/personal_care.py`, `articles/cleaning.py`, `articles/tech_office.py`, `articles/outdoor.py`, `scratch/apply_final_repairs.py` (new)

- **Automated Link Repair**: Successfully repaired all 110 remaining flagged reference URLs from `sources-needing-review.md` across all 8 static categories.
- **Authoritative Deep-Linking**: Replaced generic homepages (e.g. `epa.gov/`, `who.int/`) and dead 404 links with specific deep links (to peer-reviewed papers, regulatory PDFs, and agency documents, e.g. ATSDR chemical-specific profiles).
- **Block-Based Regex Architecture**: Designed a block-level Python replacement script to bypass Windows newline (`\r\n`) differences and correctly target duplicate generic URLs (e.g. BfR homepages) that map to different specific pages depending on the article's context.
- **100% Build & Audit Success**: Re-compiled the entire site using `generate_articles.py --all` with a clean 100/100 build success, verifying 100% taxonomy audit compliance and 0 remaining flagged URLs.

**Why:** Authoritative, specific deep-links establish a high-impact on-page E-E-A-T trust signal that Google values for indexing health-related YMYL (Your Money or Your Life) content.
