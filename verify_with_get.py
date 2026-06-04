import re
import urllib.request
import urllib.error
import urllib.parse
import ssl
import sys

# Flagged URLs from sources-needing-review.md
urls = [
    "https://www.epa.gov/indoor-air-quality-iaq/indoor-air-facts-no-4-sick-building-syndrome",
    "https://www.lung.org/clean-air/at-home/indoor-air-pollutants/cleaning-supplies",
    "https://www.alz.org/alzheimers-dementia/what-is-alzheimers/causes-and-risk-factors/myths",
    "https://www.lung.org/clean-air/at-home/indoor-air-pollutants/cleaning-supplies-and-household-chemicals",
    "https://www.bfr.bund.de/cm/349/bamboo-melamine-tableware-frequent-use-can-be-harmful-to-health.pdf",
    "https://www.fda.gov/food/chemicals/melamine-tableware",
    "https://www.efsa.europa.eu/en/topics/topic/melamine",
    "https://echa.europa.eu/registration-dossier/-/registered-dossier/15399",
    "https://www.cdc.gov/biomonitoring/pdf/BisphenolA_FactSheet.pdf",
    "https://www.ecocenter.org/toxic-inequities-2022-car-seat-report",
    "https://www.poison.org/articles/caustic-ingestions-2016",
    "https://www.epa.gov/pets/avoid-double-dosing-pets-flea-and-tick-products",
    "https://www.petpoisonhelpline.com/poison/permethrin-toxicity-in-cats/",
    "https://www.cdc.gov/niosh/docs/2011-125/",
    "https://www.lung.org/clean-air/at-home/indoor-air-pollutants/cleaning-supplies-and-household-chemicals",
    "https://www.petpoisonhelpline.com/pet-safety-tips/essential-oils-and-cats/",
    "https://www.cdc.gov/niosh/topics/fibreglass/",
    "https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/flame-retardants-furniture-and-building-materials",
    "https://www.ewg.org/healthyhome/flame-retardants",
    "https://www.epa.gov/formaldehyde/formaldehyde-your-home-what-you-need-know",
    "https://ww2.arb.ca.gov/our-work/programs/composite-wood-products-atcm",
    "https://www.ewg.org/news-insights/news/2023/10/ewg-verified-pet-grooming-products-are-here",
    "https://www.avma.org/resources/pet-owners/petcare/grooming",
    "https://www.healthychildren.org/English/ages-stages/baby/crying-colic/Pages/Pacifiers-Satisfying-Your-Babys-Needs.aspx",
    "https://www.fda.gov/food/food-ingredients-packaging/food-contact-substances-fcs",
    "https://www.fda.gov/food/chemicals/melamine-tableware",
    "https://vcahospitals.com/know-your-pet/feline-acne",
    "https://www.fda.gov/food/chemicals/melamine-tableware",
    "https://www.niehs.nih.gov/news/newsroom/releases/2022/october17",
    "https://www.nih.gov/news-events/news-releases/hair-straightening-products-associated-uterine-cancer-risk",
    "https://www.ewg.org/news-insights/news-release/2022/10/study-hair-straighteners-linked-uterine-cancer-risk",
    "https://www.cosmeticseurope.eu/files/8115/3717/9986/Recommendation_14_Mineral_Hydrocarbons_in_Cosmetic_Lip_Care_Products.pdf",
    "https://www.bfr.bund.de/cm/349/highly-refined-mineral-oils-in-cosmetics-health-risks-are-not-to-be-expected-according-to-current-knowledge.pdf",
    "https://www.epa.gov/trash-free-waters/microplastics-research",
    "https://www.aad.org/public/diseases/eczema/types/contact-dermatitis/signs-symptoms",
    "https://www.ewg.org/the-toxic-twenty/formaldehyde-releasers",
    "https://www.fda.gov/cosmetics/cosmetic-ingredients/formaldehyde-cosmetics-what-you-should-know",
    "https://www.ewg.org/the-toxic-twenty/parabens",
    "https://ww2.arb.ca.gov/our-work/programs/perchloroethylene-dry-cleaning",
    "https://monographs.iarc.who.int/agents-classified-by-the-iarc-monographs/",
    "https://www.ewg.org/news-insights/news-release/2019/01/new-study-links-oral-b-glide-floss-higher-levels-toxic-pfas-chemicals",
    "https://www.niehs.nih.gov/health/topics/agents/pfas",
    "https://www.cdc.gov/biomonitoring/pdf/Phthalates_FactSheet.pdf",
    "https://www.niehs.nih.gov/health/topics/agents/phthalates",
    "https://www.ewg.org/news-insights/news/2022/08/whats-fragrance-phthalates-and-other-chemicals-your-scented-products",
    "https://echa.europa.eu/hot-topics/phthalates",
    "https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-asthma-what-you-need-know/health-information/feline-health-topics/feline-lower-urinary-tract-disease",
    "https://www.niehs.nih.gov/health/topics/agents/bpa/",
    "https://www.atsdr.cdc.gov/ToxProfiles/tp218.pdf",
    "https://www.tuftsyourdog.com/dog-health/flame-retardants-and-pets/",
    "https://www.who.int/health-topics/endocrine-disrupting-chemicals",
    "https://www.cdc.gov/biomonitoring/Phthalates_FactSheet.html",
    "https://www.niehs.nih.gov/health/topics/agents/phthalates/index.cfm",
    "https://silentspring.org/phthalates",
    "https://www.ecocenter.org/healthy-stuff/chemicals-pet-products",
    "https://www.ewg.org/news-insights/news/2023/05/skip-quats-your-cleaning-routine",
    "https://www.aoecdata.org/",
    "https://www.bfr.bund.de/cm/349/silicone_moulds_for_baking.pdf",
    "https://lancaster.unl.edu/hort/articles/2006/bakingsoda.shtml",
    "https://cir-safety.org/sites/default/files/SLS.pdf",
    "https://www.epa.gov/",
    "https://www.atsdr.cdc.gov/toxprofiledocs/index.html",
    "https://www.fda.gov/cosmetics/cosmetic-ingredients/lead-cosmetics-draft-guidance-recommended-limit",
    "https://www.fda.gov/cosmetics/cosmetic-ingredients/titanium-dioxide-cosmetics",
    "https://www.ewg.org/news-insights/news/2023/11/chemicals-ewg-verified-products-must-avoid",
    "https://www.who.int/publications-detail-redirect/9789241546553",
    "https://www.epa.gov/indoor-air-quality-iaq/guide-indoor-air-quality",
    "https://www.atsdr.cdc.gov/sites/toxics_futures/vocs.html",
    "https://silentspring.org/factsheets/carpets"
]

# Deduplicate
urls = sorted(list(set(urls)))

# Bypass SSL errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f"Testing {len(urls)} unique URLs using GET requests...")
for idx, url in enumerate(urls, 1):
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
            status = response.status
            print(f"[{idx}/{len(urls)}] SUCCESS [{status}]: {url}")
    except urllib.error.HTTPError as e:
        print(f"[{idx}/{len(urls)}] FAILED [{e.code}]: {url}")
    except Exception as e:
        print(f"[{idx}/{len(urls)}] FAILED [Error]: {url} -> {str(e)}")
