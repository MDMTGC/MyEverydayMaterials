import urllib.request
import urllib.error
import ssl

urls = [
    "https://www.bfr.bund.de/cm/343/xv-silicones.pdf",
    "https://www.bfr.bund.de/cm/343/xv-silicones-en.pdf",
    "https://www.bfr.bund.de/cm/343/xv-silicone-en.pdf",
    "https://www.bfr.bund.de/cm/343/xv-silicones-de.pdf"
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
            print(f"SUCCESS [{response.status}]: {url}")
    except urllib.error.HTTPError as e:
        print(f"FAILED [{e.code}]: {url}")
    except Exception as e:
        print(f"FAILED [Error]: {url} -> {str(e)}")
