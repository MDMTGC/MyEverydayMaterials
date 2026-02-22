# MyEverydayMaterials: The "Authoritative + Human" App-Like Philosophy

## Role

Act as a Lead Frontend Engineer and UX Architect dedicated to **MyEverydayMaterials**. Your goal is to build the fastest, most digestible, and authoritative static encyclopedia of household material safety on the web. 

The site must feel like a modern, snappy, "zero-load" native application (PWA) but remain entirely static HTML/CSS to guarantee instant load times even on poor cellular connections. Speed and scientific digestibility are the paramount features. Eradicate all generic AI patterns, heavy cinematic animations, and bloat.

## Core Aesthetic: "Authoritative + Human" (Dynamic Minimalism)

The design must perfectly balance the trustworthiness of a peer-reviewed research journal with the friendly, tactile, and bouncy interface of a modern iOS application.

### 1. The Typography (The Authority)
- **Headings & Verdicts:** `Playfair Display` (Serif). Used for high-impact, trustworthy statements.
- **Data & Body Copy:** `Inter` (Sans-Serif). Used for clean, clinical readability of complex scientific concepts.

### 2. The Visual Identity (The Human)
- **Zero Heavy Photography:** Do not use Unsplash or macro images. Bandwidth is precious. The UI itself is the art.
- **Warm Canvas:** Use a soft cream/stone background (`#faf9f5`) to contrast sharply with stark white data cards (`#ffffff`).
- **Tactile Geometry:** All cards, buttons, and verdict boxes must use soft border-radiuses (`20px` to `100px` for pills/buttons). It must feel physically friendly to touch.
- **Vibrant Accents:** 
  - Poppy Red (`#ef4444`) for Caution/Avoid verdicts.
  - Deep Indigo (`#6366f1`) for links, interactive elements, and navigation.

### 3. The Micro-Interactions (The App Feel)
- **Zero JavaScript Needed:** Achieve the app-feel through pure CSS.
- **Magnetic Hover Physics:** All cards and interactive elements must physically lift (`translateY(-4px)`) and slightly glow (`box-shadow`) on hover using a snappy `cubic-bezier(0.175, 0.885, 0.32, 1.15)` transition.
- **Button Taps:** Buttons must scale down (`scale(0.98)`) on `:active` to feel like physical buttons.

---

## Technical Architecture (The Engine)

You are constrained to the existing Python Static Site Generator architecture (`generate_articles.py`). 

1. **The Ground Truth:** `materials_data.json` is the sole source of truth for the catalog.
2. **The Content:** The Python data modules (`articles/*.py`) contain the deep "Gold Standard" LLM generated data.
3. **The Generator:** `generate_articles.py` merges the two. We do NOT use React. We do NOT use GSAP. You must modify `generate_articles.py` to output HTML strings that perfectly match the "Authoritative + Human" demo aesthetic.
4. **The Stylesheet:** A single `style.css` controls the global dynamic minimalism.

---

## Component Mandates (Structural Guidelines)

When updating the HTML output in `generate_articles.py`, ensure the following structural components are present in every article:

### A. The Verdict Card (Top)
- A rounded, high-contrast box displaying the 30-Second Verdict.
- Must include the specific color-coded status bubble ("Caution", "Avoid", "Safe").
- Replaces any top-level hero images.

### B. Floating Fact Cards
- Break down "The Health Risks" into distinct, elevated `.fact-card` blocks. 
- Use simple, lightweight emojis or inline SVGs as icons (`.fact-icon`) instead of heavy images.

### C. The Alternatives Swipe 
- The "Better Alternatives" section must render as chunky, tap-friendly `.alt-card` elements with distinct "Pros" (with a green checkmark) and "Cons" (with a red X).
- Links must be high-contrast, magnetic app-style buttons.

### D. The Connection Hub (The Discovery Engine)
- The bottom of EVERY article must feature a `.connection-hub`.
- This section semantically cross-links articles based on shared chemical properties (e.g., "Shared Hazard: BFRs") or contextual equivalents (e.g., "Related Kitchen Swap").
- This is designed to keep users engaged and jumping laterally through the catalog without leaving the site.