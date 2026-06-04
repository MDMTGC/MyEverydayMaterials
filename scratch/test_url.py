import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://www.ewg.org/news-insights/news/2023/10/ewg-verified-pet-grooming-products-are-here"
try:
    req = urllib.request.Request(url, headers=headers, method='GET')
    with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
        print(f"STATUS for {url}: {response.status}")
except urllib.error.HTTPError as e:
    print(f"FAILED for {url} with code {e.code}")
except Exception as e:
    print(f"FAILED for {url} with error {e}")
