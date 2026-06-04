import urllib.request
import urllib.error
import ssl

candidates = [
    # General & fallback
    "https://www.atsdr.cdc.gov/toxicological-profiles/about/index.html",
    "https://www.cdc.gov/biomonitoring/index.html",
    "https://www.cdc.gov/hygiene/about/cleaning-and-disinfecting-with-bleach.html",
    "https://www.niehs.nih.gov/health/topics/agents/endocrine",
    "https://www.niehs.nih.gov/health/topics/agents/sya-bpa",
    "https://www.niehs.nih.gov/health/topics/agents/flame_retardants",
    "https://www.niehs.nih.gov/health/topics/agents/pfas",
    
    # Specific toxicological profiles (lowercase path)
    "https://www.atsdr.cdc.gov/toxprofiles/tp2.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp13.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp18.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp20.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp56.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp69.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp71.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp114.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp161.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp185.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp206-c1.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp214.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp218.pdf",
    "https://www.atsdr.cdc.gov/toxprofiles/tp9.pdf",
    
    # BfR Germany
    "https://www.bfr.bund.de/cm/349/fillable-articles-made-from-melamine-formaldehyde-resin.pdf",
    "https://www.bfr.bund.de/en/bfr_recommendations_on_food_contact_materials-19602.html",
    
    # EPA
    "https://www.epa.gov/sites/default/files/2014-08/documents/sick_building_factsheet.pdf",
    "https://www.epa.gov/pets/controlling-fleas-and-ticks-your-pet",
    "https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/phthalates",
    "https://www.epa.gov/formaldehyde/facts-about-formaldehyde",
    "https://www.epa.gov/indoor-air-quality-iaq/what-should-i-know-about-formaldehyde-and-indoor-air-quality",
    "https://www.epa.gov/indoor-air-quality-iaq/inside-story-guide-indoor-air-quality",
    "https://www.epa.gov/trash-free-waters/priority-microplastics-research-needs-0",
    "https://www.epa.gov/pets/controlling-fleas-and-ticks-your-pet",
    
    # EFSA & ECHA
    "https://www.efsa.europa.eu/en/press/news/contam100413",
    "https://www.efsa.europa.eu/en/efsajournal/pub/8215",
    "https://chem.echa.europa.eu/substance-details/100.001.125",
    
    # Other organizations
    "https://www.ecocenter.org/frequently-asked-questions-childrens-car-seats-2018",
    "https://www.ecocenter.org/healthy-stuff",
    "https://www.ecocenter.org/our-work/healthy-stuff/healthy-stuff-blog/chemicals-in-pet-products",
    "https://www.poison.org/articles/caution-with-caustics",
    "https://www.petpoisonhelpline.com/poison/pyrethrins/",
    "https://vetmed.tamu.edu/news/pet-talk/essential-oils-and-cats/",
    "https://www.petpoisonhelpline.com/blog/essential-oils-safe-pets/",
    "https://www.purdue.edu/hla/sites/yardandgarden/baking-soda-as-a-fungicide/",
    "https://www.healthychildren.org/English/safety-prevention/at-home/Pages/Pacifier-Safety.aspx",
    "https://www.avma.org/resources/pet-owners/petcare",
    "https://ww2.arb.ca.gov/resources/documents/composite-wood-products-atcm",
    "https://ww2.arb.ca.gov/our-work/programs/dry-cleaning-program",
    "https://publications.iarc.fr/Book-And-Report-Series/Iarc-Monographs-On-The-Evaluation-Of-Carcinogenic-Risks-To-Humans/Trichloroethylene-Tetrachloroethylene-And-Some-Other-Chlorinated-Agents-2014",
    "https://www.aad.org/public/diseases/eczema/types/contact-dermatitis/symptoms",
    
    # FDA
    "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/lead-cosmetic-lip-products-and-externally-applied-cosmetics-recommended-maximum-level-guidance-industry",
    "https://www.fda.gov/cosmetics/cosmetic-ingredient-names/color-additives-permitted-use-cosmetics",
    "https://www.fda.gov/food/food-ingredients-packaging/packaging-food-contact-substances-fcs",
    "https://www.fda.gov/food/chemical-contaminants-food/melamine-tableware-questions-and-answers",
    
    # Silent Spring
    "https://silentspring.org/project/household-exposure-study"
]

# Deduplicate
candidates = sorted(list(set(candidates)))

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f"Testing {len(candidates)} candidate URLs...")
for idx, url in enumerate(candidates, 1):
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
            status = response.status
            print(f"[{idx}/{len(candidates)}] SUCCESS [{status}]: {url}")
    except urllib.error.HTTPError as e:
        print(f"[{idx}/{len(candidates)}] FAILED [{e.code}]: {url}")
    except Exception as e:
        print(f"[{idx}/{len(candidates)}] FAILED [Error]: {url} -> {str(e)}")
