#!/usr/bin/env python3
"""
Generate all 12 Kitchen & Dining articles for MyEverydayMaterials.
Each article includes science-backed content, a 30-second verdict,
and high-integrity Better Alternatives with Amazon affiliate links.
"""

from datetime import date
from pathlib import Path
from html import unescape

# ── Configuration ──────────────────────────────────────────────────────────

SITE_NAME = "Everyday Materials"
SITE_URL = "https://myeverydaymaterials.com"
AFFILIATE_TAG = "myeverydaymat-20"
CSS_PATH = "../css/style.css"
OUTPUT_DIR = Path("kitchen")

EDITORS_NOTE = (
    "<strong>Note from the Editor:</strong> At Everyday Materials, our goal is "
    "to help you navigate the science of your home. We only recommend "
    "&ldquo;Better Alternatives&rdquo; that we&rsquo;ve researched extensively "
    "and would feel safe using in our own kitchens and lives. If you purchase "
    "through one of our links, we may earn a small commission from Amazon at "
    "no extra cost to you. This helps us keep the lights on and the research "
    "coming. Thank you for trusting us."
)

# ── Article Data ───────────────────────────────────────────────────────────
# Each entry contains research-verified content for one article.

ARTICLES = [
    # ─── 1. PFAS ───────────────────────────────────────────────────────
    {
        "slug": "pfas-forever-chemicals",
        "title": "PFAS in Your Kitchen: What &ldquo;Forever Chemicals&rdquo; Really Mean for Your Health",
        "meta_description": "Science-backed guide to PFAS forever chemicals in cookware and food packaging. Learn the real risks and discover safer alternatives.",
        "verdict_level": "verdict-avoid",
        "verdict_rating": "Avoid Where Possible &mdash; These chemicals never break down",
        "verdict_summary": "PFAS (per- and polyfluoroalkyl substances) are linked to cancer, thyroid disease, and immune suppression. They persist indefinitely in the body and environment. The EPA set a near-zero limit (4 ppt) for drinking water in 2024, signaling serious concern. Replace PFAS-coated cookware and avoid microwave popcorn bags.",
        "sections": [
            {
                "id": "what-are-pfas",
                "heading": "What Are PFAS?",
                "content": """<p>PFAS stands for per- and polyfluoroalkyl substances &mdash; a family of over 12,000 synthetic chemicals built around carbon-fluorine bonds, one of the strongest in organic chemistry. This extreme stability is exactly what makes them useful (water-repellent, grease-proof, heat-resistant) and dangerous (they never fully break down in the environment or the human body).</p>
<p>In the kitchen, PFAS appear in two main places: <strong>non-stick cookware coatings</strong> (marketed as PTFE, the base polymer behind Teflon) and <strong>grease-proof food packaging</strong> like microwave popcorn bags, fast-food wrappers, and some takeout containers.</p>"""
            },
            {
                "id": "health-risks",
                "heading": "The Health Risks",
                "content": """<p>The scientific consensus on PFAS has shifted dramatically. The EPA&rsquo;s 2024 National Primary Drinking Water Regulation set enforceable limits of just 4 parts per trillion for PFOA and PFOS &mdash; effectively declaring that no meaningful exposure is safe.</p>
<p>Key findings from peer-reviewed research:</p>
<ul class="key-facts">
  <li><span class="fact-label">Cancer</span> PFOA classified as a Group 2B carcinogen by IARC; linked to kidney and testicular cancer in occupational studies.</li>
  <li><span class="fact-label">Thyroid</span> Multiple studies link PFAS exposure to thyroid hormone disruption, especially in women.</li>
  <li><span class="fact-label">Immune</span> The National Academies of Sciences (2022) concluded PFAS decrease vaccine antibody response.</li>
  <li><span class="fact-label">Liver</span> PFAS exposure associated with elevated liver enzymes and non-alcoholic fatty liver disease.</li>
  <li><span class="fact-label">Half-life</span> PFOS has a human half-life of 3&ndash;5 years &mdash; it accumulates faster than the body can clear it.</li>
</ul>
<div class="callout callout-danger">
  <strong>Key fact:</strong> A 2023 study in Environmental Science &amp; Technology found that cooking in PFAS-coated pans at normal temperatures releases small amounts of PFAS into food. The dose is low per meal, but exposure is cumulative and lifelong.
</div>"""
            },
            {
                "id": "what-to-do",
                "heading": "What You Can Do Right Now",
                "content": """<p>You don&rsquo;t need to panic, but you should reduce exposure where practical:</p>
<p><strong>Stop using damaged non-stick pans.</strong> Scratched or flaking PTFE coatings release far more particles. If your non-stick pan is peeling, replace it immediately.</p>
<p><strong>Avoid microwave popcorn bags.</strong> The grease-proof lining is a significant PFAS source. Use a stovetop popper or silicone microwave bowl instead.</p>
<p><strong>Reduce fast-food packaging contact.</strong> Transfer food to a plate rather than eating directly from wrappers.</p>
<p><strong>Filter your water.</strong> Activated carbon and reverse osmosis filters reduce PFAS in drinking water significantly.</p>"""
            }
        ],
        "alternatives": [
            {
                "name": "Lodge 12-Inch Cast Iron Skillet",
                "type": "Cast Iron",
                "description": "Pre-seasoned, PFAS-free, and virtually indestructible. The polymerized oil layer provides natural non-stick performance that improves with use.",
                "pros": "Lasts a lifetime, adds dietary iron, zero chemical coatings",
                "cons": "Heavy (8 lbs), requires seasoning maintenance, slow to heat",
                "asin": "B00006JSUA"
            },
            {
                "name": "Caraway Ceramic-Coated Fry Pan",
                "type": "Ceramic Non-Stick",
                "description": "Sol-gel ceramic coating free of PTFE, PFOA, and PFAS. Tested by independent labs for chemical safety. Excellent non-stick at medium heat.",
                "pros": "Lightweight, easy to clean, no chemical off-gassing",
                "cons": "Coating degrades after 2\u20133 years, not dishwasher-safe long-term",
                "asin": "B0BFBKZJNL"
            },
            {
                "name": "All-Clad D3 Stainless Steel Fry Pan",
                "type": "Stainless Steel",
                "description": "Tri-ply bonded construction with zero coatings of any kind. Professional-grade, fully non-reactive, and built to last decades.",
                "pros": "Completely inert, oven-safe to 600\u00b0F, dishwasher-safe",
                "cons": "Food sticks without proper technique (preheat + fat), higher price",
                "asin": "B00005AL46"
            },
            {
                "name": "de Buyer Mineral B Carbon Steel Pan",
                "type": "Carbon Steel",
                "description": "French-made carbon steel that seasons like cast iron but at half the weight. Used in professional kitchens worldwide. Zero synthetic coatings.",
                "pros": "Lighter than cast iron, excellent heat response, PFAS-free",
                "cons": "Requires seasoning, not dishwasher-safe, reacts with acidic foods",
                "asin": "B00462QP1G"
            }
        ],
        "sources": [
            ("EPA PFAS National Primary Drinking Water Regulation (2024)", "https://www.epa.gov/sdwa/and-polyfluoroalkyl-substances-pfas"),
            ("National Academies &mdash; Exposure, Health Effects of PFAS (2022)", "https://nap.nationalacademies.org/catalog/26156"),
            ("IARC Monograph on PFOA (2023)", "https://monographs.iarc.who.int/"),
            ("Environmental Science &amp; Technology &mdash; PFAS release from cookware (2023)", "https://pubs.acs.org/journal/esthag"),
        ]
    },

    # ─── 2. BPA ────────────────────────────────────────────────────────
    {
        "slug": "bpa-plastic-containers",
        "title": "BPA in Plastic Containers: Why &ldquo;BPA-Free&rdquo; Isn&rsquo;t Always Safer",
        "meta_description": "The truth about BPA and its replacements in food containers. Learn which alternatives are genuinely safer based on current science.",
        "verdict_level": "verdict-caution",
        "verdict_rating": "Use Caution &mdash; BPA and its substitutes disrupt hormones",
        "verdict_summary": "BPA (Bisphenol A) is an endocrine disruptor that leaches from polycarbonate plastics and can linings into food. The FDA still permits it in most food packaging, but EFSA slashed its tolerable intake by 20,000x in 2023. Critically, many \"BPA-free\" replacements (BPS, BPF) show similar hormonal activity in studies. Switch to glass or stainless steel for food storage.",
        "sections": [
            {
                "id": "what-is-bpa",
                "heading": "What Is BPA?",
                "content": """<p>Bisphenol A is an industrial chemical used since the 1960s to make polycarbonate plastics and epoxy resins. In your kitchen, it shows up in <strong>hard clear plastic containers</strong> (marked with recycling code #7), the <strong>epoxy lining inside canned foods</strong>, and some <strong>reusable water bottles</strong>.</p>
<p>BPA is structurally similar to estrogen, which is the core problem. It binds to estrogen receptors in the body, mimicking natural hormones at remarkably low concentrations.</p>"""
            },
            {
                "id": "health-risks",
                "heading": "The Health Risks",
                "content": """<p>The scientific picture has sharpened considerably in recent years:</p>
<ul class="key-facts">
  <li><span class="fact-label">Endocrine</span> BPA acts as a xenoestrogen; detectable in 93% of Americans tested by CDC biomonitoring.</li>
  <li><span class="fact-label">EFSA 2023</span> European Food Safety Authority reduced the tolerable daily intake to 0.2 ng/kg &mdash; a 20,000-fold reduction from its previous limit.</li>
  <li><span class="fact-label">Fertility</span> Studies link BPA exposure to reduced sperm quality and disrupted ovarian function.</li>
  <li><span class="fact-label">Metabolic</span> Association with increased risk of type 2 diabetes and obesity in epidemiological studies.</li>
  <li><span class="fact-label">Heat risk</span> Leaching increases 55x when polycarbonate is exposed to boiling water vs. room temperature.</li>
</ul>
<div class="callout callout-warning">
  <strong>The &ldquo;BPA-free&rdquo; trap:</strong> A 2020 study in <em>Current Opinion in Toxicology</em> found that BPS and BPF &mdash; the most common replacements &mdash; show estrogenic activity comparable to BPA itself. &ldquo;BPA-free&rdquo; on the label does not mean &ldquo;endocrine-disruptor-free.&rdquo;
</div>"""
            },
            {
                "id": "what-to-do",
                "heading": "Practical Steps to Reduce Exposure",
                "content": """<p><strong>Never microwave plastic containers.</strong> Even &ldquo;microwave-safe&rdquo; plastics leach more chemicals when heated. Transfer food to glass or ceramic before reheating.</p>
<p><strong>Avoid putting plastic in the dishwasher.</strong> The combination of heat and detergent accelerates degradation and leaching.</p>
<p><strong>Choose cans labeled &ldquo;BPA-NI&rdquo; (non-intent).</strong> Brands like Amy&rsquo;s and Eden Foods use alternative can linings. Look for oleoresin or acrylic-based linings.</p>
<p><strong>Discard old, cloudy, or scratched plastic containers.</strong> Degraded polycarbonate leaches significantly more BPA.</p>"""
            }
        ],
        "alternatives": [
            {
                "name": "Pyrex Simply Store Glass Set (10-Piece)",
                "type": "Borosilicate Glass",
                "description": "Tempered glass containers with BPA-free lids. Completely non-reactive, microwave-safe, and oven-safe. The gold standard for food storage.",
                "pros": "Zero leaching, microwave/oven/dishwasher safe, lasts indefinitely",
                "cons": "Heavier than plastic, lids are still plastic (don\u2019t contact food), breakable",
                "asin": "B09KYGVBCN"
            },
            {
                "name": "Glasslock Oven-Safe Container Set",
                "type": "Tempered Glass",
                "description": "Snap-lock lids with silicone seals for leak-proof storage. Borosilicate glass withstands thermal shock from freezer to oven.",
                "pros": "Leak-proof lids, freezer-to-oven safe, stackable design",
                "cons": "Lids not oven-safe, slightly heavier than Pyrex equivalents",
                "asin": "B007STLBSY"
            },
            {
                "name": "LunchBots Stainless Steel Containers",
                "type": "Stainless Steel",
                "description": "18/8 food-grade stainless steel with no plastic, coatings, or linings. Ideal for packed lunches and dry or wet food storage.",
                "pros": "Virtually indestructible, zero chemicals, lightweight vs. glass",
                "cons": "Not microwave-safe, can dent, no transparent viewing",
                "asin": "B004WCXFKE"
            },
            {
                "name": "Stasher Platinum Silicone Bags",
                "type": "Platinum Silicone",
                "description": "Self-sealing platinum-cured silicone bags. No BPA, BPS, or phthalates. FDA food-grade, dishwasher-safe, and good for sous vide up to 400\u00b0F.",
                "pros": "Reusable (replaces zip-locks), flexible, microwave and freezer safe",
                "cons": "More expensive than disposable bags, can retain odors over time",
                "asin": "B07C7NHS5Q"
            }
        ],
        "sources": [
            ("EFSA Re-evaluation of BPA (2023)", "https://www.efsa.europa.eu/en/topics/topic/bisphenol"),
            ("CDC National Biomonitoring &mdash; BPA Factsheet", "https://www.cdc.gov/biomonitoring/BisphenolA_FactSheet.html"),
            ("Current Opinion in Toxicology &mdash; BPA substitutes (2020)", "https://www.sciencedirect.com/journal/current-opinion-in-toxicology"),
            ("FDA &mdash; Bisphenol A and Food Contact Applications", "https://www.fda.gov/food/food-additives-petitions/bisphenol-bpa-use-food-contact-application"),
        ]
    },

    # ─── 3. Phthalates ────────────────────────────────────────────────
    {
        "slug": "phthalates-food-wrap",
        "title": "Phthalates in Food Wrap: The Hidden Plasticizer in Your Kitchen",
        "meta_description": "How phthalates in plastic wraps and food packaging affect your health. Science-backed guide to safer food storage alternatives.",
        "verdict_level": "verdict-caution",
        "verdict_rating": "Use Caution &mdash; Known endocrine disruptors in everyday wraps",
        "verdict_summary": "Phthalates are plasticizers added to PVC cling wraps and food packaging to make them flexible. They are established endocrine disruptors linked to reproductive harm, and they migrate into fatty and hot foods. The NAS confirmed in 2017 that cumulative phthalate exposure poses a real risk. Switch to beeswax wraps, silicone lids, or parchment paper.",
        "sections": [
            {
                "id": "what-are-phthalates",
                "heading": "What Are Phthalates?",
                "content": """<p>Phthalates are a group of chemicals used to make plastics soft and flexible. In food contact, the main culprits are <strong>DEHP</strong> (di-2-ethylhexyl phthalate) and <strong>DBP</strong> (dibutyl phthalate), commonly found in PVC-based cling wraps, food processing tubing, and printed food packaging.</p>
<p>Unlike BPA, phthalates are not chemically bonded to the plastic &mdash; they&rsquo;re additives that can leach out easily, especially into fatty foods (cheese, meat, oils) and when exposed to heat.</p>"""
            },
            {
                "id": "health-risks",
                "heading": "The Health Risks",
                "content": """<ul class="key-facts">
  <li><span class="fact-label">Endocrine</span> Phthalates are anti-androgenic &mdash; they interfere with testosterone and reproductive development.</li>
  <li><span class="fact-label">Fertility</span> DEHP exposure linked to reduced sperm count and quality in multiple human studies.</li>
  <li><span class="fact-label">Children</span> Higher phthalate metabolites in children&rsquo;s urine associated with ADHD-like behaviors (meta-analysis, 2021).</li>
  <li><span class="fact-label">Migration</span> Studies show phthalates migrate into food at 5&ndash;50x higher rates when wraps contact fatty foods or are heated.</li>
  <li><span class="fact-label">Regulation</span> EU banned DEHP and three other phthalates in food contact materials. The US has been slower to act.</li>
</ul>
<div class="callout callout-warning">
  <strong>The delivery food problem:</strong> A 2021 study in the <em>Journal of Exposure Science &amp; Environmental Epidemiology</em> found that people who eat restaurant or fast-food meals have 35% higher urinary phthalate levels than those who eat home-cooked food &mdash; largely due to food handling gloves and packaging.
</div>"""
            },
            {
                "id": "what-to-do",
                "heading": "How to Reduce Your Exposure",
                "content": """<p><strong>Don&rsquo;t microwave food in plastic wrap.</strong> Even &ldquo;microwave-safe&rdquo; cling wrap can release phthalates when heated. Use a ceramic plate or silicone lid as a splatter guard instead.</p>
<p><strong>Avoid PVC wraps on fatty foods.</strong> If you must use plastic wrap, choose polyethylene (PE/LDPE) wraps, which are phthalate-free. Check the box &mdash; it should say &ldquo;PVC-free&rdquo; or &ldquo;made from polyethylene.&rdquo;</p>
<p><strong>Cook at home more often.</strong> The single biggest factor is reducing contact with commercial food-handling plastics and gloves.</p>
<p><strong>Store oils and fatty foods in glass.</strong> Olive oil, butter, cheese, and nut butters should never sit in plastic long-term.</p>"""
            }
        ],
        "alternatives": [
            {
                "name": "Bee\u2019s Wrap Reusable Food Wraps (Assorted 3-Pack)",
                "type": "Beeswax Wrap",
                "description": "Organic cotton coated with beeswax, jojoba oil, and tree resin. Moldable, washable, and compostable. Replaces plastic wrap for most uses.",
                "pros": "Biodegradable, reusable for ~1 year, grips to bowls and food",
                "cons": "Not for raw meat, can\u2019t be used with hot food, needs hand-washing",
                "asin": "B0126LMDFK"
            },
            {
                "name": "Silicone Stretch Lids (14-Pack, BPA-Free)",
                "type": "Silicone Lids",
                "description": "Food-grade silicone that stretches over bowls, cups, and cut produce. Airtight seal without any PVC or phthalates.",
                "pros": "Reusable thousands of times, microwave/dishwasher safe, airtight",
                "cons": "Don\u2019t work well on non-circular openings, limited sizes",
                "asin": "B07FYPNFFS"
            },
            {
                "name": "If You Care Parchment Paper (Unbleached)",
                "type": "Parchment Paper",
                "description": "Chlorine-free, silicone-coated parchment from FSC-certified wood. Excellent for wrapping food for storage or baking without any plastic contact.",
                "pros": "No plastic chemicals, compostable, oven-safe to 428\u00b0F",
                "cons": "Single-use, not suitable for liquids, less clingy than wrap",
                "asin": "B002YUAM0Q"
            },
            {
                "name": "Pyrex Glass Storage with Lids",
                "type": "Glass Containers",
                "description": "Non-porous glass eliminates all plasticizer contact with food. Ideal for storing fatty foods like cheese, oils, and leftovers.",
                "pros": "Zero chemical migration, see-through, microwave/oven safe",
                "cons": "Heavier, breakable, lid still plastic (but doesn\u2019t contact food)",
                "asin": "B09KYGVBCN"
            }
        ],
        "sources": [
            ("NAS &mdash; Phthalates Cumulative Risk Assessment (2017)", "https://nap.nationalacademies.org/catalog/25043"),
            ("Journal of Exposure Science &mdash; Dining out and phthalates (2021)", "https://www.nature.com/jes/"),
            ("EU REACH Restriction on Phthalates in Food Contact", "https://echa.europa.eu/"),
            ("FDA &mdash; Phthalates in Food Packaging", "https://www.fda.gov/food/food-ingredients-packaging"),
        ]
    },

    # ─── 4. Melamine ──────────────────────────────────────────────────
    {
        "slug": "melamine-plates-safety",
        "title": "Melamine Plates: Safe for Serving, Risky When Heated",
        "meta_description": "Is melamine dinnerware safe? The science on when melamine leaches into food and the best shatter-proof alternatives for families.",
        "verdict_level": "verdict-caution",
        "verdict_rating": "Use with Caution &mdash; Safe cold, problematic when heated",
        "verdict_summary": "Melamine dinnerware is stable at room temperature but leaches melamine and formaldehyde into food when microwaved or used with hot, acidic foods (above 160\u00b0F). The FDA says do not microwave melamine. For families wanting durable, shatter-proof plates, there are genuinely safer options that handle heat without chemical migration.",
        "sections": [
            {
                "id": "what-is-melamine",
                "heading": "What Is Melamine Dinnerware?",
                "content": """<p>Melamine is a nitrogen-rich organic compound that, when combined with formaldehyde, creates melamine-formaldehyde resin &mdash; a hard, glossy, shatter-resistant plastic. It&rsquo;s the material behind those colorful, lightweight plates marketed for outdoor dining, kids&rsquo; meals, and cafeterias.</p>
<p>The appeal is obvious: it looks like ceramic, won&rsquo;t break when dropped, and costs a fraction of the price. The problem is what happens when heat enters the equation.</p>"""
            },
            {
                "id": "health-risks",
                "heading": "The Health Risks",
                "content": """<ul class="key-facts">
  <li><span class="fact-label">FDA Warning</span> The FDA explicitly states: &ldquo;Don&rsquo;t microwave food in melamine dishware.&rdquo; High heat causes measurable leaching.</li>
  <li><span class="fact-label">Kidneys</span> Chronic melamine exposure damages renal tubules. The 2008 Chinese milk scandal (melamine-adulterated formula) caused kidney stones in 300,000 infants.</li>
  <li><span class="fact-label">Leaching</span> A Taiwanese study found melamine levels in urine increased 8.35x after eating hot noodle soup from melamine bowls vs. ceramic bowls.</li>
  <li><span class="fact-label">Acid trigger</span> Acidic foods (tomato sauce, citrus, vinegar-based dressings) significantly increase melamine migration, even at lower temperatures.</li>
  <li><span class="fact-label">Degradation</span> Repeated dishwasher use gradually erodes the surface, increasing leaching in older plates.</li>
</ul>
<div class="callout callout-safe">
  <strong>The good news:</strong> At room temperature with non-acidic foods (crackers, sandwiches, dry snacks), melamine plates pose minimal risk. The key is understanding when NOT to use them.
</div>"""
            },
            {
                "id": "what-to-do",
                "heading": "Safe Use Guidelines",
                "content": """<p><strong>Never microwave melamine.</strong> This is the single most important rule. Transfer food to a ceramic or glass dish before reheating.</p>
<p><strong>Don&rsquo;t serve hot soups or sauces in melamine bowls.</strong> If the food is steaming, use a different vessel.</p>
<p><strong>Retire scratched or worn melamine.</strong> Surface degradation increases chemical migration significantly.</p>
<p><strong>Use melamine for cold foods only.</strong> Chips, crackers, fruit salads, and sandwiches are fine. It&rsquo;s still excellent poolside or for camping with cold items.</p>"""
            }
        ],
        "alternatives": [
            {
                "name": "Corelle Vitrelle Glass Dinnerware Set",
                "type": "Tempered Glass",
                "description": "Triple-layer Vitrelle glass that\u2019s ultra-thin, lightweight, and remarkably break-resistant. Microwave, oven, and dishwasher safe with zero chemical leaching.",
                "pros": "Chip/break resistant, lightweight like melamine, completely non-reactive",
                "cons": "Can shatter on hard impact (though rarely), higher upfront cost",
                "asin": "B0C1QNSVY8"
            },
            {
                "name": "Kangovou Stainless Steel Kids\u2019 Plate Set",
                "type": "Stainless Steel",
                "description": "18/8 stainless steel divided plates with BPA-free PP lids. Designed specifically for children\u2019s meals with no chemical coatings.",
                "pros": "Truly unbreakable, zero leaching, dishwasher safe",
                "cons": "Gets hot with hot food, not microwave safe, metallic look",
                "asin": "B00E6PUTQI"
            },
            {
                "name": "Bamboozle Bamboo Dinnerware Set",
                "type": "Bamboo Composite",
                "description": "Made from bamboo fiber bound with plant-based (non-formaldehyde) resin. Lightweight and biodegradable. Verify &ldquo;melamine-free&rdquo; on label.",
                "pros": "Biodegradable, lightweight, stylish earth tones",
                "cons": "Not microwave-safe, hand-wash only, less durable than melamine",
                "asin": "B07P63BFKJ"
            },
            {
                "name": "IKEA OFTAST Tempered Glass Plates",
                "type": "Tempered Glass",
                "description": "Budget-friendly tempered glass plates that handle everyday use. Microwave and dishwasher safe with no coatings or chemical treatments.",
                "pros": "Very affordable, microwave safe, no chemicals",
                "cons": "Heavier than melamine, can break if dropped on hard floors",
                "asin": "B0DHDTBB23"
            }
        ],
        "sources": [
            ("FDA &mdash; Melamine in Tableware", "https://www.fda.gov/food/chemicals/melamine-tableware"),
            ("JAMA Internal Medicine &mdash; Melamine in urine after soup consumption (2013)", "https://jamanetwork.com/journals/jamainternalmedicine"),
            ("WHO &mdash; Melamine and Cyanuric Acid Toxicity", "https://www.who.int/news-room/questions-and-answers/item/melamine"),
            ("European Commission &mdash; Melamine Migration Limits", "https://food.ec.europa.eu/safety/chemical-safety_en"),
        ]
    },

    # ─── 5. Aluminum Foil ─────────────────────────────────────────────
    {
        "slug": "aluminum-foil-cooking",
        "title": "Aluminum Foil and Cooking: When It&rsquo;s Safe and When It&rsquo;s Not",
        "meta_description": "Is cooking with aluminum foil safe? Science-based guide to when aluminum leaches into food and practical alternatives for high-risk uses.",
        "verdict_level": "verdict-safe",
        "verdict_rating": "Generally Safe &mdash; Avoid with acidic foods at high heat",
        "verdict_summary": "Aluminum foil is safe for most kitchen uses. The body efficiently excretes small amounts of dietary aluminum, and the Alzheimer\u2019s link from the 1960s has not held up in modern research. However, wrapping acidic foods (tomatoes, lemon, vinegar) in foil at high oven temperatures does cause measurable leaching that can exceed WHO\u2019s tolerable weekly intake. Use parchment paper for those cases.",
        "sections": [
            {
                "id": "the-science",
                "heading": "What the Science Actually Says",
                "content": """<p>Aluminum is the most abundant metal in Earth&rsquo;s crust, and trace amounts are in most foods naturally. The question isn&rsquo;t whether you ingest aluminum &mdash; you do, daily &mdash; but whether cooking with foil pushes intake to harmful levels.</p>
<p>The WHO established a Provisional Tolerable Weekly Intake (PTWI) of 2 mg/kg body weight. For a 150-lb adult, that&rsquo;s about 136 mg per week. Most people consume 1&ndash;10 mg daily from food alone.</p>"""
            },
            {
                "id": "health-risks",
                "heading": "When Foil Becomes a Concern",
                "content": """<ul class="key-facts">
  <li><span class="fact-label">Acidic foods</span> A 2019 study in <em>International Journal of Electrochemical Science</em> found tomatoes wrapped in foil at 400\u00b0F leached 4&ndash;6 mg of aluminum per serving.</li>
  <li><span class="fact-label">Spices</span> Salt and acidic spices (turmeric, vinegar-based marinades) accelerate leaching significantly.</li>
  <li><span class="fact-label">Temperature</span> Leaching increases exponentially above 350\u00b0F, especially with extended cooking times.</li>
  <li><span class="fact-label">Alzheimer&rsquo;s</span> The 1965 hypothesis linking aluminum to Alzheimer&rsquo;s has been largely discredited. The Alzheimer&rsquo;s Association states the evidence is not convincing.</li>
  <li><span class="fact-label">Kidneys</span> People with impaired kidney function cannot excrete aluminum as efficiently and should limit exposure.</li>
</ul>
<div class="callout callout-safe">
  <strong>Bottom line:</strong> Wrapping a sandwich in foil or covering a baking sheet? Perfectly fine. Wrapping a lemon-herb chicken in foil at 425\u00b0F for an hour? Use parchment paper instead.
</div>"""
            },
            {
                "id": "what-to-do",
                "heading": "Simple Rules for Safe Use",
                "content": """<p><strong>Use foil freely for storage and cold wrapping.</strong> No leaching occurs at room or refrigerator temperatures.</p>
<p><strong>Switch to parchment for acidic + hot.</strong> If your recipe involves tomatoes, citrus, vinegar, or wine &mdash; and heat &mdash; parchment paper is the better choice.</p>
<p><strong>Don&rsquo;t cook directly on foil at high heat.</strong> Use it as a tent or cover, not as a direct cooking surface for acidic marinades.</p>
<p><strong>Avoid foil with salty or spiced rubs.</strong> Salt + acid + heat is the worst-case combination for aluminum leaching.</p>"""
            }
        ],
        "alternatives": [
            {
                "name": "If You Care Unbleached Parchment Paper",
                "type": "Parchment Paper",
                "description": "Silicone-coated, chlorine-free parchment that handles up to 428\u00b0F. Perfect for acidic foods in the oven \u2014 zero metal contact.",
                "pros": "No aluminum leaching, non-stick, compostable",
                "cons": "Single-use, not great for wrapping leftovers, max 428\u00b0F",
                "asin": "B002YUAM0Q"
            },
            {
                "name": "Silpat Premium Silicone Baking Mat",
                "type": "Silicone Mat",
                "description": "Fiberglass-reinforced food-grade silicone. Reusable for 3,000+ baking sessions. Replaces foil on baking sheets entirely.",
                "pros": "Reusable for years, non-stick, no chemicals or metal contact",
                "cons": "Only for flat sheet pans, not for wrapping, needs washing",
                "asin": "B00008T960"
            },
            {
                "name": "Pyrex Deep Glass Baking Dish",
                "type": "Glass Bakeware",
                "description": "Borosilicate glass handles oven temperatures without any reactivity. Ideal for casseroles and acidic dishes like lasagna.",
                "pros": "Completely non-reactive, oven and microwave safe, doubles as storage",
                "cons": "Heavy, breakable, can\u2019t wrap food in it",
                "asin": "B09V233X46"
            },
            {
                "name": "Lodge Cast Iron Grill Pan",
                "type": "Cast Iron",
                "description": "Pre-seasoned cast iron for grilling or roasting without foil. The iron surface is non-reactive once properly seasoned.",
                "pros": "Adds iron to food (beneficial), excellent heat retention, PFAS-free",
                "cons": "Very heavy, requires seasoning maintenance",
                "asin": "B0000CF66W"
            }
        ],
        "sources": [
            ("WHO Provisional Tolerable Weekly Intake for Aluminum", "https://www.who.int/publications/i/item/9789241660600"),
            ("International Journal of Electrochemical Science &mdash; Al leaching in cooking (2019)", "https://www.electrochemsci.org/"),
            ("Alzheimer&rsquo;s Association &mdash; Aluminum and Alzheimer&rsquo;s", "https://www.alz.org/alzheimers-dementia/what-is-alzheimers/myths"),
            ("EFSA &mdash; Safety of Aluminum from Dietary Intake (2008)", "https://www.efsa.europa.eu/en/efsajournal/pub/754"),
        ]
    },

    # ─── 6. Cast Iron Seasoning ───────────────────────────────────────
    {
        "slug": "cast-iron-seasoning",
        "title": "Cast Iron Seasoning: The Science Behind the Safest Non-Stick Surface",
        "meta_description": "Is cast iron seasoning safe? The food science behind polymerized oil, iron leaching benefits, and how to maintain your skillet properly.",
        "verdict_level": "verdict-safe",
        "verdict_rating": "Safe &mdash; One of the healthiest cookware choices available",
        "verdict_summary": "Cast iron seasoning is polymerized oil \u2014 a food-safe, carbon-based coating formed by heating oil past its smoke point. It is not burnt food and is not carcinogenic. Cast iron can leach small amounts of dietary iron into food, which is actually beneficial for most people. Properly seasoned cast iron is one of the safest, most durable cookware options available.",
        "sections": [
            {
                "id": "what-is-seasoning",
                "heading": "What Is Cast Iron Seasoning, Really?",
                "content": """<p>Seasoning is not a spice or flavoring \u2014 it&rsquo;s a <strong>thin polymer layer</strong> formed when cooking oil is heated beyond its smoke point on the iron surface. The fatty acid chains in the oil break down (pyrolyze) and then re-bond through cross-linking, creating a hard, smooth, plastic-like film that is chemically bonded to the metal.</p>
<p>This process is called <strong>oil polymerization</strong>, and it&rsquo;s the same chemistry behind drying oils used in art (linseed oil on paintings, for example). The result is a naturally non-stick surface that contains no synthetic chemicals whatsoever.</p>"""
            },
            {
                "id": "is-it-safe",
                "heading": "Is the &ldquo;Burnt Oil&rdquo; Carcinogenic?",
                "content": """<p>This is the most common concern, and the answer is clear: <strong>no</strong>.</p>
<ul class="key-facts">
  <li><span class="fact-label">Polymerized</span> The oil undergoes a chemical transformation into a stable polymer. It is not &ldquo;burnt&rdquo; food or charred residue.</li>
  <li><span class="fact-label">Inert</span> Once polymerized, the coating is chemically inert \u2014 it does not break down during normal cooking temperatures (up to 500\u00b0F).</li>
  <li><span class="fact-label">Iron leaching</span> Cast iron does transfer small amounts of iron into food (1\u20133 mg per serving), especially with acidic foods. For most adults, this is beneficial and helps prevent iron deficiency.</li>
  <li><span class="fact-label">No PAHs</span> Unlike charring meat, the thin-layer polymerization of oil at seasoning temperatures does not produce meaningful polycyclic aromatic hydrocarbons.</li>
  <li><span class="fact-label">Track record</span> Cast iron has been used safely for cooking for over 2,000 years across virtually every culture.</li>
</ul>
<div class="callout callout-warning">
  <strong>One exception:</strong> People with hemochromatosis (iron overload disorder) should limit cast iron use, as the extra dietary iron can be harmful. If you have this condition, consult your doctor.
</div>"""
            },
            {
                "id": "maintenance",
                "heading": "How to Season and Maintain Properly",
                "content": """<p><strong>Initial seasoning:</strong> Apply a thin layer of high-smoke-point oil (grapeseed, flaxseed, or Crisbee) and bake upside-down at 450\u00b0F for one hour. Repeat 2\u20133 times for a solid base layer.</p>
<p><strong>Daily maintenance:</strong> After cooking, rinse with hot water and a stiff brush. A small amount of soap is fine \u2014 the myth that soap destroys seasoning is outdated (modern dish soap doesn&rsquo;t contain lye).</p>
<p><strong>Dry immediately.</strong> Cast iron rusts quickly. Dry on the stovetop over low heat, then apply a very thin oil layer.</p>
<p><strong>Avoid long-simmered acidic foods.</strong> Tomato sauce simmered for 30+ minutes will strip seasoning and add a metallic taste. Use enameled cast iron for those dishes.</p>"""
            }
        ],
        "alternatives": [
            {
                "name": "Lodge 10.25-Inch Cast Iron Skillet",
                "type": "Pre-Seasoned Cast Iron",
                "description": "America\u2019s best-selling cast iron skillet. Pre-seasoned with vegetable oil at the foundry, ready to use. Made in the USA since 1896.",
                "pros": "Lifetime warranty, affordable, excellent heat retention",
                "cons": "Weighs 5 lbs, requires maintenance, slow to heat evenly",
                "asin": "B00006JSUA"
            },
            {
                "name": "Le Creuset Enameled Cast Iron Dutch Oven",
                "type": "Enameled Cast Iron",
                "description": "Porcelain enamel over cast iron eliminates the need for seasoning and prevents iron leaching. Ideal for acidic dishes, soups, and braises.",
                "pros": "No seasoning needed, non-reactive with acids, stunning colors",
                "cons": "Expensive, enamel can chip, slightly less non-stick than seasoned iron",
                "asin": "B00004S9H4"
            },
            {
                "name": "Crisbee Cast Iron Seasoning Puck",
                "type": "Seasoning Product",
                "description": "Blend of beeswax, soy, and palm oils specifically formulated for cast iron. Easier and more consistent than DIY oil seasoning.",
                "pros": "Easy application, great results, also works on carbon steel",
                "cons": "Added cost, not strictly necessary (any oil works)",
                "asin": "B00R5BXF4Y"
            },
            {
                "name": "The Ringer Stainless Steel Chainmail Scrubber",
                "type": "Cleaning Tool",
                "description": "316 stainless steel chainmail scrubber that cleans stuck-on food without stripping seasoning. No soap needed for routine cleaning.",
                "pros": "Preserves seasoning, lasts forever, no chemicals",
                "cons": "Only useful for cast iron/carbon steel, doesn\u2019t replace soap for sanitation",
                "asin": "B00FKBR1ZG"
            }
        ],
        "sources": [
            ("Journal of Food Science &mdash; Iron leaching from cast iron cookware", "https://ift.onlinelibrary.wiley.com/journal/17503841"),
            ("America&rsquo;s Test Kitchen &mdash; Science of Cast Iron Seasoning", "https://www.americastestkitchen.com/"),
            ("Sheryl Canter &mdash; Chemistry of Cast Iron Seasoning (Polymerization)", "https://sherylcanter.com/wordpress/2010/01/a-science-based-technique-for-seasoning-cast-iron/"),
            ("NIH &mdash; Iron Deficiency and Dietary Sources", "https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/"),
        ]
    },

    # ─── 7. Silicone Bakeware ─────────────────────────────────────────
    {
        "slug": "silicone-bakeware-heat",
        "title": "Silicone Bakeware: Safe at What Temperature?",
        "meta_description": "Is silicone bakeware safe at high heat? How to identify quality food-grade silicone and when to use alternatives instead.",
        "verdict_level": "verdict-safe",
        "verdict_rating": "Generally Safe &mdash; Quality matters more than material",
        "verdict_summary": "Food-grade, platinum-cured silicone is stable and inert up to about 425\u00b0F (220\u00b0C). Above this, some studies detect trace volatile compounds, though at levels below regulatory concern. The real issue is cheap, low-quality silicone that may contain fillers. Use the twist test: if white shows through when you twist it, it contains fillers and should be avoided.",
        "sections": [
            {
                "id": "what-is-silicone",
                "heading": "What Is Food-Grade Silicone?",
                "content": """<p>Silicone (polydimethylsiloxane, or PDMS) is a synthetic polymer made from silicon, oxygen, carbon, and hydrogen. Unlike plastics derived from petroleum, silicone is based on <strong>siloxane bonds</strong> (silicon-oxygen), which are exceptionally stable and heat-resistant.</p>
<p>There are two manufacturing processes: <strong>platinum-cured</strong> (addition cure) and <strong>peroxide-cured</strong> (tin-cured). Platinum-cured silicone is the gold standard for food contact \u2014 it produces no byproducts and contains no residual catalysts that could leach.</p>"""
            },
            {
                "id": "health-risks",
                "heading": "What the Research Shows",
                "content": """<ul class="key-facts">
  <li><span class="fact-label">FDA status</span> Silicone is classified as GRAS (Generally Recognized As Safe) for food contact by the FDA.</li>
  <li><span class="fact-label">Stability</span> Quality silicone remains stable up to approximately 425\u00b0F. Most baking occurs in the 325\u2013400\u00b0F range.</li>
  <li><span class="fact-label">Above 425\u00b0F</span> A 2018 German Federal Institute study detected trace siloxane compounds at high temperatures, but below levels of health concern.</li>
  <li><span class="fact-label">No leaching</span> Multiple studies confirm platinum-cured silicone does not leach detectable chemicals into food at normal baking temperatures.</li>
  <li><span class="fact-label">Fillers</span> Low-cost silicone may contain plastic fillers that compromise heat stability \u2014 this is the primary safety concern.</li>
</ul>
<div class="callout callout-warning">
  <strong>The twist test:</strong> Pinch and twist the silicone. If it stays the same color, it\u2019s pure silicone. If a white line or white color shows through, it contains fillers and should not be used for baking.
</div>"""
            },
            {
                "id": "what-to-do",
                "heading": "How to Buy and Use Silicone Safely",
                "content": """<p><strong>Buy platinum-cured, FDA-grade silicone.</strong> Look for brands that specifically advertise &ldquo;platinum-cured&rdquo; or &ldquo;medical-grade&rdquo; silicone.</p>
<p><strong>Stay below 425\u00b0F.</strong> This covers virtually all baking. If you\u2019re broiling or cooking above 450\u00b0F, use metal or glass instead.</p>
<p><strong>Perform the twist test before first use.</strong> Reject any silicone product that shows white when deformed.</p>
<p><strong>&ldquo;Cure&rdquo; new silicone bakeware.</strong> Bake empty at 350\u00b0F for 30 minutes to off-gas any manufacturing residues. This is a one-time step.</p>"""
            }
        ],
        "alternatives": [
            {
                "name": "Silpat Premium Silicone Baking Mat",
                "type": "Platinum-Cured Silicone",
                "description": "The original French-made silicone baking mat used in professional pastry kitchens. Fiberglass-reinforced, platinum-cured, and rated to 480\u00b0F.",
                "pros": "Professional-grade, 3,000+ uses, even heat distribution",
                "cons": "Only fits standard sheet pans, must hand-wash, not for cutting on",
                "asin": "B00008T960"
            },
            {
                "name": "USA Pan Half Sheet Baking Pan",
                "type": "Aluminized Steel",
                "description": "Commercial-grade aluminized steel with a silicone-based Americoat non-stick coating. PTFE and BPA-free. Handles any oven temperature.",
                "pros": "Warp-resistant, oven-safe to 450\u00b0F+, excellent browning",
                "cons": "Heavier than silicone mats, coating wears over years, hand-wash recommended",
                "asin": "B0029JOC6I"
            },
            {
                "name": "Pyrex Basics Glass Baking Dish",
                "type": "Tempered Glass",
                "description": "Non-porous tempered glass that never reacts with food. Ideal for casseroles, roasting, and any recipe involving acidic ingredients.",
                "pros": "Completely inert, doubles as serving dish, microwave safe",
                "cons": "Cannot handle sudden temperature changes (thermal shock), heavy",
                "asin": "B09V233X46"
            },
            {
                "name": "Nordic Ware Natural Aluminum Muffin Pan",
                "type": "Uncoated Aluminum",
                "description": "Pure aluminum with no non-stick coating. Use with paper liners or a thin coat of butter. Professional bakeries prefer uncoated aluminum for even browning.",
                "pros": "Best heat conductivity, no coatings to wear out, dishwasher safe",
                "cons": "Requires liners or greasing, reacts with highly acidic batters",
                "asin": "B0049EILDI"
            }
        ],
        "sources": [
            ("FDA &mdash; Silicone as GRAS for Food Contact", "https://www.fda.gov/food/food-ingredients-packaging"),
            ("German Federal Institute for Risk Assessment &mdash; Silicone bakeware (2018)", "https://www.bfr.bund.de/en/"),
            ("European Commission Regulation on Silicone Food Contact Materials", "https://food.ec.europa.eu/safety/chemical-safety/food-contact-materials_en"),
        ]
    },

    # ─── 8. Unlined Copper ────────────────────────────────────────────
    {
        "slug": "unlined-copper-toxicity",
        "title": "Unlined Copper Cookware: Beautiful but Potentially Toxic",
        "meta_description": "Why cooking with unlined copper is risky, how copper salts form in acidic foods, and the best lined copper alternatives for safe cooking.",
        "verdict_level": "verdict-avoid",
        "verdict_rating": "Avoid for Cooking &mdash; Copper reacts with acids to form toxic salts",
        "verdict_summary": "Unlined copper cookware reacts with acidic, alkaline, and salty foods to produce copper salts (verdigris) that can cause nausea, vomiting, and liver damage at high doses. The WHO sets a tolerable daily intake of 0.5 mg/kg. A single acidic meal cooked in unlined copper can exceed this. Always use copper cookware with a stainless steel or tin lining.",
        "sections": [
            {
                "id": "the-appeal",
                "heading": "Why Copper Is Prized in Kitchens",
                "content": """<p>Copper has the best thermal conductivity of any common cookware metal \u2014 roughly 25x better than stainless steel. This means <strong>instant, even heat response</strong> with no hot spots. It&rsquo;s why professional French kitchens have used copper for centuries.</p>
<p>The problem is that copper is also <strong>highly reactive</strong>. When it contacts acidic foods (tomatoes, wine, lemon juice, vinegar), it dissolves into the food as copper ions, forming compounds like copper acetate and copper citrate \u2014 collectively known as <strong>verdigris</strong>.</p>"""
            },
            {
                "id": "health-risks",
                "heading": "The Health Risks",
                "content": """<ul class="key-facts">
  <li><span class="fact-label">Acute toxicity</span> Ingesting more than 15 mg of copper in a single dose can cause nausea, vomiting, and abdominal pain.</li>
  <li><span class="fact-label">WHO limit</span> Tolerable upper intake is 10 mg/day for adults. A single acidic dish cooked in unlined copper can leach 5\u201350 mg.</li>
  <li><span class="fact-label">Liver damage</span> Chronic copper overexposure causes hepatic (liver) damage. Wilson&rsquo;s disease patients are especially vulnerable.</li>
  <li><span class="fact-label">Verdigris</span> The green patina on old copper is copper carbonate/acetate \u2014 toxic if it contacts food.</li>
  <li><span class="fact-label">Safe use exists</span> Copper bowls for whipping egg whites are safe because eggs are not acidic, and the copper stabilizes the foam via a protein-copper interaction.</li>
</ul>
<div class="callout callout-danger">
  <strong>Warning:</strong> Never cook tomato sauce, wine-based sauces, citrus marinades, or vinegar dressings in unlined copper. The copper leaching can be rapid and significant.
</div>"""
            },
            {
                "id": "what-to-do",
                "heading": "How to Enjoy Copper Safely",
                "content": """<p><strong>Always buy lined copper.</strong> Modern copper cookware uses stainless steel linings that completely prevent food-metal contact. Tin-lined is traditional but requires re-tinning every few years.</p>
<p><strong>Inspect tin linings regularly.</strong> If the tin layer wears through to expose copper, stop cooking in it until it&rsquo;s re-tinned.</p>
<p><strong>Use unlined copper only for sugar work and egg whites.</strong> These are the two culinary applications where unlined copper is both safe and beneficial.</p>
<p><strong>Never let copper develop green patina near food.</strong> Clean copper regularly if used decoratively in the kitchen.</p>"""
            }
        ],
        "alternatives": [
            {
                "name": "Mauviel M\u2019150S Copper Saucepan (Stainless Lined)",
                "type": "Lined Copper",
                "description": "1.5mm French copper with a bonded stainless steel interior. All the thermal performance of copper with a fully non-reactive cooking surface.",
                "pros": "Best of both worlds \u2014 copper conductivity + safe interior, gorgeous",
                "cons": "Expensive, heavy, requires copper polishing for appearance",
                "asin": "B00EOGMJSC"
            },
            {
                "name": "All-Clad Copper Core 3-Qt Saucepan",
                "type": "Copper-Core Stainless",
                "description": "Five-ply construction with a copper core sandwiched between stainless steel. Excellent conductivity without any copper touching food.",
                "pros": "Dishwasher safe, no copper maintenance, professional heat control",
                "cons": "Expensive, copper is hidden (no aesthetic copper look)",
                "asin": "B004O6KXR4"
            },
            {
                "name": "Matfer Bourgeat Copper Egg White Bowl",
                "type": "Unlined Copper (Safe Use)",
                "description": "14-inch unlined copper bowl specifically designed for whipping egg whites. The copper ions stabilize egg foam, producing superior meringue. This is the one safe use of unlined copper.",
                "pros": "Produces better meringue, traditional French technique, stunning",
                "cons": "Single-purpose, expensive, must be cleaned with salt and vinegar before each use",
                "asin": "B00009B7NR"
            },
            {
                "name": "Demeyere Industry5 Stainless Steel Saucepan",
                "type": "Stainless Steel",
                "description": "If you want excellent heat distribution without copper maintenance, five-ply stainless steel with an aluminum core is the practical choice.",
                "pros": "Non-reactive, dishwasher safe, no special maintenance",
                "cons": "Not as responsive as copper, utilitarian appearance",
                "asin": "B000ON8ILG"
            }
        ],
        "sources": [
            ("WHO &mdash; Copper in Drinking Water Guidelines", "https://www.who.int/publications/i/item/9789241546553"),
            ("European Copper Institute &mdash; Copper and Health", "https://copperalliance.org/"),
            ("NIH &mdash; Copper Fact Sheet for Health Professionals", "https://ods.od.nih.gov/factsheets/Copper-HealthProfessional/"),
            ("Harold McGee &mdash; On Food and Cooking (Copper Chemistry)", "https://www.penguinrandomhouse.com/books/293199/on-food-and-cooking-by-harold-mcgee/"),
        ]
    },

    # ─── 9. Antimony / PET Bottles ────────────────────────────────────
    {
        "slug": "antimony-pet-bottles",
        "title": "Antimony in PET Bottles: Should You Worry About Your Water Bottle?",
        "meta_description": "The science on antimony leaching from PET plastic water bottles. When it's a real risk, and the best reusable alternatives.",
        "verdict_level": "verdict-caution",
        "verdict_rating": "Low Risk Normally &mdash; Significant risk when heated or stored long-term",
        "verdict_summary": "Antimony trioxide is used as a catalyst in PET plastic production and remains as a trace residue. At room temperature, leaching is well below WHO limits. But when PET bottles are exposed to heat (car dashboards, sunlight, hot storage), antimony leaching increases 2\u201390x and can approach or exceed the EPA drinking water standard of 6 ppb. Don\u2019t reuse single-use PET bottles, and switch to reusable alternatives.",
        "sections": [
            {
                "id": "what-is-antimony",
                "heading": "What Is Antimony and Why Is It in Plastic?",
                "content": """<p>Antimony trioxide (Sb\u2082O\u2083) is a catalyst used during the polymerization of PET (polyethylene terephthalate) \u2014 the plastic used in virtually all single-use water bottles, soda bottles, and many food containers marked with recycling code #1.</p>
<p>After manufacturing, trace amounts of antimony remain embedded in the plastic. Under normal conditions, the amount that leaches into water is extremely small. The concern arises with <strong>heat, time, and repeated use</strong>.</p>"""
            },
            {
                "id": "health-risks",
                "heading": "When Antimony Becomes a Problem",
                "content": """<ul class="key-facts">
  <li><span class="fact-label">EPA limit</span> Maximum contaminant level for antimony in drinking water is 6 ppb (parts per billion).</li>
  <li><span class="fact-label">Room temp</span> Studies consistently show leaching below 1 ppb at 25\u00b0C \u2014 well within safe limits.</li>
  <li><span class="fact-label">Heat effect</span> A 2016 study in <em>Journal of Environmental Monitoring</em> found that storing PET bottles at 60\u00b0C (140\u00b0F) for one week increased antimony leaching up to 90x vs. room temperature.</li>
  <li><span class="fact-label">Sunlight</span> UV exposure also accelerates leaching, even at moderate temperatures.</li>
  <li><span class="fact-label">Chronic risk</span> Antimony is classified as a possible carcinogen (IARC Group 2B as antimony trioxide). Chronic exposure affects the lungs, heart, and liver.</li>
</ul>
<div class="callout callout-warning">
  <strong>The car dashboard scenario:</strong> On a 90\u00b0F day, the inside of a parked car reaches 130\u2013170\u00b0F. A PET water bottle left on the dashboard for hours can leach antimony well above safe levels. This is the most common real-world risk.
</div>"""
            },
            {
                "id": "what-to-do",
                "heading": "Simple Precautions",
                "content": """<p><strong>Never leave PET bottles in hot cars.</strong> This is the single most impactful step you can take.</p>
<p><strong>Don\u2019t refill single-use PET bottles.</strong> Repeated filling, squeezing, and washing degrades the plastic and increases leaching.</p>
<p><strong>Store bottled water in a cool, dark place.</strong> A pantry or refrigerator is ideal. Avoid garages and storage sheds.</p>
<p><strong>Switch to a reusable bottle.</strong> Stainless steel and glass eliminate the issue entirely and pay for themselves quickly.</p>"""
            }
        ],
        "alternatives": [
            {
                "name": "Hydro Flask Standard Mouth (21 oz)",
                "type": "Stainless Steel",
                "description": "Double-wall vacuum-insulated 18/8 stainless steel. Keeps water cold for 24 hours. No plastic touches the water \u2014 the entire interior is steel.",
                "pros": "Insulated, no chemicals, extremely durable, BPA/phthalate-free",
                "cons": "Heavier than plastic, dents if dropped, hand-wash recommended",
                "asin": "B09YDQP4Q4"
            },
            {
                "name": "Lifefactory Glass Water Bottle (22 oz)",
                "type": "Glass",
                "description": "Borosilicate glass with a protective silicone sleeve. Completely inert \u2014 glass doesn\u2019t leach anything regardless of temperature or time.",
                "pros": "Zero chemical migration, dishwasher safe, taste-neutral",
                "cons": "Heavier than steel, can break even with sleeve, no insulation",
                "asin": "B07CSPG2GG"
            },
            {
                "name": "Nalgene Tritan Wide Mouth (32 oz)",
                "type": "Tritan Copolyester",
                "description": "Made from Eastman Tritan (not PET), which is BPA-free, antimony-free, and does not use bisphenol catalysts. Independently tested for estrogenic activity.",
                "pros": "Lightweight like PET, shatter-resistant, no antimony or BPA",
                "cons": "Still plastic (though inert), not insulated, can retain odors",
                "asin": "B08198JKFG"
            },
            {
                "name": "Brita Premium Filtering Water Bottle (26 oz)",
                "type": "Filtered Bottle",
                "description": "BPA-free bottle with a built-in activated carbon filter that reduces chlorine taste, microplastics, and some contaminants as you drink.",
                "pros": "Filters on the go, reduces microplastics, affordable",
                "cons": "Filters need replacement every 40 gallons, still a plastic shell",
                "asin": "B0BT9F1P5P"
            }
        ],
        "sources": [
            ("EPA &mdash; Antimony Drinking Water Standard", "https://www.epa.gov/ground-water-and-drinking-water/national-primary-drinking-water-regulations"),
            ("Journal of Environmental Monitoring &mdash; Antimony leaching from PET (2016)", "https://pubs.rsc.org/en/journals/journalissues/em"),
            ("IARC &mdash; Antimony Trioxide Classification", "https://monographs.iarc.who.int/"),
            ("Water Research &mdash; PET bottle leaching review (2018)", "https://www.sciencedirect.com/journal/water-research"),
        ]
    },

    # ─── 10. Teflon (PTFE) ────────────────────────────────────────────
    {
        "slug": "teflon-ptfe-offgassing",
        "title": "Teflon Off-Gassing: What Happens When Non-Stick Pans Overheat",
        "meta_description": "The science on PTFE (Teflon) off-gassing at high temperatures. When non-stick is safe, when it's dangerous, and what to use instead.",
        "verdict_level": "verdict-caution",
        "verdict_rating": "Use with Caution &mdash; Safe at normal temps, toxic above 500\u00b0F",
        "verdict_summary": "PTFE (Teflon) is chemically stable and safe at normal cooking temperatures below 450\u00b0F. Above 500\u00b0F, it begins releasing toxic fumes that cause \"polymer fume fever\" in humans and can kill pet birds. Modern Teflon no longer contains PFOA (phased out by 2015), but the PTFE polymer itself is the concern at extreme heat. Never preheat an empty non-stick pan, and keep heat at medium or below.",
        "sections": [
            {
                "id": "ptfe-vs-pfoa",
                "heading": "PTFE vs. PFOA: An Important Distinction",
                "content": """<p>There is massive public confusion between PTFE and PFOA, and understanding the difference is critical:</p>
<p><strong>PTFE (polytetrafluoroethylene)</strong> is the actual non-stick coating on your pan. It&rsquo;s a large, stable polymer that is biologically inert at normal temperatures. If you accidentally swallowed a flake of Teflon, it would pass through you undigested \u2014 your body can&rsquo;t break it down.</p>
<p><strong>PFOA (perfluorooctanoic acid)</strong> was a processing aid used to manufacture PTFE coatings. It was the genuinely dangerous part \u2014 a PFAS chemical linked to cancer. PFOA was <strong>voluntarily phased out of Teflon production by 2015</strong> under EPA pressure. Modern non-stick pans do not contain PFOA.</p>
<p>The remaining concern with PTFE is purely thermal: <strong>what happens when it gets too hot</strong>.</p>"""
            },
            {
                "id": "health-risks",
                "heading": "The Temperature Thresholds",
                "content": """<ul class="key-facts">
  <li><span class="fact-label">Below 400\u00b0F</span> PTFE is completely stable. Most cooking (saut\u00e9ing, eggs, pancakes) occurs in this range. No risk.</li>
  <li><span class="fact-label">400\u2013500\u00b0F</span> PTFE begins to degrade slightly. Normal cooking rarely sustains these temperatures, but an empty pan on high heat reaches them in 2\u20135 minutes.</li>
  <li><span class="fact-label">Above 500\u00b0F</span> PTFE releases measurable toxic fumes (ultrafine particles and fluorocarbon gases). Causes &ldquo;polymer fume fever&rdquo; &mdash; flu-like symptoms in humans.</li>
  <li><span class="fact-label">Above 660\u00b0F</span> Rapid decomposition with more dangerous fumes. Essentially impossible in normal cooking but possible with prolonged empty preheating on max heat.</li>
  <li><span class="fact-label">Pet birds</span> Birds have extremely efficient respiratory systems. PTFE fumes that cause mild symptoms in humans can kill a pet bird in minutes. This is well-documented in veterinary literature.</li>
</ul>
<div class="callout callout-danger">
  <strong>The empty pan problem:</strong> An empty non-stick pan on high heat reaches 500\u00b0F+ in just 2\u20133 minutes. Never preheat non-stick pans empty. Always add oil or food before turning on the heat, and keep the burner at medium or below.
</div>"""
            },
            {
                "id": "what-to-do",
                "heading": "Safe Use Guidelines for Non-Stick",
                "content": """<p><strong>Keep heat at medium or below.</strong> Non-stick pans are designed for low-to-medium heat cooking: eggs, crepes, fish, delicate saut\u00e9s.</p>
<p><strong>Never preheat empty.</strong> Add butter, oil, or food to the pan before turning on the burner.</p>
<p><strong>Use wooden, silicone, or nylon utensils.</strong> Metal utensils scratch the coating, creating areas where food sticks and the coating degrades faster.</p>
<p><strong>Replace damaged pans.</strong> If the coating is flaking, peeling, or visibly scratched to the metal, it\u2019s time for a new pan. A damaged coating is less effective and may release particles.</p>
<p><strong>Ventilate your kitchen.</strong> Use a range hood or open a window when cooking, regardless of cookware type.</p>"""
            }
        ],
        "alternatives": [
            {
                "name": "GreenPan Valencia Pro Ceramic Fry Pan",
                "type": "Ceramic Non-Stick",
                "description": "Thermolon ceramic coating derived from sand. Contains zero PTFE, PFOA, or PFAS. Diamond-reinforced for better durability than first-gen ceramic.",
                "pros": "PTFE-free, safe if overheated, lightweight",
                "cons": "Non-stick degrades after 1\u20132 years, less slippery than Teflon when new",
                "asin": "B071JMPFXX"
            },
            {
                "name": "de Buyer Mineral B Carbon Steel Frying Pan",
                "type": "Carbon Steel",
                "description": "Professional-grade French carbon steel that develops a natural non-stick seasoning. Same polymerized-oil approach as cast iron but much lighter.",
                "pros": "Oven-safe to any temperature, improves with use, lighter than cast iron",
                "cons": "Requires seasoning, reacts with acidic foods, not dishwasher safe",
                "asin": "B00462QP1G"
            },
            {
                "name": "Lodge 12-Inch Cast Iron Skillet",
                "type": "Cast Iron",
                "description": "The zero-technology solution: seasoned iron that performs beautifully with zero chemical coatings. Lasts generations.",
                "pros": "Lifetime durability, zero chemicals, adds dietary iron",
                "cons": "Heavy (8 lbs), heats slowly, requires maintenance",
                "asin": "B00006JSUA"
            },
            {
                "name": "All-Clad D3 Stainless Steel Fry Pan",
                "type": "Stainless Steel",
                "description": "For high-heat searing and deglazing that non-stick can\u2019t handle. Tri-ply construction provides even heat without any coating.",
                "pros": "No coatings, oven-safe to 600\u00b0F, dishwasher safe, indestructible",
                "cons": "Not non-stick (requires technique), food sticks without fat",
                "asin": "B00005AL46"
            }
        ],
        "sources": [
            ("EPA &mdash; PFOA Stewardship Program (Phase-out)", "https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/risk-management-and-polyfluoroalkyl-substances-pfas"),
            ("Environmental Science &amp; Technology &mdash; PTFE decomposition products (2001)", "https://pubs.acs.org/journal/esthag"),
            ("Avian and Exotic Animal Clinic &mdash; PTFE toxicosis in birds", "https://www.avianandexotic.com/"),
            ("DuPont &mdash; Teflon Safety Data (Thermal Decomposition Thresholds)", "https://www.chemours.com/en/brands-and-products/teflon"),
        ]
    },

    # ─── 11. Black Plastic Takeout Containers ─────────────────────────
    {
        "slug": "black-plastic-takeout",
        "title": "Black Plastic Takeout Containers: The Hidden Recycling Problem in Your Kitchen",
        "meta_description": "Why black plastic takeout containers may contain flame retardants from recycled electronics and what to use instead for reheating leftovers.",
        "verdict_level": "verdict-caution",
        "verdict_rating": "Use Caution &mdash; May contain recycled electronic waste chemicals",
        "verdict_summary": "Black plastic takeout containers are often made from recycled electronic waste (e-waste) plastics, which can contain brominated flame retardants, heavy metals, and other hazardous chemicals not intended for food contact. A 2019 study found regulated flame retardants in 25% of black kitchen utensils tested. Never microwave food in these containers, and transfer leftovers to glass or ceramic before reheating.",
        "sections": [
            {
                "id": "the-problem",
                "heading": "Why Black Plastic Is Different",
                "content": """<p>Most colored plastics are tinted with conventional pigments. Black plastic is different. <strong>Carbon black pigment</strong> makes the plastic invisible to the near-infrared sensors used in recycling facilities, so it cannot be sorted. This creates a glut of cheap, unsorted black plastic on the recycling market.</p>
<p>The problem: this unsorted stream often includes black plastic from <strong>electronics housings</strong> &mdash; TV casings, computer monitors, printers &mdash; which are treated with <strong>brominated flame retardants (BFRs)</strong>. When this e-waste plastic enters the food packaging supply chain, those flame retardants come with it.</p>"""
            },
            {
                "id": "health-risks",
                "heading": "The Health Risks",
                "content": """<ul class="key-facts">
  <li><span class="fact-label">BFRs found</span> A 2019 University of Plymouth study found brominated flame retardants in 25% of black plastic kitchen utensils purchased at retail.</li>
  <li><span class="fact-label">Heavy metals</span> The same study detected cadmium, lead, and chromium in some black plastic food contact items.</li>
  <li><span class="fact-label">Not food-grade</span> Flame retardants like decaBDE are regulated under the EU&rsquo;s REACH and the Stockholm Convention. They are endocrine disruptors linked to thyroid dysfunction and neurodevelopmental effects.</li>
  <li><span class="fact-label">Heat accelerates</span> Microwaving or heating food in contaminated black plastic increases chemical migration into food significantly.</li>
  <li><span class="fact-label">No labeling</span> There is no requirement to label black plastic with its recycled source material, so consumers cannot tell safe from contaminated by looking at it.</li>
</ul>
<div class="callout callout-warning">
  <strong>The microwave problem:</strong> Takeout containers marked &ldquo;microwave-safe&rdquo; are tested for structural integrity (they won&rsquo;t melt), not for chemical migration. A container that survives the microwave physically may still be leaching harmful compounds into your food.
</div>"""
            },
            {
                "id": "what-to-do",
                "heading": "Simple Precautions",
                "content": """<p><strong>Never microwave black plastic containers.</strong> Transfer food to a glass or ceramic dish before reheating. This is the single most impactful step.</p>
<p><strong>Don&rsquo;t store hot food in them long-term.</strong> If the restaurant packs steaming food into a black plastic tray, transfer it when you get home.</p>
<p><strong>Bring your own containers.</strong> A glass or stainless steel container eliminates the question entirely for regular takeout orders.</p>
<p><strong>Avoid black plastic utensils for cooking.</strong> Spatulas, spoons, and turners that contact hot food directly are a greater exposure risk than storage containers.</p>"""
            }
        ],
        "alternatives": [
            {
                "name": "Pyrex Simply Store Glass Set (10-Piece)",
                "type": "Glass Containers",
                "description": "Tempered glass containers ideal for storing and reheating takeout leftovers. Completely non-reactive at any temperature. Microwave and oven safe.",
                "pros": "Zero chemical migration, microwave safe, see-through for easy ID",
                "cons": "Heavier than plastic, breakable, lids are still plastic",
                "asin": "B09KYGVBCN"
            },
            {
                "name": "LunchBots Stainless Steel Containers",
                "type": "Stainless Steel",
                "description": "18/8 food-grade stainless steel with no coatings. Excellent for packing meals and storing leftovers. Completely inert.",
                "pros": "Virtually indestructible, zero leaching, lightweight vs. glass",
                "cons": "Not microwave-safe, opaque, can dent",
                "asin": "B004WCXFKE"
            },
            {
                "name": "Glasslock Oven-Safe Container Set",
                "type": "Tempered Glass",
                "description": "Snap-lock lids with silicone seals for leak-proof takeout storage. Freezer to oven safe with no thermal shock risk.",
                "pros": "Leak-proof, freezer-to-oven transition, stackable",
                "cons": "Bulkier than disposable containers, heavier for transport",
                "asin": "B007STLBSY"
            },
            {
                "name": "Stasher Reusable Silicone Bags",
                "type": "Platinum Silicone",
                "description": "FDA food-grade platinum-cured silicone bags. Great for storing portioned leftovers. Microwave and dishwasher safe.",
                "pros": "Flexible, microwave safe, replaces zip-lock bags",
                "cons": "Can retain odors, pricier than disposables",
                "asin": "B07C7NHS5Q"
            }
        ],
        "sources": [
            ("University of Plymouth &mdash; BFRs in black plastic kitchen utensils (2019)", "https://www.plymouth.ac.uk/"),
            ("Environment International &mdash; Hazardous substances in recycled plastics", "https://www.sciencedirect.com/journal/environment-international"),
            ("Stockholm Convention &mdash; Brominated Flame Retardants", "http://chm.pops.int/"),
            ("WRAP UK &mdash; Black Plastic Packaging Report", "https://wrap.org.uk/"),
        ]
    },

    # ─── 12. Bamboo Fiber Plates ──────────────────────────────────────
    {
        "slug": "bamboo-fiber-plates",
        "title": "Bamboo Fiber Plates: The &ldquo;Eco-Friendly&rdquo; Dinnerware with a Hidden Problem",
        "meta_description": "Why bamboo fiber plates often contain formaldehyde-melamine resin and can leach chemicals into hot food. Safer eco-friendly alternatives inside.",
        "verdict_level": "verdict-caution",
        "verdict_rating": "Use Caution &mdash; Often bound with formaldehyde-melamine resin",
        "verdict_summary": "Most bamboo fiber dinnerware is not solid bamboo \u2014 it\u2019s bamboo powder mixed with melamine-formaldehyde resin, the same binder used in melamine plates. The German Federal Institute for Risk Assessment (BfR) found that these products leach formaldehyde and melamine into hot food at levels exceeding EU safety limits. Several EU countries have banned their sale. If you want eco-friendly plates, choose solid bamboo, palm leaf, or tempered glass instead.",
        "sections": [
            {
                "id": "the-deception",
                "heading": "What &ldquo;Bamboo Fiber&rdquo; Really Means",
                "content": """<p>When you see a plate marketed as &ldquo;bamboo fiber,&rdquo; &ldquo;bamboo composite,&rdquo; or &ldquo;eco-friendly bamboo,&rdquo; it almost never means the plate is made from solid bamboo. Instead, it&rsquo;s <strong>bamboo powder or fiber</strong> mixed with a <strong>melamine-formaldehyde resin binder</strong> that holds the particles together and gives the plate its rigid, smooth finish.</p>
<p>This creates a cruel irony: consumers choosing bamboo plates to avoid plastic are getting a product that is <strong>majority plastic resin by weight</strong>, with the same chemical leaching concerns as melamine dinnerware \u2014 and often worse, because the bamboo fibers can degrade the resin matrix faster.</p>"""
            },
            {
                "id": "health-risks",
                "heading": "The Health Risks",
                "content": """<ul class="key-facts">
  <li><span class="fact-label">BfR testing</span> The German Federal Institute for Risk Assessment found formaldehyde migration 5&ndash;8x above the EU specific migration limit (SML) of 15 mg/kg in bamboo-melamine products tested with hot liquids.</li>
  <li><span class="fact-label">Melamine</span> Migration of melamine from these products also exceeded the EU SML of 2.5 mg/kg in the same tests.</li>
  <li><span class="fact-label">EU ban</span> Multiple EU countries (Belgium, Luxembourg, Netherlands, Austria) have banned the sale of bamboo-melamine food contact products.</li>
  <li><span class="fact-label">Formaldehyde</span> Classified as a Group 1 carcinogen by IARC. Chronic low-level exposure causes respiratory irritation and is linked to nasopharyngeal cancer.</li>
  <li><span class="fact-label">Degradation</span> The bamboo fibers absorb moisture and swell, cracking the resin matrix over time. Older, worn bamboo-composite plates leach more than new ones.</li>
</ul>
<div class="callout callout-danger">
  <strong>The hot liquid trigger:</strong> Like melamine, the leaching from bamboo-composite plates is heavily temperature-dependent. Pouring hot coffee, tea, or soup into these products causes the highest chemical migration. Never use them for hot foods or beverages.
</div>"""
            },
            {
                "id": "what-to-do",
                "heading": "How to Identify and Avoid Risky Products",
                "content": """<p><strong>Read the fine print.</strong> If the product description mentions &ldquo;bamboo powder,&rdquo; &ldquo;bamboo fiber,&rdquo; or &ldquo;bamboo composite,&rdquo; it contains resin binder. Genuine bamboo products are made from solid bamboo pieces, not powder.</p>
<p><strong>Avoid for hot food and drinks.</strong> If you already own bamboo-composite plates, use them only for cold, dry foods (crackers, fruit, sandwiches).</p>
<p><strong>Don&rsquo;t microwave or dishwasher-wash them.</strong> Both heat sources accelerate resin breakdown and chemical migration.</p>
<p><strong>Choose genuinely eco-friendly alternatives.</strong> Palm leaf plates, solid bamboo, or tempered glass are all better choices for the environment and your health.</p>"""
            }
        ],
        "alternatives": [
            {
                "name": "Fallen Leaf Palm Leaf Plates (25-Pack)",
                "type": "Palm Leaf",
                "description": "Made from naturally fallen areca palm leaves \u2014 no binders, resins, or chemicals. Fully compostable and sturdy enough for hot food.",
                "pros": "100% natural, compostable, handles hot food safely, no chemicals",
                "cons": "Disposable (single-use), limited shapes, natural color variation",
                "asin": "B0CHKP8XFG"
            },
            {
                "name": "Corelle Vitrelle Glass Dinnerware Set",
                "type": "Tempered Glass",
                "description": "Triple-layer Vitrelle glass that\u2019s ultra-thin and break-resistant. Microwave, oven, and dishwasher safe with zero chemical leaching.",
                "pros": "Lightweight, nearly unbreakable, completely non-reactive, lasts decades",
                "cons": "Not compostable (but lasts so long it offsets environmental cost)",
                "asin": "B0C1QNSVY8"
            },
            {
                "name": "Bambu Veneerware Disposable Bamboo Plates",
                "type": "Solid Bamboo Veneer",
                "description": "Made from a single sheet of solid bamboo veneer \u2014 no powders, resins, or melamine. Certified organic and compostable.",
                "pros": "Genuinely bamboo (no resin), compostable, attractive grain pattern",
                "cons": "Single-use, more expensive than palm leaf, limited heat tolerance",
                "asin": "B001BKRSW0"
            },
            {
                "name": "Kangovou Stainless Steel Kids\u2019 Plate Set",
                "type": "Stainless Steel",
                "description": "18/8 stainless steel divided plates. Truly unbreakable, zero chemical risk, and dishwasher safe. Great for families wanting durability.",
                "pros": "Indestructible, zero leaching, dishwasher safe, reusable for life",
                "cons": "Not compostable, metallic appearance, not microwave safe",
                "asin": "B00E6PUTQI"
            }
        ],
        "sources": [
            ("BfR &mdash; Release of melamine and formaldehyde from bamboo tableware (2020)", "https://www.bfr.bund.de/en/"),
            ("European Commission RASFF &mdash; Notifications on bamboo-melamine products", "https://webgate.ec.europa.eu/rasff-window/"),
            ("IARC &mdash; Formaldehyde Classification (Group 1)", "https://monographs.iarc.who.int/"),
            ("Belgian Federal Agency for the Safety of the Food Chain &mdash; Bamboo ware ban", "https://www.favv-afsca.be/"),
        ]
    },
]


# ── HTML Template ──────────────────────────────────────────────────────────

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
        <a href="{link}" class="alt-link" rel="sponsored nofollow" target="_blank">View on Amazon</a>
      </div>""")
    return "\n".join(cards)


def build_sources(sources):
    """Build numbered source list."""
    items = []
    for i, (title, url) in enumerate(sources, 1):
        items.append(f'        <li>{title} &mdash; <a href="{url}" target="_blank" rel="noopener">{url}</a></li>')
    return "\n".join(items)


def plain_text(html_str):
    """Strip HTML entities for use in JSON-LD and meta tags."""
    return unescape(html_str).replace('"', '&quot;')


def generate_article(article):
    """Generate complete HTML for one article."""
    toc = build_toc(article["sections"])
    body = build_sections(article["sections"])
    alternatives = build_alternatives(article["alternatives"], AFFILIATE_TAG)
    sources = build_sources(article["sources"])
    today = date.today().isoformat()
    slug = article["slug"]
    canonical = f"{SITE_URL}/kitchen/{slug}.html"
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
  {{
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
  }}
  </script>

  <link rel="icon" href="../favicon.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="{CSS_PATH}" />
</head>
<body>

  <nav><a href="../index.html">&larr; {SITE_NAME}</a></nav>

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
  </article>

  <footer>
    <p>&copy; 2026 {SITE_NAME}</p>
  </footer>

</body>
</html>
"""


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    generated = []
    for article in ARTICLES:
        filename = f"{article['slug']}.html"
        filepath = OUTPUT_DIR / filename
        html = generate_article(article)
        filepath.write_text(html, encoding="utf-8")
        generated.append((article["slug"], article["title"]))
        print(f"  Generated: kitchen/{filename}")

    print(f"\nDone. {len(generated)} articles written to {OUTPUT_DIR}/")

    # Write a simple index for the kitchen category
    links = "\n".join(
        f'        <li><a href="{slug}.html">{title}</a></li>'
        for slug, title in generated
    )
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Kitchen &amp; Dining Safety &mdash; {SITE_NAME}</title>
  <meta name="description" content="Science-backed safety guides for kitchen materials — PFAS, BPA, Teflon, melamine, and more. Learn what's safe and find better alternatives." />
  <link rel="icon" href="../favicon.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="{CSS_PATH}" />
</head>
<body>

  <nav><a href="../index.html">&larr; {SITE_NAME}</a></nav>

  <div class="category-header">
    <h1>Kitchen &amp; Dining Safety</h1>
    <p>Science-backed guides to the materials that touch your food every day.</p>
  </div>

  <main>
    <ul>
{links}
    </ul>
  </main>

  <footer>
    <p>&copy; 2026 {SITE_NAME}</p>
  </footer>

</body>
</html>
"""
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  Generated: kitchen/index.html (category page)")

    # ── Sitemap ──
    update_sitemap(generated)


def update_sitemap(generated_articles):
    """Rebuild sitemap.xml with all known pages."""
    today = date.today().isoformat()

    # Static pages
    urls = [
        (f"{SITE_URL}/", "1.0"),
        (f"{SITE_URL}/kitchen/", "0.8"),
    ]
    # Article pages
    for slug, _title in generated_articles:
        urls.append((f"{SITE_URL}/kitchen/{slug}.html", "0.9"))

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


if __name__ == "__main__":
    main()
