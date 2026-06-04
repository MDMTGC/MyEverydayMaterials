import os
import re

# Define paths
WORKSPACE_DIR = r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials"
ARTICLES_DIR = os.path.join(WORKSPACE_DIR, "articles")

# 1. Replacements for articles/kitchen.py
kitchen_file = os.path.join(ARTICLES_DIR, "kitchen.py")
kitchen_replacements = [
    ("https://www.cdc.gov/biomonitoring/BisphenolA_FactSheet.html", "https://www.cdc.gov/biomonitoring/pdf/BisphenolA_FactSheet.pdf"),
    ("https://echa.europa.eu/", "https://echa.europa.eu/hot-topics/phthalates"),
    ("https://www.fda.gov/food/food-ingredients-packaging", "https://www.fda.gov/food/food-ingredients-packaging/phthalates-food-packaging-and-food-contact-applications"),
    ("https://jamanetwork.com/journals/jamainternalmedicine", "https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/1557876"),
    ("https://www.who.int/publications/i/item/9789241546553", "https://www.who.int/publications-detail-redirect/9789241546553"),
    ("https://monographs.iarc.who.int/news-events/iarc-monographs-volume-131-cobalt-antimony-compounds-and-weapons-grade-tungsten-alloy/", "https://publications.iarc.fr/618"),
    (
        '[\n                "German Federal Institute for Risk Assessment &mdash; Silicone bakeware (2018)",\n                "https://www.bfr.bund.de/en/"\n            ]',
        '[\n                "German Federal Institute for Risk Assessment &mdash; Silicone bakeware (2018)",\n                "https://www.bfr.bund.de/cm/349/silicone_moulds_for_baking.pdf"\n            ]'
    ),
    (
        '[\n                "BfR &mdash; Release of melamine and formaldehyde from bamboo tableware (2020)",\n                "https://www.bfr.bund.de/en/"\n            ]',
        '[\n                "BfR &mdash; Release of melamine and formaldehyde from bamboo tableware (2020)",\n                "https://www.bfr.bund.de/cm/349/bamboo-melamine-tableware-frequent-use-can-be-harmful-to-health.pdf"\n            ]'
    )
]

# 2. Replacements for articles/nursery.py
nursery_file = os.path.join(ARTICLES_DIR, "nursery.py")
nursery_replacements = [
    (
        '[\n                "FDA: Cosmetics Q&A: Preservatives",\n                "https://www.fda.gov/cosmetics/resources-consumers-cosmetics/cosmetics-qa-preservatives"\n            ]',
        '[\n                "FDA: Parabens in Cosmetics",\n                "https://www.fda.gov/cosmetics/cosmetic-ingredients/parabens-cosmetics"\n            ]'
    ),
    ("https://www.aad.org/public/diseases/eczema/types/contact-dermatitis/causes-children", "https://www.aad.org/public/diseases/eczema/types/contact-dermatitis"),
    (
        '[\n                "FDA: Melamine in Food Contact Substances",\n                "https://www.fda.gov/food/packaging-food-contact-substances-fcs/melamine-food-contact-substances"\n            ]',
        '[\n                "FDA: Melamine in Tableware",\n                "https://www.fda.gov/food/chemicals/melamine-tableware"\n            ]'
    ),
    (
        '[\n                "EPA: Formaldehyde Hazard Summary",\n                "https://www.epa.gov/iris/basic-information-about-formaldehyde-inhalation-reference-concentration"\n            ]',
        '[\n                "EPA: Formaldehyde IRIS Chemical Assessment Summary",\n                "https://cfpub.epa.gov/ncea/iris2/chemicalLanding.cfm?substance_nmbr=419"\n            ]'
    ),
    (
        '[\n                "European Food Safety Authority (EFSA): Melamine in food and feed",\n                "https://www.efsa.europa.eu/en/topics/topic/melamine-food-and-feed"\n            ]',
        '[\n                "European Food Safety Authority (EFSA): Melamine",\n                "https://www.efsa.europa.eu/en/topics/topic/melamine"\n            ]'
    ),
    ("https://www.ecocenter.org/healthy-stuff/healthy-car-seats/", "https://www.ecocenter.org/toxic-inequities-2022-car-seat-report"),
    ("https://www.niehs.nih.gov/research/supported/assets/docs/d_g/childrens_exposure_to_flame_retardants_in_the_car_environment_508.pdf", "https://www.niehs.nih.gov/health/topics/agents/flame_retardants"),
    ("https://www.atsdr.cdc.gov/sites/KIDS/documents/flame_retardants.pdf", "https://www.atsdr.cdc.gov/toxfaqs/index.html"),
    ("https://www.cdc.gov/niosh/topics/fibreglass/default.html", "https://www.cdc.gov/niosh/topics/fibreglass/"),
    ("https://www.healthychildren.org/English/ages-stages/baby/preemie/Pages/Choosing-a-Pacifier-for-Your-Preemie.aspx", "https://www.healthychildren.org/English/ages-stages/baby/crying-colic/Pages/Pacifiers-Satisfying-Your-Babys-Needs.aspx"),
    ("https://www.fda.gov/food/chemicals/melamine-safety", "https://www.fda.gov/food/chemicals/melamine-tableware"),
    (
        '[\n                "An Update on Phthalates and Child Health",\n                "https://ehp.niehs.nih.gov/doi/10.1289/ehp.1408822"\n            ]',
        '[\n                "Phthalate Exposure and Children\'s Health: An Update",\n                "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8157593/"\n            ]'
    ),
    (
        '[\n                "What Are Phthalates? (US EPA)",\n                "https://www.epa.gov/assessing-and-managing-chemicals/what-are-phthalates"\n            ]',
        '[\n                "Phthalates (US EPA)",\n                "https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/phthalates"\n            ]'
    ),
    (
        '[\n                "Endocrine Disrupting Chemicals (EDCs) (WHO/UNEP)",\n                "https://www.who.int/news-room/fact-sheets/detail/endocrine-disrupting-chemicals-(edcs)"\n            ]',
        '[\n                "Endocrine Disrupting Chemicals (EDCs) (WHO)",\n                "https://www.who.int/health-topics/endocrine-disrupting-chemicals"\n            ]'
    ),
    (
        '[\n                "Talcum Powder and Asbestos: Frequently Asked Questions - FDA",\n                "https://www.fda.gov/consumers/consumer-updates/talcum-powder-and-asbestos-frequently-asked-questions"\n            ]',
        '[\n                "Talc and Asbestos in Cosmetics - FDA",\n                "https://www.fda.gov/cosmetics/cosmetic-ingredients/talc"\n            ]'
    ),
    ("https://www.cdc.gov/niosh/topics/asbestos/default.html", "https://www.cdc.gov/niosh/topics/asbestos/"),
    ("https://www.fda.gov/food/packaging-food-contact-substances-fcs/food-contact-materials", "https://www.fda.gov/food/food-ingredients-packaging/food-contact-substances-fcs")
]

# 3. Replacements for articles/tech_office.py
tech_file = os.path.join(ARTICLES_DIR, "tech_office.py")
tech_replacements = [
    ("https://www.usgs.gov/mission-areas/natural-resources/mineral-resources/science/rare-earth-elements", "https://www.usgs.gov/centers/national-minerals-information-center/rare-earths-statistics-and-information"),
    ("https://ntp.niehs.nih.gov/", "https://www.niehs.nih.gov/health/topics/agents/sya-bpa"),
    ("https://echa.europa.eu/-/echa-raises-environmental-concerns-over-certain-aromatic-brominated-flame-retardants", "https://echa.europa.eu/registration-dossier/-/registered-dossier/15399"),
    ("https://ehp.niehs.nih.gov/doi/10.1289/ehp.1104753", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3222079/"),
    ("https://www.epa.gov/smm/electronics-waste-management", "https://www.epa.gov/recycle/electronics-donation-and-recycling"),
    ("https://ec.europa.eu/environment/topics/waste/rohs-directive_en", "https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en"),
    ("https://www.fda.gov/media/89360/download", "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/CFRSearch.cfm?fr=177.1210"),
    ("https://www.greenpeace.org/international/publication/10398/green-electronics-guide-2017/", "https://www.greenpeace.org/usa/reports/greener-electronics-2017/"),
    ("https://www.astm.org/products-services/standards-and-publications/standards/d-section-thermoplastic-elastomers.html", "https://www.astm.org/d5538-13r23.html"),
    ("https://www.osha.gov/electric-power/safety-guidance/lithium-ion-battery-safety", "https://www.osha.gov/sites/default/files/publications/shib011819.pdf"),
    ("https://www.nfpa.org/Public-Education/By-topic/Safety-in-the-home/Lithium-ion-batteries", "https://www.nfpa.org/education-and-research/home-fire-safety/lithium-ion-batteries")
]

# 4. Replacements for articles/cleaning.py
cleaning_file = os.path.join(ARTICLES_DIR, "cleaning.py")
cleaning_replacements = [
    ("https://www.ewg.org/guides/cleaners/content/quats/", "https://www.ewg.org/news-insights/news/2023/05/skip-quats-your-cleaning-routine"),
    ("http://www.aoec.org/", "https://www.aoecdata.org/"),
    ("https://www.cdc.gov/niosh/topics/bleach.html", "https://www.cdc.gov/niosh/docs/2011-125/"),
    ("https://www.lung.org/clean-air/at-home/indoor-air-pollutants/cleaning-supplies", "https://www.lung.org/clean-air/at-home/indoor-air-pollutants/cleaning-supplies-and-household-chemicals"),
    ("https://www.osha.gov/ammonia", "https://www.osha.gov/sites/default/files/publications/osha3144.pdf")
]

# 5. Replacements for articles/personal_care.py
personal_file = os.path.join(ARTICLES_DIR, "personal_care.py")
personal_replacements = [
    ("https://www.aad.org/public/diseases/eczema/itchy-skin/relieve-itch", "https://www.aad.org/public/diseases/eczema/types/contact-dermatitis"),
    ("https://www.cir-safety.org/sites/default/files/SLES.pdf", "https://cir-safety.org/sites/default/files/SLS.pdf"),
    ("https://www.fda.gov/cosmetics/potential-contaminants-cosmetics/14-dioxane-cosmetics", "https://www.fda.gov/cosmetics/potential-contaminants-cosmetics/14-dioxane-cosmetics-manufacturing-byproduct"),
    ("https://www.alz.org/alzheimer_s_dementia_risk_factors.asp", "https://www.alz.org/alzheimers-dementia/what-is-alzheimers/causes-and-risk-factors/myths"),
    ("https://www.fda.gov/cosmetics/cosmetic-ingredients/lead-cosmetics", "https://www.fda.gov/cosmetics/cosmetic-ingredients/lead-cosmetics-draft-guidance-recommended-limit"),
    ("https://wwwn.cdc.gov/ATSDR/toxfaqs/index.asp", "https://www.atsdr.cdc.gov/toxfaqs/index.html"),
    ("https://www.ewg.org/the-toxic-twenty/triclosan", "https://www.ewg.org/news-insights/news/2023/11/chemicals-ewg-verified-products-must-avoid"),
    ("https://www.fda.gov/consumers/consumer-updates/sunscreen-how-help-protect-your-skin-sun", "https://www.fda.gov/cosmetics/cosmetic-ingredients/titanium-dioxide-cosmetics"),
    ("https://cosmeticseurope.eu/publications/mineral-hydrocarbons-cosmetic-products/", "https://www.cosmeticseurope.eu/files/8115/3717/9986/Recommendation_14_Mineral_Hydrocarbons_in_Cosmetic_Lip_Care_Products.pdf"),
    ("https://www.bfr.bund.de/cm/349/mineral-oils-in-cosmetics-risk-assessment-shows-need-for-optimization.pdf", "https://www.bfr.bund.de/cm/349/highly-refined-mineral-oils-in-cosmetics-health-risks-are-not-to-be-expected-according-to-current-knowledge.pdf"),
    ("https://www.aad.org/public/diseases/eczema/types/contact-dermatitis/p-phenylenediamine", "https://www.aad.org/public/diseases/eczema/types/contact-dermatitis"),
    ("https://health.ec.europa.eu/scientific-committees/scientific-committee-consumer-safety_en", "https://health.ec.europa.eu/scientific-committees/scientific-committee-consumer-safety-sccs_en"),
    ("https://www.niehs.nih.gov/news/newsroom/releases/2022/oct/hair-straightening-products-associated-with-uterine-cancer-risk", "https://www.niehs.nih.gov/news/newsroom/releases/2022/october17"),
    ("https://www.nih.gov/news-events/news-releases/hair-dye-straightener-use-may-be-linked-cancer-risk", "https://www.nih.gov/news-events/news-releases/hair-straightening-products-associated-uterine-cancer-risk"),
    ("https://www.ewg.org/news-insights/news-release/2029/03/hair-relaxers-linked-uterine-cancer-and-other-womens-health", "https://www.ewg.org/news-insights/news-release/2022/10/study-hair-straighteners-linked-uterine-cancer-risk"),
    ("https://www.cdc.gov/biomonitoring/Phthalates_FactSheet.html", "https://www.cdc.gov/biomonitoring/pdf/Phthalates_FactSheet.pdf"),
    ("https://www.niehs.nih.gov/health/topics/agents/phthalates/index.cfm", "https://www.niehs.nih.gov/health/topics/agents/phthalates"),
    ("https://www.ewg.org/news-insights/news/whats-your-fragrance-phthalates-and-more", "https://www.ewg.org/news-insights/news/2022/08/whats-fragrance-phthalates-and-other-chemicals-your-scented-products"),
    ("https://www.ewg.org/news-insights/news-release/2019/01/toxic-pfas-chemicals-dental-floss", "https://www.ewg.org/news-insights/news-release/2019/01/new-study-links-oral-b-glide-floss-higher-levels-toxic-pfas-chemicals"),
    ("https://www.niehs.nih.gov/health/topics/agents/pfas/index.cfm", "https://www.niehs.nih.gov/health/topics/agents/pfas"),
    ("https://www.fda.gov/food/environmental-contaminants-food/pfas-per-and-polyfluoroalkyl-substances", "https://www.fda.gov/food/chemical-contaminants-food/and-polyfluoroalkyl-substances-pfas")
]

# 6. Replacements for articles/pet_care.py
pet_file = os.path.join(ARTICLES_DIR, "pet_care.py")
pet_replacements = [
    ("https://www.acvs.org/small-animal/intestinal-foreign-bodies-cats", "https://www.acvs.org/small-animal/gastrointestinal-foreign-bodies"),
    ("https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center", "https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-asthma-what-you-need-know"),
    ("https://www.fda.gov/animal-veterinary/recalls-withdrawals/melamine-pet-food-recall-2007", "https://www.fda.gov/animal-veterinary/safety-health/recalls-withdrawals"),
    ("https://www.petpoisonhelpline.com/poison/essential-oils/", "https://www.petpoisonhelpline.com/pet-safety-tips/essential-oils-and-cats/"),
    ("https://www.epa.gov/pets/flea-and-tick-products-pets", "https://www.epa.gov/pets/avoid-double-dosing-pets-flea-and-tick-products"),
    ("https://www.petpoisonhelpline.com/poison/permethrin/", "https://www.petpoisonhelpline.com/poison/permethrin-toxicity-in-cats/"),
    ("https://www.ecocenter.org/our-work/healthy-stuff/healthy-stuff-blog/chemicals-in-pet-products", "https://www.ecocenter.org/healthy-stuff/chemicals-pet-products"),
    ("https://www.atsdr.cdc.gov/toxprofiledocs/index.html", "https://www.atsdr.cdc.gov/ToxProfiles/tp20.pdf"),
    ("https://www.tuftsyourdog.com/dog-health/flame-retardants-and-pets-how-much-is-too-much/", "https://www.tuftsyourdog.com/dog-health/flame-retardants-and-pets/"),
    ("https://www.ewg.org/areas-of-work/healthy-living/pets/phthalates-and-animal-health", "https://www.ewg.org/news-insights/news/2023/10/ewg-verified-pet-grooming-products-are-here"),
    ("https://www.avma.org/resources/pet-owners/petcare/pet-grooming-product-safety", "https://www.avma.org/resources/pet-owners/petcare/grooming"),
    ("https://www.epa.gov/indoor-air-quality-iaq/indoor-air-quality-pet-health", "https://www.epa.gov/indoor-air-quality-iaq"),
    ("https://ww2.arb.ca.gov/our-work/programs/air-quality-standards/formaldehyde-emission-standards-composite-wood-products", "https://ww2.arb.ca.gov/our-work/programs/composite-wood-products-program")
]

# 7. Replacements for articles/surfaces_fabrics.py
surfaces_file = os.path.join(ARTICLES_DIR, "surfaces_fabrics.py")
surfaces_replacements = [
    ("https://wwwn.cdc.gov/TSP/ToxProfiles/TP.asp?id=516&tid=91", "https://www.atsdr.cdc.gov/ToxProfiles/tp218.pdf")
]

def apply_replacements(file_path, reps):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    for target, rep in reps:
        if target in content:
            content = content.replace(target, rep)
            modified = True
            print(f"Replaced in {os.path.basename(file_path)}: {target} -> {rep}")
    
    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {file_path}\n")
    else:
        print(f"No replacements made in {file_path}\n")

# Run simple files replacements
apply_replacements(kitchen_file, kitchen_replacements)
apply_replacements(nursery_file, nursery_replacements)
apply_replacements(tech_file, tech_replacements)
apply_replacements(cleaning_file, cleaning_replacements)
apply_replacements(personal_file, personal_replacements)
apply_replacements(pet_file, pet_replacements)
apply_replacements(surfaces_file, surfaces_replacements)

# 8. Special Replacements for articles/outdoor.py (based on article specific sections)
# Let's write custom logic to target each article sources in outdoor.py
if os.path.exists(os.path.join(ARTICLES_DIR, "outdoor.py")):
    with open(os.path.join(ARTICLES_DIR, "outdoor.py"), "r", encoding="utf-8") as f:
        outdoor_content = f.read()
        
    outdoor_article_reps = {
        "cca-treated-wood": "https://www.atsdr.cdc.gov/ToxProfiles/tp2.pdf",
        "citronella-candles-soot": "https://www.atsdr.cdc.gov/ToxProfiles/tp56.pdf",
        "deet-bug-sprays": "https://www.atsdr.cdc.gov/ToxProfiles/tp185.pdf",
        "epoxy-garage-coatings": "https://www.atsdr.cdc.gov/ToxProfiles/tp71.pdf",
        "gas-mower-exhaust": "https://www.atsdr.cdc.gov/ToxProfiles/tp114.pdf",
        "glyphosate-weed-killer": "https://www.atsdr.cdc.gov/ToxProfiles/tp214.pdf",
        "neonicotinoid-pesticides": "https://www.epa.gov/pollinator-protection/schedule-review-neonicotinoid-pesticides",
        "pvc-garden-hoses": "https://www.atsdr.cdc.gov/ToxProfiles/tp13.pdf",
        "rubber-mulch": "https://www.atsdr.cdc.gov/ToxProfiles/tp69.pdf",
    }
    
    # We will split outdoor_content by articles
    # Each article has unique slug, and its sources: [ ... ] block
    for slug, new_url in outdoor_article_reps.items():
        # Find the article section using regex
        # We look for a pattern starting with the slug and capturing up to the sources list
        pattern = re.compile(
            r'("slug":\s*"' + slug + r'".*?"sources":\s*\[\s*\[\s*".*?"\s*,\s*")(https://www\.atsdr\.cdc\.gov/toxprofiledocs/index\.html)(")',
            re.DOTALL
        )
        if pattern.search(outdoor_content):
            outdoor_content = pattern.sub(r'\1' + new_url + r'\3', outdoor_content)
            print(f"Replaced outdoor.py source for {slug} -> {new_url}")
            
    # And synthetic-turf-pfas needs two replacements (EPA and ATSDR)
    pfas_pattern = re.compile(
        r'("slug":\s*"synthetic-turf-pfas".*?"sources":\s*\[\s*\[\s*".*?"\s*,\s*")https://www\.epa\.gov/("\s*\],\s*\[\s*"ATSDR Toxicological Profiles"\s*,\s*")https://www\.atsdr\.cdc\.gov/toxprofiledocs/index\.html(")',
        re.DOTALL
    )
    if pfas_pattern.search(outdoor_content):
        outdoor_content = pfas_pattern.sub(
            r'\1https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/risk-management-and-polyfluoroalkyl-substances-pfas\2https://www.atsdr.cdc.gov/ToxProfiles/tp200.pdf\3',
            outdoor_content
        )
        print("Replaced synthetic-turf-pfas sources in outdoor.py")
        
    with open(os.path.join(ARTICLES_DIR, "outdoor.py"), "w", encoding="utf-8") as f:
        f.write(outdoor_content)
        
print("All replacements done!")
