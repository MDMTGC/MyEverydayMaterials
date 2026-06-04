import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Master list of replacement candidates to verify
candidates = {
    "sick_building_pdf": "https://www.epa.gov/sites/default/files/2014-08/documents/sick_building_factsheet.pdf",
    "clean_supplies_lung": "https://www.lung.org/clean-air/at-home/cleaning-supplies-household-chemicals",
    "alz_myths": "https://www.alz.org/alzheimers-dementia/what-is-alzheimers/myths",
    "bfr_melamine_pdf": "https://www.bfr.bund.de/cm/349/fillable-articles-made-from-melamine-formaldehyde-resin.pdf",
    "fda_melamine_qa": "https://www.fda.gov/food/chemical-contaminants-food/melamine-tableware-questions-and-answers",
    "efsa_melamine_news": "https://www.efsa.europa.eu/en/press/news/contam100413",
    "echa_tbbpa_dossier": "https://chem.echa.europa.eu/substance-details/100.001.125",
    "niehs_bpa": "https://www.niehs.nih.gov/health/topics/agents/sya-bpa",
    "ecocenter_car_seats": "https://www.ecocenter.org/frequently-asked-questions-childrens-car-seats-2018",
    "poison_caustics": "https://www.poison.org/articles/caution-with-caustics",
    "epa_flea_pet": "https://www.epa.gov/pets/controlling-fleas-and-ticks-your-pet",
    "petpoison_pyrethrins": "https://www.petpoisonhelpline.com/poison/pyrethrins/",
    "cdc_hygiene_bleach": "https://www.cdc.gov/hygiene/about/cleaning-and-disinfecting-with-bleach.html",
    "tamu_essential_oils": "https://vetmed.tamu.edu/news/pet-talk/essential-oils-and-cats/",
    "atsdr_fiberglass": "https://www.atsdr.cdc.gov/toxprofiles/tp161.pdf",
    "epa_tsca_main": "https://www.epa.gov/assessing-and-managing-chemicals-under-tsca",
    "epa_formaldehyde_facts": "https://www.epa.gov/formaldehyde/facts-about-formaldehyde",
    "carb_composite_program": "https://ww2.arb.ca.gov/our-work/programs/composite-wood-products-program",
    "avma_petcare": "https://www.avma.org/resources/pet-owners/petcare",
    "healthychildren_pacifier": "https://www.healthychildren.org/English/safety-prevention/at-home/Pages/Pacifier-Safety.aspx",
    "fda_packaging_fcs": "https://www.fda.gov/food/food-ingredients-packaging/packaging-food-contact-substances-fcs",
    "vca_feline_acne": "https://vcahospitals.com/know-your-pet/chin-acne-in-cats",
    "niehs_uterine_cancer": "https://www.niehs.nih.gov/news/factor/2022/11/papers/uterine-cancer",
    "efsa_lip_care": "https://www.efsa.europa.eu/en/efsajournal/pub/8215",
    "bfr_food_contact": "https://www.bfr.bund.de/en/bfr_recommendations_on_food_contact_materials-19602.html",
    "epa_nepis_microplastics": "https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P101AJ2S.TXT",
    "aad_dermatitis_symptoms": "https://www.aad.org/public/diseases/eczema/types/contact-dermatitis/symptoms",
    "carb_dry_cleaning": "https://ww2.arb.ca.gov/our-work/programs/dry-cleaning-program",
    "iarc_monograph_perc": "https://publications.iarc.who.int/Book-And-Report-Series/Iarc-Monographs-On-The-Identification-Of-Carcinogenic-Hazards-To-Humans/Trichloroethylene-Tetrachloroethylene-And-Some-Other-Chlorinated-Agents-2014",
    "niehs_endocrine": "https://www.niehs.nih.gov/health/topics/agents/endocrine",
    "silentspring_dust": "https://silentspring.org/news/toxic-chemicals-widespread-household-dust",
    "cornell_lutd": "https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-lower-urinary-tract-disease",
    "atsdr_tdi_new": "https://www.atsdr.cdc.gov/toxprofiles/tp206-c1.pdf",
    "petpoison_flame_retardants": "https://pubmed.ncbi.nlm.nih.gov/21491873/",
    "who_endocrine_kids": "https://www.who.int/teams/environment-climate-change-and-health/settings-and-populations/children/endocrine-disrupters",
    "ecocenter_main": "https://www.ecocenter.org/healthy-stuff",
    "purdue_baking_soda": "https://www.purdue.edu/hla/sites/yardandgarden/baking-soda-as-a-fungicide/",
    "fda_lead_cosmetic_guidance": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/lead-cosmetic-lip-products-and-externally-applied-cosmetics-recommended-maximum-level-guidance-industry",
    "fda_titanium_cosmetic": "https://www.fda.gov/cosmetics/cosmetic-ingredient-names/color-additives-permitted-use-cosmetics",
    "who_copper_pdf": "https://cdn.who.int/media/docs/default-source/wash-documents/water-safety-and-quality/chemical-fact-sheets-2022/copper-fact-sheet-2022.pdf",
    "epa_indoor_guide": "https://www.epa.gov/indoor-air-quality-iaq/inside-story-guide-indoor-air-quality",
    "atsdr_substances_portal": "https://www.atsdr.cdc.gov/substances/index.html",
    # Remaining ones:
    "ewg_formaldehyde_releasers": "https://www.ewg.org/skindeep/ingredients/702500-FORMALDEHYDE/",
    "fda_formaldehyde_smoothing": "https://www.fda.gov/cosmetics/cosmetic-ingredients/formaldehyde-hair-smoothing-products",
    "ewg_parabens": "https://www.ewg.org/what-are-parabens",
    "epa_synthetic_turf_program": "https://www.epa.gov/chemical-research/federal-research-recycled-tire-crumb-used-playing-fields-and-playgrounds",
    "nih_uterine_cancer_straightener": "https://www.nih.gov/news-events/news-releases/hair-straightening-chemicals-associated-higher-uterine-cancer-risk",
    "ewg_straightener_uterine": "https://www.ewg.org/news-insights/news/2022/10/new-study-links-chemicals-hair-straighteners-uterine-cancer",
    "ewg_verified_general": "https://www.ewg.org/ewgverified/",
    "ewg_flame_retardants_guide": "https://www.ewg.org/news-insights/news/2020/12/reducing-flame-retardants-your-home-and-body"
}

for name, url in candidates.items():
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
            print(f"SUCCESS [200]: {name} -> {url}")
    except urllib.error.HTTPError as e:
        print(f"FAILED [{e.code}]: {name} -> {url}")
    except Exception as e:
        print(f"FAILED [Error]: {name} -> {url} -> {str(e)}")
