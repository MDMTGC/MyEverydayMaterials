# Everyday Materials — Site Improvement Task for Claude Code

## How to use this document

1. Fill in the `<<FILL_IN>>` placeholders in the **User-Supplied Information** section below.
2. Save an author photo to your repo (recommended path: `/assets/author.jpg` or whatever your static-asset convention is) and put the path in `AUTHOR_PHOTO_PATH`.
3. Review the three content blocks (author bio, about page, methodology page) under **Embedded Content**. Edit freely — change wording, swap anecdotes, adjust tone. These are drafts.
4. From your repo root, run:
   ```
   claude-code "Read ./everyday-materials-claude-code-prompt.md and execute it one phase at a time. Pause for my confirmation at the end of each phase before moving to the next."
   ```

---

## User-Supplied Information

Fill these in before running. Claude Code will refuse to proceed past Phase 0 if any required field still contains `<<FILL_IN>>`.

```
AUTHOR_NAME              = "<<Melecio>>"              # Real name or pen name
AUTHOR_PHOTO_PATH        = "<<C:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials\Image Assets>>"              # e.g., /assets/author.jpg (repo-root-relative)
CONTACT_EMAIL            = "<<myeverydaymaterials@gmail.com>>"              # e.g., hello@myeverydaymaterials.com
AUTHOR_SOCIAL_URL        = "<<>>"  # Twitter/X, LinkedIn, etc. — one URL or ""
SITE_URL                 = "https://myeverydaymaterials.com"
DEFAULT_PUBLISH_DATE     = "<<Claude Code discretion>>"              # YYYY-MM-DD — used when no per-article date exists
DEFAULT_REVIEW_DATE      = "<<4/19/2026>>"              # YYYY-MM-DD — today's date is fine
```

---

## Context

This is a site improvement task on `myeverydaymaterials.com` — a 100-article site of science-backed household material safety guides across eight categories (kitchen, nursery, pet care, household, personal care, cleaning, tech, outdoor).

**The problem being solved:** Google Search Console reports most pages as "Discovered — currently not indexed" or "Crawled — currently not indexed." A diagnostic review identified that the content itself is high-quality, but the site is failing Google's E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) signals for YMYL (Your Money or Your Life) content. Specifically:

- No named author on articles — "we" language with no person behind it
- No published or updated dates visible anywhere
- Identical article templates across all 100 entries (reads as programmatic)
- Source citations that link to journal homepages instead of specific papers
- No `Person` or proper `Article` schema
- Homepage is a category grid with no indexable content
- Verdict labels inconsistent ("Generally Safe" badge + "Research-Weighted Household Verdict" subtitle)
- "Guide Safe / Guide Caution / Guide Avoid" labels on category pages read as internal taxonomy rather than consumer-facing

This task addresses the structural/signal problems. Content-level work (adding personal anecdotes, photos, idiosyncratic sections to break template uniformity) is out of scope — that requires human voice and will be done separately.

---

## Rules

- **Do not push.** Commit locally; leave review and deploy to the user.
- **Ask before destructive operations.** Mass find-and-replace, file deletion, schema block removal — all require explicit confirmation.
- **Preserve existing article content.** You are adding structural elements (bylines, dates, schema), not rewriting article bodies.
- **Log every change.** Append to `CHANGES.md` at repo root. Each entry: phase, files touched, what changed, why.
- **Pause at the end of each phase** and summarize what was done. Wait for confirmation before continuing.
- **If you encounter unexpected complexity** (unusual framework, custom build, broken state), stop and report rather than improvising.
- **No deploy commands.** Do not run `netlify deploy`, `vercel`, `hugo deploy`, or equivalent.

---

## Phase 0: Repo Audit

Before making any changes, investigate and report on:

1. **Framework / SSG.** Hugo? 11ty? Astro? Next.js? Jekyll? Custom? Identify by examining `package.json`, config files (`config.yaml`, `astro.config.mjs`, `_config.yml`, etc.), and build scripts.
2. **Article directory structure.** Where do the 100 articles live? What format (Markdown with frontmatter, MDX, HTML)? Show one example article's raw source.
3. **Template locations.** Where is the article template rendered? Where is the category page template? Where is the homepage template?
4. **Existing metadata.** What frontmatter/data fields already exist on articles? Is there any date field? Any author field?
5. **Existing schema.** Grep for `application/ld+json` across templates. What structured data is currently emitted?
6. **Data directory.** Where would a new `authors.yml` / `authors.json` file logically live for this framework?
7. **Static assets path.** Where are images served from?
8. **Build command.** What's the local build command (`npm run build`, `hugo`, `eleventy --serve`, etc.)?

**Output:** A summary of findings in this format:

```
Framework: [name + version]
Articles: [count] files at [path], format [markdown/mdx/html]
Article template: [path]
Category template: [path]
Homepage template: [path]
Existing frontmatter fields: [list]
Existing schema: [yes/no — if yes, what types]
Authors data location (proposed): [path]
Static assets: [path]
Build command: [command]
Notable observations: [anything unexpected]
```

**Stop after Phase 0 and wait for confirmation before proceeding.**

---

## Phase 1: Author System

1. Create an authors data file at the path proposed in Phase 0 (e.g., `_data/authors.yml` for 11ty, `content/authors/main.md` for Hugo, `src/data/authors.json` for Astro/Next). Structure:

   ```yaml
   main:
     name: "{{AUTHOR_NAME}}"
     slug: "main"
     photo: "{{AUTHOR_PHOTO_PATH}}"
     bio_short: |
       {{AUTHOR_BIO_SHORT — embedded below}}
     email: "{{CONTACT_EMAIL}}"
     social_url: "{{AUTHOR_SOCIAL_URL}}"
     url: "{{SITE_URL}}/about"
   ```

2. Create a reusable byline partial/component. It should render:
   - Author photo (small, circular, ~48px)
   - `By {{AUTHOR_NAME}}` with link to `/about`
   - Published date
   - "Last reviewed" date (if different from published)

3. Inject the byline into the article template, positioned immediately below the article H1 title and above the verdict badge.

4. Add `Person` schema as a JSON-LD block on `/about` and reference it by `@id` from `Article` schema on each guide. Use this structure:

   ```json
   {
     "@context": "https://schema.org",
     "@type": "Person",
     "@id": "{{SITE_URL}}/about#author",
     "name": "{{AUTHOR_NAME}}",
     "url": "{{SITE_URL}}/about",
     "image": "{{SITE_URL}}{{AUTHOR_PHOTO_PATH}}",
     "email": "{{CONTACT_EMAIL}}",
     "sameAs": ["{{AUTHOR_SOCIAL_URL}}"]
   }
   ```

   (Omit `sameAs` entirely if `AUTHOR_SOCIAL_URL` is blank. Do not emit empty arrays.)

**Pause and confirm before Phase 2.**

---

## Phase 2: Dates + Article Schema

1. Audit article frontmatter. If articles already have `date` / `published` / `updated` fields, use them. If not, add two fields to every article's frontmatter:

   ```
   published: {{DEFAULT_PUBLISH_DATE}}
   reviewed: {{DEFAULT_REVIEW_DATE}}
   ```

   Prefer file creation date from `git log --diff-filter=A --follow` if available; fall back to `DEFAULT_PUBLISH_DATE` otherwise.

2. Render visible dates on the article page, in the byline:
   - Format: `Published {{date_long}} · Last reviewed {{date_long}}`
   - If `published == reviewed`, show only `Published {{date_long}}`

3. Emit `Article` JSON-LD on every guide:

   ```json
   {
     "@context": "https://schema.org",
     "@type": "Article",
     "headline": "{{article.title}}",
     "description": "{{article.description}}",
     "datePublished": "{{article.published}}",
     "dateModified": "{{article.reviewed}}",
     "author": { "@id": "{{SITE_URL}}/about#author" },
     "publisher": {
       "@type": "Organization",
       "name": "Everyday Materials",
       "url": "{{SITE_URL}}"
     },
     "mainEntityOfPage": "{{article.canonical_url}}"
   }
   ```

4. Validate output against schema.org's validator (or use `schema-dts` types if available in the framework) for one article per category. Report results.

**Pause and confirm before Phase 3.**

---

## Phase 3: About + Methodology Pages

1. Replace (or create, if missing) the About page at `/about` with the content in the **ABOUT_PAGE** block below.
2. Replace (or create) the Methodology page at `/methodology` with the content in the **METHODOLOGY_PAGE** block below.
3. Both pages should:
   - Render with the same site template as other static pages
   - Include the author byline at the top
   - Link to each other where indicated
   - Include the `Person` schema on About

4. Substitute `[Your Name]` → `{{AUTHOR_NAME}}` and `[contact email]` → `{{CONTACT_EMAIL}}` throughout.

**Pause and confirm before Phase 4.**

---

## Phase 4: Homepage Rework

Current homepage is a pure category grid with no indexable prose. Rework to:

1. **Hero block** — site name + tagline (keep existing) + a new 2–3 sentence intro paragraph. Draft:

   > Every guide here is a plain-English translation of what peer-reviewed research, regulatory agencies, and independent testing say about a material in your home. Each lands on one of three verdicts — Safe, Caution, or Avoid — with sources cited. Written by {{AUTHOR_NAME}}, updated as evidence changes.

2. **Featured guide** — a single featured article card above the category grid. Pull from a `featured: true` flag on article frontmatter, or fall back to the most recently reviewed article. Add `featured: true` to one article in each of the following categories during this phase (pick the one with the most substantive content): Kitchen, Personal Care, Cleaning.

3. **Category grid** — keep it, but:
   - Remove the "X/X Published · Live" status badges entirely
   - Remove the "Browse 100 household material safety entries across 8 categories" subtitle
   - Replace with: "Browse guides by category"

4. **Footer addition** — add a "Recently reviewed" strip showing the 3 most recently `reviewed`-dated articles.

**Pause and confirm before Phase 5.**

---

## Phase 5: Label Cleanup

1. **Verdict labels on articles.** Current pattern on article pages is a "Generally Safe" badge followed by a "Research-Weighted Household Verdict" subtitle followed by the verdict paragraph. Consolidate to: single colored badge (`SAFE` / `CAUTION` / `AVOID`) + verdict paragraph. Delete the "Research-Weighted Household Verdict" subtitle text throughout. Confirm the change with user before mass-replacing.

2. **Category page guide labels.** Change `Guide Safe` / `Guide Caution` / `Guide Avoid` to just `Safe` / `Caution` / `Avoid` as colored pill badges.

3. **Ensure verdict taxonomy is consistent in article frontmatter.** Every article should have a `verdict` field with exactly one of: `safe`, `caution`, `avoid`. Audit and report any articles with missing/inconsistent values.

**Pause and confirm before Phase 6.**

---

## Phase 6: Source Hyperlinking Pass

1. Scan all 100 articles' **Sources** sections.
2. For each source entry, if the URL is plain text (not wrapped in an `<a>` tag or Markdown link syntax), wrap it as a Markdown link or `<a href="..." target="_blank" rel="noopener">`.
3. **Flag for manual review** any source where the URL is:
   - A journal homepage (e.g., `https://www.electrochemsci.org/`) rather than a specific paper
   - An agency homepage (e.g., `https://www.efsa.europa.eu/`) without a specific document path
   - A dead link (HTTP 404/410) — run a quick HEAD check on each URL

   Output flagged items to `./sources-needing-review.md` with columns: `article slug | source # | current URL | reason flagged`.

4. Do **not** attempt to find replacement URLs — that's research work for the human.

**Pause and confirm before Phase 7.**

---

## Phase 7: Build, Validate, Commit

1. Run the local build. Report any errors or warnings.
2. Verify:
   - All articles render with byline + dates
   - `/about` and `/methodology` render with new content
   - Homepage renders with new intro + featured article
   - No broken internal links (use a link checker if available: `npx linkinator ./dist` or similar)
   - JSON-LD validates on 3 sample pages (one article, /about, homepage)
3. Commit changes in logical chunks:
   - Commit 1: "Add author system (data, byline component, Person schema)"
   - Commit 2: "Add article dates and Article schema"
   - Commit 3: "Rewrite About and Methodology pages"
   - Commit 4: "Rework homepage with intro and featured guide"
   - Commit 5: "Consolidate verdict labels"
   - Commit 6: "Hyperlink source citations + flag items needing review"
4. Do **not** push.
5. Output a final summary:
   - Files changed (count + list)
   - Commits made
   - Flagged items requiring follow-up (from Phase 6)
   - Recommended next steps for the user

---

## Embedded Content

### AUTHOR_BIO_SHORT

```
Hi, I'm {{AUTHOR_NAME}}. I started Everyday Materials because I got tired of Googling whether something in my kitchen was safe and getting back a mix of fearmongering listicles and industry-funded reassurance. I'm not a toxicologist or a chemist — I'm a careful reader. Every guide on this site walks through what peer-reviewed research, regulatory agencies (EPA, FDA, ECHA, WHO), and independent testing bodies actually say about a household material, then translates it into a clear call: safe, caution, or avoid. I show my sources. I update when evidence changes. If I'm wrong about something, email me and I'll fix it.

[More about my research process →](/methodology)
```

### ABOUT_PAGE

```markdown
# About Everyday Materials

I'm {{AUTHOR_NAME}}, and I started this site because the internet is terrible at answering a specific kind of question.

Is the plastic in my kid's sippy cup safe? Does that non-stick pan leach something when I overheat it? Is bamboo dinnerware actually eco-friendly, or is it a scam? What's in the fire retardant on my couch?

Google these questions and you get two extremes: alarmist blogs selling you a $60 "clean" alternative, or industry pages quietly reassuring you everything is fine. Neither shows its work. Neither tells you which specific conditions matter. Neither updates when new research comes out.

I got frustrated enough to start doing my own research. Download the actual studies. Read the methodology sections. Check what regulatory agencies — the EPA, FDA, European Chemicals Agency, WHO — had actually published, versus what a blog claimed they'd published. Over a few years of this, I got reasonably good at it.

Everyday Materials is what that process looks like when I write it down.

## What this site is

A growing library of evidence-based guides on household materials — what they're made of, what's known about their safety, and what a reasonable person should actually do about it. Every guide lands on one of three verdicts: **Safe**, **Caution**, or **Avoid**, based on the weight of current research. Every claim links to a source. Every verdict explains its reasoning. When research is genuinely mixed, I say so.

## What I'm not

I'm not a toxicologist, chemist, materials scientist, or medical professional. I don't have a degree in any relevant field. I have no financial relationship with any manufacturer covered on this site and no brand partnerships that influence verdicts. Amazon affiliate links fund this site — those are disclosed on every guide.

What I *am* is a careful researcher who decided the internet needed fewer opinion pieces and more synthesis. If you want credentialed medical advice, see a doctor. If you want to understand the research landscape around the plastic in your kitchen before you buy the $40 alternative, this site is for you.

## Reach me

Email: {{CONTACT_EMAIL}}. If you spot an error, find a newer study I should incorporate, or have a material you'd like me to research, I want to hear about it.

[Read my research methodology →](/methodology)
```

### METHODOLOGY_PAGE

```markdown
# Methodology

Every guide on Everyday Materials follows the same research and writing process. This page documents that process so you can evaluate the work on its merits.

## How topics are selected

Topics come from three sources: (1) direct reader questions, (2) materials that appear in common consumer products where safety claims are contested or confusing, and (3) emerging chemicals of regulatory interest — the EPA's TSCA work plan, ECHA's SVHC candidate list, Proposition 65 listings. Topics are prioritized by how often real people need to make decisions about them and how confusing the existing information landscape is.

## Source hierarchy

Not all sources are equal. Guides prioritize in this order:

**Tier 1 — Primary research and official regulatory documents.** Peer-reviewed studies, systematic reviews and meta-analyses, government agency technical reports (EPA, FDA, CDC, WHO, EFSA, ECHA, NIOSH), and the testing standards they reference.

**Tier 2 — Secondary synthesis from authoritative bodies.** Position statements from established medical and scientific organizations (American Academy of Pediatrics, ACS, Consumer Reports independent testing), regulatory fact sheets, well-cited review articles.

**Tier 3 — Reliable journalism.** Investigative reporting from outlets with demonstrated science-reporting track records, when they're citing Tier 1 sources I can verify independently.

Blog posts, industry marketing, and single-study claims without replication are not accepted as evidence. Industry-funded research is cited only when it's the available evidence — and the funding source is always disclosed.

## How verdicts are assigned

Each guide lands on one of three verdicts:

**Safe** — The weight of current evidence supports normal, common-sense use. No credible mechanism of harm at realistic exposure levels. Any narrow conditions under which the material should still be avoided are specified (e.g., kidney-impaired individuals, extreme temperatures).

**Caution** — Evidence suggests harm is possible under specific conditions (heat, acidity, damage, prolonged exposure). The material is usable if those conditions are avoided. Guides specify what to do and not do.

**Avoid** — Either clear evidence of harm at realistic exposure levels, or a recognized regulatory action (ban, restriction, SVHC listing) that supports removal from normal use. Alternatives are always provided.

These verdicts reflect research weight, not personal risk tolerance. A "Caution" rating means *be thoughtful*, not *this will hurt you*.

## Update policy

Guides are reviewed on a rolling basis when a new peer-reviewed study or meta-analysis is published, a regulatory body issues new guidance, a reader flags a missed source, or twelve months have passed since the last review. Each guide displays its publish date and most recent review date. Substantive changes are logged in a visible change note on the guide.

## Conflicts of interest

Everyday Materials earns commissions on qualifying Amazon purchases made through links in the "Better Alternatives" section of guides. These affiliate relationships do not influence which products are recommended — recommendations are selected before affiliate availability is checked, and products without affiliate options are included when they're the right call. No sponsored content, no brand partnerships, no paid placements.

## Limitations

This site is not medical advice. It does not substitute for consultation with a physician, toxicologist, or other credentialed professional regarding your specific situation. Guides cover material safety at the population level based on published research — individual risk factors (pregnancy, pre-existing conditions, occupational exposure, children) may warrant different thresholds than the general guidance here.

## Corrections

If you find an error — a misquoted source, an outdated study, a missed update, a logical mistake — email {{CONTACT_EMAIL}} with specifics. Every correction submitted is acted on. Substantive corrections are logged with a dated changelog on the guide.

---

*Maintained by {{AUTHOR_NAME}}. [About →](/about)*
```

---

## What this prompt does NOT do

The following are intentionally out of scope. They require human judgment or research and should be done separately:

1. **Template variance / human voice injection.** Adding personal anecdotes, custom photos, weird edge cases, or "here's what surprised me" sections to break the 100-article template uniformity. This is high-leverage but requires your voice — no AI pass should touch it.

2. **Replacing flagged journal-homepage source URLs with specific paper URLs.** Phase 6 flags these; resolving them is research work (finding DOIs, locating specific papers). Feed the flagged list to a Claude chat session and work through them one category at a time.

3. **Backlink building.** Structural fix only goes so far. Phase 8, after this prompt is complete: one backlink from a real source (Reddit participation, Pinterest, niche forum, guest post) will change indexing behavior more than anything on-page.

4. **Google Search Console re-submission.** After build + deploy, manually request indexing for your 10 strongest articles via URL Inspection. Don't spam-submit all 100.

5. **Image additions to articles.** Even one custom image per article (photo, diagram, screenshot) breaks the "text-only content farm" signal. Phase this separately; don't try to automate.
