import urllib.request
import ssl

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEbnFuNUVPrKqfDdoyXYU-TazBveE4w4j7m_tJDVjEBSLtx-6dx6fVcjcTEg28cMNrwokSGm3Ed0cA2COG9wlsklNJphHOUjr2hFktZ6DoW1xuZ_Gv2Jzlv9GbqF8VIwc9zqvXIdWtHbw=="

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
)

try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
        print("Final URL:", response.geturl())
        print("Status code:", response.status)
except Exception as e:
    print("Error:", e)
