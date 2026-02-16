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
                "asin": "B0C4M7R2X1",
            },
            {
                "name": "Composite Deck Boards",
                "type": "Low-Maintenance Option",
                "description": "Composite boards avoid preservative chemistry and can reduce splintering.",
                "pros": "No arsenic legacy risk",
                "cons": "Heat retention and upfront cost",
                "asin": "B0BZT8L4M2",
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
                "asin": "B0C2K9P8J5",
            },
            {
                "name": "Plant-Oil Exterior Finish",
                "type": "Natural-Finish Option",
                "description": "Plant-oil products can reduce synthetic solvent exposure when used correctly.",
                "pros": "Often simpler ingredient profile",
                "cons": "Requires careful rag handling",
                "asin": "B0BN7N5QF3",
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
                "asin": "B09ZK8R6Y4",
            },
            {
                "name": "Manual Stand-Up Weeder",
                "type": "Mechanical Removal",
                "description": "Root-level removal tool for regular maintenance without sprays.",
                "pros": "Immediate, targeted control",
                "cons": "Best for smaller areas",
                "asin": "B07NQ5W3L8",
            },
        ],
        "sources": [
            ("IARC: Glyphosate Monograph summary", "https://www.iarc.who.int/featured-news/media-centre-iarc-news-glyphosate/"),
            ("Environmental risks of neonicotinoids", "https://pubs.acs.org/doi/10.1021/acs.est.7b06388"),
        ],
    },
]
"rubber-mulch": {
        "title": "Tire Crumb & Heavy Metals in Rubber Mulch",
        "verdict": "AVOID — Made from recycled tires, this material can leach lead, zinc, and PAHs into the soil and off-gas VOCs in high heat.",
        "content": """
<h3>The Origin of Rubber Mulch</h3>
Rubber mulch is primarily produced from pulverized scrap tires. While marketed as an eco-friendly recycling solution, tires are complex chemical mixtures not originally intended for close human or environmental contact.

<h3>The Health Risks (The Deep Dive)</h3>
<ul>
    <li><strong>Heavy Metal Leaching:</strong> Tires contain high concentrations of **Zinc** (used in vulcanization) and can contain trace amounts of **Lead** and **Cadmium**. These metals can leach into the soil, impacting plant health and soil-dwelling organisms.</li>
    <li><strong>Polycyclic Aromatic Hydrocarbons (PAHs):</strong> PAHs are a group of chemicals naturally found in coal, crude oil, and gasoline—all used in tire manufacturing. Several PAHs are classified as known or probable human carcinogens.</li>
    <li><strong>Heat and Off-gassing:</strong> On hot summer days, rubber mulch can reach temperatures 30-50°F higher than the ambient air, significantly accelerating the off-gassing of Volatile Organic Compounds (VOCs) that create a distinct "tire smell."</li>
</ul>

<h3>What You Can Do Right Now</h3>
<ul>
    <li><strong>Check the Application:</strong> Never use rubber mulch in vegetable gardens or near fruit trees where heavy metals could be taken up by the roots.</li>
    <li><strong>Wear Gloves:</strong> If you must handle rubber mulch, wear thick gardening gloves to prevent the transfer of carbon black and chemical residues to your skin.</li>
</ul>

<h3>Better Alternatives</h3>
Use **Cedar or Cypress Mulch**, which provides natural pest resistance and moisture retention without the chemical profile of industrial rubber.
""",
        "sources": [
            {"title": "Chemicals in Recycled Tires", "org": "EPA", "url": "https://www.epa.gov/tire-tokens"},
            {"title": "Rubber Mulch Safety", "org": "Healthy Building Network", "url": "https://healthybuilding.net"}
        ]
    },

    "pvc-garden-hoses": {
        "title": "Lead and Phthalates in PVC Garden Hoses",
        "verdict": "CAUTION — Standard green PVC hoses often contain lead stabilizers and phthalates; never drink from a hose unless it is labeled 'Potable Water Safe'.",
        "content": """
<h3>Why Hoses Are Toxic</h3>
Most garden hoses are made of Polyvinyl Chloride (PVC). To make the plastic flexible and UV-resistant, manufacturers add phthalates and often use lead as a stabilizer.

<h3>The Health Risks (The Deep Dive)</h3>
<ul>
    <li><strong>Leaching into Water:</strong> When a hose sits in the sun, the water inside can reach high temperatures, causing chemicals to leach out of the PVC walls. Testing by the <i>Ecology Center</i> found lead levels in "hose water" that exceeded federal drinking water standards by up to 100 times.</li>
    <li><strong>Organ Toxicity:</strong> Phthalates are known endocrine disruptors. When you water your garden with a PVC hose, these chemicals can settle on the surface of your vegetables.</li>
</ul>

<h3>What You Can Do Right Now</h3>
<ul>
    <li><strong>Flush the Line:</strong> Let the water run for at least 30-60 seconds before using it to water plants or fill a pet bowl. This flushes out the water that has been sitting in contact with the hose walls.</li>
</ul>

<h3>Better Alternatives</h3>
Look for hoses made of **Polyurethane** or **Natural Rubber** that are explicitly labeled **"Drinking Water Safe"** and **"Lead-Free."**
""",
        "sources": [
            {"title": "Garden Hose Study", "org": "Ecology Center / HealthyStuff.org", "url": "https://www.ecocenter.org/"},
            {"title": "Lead in Consumer Products", "org": "CPSC", "url": "https://www.cpsc.gov"}
        ]
    },

    "deet-repellents": {
        "title": "DEET and Neurotoxicity in Insect Repellents",
        "verdict": "CAUTION — Highly effective but a potent solvent that can cause skin irritation and, in rare cases, neurological symptoms if overused.",
        "content": """
<h3>The Gold Standard of Repellents</h3>
DEET (N,N-Diethyl-meta-toluamide) has been used since 1946. It is a powerful solvent capable of melting certain plastics and synthetic fabrics.

<h3>The Health Risks (The Deep Dive)</h3>
<ul>
    <li><strong>Dermal Absorption:</strong> Approximately 10-15% of topically applied DEET is absorbed through the skin into the bloodstream.</li>
    <li><strong>Neurological Impact:</strong> While rare, high-dose exposure to DEET has been linked to seizures, tremors, and slurred speech, particularly in children. It is believed to inhibit acetylcholinesterase, an enzyme essential for proper nerve function.</li>
</ul>

<h3>What You Can Do Right Now</h3>
<ul>
    <li><strong>Concentration Matters:</strong> A 30% concentration of DEET is as effective as a 100% concentration, it just lasts for a shorter duration. Avoid 100% DEET products for casual use.</li>
    <li><strong>Spray Clothes, Not Skin:</strong> Apply repellent to the outside of your clothing to reduce direct skin absorption.</li>
</ul>
""",
        "sources": [
            {"title": "DEET General Fact Sheet", "org": "NPIC", "url": "http://npic.orst.edu/factsheets/DEETgen.html"},
            {"title": "Repellent Safety", "org": "CDC", "url": "https://www.cdc.gov"}
        ]
    }
}
"pool-disinfection-byproducts": {
        "title": "Chloramines & Disinfection Byproducts (DBPs) in Pools",
        "verdict": "CAUTION — Chlorine reacting with organic matter creates chloramines, which are potent respiratory irritants and possible carcinogens.",
        "content": """
<h3>The Chemistry of Pool Water</h3>
Chlorine is a highly effective disinfectant, but its safety profile changes when it interacts with organic matter (sweat, skin cells, and nitrogenous waste) to form **Disinfection Byproducts (DBPs)**, specifically trihalomethanes (THMs) and chloramines.

<h3>The Health Risks (The Deep Dive)</h3>
<ul>
    <li><strong>Respiratory Irritation:</strong> That "pool smell" is actually the scent of chloramines. Inhaling these at the water's surface is a primary trigger for "Lifeguard Lung" and can exacerbate exercise-induced asthma in children.</li>
    <li><strong>Genotoxicity:</strong> Research indicates that long-term exposure to certain THMs through skin absorption and inhalation can lead to DNA damage and is associated with an increased risk of bladder cancer.</li>
    <li><strong>Skin Barrier Disruption:</strong> High chlorine levels strip the skin’s natural lipids, leading to "swimmer's itch" and chronic xerosis (dry skin).</li>
</ul>

<h3>What You Can Do Right Now</h3>
<ul>
    <li><strong>The Pre-Swim Shower:</strong> A 60-second rinse before entering the pool removes the majority of organic precursors, significantly reducing the formation of toxic chloramines.</li>
    <li><strong>Ventilation is Key:</strong> If using an indoor or covered pool, ensure high-capacity airflow at the water's surface to disperse gasses.</li>
</ul>

<h3>Better Alternatives</h3>
Consider a **Saltwater Bromine** system or **UV/Ozone** sanitation, which allows for significantly lower baseline chlorine levels while maintaining superior pathogen control.
""",
        "sources": [
            {"title": "Disinfection Byproducts in Swimming Pools", "org": "CDC", "url": "https://www.cdc.gov/healthywater/swimming/oceans-lakes-rivers/disinfection-byproducts.html"},
            {"title": "Health Effects of Pool Chemicals", "org": "WHO", "url": "https://www.who.int/"}
        ]
    },

    "small-engine-exhaust": {
        "title": "Benzene & Particulates in Small Engine Exhaust",
        "verdict": "CAUTION — Gas-powered lawn mowers and leaf blowers lack the catalytic converters of cars, emitting high levels of VOCs and fine particulate matter.",
        "content": """
<h3>Unregulated Emissions</h3>
Small two-stroke engines (common in weed eaters and leaf blowers) are significantly dirtier than modern car engines. Operating a gas leaf blower for one hour can emit as much smog-forming pollution as driving a passenger car for 1,100 miles.

<h3>The Health Risks (The Deep Dive)</h3>
<ul>
    <li><strong>Benzene Exposure:</strong> Small engine fuel and exhaust contain **Benzene**, a known human carcinogen. Inhalation during refueling or operation can lead to immediate dizziness and long-term hematological issues.</li>
    <li><strong>Carbon Monoxide (CO):</strong> In partially enclosed spaces like carports or sheds, CO levels from a running mower can reach toxic levels in minutes, interfering with oxygen transport in the blood.</li>
    <li><strong>Fine Particulate (PM2.5):</strong> The incomplete combustion in small engines creates microscopic soot that enters the bloodstream via the lungs, contributing to systemic inflammation.</li>
</ul>

<h3>What You Can Do Right Now</h3>
<ul>
    <li><strong>Upwind Operation:</strong> Always stand upwind of the engine exhaust while working.</li>
    <li><strong>Ditch the Two-Stroke:</strong> If you use gas, switch to **Four-Stroke** engines which are marginally cleaner and do not require mixing oil and gas.</li>
</ul>

<h3>Better Alternatives</h3>
Switch to **Electric/Battery-Powered** lawn tools. Modern lithium-ion tech provides comparable power with zero point-of-use emissions and 50% less noise pollution.
""",
        "sources": [
            {"title": "Small Engine Emissions", "org": "EPA", "url": "https://www.epa.gov/moves/small-engine-and-nonroad-emissions"},
            {"title": "Benzene Toxicity", "org": "ATSDR", "url": "https://www.atsdr.cdc.gov/"}
        ]
    },

    "synthetic-fertilizer-nitrates": {
        "title": "Nitrates & Synthetic Nutrients in Lawn Care",
        "verdict": "CAUTION — Highly soluble synthetic fertilizers can leach into groundwater and contribute to toxic algal blooms; use slow-release organic options.",
        "content": """
<h3>The Nutrient Overload</h3>
Synthetic fertilizers utilize fast-acting salts like **Ammonium Nitrate** and **Urea**. While they provide a "green spike," they are easily washed away by rain or over-irrigation.

<h3>The Health Risks (The Deep Dive)</h3>
<ul>
    <li><strong>Groundwater Contamination:</strong> Excessive nitrate runoff enters the water table. High nitrate levels in drinking water are linked to "Blue Baby Syndrome" (methemoglobinemia) and may be associated with thyroid dysfunction.</li>
    <li><strong>Soil Microbiome Depletion:</strong> High-salt synthetic fertilizers can kill beneficial soil microbes and earthworms, creating a "dependency loop" where the lawn requires more chemicals to stay green.</li>
</ul>

<h3>What You Can Do Right Now</h3>
<ul>
    <li><strong>Sweep the Hardscape:</strong> Always sweep fertilizer granules off sidewalks and driveways back onto the grass to prevent direct runoff into storm drains.</li>
</ul>
""",
        "sources": [
            {"title": "Nitrates in Drinking Water", "org": "EPA", "url": "https://www.epa.gov/ground-water-and-drinking-water"},
            {"title": "Environmental Impact of Fertilizers", "org": "USDA", "url": "https://www.usda.gov/"}
        ]
    },

    "charcoal-grill-pah": {
        "title": "PAHs & Carbon Monoxide in Charcoal Grilling",
        "verdict": "CAUTION — Fat dripping on hot coals creates Polycyclic Aromatic Hydrocarbons (PAHs) that coat food; avoid petroleum-based lighter fluids.",
        "content": """
<h3>Combustion Chemistry</h3>
Charcoal grilling involves the incomplete combustion of organic matter, which releases a variety of hazardous gasses and particulates.

<h3>The Health Risks (The Deep Dive)</h3>
<ul>
    <li><strong>PAH Formation:</strong> When meat fat drips onto glowing coals, it vaporizes into **Polycyclic Aromatic Hydrocarbons (PAHs)**. These rise with the smoke and deposit onto the surface of the food. Many PAHs are known mutagens and carcinogens.</li>
    <li><strong>Lighter Fluid VOCs:</strong> Petroleum-based lighter fluids contain volatile hydrocarbons that can leave chemical residues on food and contribute to localized ozone formation.</li>
</ul>

<h3>What You Can Do Right Now</h3>
<ul>
    <li><strong>Use a Chimney Starter:</strong> Eliminate the need for lighter fluid entirely by using a charcoal chimney starter and paper.</li>
    <li><strong>Leaner Cuts:</strong> Using leaner meats reduces the amount of fat dripping on the coals, significantly lowering PAH levels in your food.</li>
</ul>
""",
        "sources": [
            {"title": "Chemicals in Meat Cooked at High Temperatures", "org": "National Cancer Institute", "url": "https://www.cancer.gov/about-cancer/causes-prevention/risk/diet/cooked-meats-fact-sheet"},
            {"title": "PAHs and Health", "org": "WHO", "url": "https://www.who.int/"}
        ]
    }
}
