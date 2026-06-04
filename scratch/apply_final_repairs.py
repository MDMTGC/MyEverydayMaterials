import os
import re

# Define paths
WORKSPACE_DIR = r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials"
ARTICLES_DIR = os.path.join(WORKSPACE_DIR, "articles")

def replace_in_slug_block(content, slug, old_url, new_url):
    # Find position of the slug
    slug_pos = content.find(f'"slug": "{slug}"')
    if slug_pos == -1:
        slug_pos = content.find(f"'slug': '{slug}'")
    if slug_pos == -1:
        return content, False
        
    # Find next slug position
    next_slug_pos = content.find('"slug":', slug_pos + 10)
    if next_slug_pos == -1:
        next_slug_pos = content.find("'slug':", slug_pos + 10)
    if next_slug_pos == -1:
        next_slug_pos = len(content)
        
    block = content[slug_pos:next_slug_pos]
    if old_url in block:
        block = block.replace(old_url, new_url)
        return content[:slug_pos] + block + content[next_slug_pos:], True
    return content, False

def apply_global_reps(filepath, reps):
    if not os.path.exists(filepath):
        print(f"Skipped (not found): {filepath}")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    for old, new in reps:
        if old in content:
            content = content.replace(old, new)
            modified = True
            print(f"[{os.path.basename(filepath)}] Global replaced: {old} -> {new}")
            
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved global changes to: {filepath}\n")
    else:
        print(f"No global changes made to: {filepath}\n")

# --- 1. Global replacements (no duplicate-key ambiguity) ---

# cleaning.py
cleaning_file = os.path.join(ARTICLES_DIR, "cleaning.py")
cleaning_reps = [
    ("https://www.ewg.org/guides/cleaners/content/quats/", "https://www.ewg.org/news-insights/news/2023/05/skip-quats-your-cleaning-routine"),
    ("http://www.aoec.org/", "https://www.aoecdata.org/"),
    ("https://www.cdc.gov/niosh/topics/bleach.html", "https://www.cdc.gov/hygiene/about/cleaning-and-disinfecting-with-bleach.html"),
    ("https://www.lung.org/clean-air/at-home/indoor-air-pollutants/cleaning-supplies", "https://www.lung.org/clean-air/at-home/indoor-air-pollutants/cleaning-supplies-household-chem"),
    ("https://www.osha.gov/ammonia", "https://www.osha.gov/sites/default/files/publications/osha3144.pdf"),
    ("https://lancaster.unl.edu/hort/articles/2006/bakingsoda.shtml", "https://www.purdue.edu/hla/sites/yardandgarden/baking-soda-as-a-fungicide/"),
    ("https://www.poison.org/articles/caustic-ingestions-2016", "https://www.poison.org/articles/caution-with-caustics")
]
apply_global_reps(cleaning_file, cleaning_reps)

# kitchen.py
kitchen_file = os.path.join(ARTICLES_DIR, "kitchen.py")
kitchen_reps = [
    ("https://monographs.iarc.who.int/news-events/iarc-monographs-volume-131-cobalt-antimony-compounds-and-weapons-grade-tungsten-alloy/", "https://publications.iarc.who.int/618"),
    ("https://echa.europa.eu/", "https://echa.europa.eu/hot-topics/phthalates"),
    ("https://www.who.int/publications/i/item/9789241546553", "https://cdn.who.int/media/docs/default-source/wash-documents/water-safety-and-quality/chemical-fact-sheets-2022/copper-fact-sheet-2022.pdf"),
    ("https://www.fda.gov/food/chemicals/melamine-tableware", "https://www.fda.gov/food/chemical-contaminants-food/melamine-tableware-questions-and-answers"),
    ("https://www.cdc.gov/biomonitoring/BisphenolA_FactSheet.html", "https://www.cdc.gov/biomonitoring/index.html"),
    ("https://ods.od.nih.gov/factsheets/Copper-HealthProfessional/", "https://ods.od.nih.gov/factsheets/Copper-Consumer/"),
    ("https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/", "https://ods.od.nih.gov/factsheets/Iron-Consumer/")
]
apply_global_reps(kitchen_file, kitchen_reps)

# nursery.py
nursery_file = os.path.join(ARTICLES_DIR, "nursery.py")
nursery_reps = [
    ("https://www.fda.gov/cosmetics/resources-consumers-cosmetics/cosmetics-qa-preservatives", "https://www.fda.gov/cosmetics/cosmetic-ingredients/parabens-cosmetics"),
    ("https://www.aad.org/public/diseases/eczema/types/contact-dermatitis/causes-children", "https://www.aad.org/public/diseases/eczema/types/contact-dermatitis"),
    ("https://www.fda.gov/food/packaging-food-contact-substances-fcs/melamine-food-contact-substances", "https://www.fda.gov/food/chemical-contaminants-food/melamine-tableware-questions-and-answers"),
    ("https://www.epa.gov/iris/basic-information-about-formaldehyde-inhalation-reference-concentration", "https://cfpub.epa.gov/ncea/iris2/chemicalLanding.cfm?substance_nmbr=419"),
    ("https://www.efsa.europa.eu/en/topics/topic/melamine-food-and-feed", "https://www.efsa.europa.eu/en/press/news/contam100413"),
    ("https://www.ecocenter.org/healthy-stuff/healthy-car-seats/", "https://www.ecocenter.org/frequently-asked-questions-childrens-car-seats-2018"),
    ("https://www.healthychildren.org/English/ages-stages/baby/preemie/Pages/Choosing-a-Pacifier-for-Your-Preemie.aspx", "https://www.healthychildren.org/English/safety-prevention/at-home/Pages/Pacifier-Safety.aspx"),
    ("https://www.fda.gov/food/packaging-food-contact-substances-fcs/food-contact-materials", "https://www.fda.gov/food/food-ingredients-packaging/food-contact-substances-fcs"),
    ("https://www.fda.gov/food/chemicals/melamine-safety", "https://www.fda.gov/food/chemical-contaminants-food/melamine-tableware-questions-and-answers"),
    ("https://ehp.niehs.nih.gov/doi/10.1289/ehp.1408822", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8157593/"),
    ("https://www.epa.gov/assessing-and-managing-chemicals/what-are-phthalates", "https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/phthalates"),
    ("https://www.who.int/news-room/fact-sheets/detail/endocrine-disrupting-chemicals-(edcs)", "https://www.who.int/teams/environment-climate-change-and-health/settings-and-populations/children/endocrine-disrupters"),
    ("https://www.fda.gov/consumers/consumer-updates/talcum-powder-and-asbestos-frequently-asked-questions", "https://www.fda.gov/cosmetics/cosmetic-ingredients/talc"),
    ("https://www.niehs.nih.gov/research/supported/assets/docs/d_g/childrens_exposure_to_flame_retardants_in_the_car_environment_508.pdf", "https://www.niehs.nih.gov/health/topics/agents/flame_retardants"),
    ("https://www.atsdr.cdc.gov/sites/KIDS/documents/flame_retardants.pdf", "https://www.atsdr.cdc.gov/toxfaqs/index.html"),
    ("https://www.cdc.gov/niosh/topics/fibreglass/default.html", "https://www.atsdr.cdc.gov/toxprofiles/tp161.pdf")
]
apply_global_reps(nursery_file, nursery_reps)

# personal_care.py
personal_file = os.path.join(ARTICLES_DIR, "personal_care.py")
personal_reps = [
    ("https://www.aad.org/public/diseases/eczema/itchy-skin/relieve-itch", "https://www.aad.org/public/diseases/eczema/childhood/itch-relief"),
    ("https://www.cir-safety.org/sites/default/files/SLES.pdf", "https://pubmed.ncbi.nlm.nih.gov/16019448/"),
    ("https://www.fda.gov/cosmetics/potential-contaminants-cosmetics/14-dioxane-cosmetics", "https://www.fda.gov/cosmetics/potential-contaminants-cosmetics/14-dioxane-cosmetics-manufacturing-byproduct"),
    ("https://www.alz.org/alzheimer_s_dementia_risk_factors.asp", "https://www.alz.org/alzheimers-dementia/what-is-alzheimers/myths"),
    ("https://www.fda.gov/cosmetics/cosmetic-ingredients/lead-cosmetics", "https://www.fda.gov/cosmetics/potential-contaminants-cosmetics/lead-cosmetics"),
    ("https://wwwn.cdc.gov/ATSDR/toxfaqs/index.asp", "https://www.atsdr.cdc.gov/toxfaqs/index.html"),
    ("https://www.ewg.org/the-toxic-twenty/triclosan", "https://www.ewg.org/news-insights/news/2023/11/chemicals-ewg-verified-products-must-avoid"),
    ("https://www.fda.gov/consumers/consumer-updates/sunscreen-how-help-protect-your-skin-sun", "https://www.fda.gov/cosmetics/cosmetic-ingredient-names/color-additives-permitted-use-cosmetics"),
    ("https://cosmeticseurope.eu/publications/mineral-hydrocarbons-cosmetic-products/", "https://www.efsa.europa.eu/en/efsajournal/pub/8215"),
    ("https://www.bfr.bund.de/cm/349/mineral-oils-in-cosmetics-risk-assessment-shows-need-for-optimization.pdf", "https://www.bfr.bund.de/cm/349/highly-refined-mineral-oils-in-cosmetics-health-risks-are-not-to-be-expected-according-to-current-knowledge.pdf"),
    ("https://www.aad.org/public/diseases/eczema/types/contact-dermatitis/signs-symptoms", "https://www.aad.org/public/diseases/eczema/types/contact-dermatitis/symptoms"),
    ("https://www.aad.org/public/diseases/eczema/types/contact-dermatitis/p-phenylenediamine", "https://www.aad.org/public/diseases/eczema/types/contact-dermatitis"),
    ("https://www.ewg.org/the-toxic-twenty/formaldehyde-releasers", "https://www.ewg.org/skindeep/ingredients/702500-FORMALDEHYDE/"),
    ("https://www.fda.gov/cosmetics/cosmetic-ingredients/formaldehyde-cosmetics-what-you-should-know", "https://www.fda.gov/cosmetics/cosmetic-products/nail-care-products"),
    ("https://www.ewg.org/the-toxic-twenty/parabens", "https://www.ewg.org/what-are-parabens"),
    ("https://health.ec.europa.eu/scientific-committees/scientific-committee-consumer-safety_en", "https://health.ec.europa.eu/scientific-committees/scientific-committee-consumer-safety-sccs_en"),
    ("https://www.niehs.nih.gov/news/newsroom/releases/2022/oct/hair-straightening-products-associated-with-uterine-cancer-risk", "https://www.niehs.nih.gov/news/factor/2022/11/papers/uterine-cancer"),
    ("https://www.nih.gov/news-events/news-releases/hair-dye-straightener-use-may-be-linked-cancer-risk", "https://www.nih.gov/news-events/news-releases/hair-straightening-chemicals-associated-higher-uterine-cancer-risk"),
    ("https://www.ewg.org/news-insights/news-release/2029/03/hair-relaxers-linked-uterine-cancer-and-other-womens-health", "https://www.ewg.org/news-insights/news/2022/10/new-study-links-chemicals-hair-straighteners-uterine-cancer"),
    ("https://www.cdc.gov/biomonitoring/Phthalates_FactSheet.html", "https://www.cdc.gov/biomonitoring/index.html"),
    ("https://www.niehs.nih.gov/health/topics/agents/phthalates/index.cfm", "https://www.niehs.nih.gov/health/topics/agents/phthalates"),
    ("https://www.ewg.org/news-insights/news/whats-your-fragrance-phthalates-and-more", "https://www.ewg.org/news-insights/news/2022/08/whats-fragrance-phthalates-and-other-chemicals-your-scented-products"),
    ("https://www.ewg.org/news-insights/news-release/2019/01/toxic-pfas-chemicals-dental-floss", "https://www.ewg.org/news-insights/news-release/2019/01/new-study-links-oral-b-glide-floss-higher-levels-toxic-pfas-chemicals"),
    ("https://www.niehs.nih.gov/health/topics/agents/pfas/index.cfm", "https://www.niehs.nih.gov/health/topics/agents/pfas"),
    ("https://www.fda.gov/food/environmental-contaminants-food/pfas-per-and-polyfluoroalkyl-substances", "https://www.fda.gov/food/chemical-contaminants-food/and-polyfluoroalkyl-substances-pfas")
]
apply_global_reps(personal_file, personal_reps)

# pet_care.py
pet_file = os.path.join(ARTICLES_DIR, "pet_care.py")
pet_reps = [
    ("https://www.acvs.org/small-animal/intestinal-foreign-bodies-cats", "https://www.acvs.org/small-animal/gastrointestinal-foreign-bodies"),
    ("https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center", "https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-asthma-what-you-need-know"),
    ("https://www.fda.gov/animal-veterinary/recalls-withdrawals/melamine-pet-food-recall-2007", "https://www.fda.gov/animal-veterinary/safety-health/recalls-withdrawals"),
    ("https://www.petpoisonhelpline.com/poison/essential-oils/", "https://www.petpoisonhelpline.com/pet-safety-tips/essential-oils-and-cats/"),
    ("https://www.epa.gov/pets/flea-and-tick-products-pets", "https://www.epa.gov/pets/controlling-fleas-and-ticks-your-pet"),
    ("https://www.petpoisonhelpline.com/poison/permethrin/", "https://www.petpoisonhelpline.com/poison/pyrethrin/"),
    ("https://www.ecocenter.org/our-work/healthy-stuff/healthy-stuff-blog/chemicals-in-pet-products", "https://www.ecocenter.org/healthy-stuff"),
    ("https://www.atsdr.cdc.gov/toxprofiledocs/index.html", "https://www.atsdr.cdc.gov/toxprofiles/tp20.pdf"),
    ("https://www.tuftsyourdog.com/dog-health/flame-retardants-and-pets-how-much-is-too-much/", "https://www.tuftsyourdog.com/dog-health/flame-retardants-and-pets/"),
    ("https://www.ewg.org/areas-of-work/healthy-living/pets/phthalates-and-animal-health", "https://www.ewg.org/research/polluted-pets"),
    ("https://www.avma.org/resources/pet-owners/petcare/pet-grooming-product-safety", "https://www.avma.org/resources/pet-owners/petcare"),
    ("https://www.epa.gov/indoor-air-quality-iaq/indoor-air-quality-pet-health", "https://www.epa.gov/indoor-air-quality-iaq"),
    ("https://ww2.arb.ca.gov/our-work/programs/air-quality-standards/formaldehyde-emission-standards-composite-wood-products", "https://ww2.arb.ca.gov/our-work/programs/composite-wood-products-program"),
    ("https://vcahospitals.com/know-your-pet/feline-acne", "https://vcahospitals.com/know-your-pet/chin-acne-in-cats"),
    ("https://www.niehs.nih.gov/health/topics/agents/bpa/", "https://www.niehs.nih.gov/health/topics/agents/sya-bpa")
]
apply_global_reps(pet_file, pet_reps)

# surfaces_fabrics.py
surfaces_file = os.path.join(ARTICLES_DIR, "surfaces_fabrics.py")
surfaces_reps = [
    ("https://wwwn.cdc.gov/TSP/ToxProfiles/TP.asp?id=516&tid=91", "https://www.atsdr.cdc.gov/toxprofiles/tp218.pdf"),
    ("https://www.epa.gov/indoor-air-quality-iaq/indoor-air-facts-no-4-sick-building-syndrome", "https://www.epa.gov/sites/default/files/2014-08/documents/sick_building_factsheet.pdf"),
    ("https://www.lung.org/clean-air/at-home/indoor-air-pollutants/cleaning-supplies", "https://www.lung.org/clean-air/at-home/indoor-air-pollutants/cleaning-supplies-household-chem"),
    ("https://www.epa.gov/trash-free-waters/microplastics-research", "https://www.epa.gov/trash-free-waters/priority-microplastics-research-needs-0"),
    ("https://ww2.arb.ca.gov/our-work/programs/perchloroethylene-dry-cleaning", "https://ww2.arb.ca.gov/our-work/programs/dry-cleaning-program"),
    ("https://monographs.iarc.who.int/agents-classified-by-the-iarc-monographs/", "https://publications.iarc.who.int/Book-And-Report-Series/Iarc-Monographs-On-The-Identification-Of-Carcinogenic-Hazards-To-Humans/Trichloroethylene-Tetrachloroethylene-And-Some-Other-Chlorinated-Agents-2014"),
    ("https://www.ewg.org/healthyhome/flame-retardants", "https://www.ewg.org/research/flame-retardants"),
    ("https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/flame-retardants-furniture-and-building-materials", "https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/fact-sheet-assessing-risks-flame-retardants"),
    ("https://ww2.arb.ca.gov/our-work/programs/composite-wood-products-atcm", "https://ww2.arb.ca.gov/resources/documents/composite-wood-products-atcm"),
    ("https://www.epa.gov/formaldehyde/formaldehyde-your-home-what-you-need-know", "https://www.epa.gov/indoor-air-quality-iaq/what-should-i-know-about-formaldehyde-and-indoor-air-quality"),
    ("https://www.cdc.gov/biomonitoring/Phthalates_FactSheet.html", "https://www.cdc.gov/biomonitoring/index.html"),
    ("https://www.niehs.nih.gov/health/topics/agents/phthalates/index.cfm", "https://www.niehs.nih.gov/health/topics/agents/phthalates"),
    ("https://silentspring.org/phthalates", "https://silentspring.org/project/household-exposure-study"),
    ("https://www.epa.gov/indoor-air-quality-iaq/guide-indoor-air-quality", "https://www.epa.gov/indoor-air-quality-iaq/inside-story-guide-indoor-air-quality"),
    ("https://www.atsdr.cdc.gov/sites/toxics_futures/vocs.html", "https://www.atsdr.cdc.gov/substances/index.html"),
    ("https://silentspring.org/factsheets/carpets", "https://silentspring.org/project/household-exposure-study")
]
apply_global_reps(surfaces_file, surfaces_reps)

# tech_office.py
tech_file = os.path.join(ARTICLES_DIR, "tech_office.py")
tech_reps = [
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
apply_global_reps(tech_file, tech_reps)


# --- 2. Article-Specific Block Replacements ---

# A. articles/kitchen.py (BfR duplicate homepage)
if os.path.exists(kitchen_file):
    with open(kitchen_file, "r", encoding="utf-8") as f:
        kitchen_content = f.read()
        
    kitchen_content, ok1 = replace_in_slug_block(
        kitchen_content,
        "bamboo-fiber-plates",
        "https://www.bfr.bund.de/en/",
        "https://www.bfr.bund.de/cm/349/fillable-articles-made-from-melamine-formaldehyde-resin.pdf"
    )
    kitchen_content, ok2 = replace_in_slug_block(
        kitchen_content,
        "silicone-bakeware-heat",
        "https://www.bfr.bund.de/en/",
        "https://www.bfr.bund.de/en/bfr_recommendations_on_food_contact_materials-19602.html"
    )
    
    if ok1 or ok2:
        with open(kitchen_file, "w", encoding="utf-8") as f:
            f.write(kitchen_content)
        print(f"[kitchen.py] Applied specific BfR block replacements: bamboo={ok1}, silicone={ok2}")

# B. articles/outdoor.py (ATSDR duplicate index)
outdoor_file = os.path.join(ARTICLES_DIR, "outdoor.py")
if os.path.exists(outdoor_file):
    with open(outdoor_file, "r", encoding="utf-8") as f:
        outdoor_content = f.read()
        
    outdoor_article_reps = {
        "cca-treated-wood": "https://www.atsdr.cdc.gov/toxprofiles/tp2.pdf",
        "citronella-candles-soot": "https://www.atsdr.cdc.gov/toxprofiles/tp56.pdf",
        "deet-bug-sprays": "https://www.atsdr.cdc.gov/toxprofiles/tp185.pdf",
        "epoxy-garage-coatings": "https://www.atsdr.cdc.gov/toxprofiles/tp71.pdf",
        "gas-mower-exhaust": "https://www.atsdr.cdc.gov/toxprofiles/tp114.pdf",
        "glyphosate-weed-killer": "https://www.atsdr.cdc.gov/toxprofiles/tp214.pdf",
        "neonicotinoid-pesticides": "https://www.epa.gov/pollinator-protection/schedule-review-neonicotinoid-pesticides",
        "pvc-garden-hoses": "https://www.atsdr.cdc.gov/toxprofiles/tp13.pdf",
        "rubber-mulch": "https://www.atsdr.cdc.gov/toxprofiles/tp69.pdf",
    }
    
    modified = False
    for slug, new_url in outdoor_article_reps.items():
        outdoor_content, ok = replace_in_slug_block(
            outdoor_content,
            slug,
            "https://www.atsdr.cdc.gov/toxprofiledocs/index.html",
            new_url
        )
        if ok:
            modified = True
            print(f"[outdoor.py] Block replaced for {slug} -> {new_url}")
            
    # For synthetic-turf-pfas (EPA and ATSDR both need replacement in this block)
    slug = "synthetic-turf-pfas"
    slug_pos = outdoor_content.find(f'"slug": "{slug}"')
    if slug_pos != -1:
        next_slug_pos = outdoor_content.find('"slug":', slug_pos + 10)
        if next_slug_pos == -1:
            next_slug_pos = len(outdoor_content)
        block = outdoor_content[slug_pos:next_slug_pos]
        if "https://www.epa.gov/" in block:
            block = block.replace("https://www.epa.gov/", "https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/risk-management-and-polyfluoroalkyl-substances-pfas")
            modified = True
        if "https://www.atsdr.cdc.gov/toxprofiledocs/index.html" in block:
            block = block.replace("https://www.atsdr.cdc.gov/toxprofiledocs/index.html", "https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf")
            modified = True
        if modified:
            outdoor_content = outdoor_content[:slug_pos] + block + outdoor_content[next_slug_pos:]
            print(f"[outdoor.py] Block replaced for synthetic-turf-pfas")
            
    if modified:
        with open(outdoor_file, "w", encoding="utf-8") as f:
            f.write(outdoor_content)
        print(f"Saved specific block changes to: {outdoor_file}\n")
    else:
        print("No block changes made in: outdoor.py\n")

print("Repair execution completed successfully!")
