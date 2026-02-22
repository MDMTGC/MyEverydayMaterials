"""Outdoor & Garden article data for MyEverydayMaterials generator."""

RELATED_MAP = {
    "pressure-treated-lumber": ["deck-sealants", "chemical-pesticides"],
    "deck-sealants": ["pressure-treated-lumber", "chemical-pesticides"],
    "chemical-pesticides": ["pressure-treated-lumber", "deck-sealants"],
}

ARTICLES = [
    {
        "slug": "pressure-treated-lumber",
        "title": "Pressure-Treated Lumber: Arsenic Legacy, Modern Risks, and Safer Builds",
        "meta_description": "Learn the real safety risks of pressure-treated lumber, including older CCA arsenic wood and safer options for decks and raised beds.",
        "verdict_level": "verdict-caution",
        "verdict_rating": "Use with Caution — especially for older CCA wood",
        "verdict_summary": "Older pressure-treated wood may contain arsenic (CCA) and should be handled carefully. Newer treatments are safer but still require dust control, sealing, and proper disposal.",
        "sections": [
            {
                "id": "what-it-is",
                "heading": "What It Is",
                "content": """<p>Pressure-treated lumber is wood infused with preservatives to resist rot and insects. Older stock often used <strong>chromated copper arsenate (CCA)</strong>, while newer products use formulations like ACQ or copper azole.</p>""",
            },
            {
                "id": "risk-breakdown",
                "heading": "Risk Breakdown",
                "content": """<p>CCA-treated wood can transfer arsenic residues to skin and surrounding soil, and cutting creates contaminated dust. The EPA phase-out for most residential uses reduced new CCA exposure, but many existing decks and structures remain in service.</p>
<p>Newer treated wood removes arsenic concerns, but still contains biocides and should not be burned or used where food contact is likely.</p>""",
            },
            {
                "id": "what-to-do",
                "heading": "What You Can Do Right Now",
                "content": """<ul class=\"key-facts\">
  <li>Seal exterior treated wood regularly to reduce leaching.</li>
  <li>Wear gloves and a dust mask when cutting or sanding.</li>
  <li>Wash hands and work clothes after handling.</li>
  <li>Never burn treated wood scraps.</li>
</ul>""",
            },
        ],
        "alternatives": [
            {
                "name": "Food-Safe Cedar for Raised Beds",
                "type": "Material Swap",
                "description": "Naturally durable cedar is a common alternative where food contact is a concern.",
                "pros": "No pressure-treatment preservatives",
                "cons": "Higher cost and periodic maintenance",
                "url": "https://www.amazon.com/s?k=Food-Safe+Cedar+for+Raised+Beds&tag=myeverydaymat-20",
            },
            {
                "name": "Composite Deck Boards",
                "type": "Low-Maintenance Option",
                "description": "Composite boards avoid preservative chemistry and can reduce splintering.",
                "pros": "No arsenic legacy risk",
                "cons": "Heat retention and upfront cost",
                "url": "https://www.amazon.com/s?k=Composite+Deck+Boards&tag=myeverydaymat-20",
            },
        ],
        "sources": [
            ("US EPA: Chromated Arsenicals (CCA)", "https://www.epa.gov/ingredients-used-pesticide-products/chromated-arsenicals-cca"),
            ("NPIC FAQ: CCA-treated wood", "https://npic.orst.edu/faq/cca.html"),
        ],
    },
    {
        "slug": "deck-sealants",
        "title": "Deck Sealants and VOCs: How to Cut Fumes Without Sacrificing Protection",
        "meta_description": "Many deck sealants emit VOCs. Compare oil-based and water-based formulas and choose lower-emission options for safer outdoor projects.",
        "verdict_level": "verdict-caution",
        "verdict_rating": "Prefer Low-VOC Formulas",
        "verdict_summary": "Oil-based sealants can emit high VOC levels during application and curing. Water-based low-VOC products are usually a safer choice for routine projects.",
        "sections": [
            {
                "id": "why-vocs-matter",
                "heading": "Why VOCs Matter",
                "content": """<p>Volatile organic compounds (VOCs) evaporate into air during application and drying. Short-term exposure can irritate eyes and airways and trigger headaches, especially in poorly ventilated spaces.</p>""",
            },
            {
                "id": "product-differences",
                "heading": "Oil-Based vs Water-Based",
                "content": """<p>Oil-based products often provide deep penetration but usually carry more solvent load. Water-based sealants generally dry faster, clean up with soap and water, and can significantly reduce VOC emissions.</p>""",
            },
            {
                "id": "practical-steps",
                "heading": "Practical Steps",
                "content": """<ul class=\"key-facts\">
  <li>Choose products labeled low-VOC or zero-VOC.</li>
  <li>Apply outdoors in dry weather with airflow.</li>
  <li>Store and dispose of oily rags safely to avoid fire risk.</li>
</ul>""",
            },
        ],
        "alternatives": [
            {
                "name": "Water-Based Low-VOC Deck Sealer",
                "type": "Lower-Emission Coating",
                "description": "Good protection profile with lower solvent odor and easier cleanup.",
                "pros": "Lower VOC burden",
                "cons": "May need more frequent recoat",
                "url": "https://www.amazon.com/s?k=Water-Based+Low-VOC+Deck+Sealer&tag=myeverydaymat-20",
            },
            {
                "name": "Plant-Oil Exterior Finish",
                "type": "Natural-Finish Option",
                "description": "Plant-oil products can reduce synthetic solvent exposure when used correctly.",
                "pros": "Often simpler ingredient profile",
                "cons": "Requires careful rag handling",
                "url": "https://www.amazon.com/s?k=Plant-Oil+Exterior+Finish&tag=myeverydaymat-20",
            },
        ],
        "sources": [
            ("US EPA: VOCs and indoor air quality", "https://www.epa.gov/indoor-air-quality-iaq/volatile-organic-compounds-impact-indoor-air-quality"),
            ("Green Seal guide to VOCs", "https://greenseal.org/guide-to-vocs-in-paint-and-cleaning-products/"),
        ],
    },
    {
        "slug": "chemical-pesticides",
        "title": "Glyphosate and Neonicotinoids: What Home Gardeners Should Know",
        "meta_description": "Evidence-based overview of glyphosate and neonicotinoid concerns, with practical integrated pest management alternatives for home gardens.",
        "verdict_level": "verdict-caution",
        "verdict_rating": "Reduce Routine Use",
        "verdict_summary": "Both glyphosate and neonicotinoids remain controversial. For household use, minimizing routine application and prioritizing integrated pest management is a safer default.",
        "sections": [
            {
                "id": "core-concerns",
                "heading": "Core Concerns",
                "content": """<p>Glyphosate has conflicting regulatory conclusions and ongoing scientific debate about long-term risk. Neonicotinoids are strongly linked to pollinator harm and aquatic ecosystem impacts.</p>""",
            },
            {
                "id": "why-home-use-matters",
                "heading": "Why Home Use Still Matters",
                "content": """<p>Even non-farm use contributes to cumulative local exposure. Overspray, runoff, and repeated spot treatments can affect children, pets, and beneficial insects in residential areas.</p>""",
            },
            {
                "id": "lower-risk-strategy",
                "heading": "Lower-Risk Strategy",
                "content": """<ul class=\"key-facts\">
  <li>Use mechanical weeding and mulching first.</li>
  <li>Spot-treat only when needed instead of blanket spraying.</li>
  <li>Encourage beneficial insects and native plant diversity.</li>
</ul>""",
            },
        ],
        "alternatives": [
            {
                "name": "Weed Barrier + Mulch System",
                "type": "Non-Chemical Control",
                "description": "Physical suppression of weeds reduces need for herbicide reapplication.",
                "pros": "No pesticide drift",
                "cons": "Labor and seasonal upkeep",
                "url": "https://www.amazon.com/s?k=Weed+Barrier+%2B+Mulch+System&tag=myeverydaymat-20",
            },
            {
                "name": "Manual Stand-Up Weeder",
                "type": "Mechanical Removal",
                "description": "Root-level removal tool for regular maintenance without sprays.",
                "pros": "Immediate, targeted control",
                "cons": "Best for smaller areas",
                "url": "https://www.amazon.com/s?k=Manual+Stand-Up+Weeder&tag=myeverydaymat-20",
            },
        ],
        "sources": [
            ("IARC: Glyphosate Monograph summary", "https://www.iarc.who.int/featured-news/media-centre-iarc-news-glyphosate/"),
            ("Environmental risks of neonicotinoids", "https://pubs.acs.org/doi/10.1021/acs.est.7b06388"),
        ],
    },
]
