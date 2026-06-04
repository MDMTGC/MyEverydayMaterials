import urllib.request
import ssl

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHhalek8JolrcocZlyuZBXB86MD6MqUMkwt98sqPGMLXRMPB0vpbUUPGUlBxVsjCOJsrZsZeSP-71k0MG0e_5xsmbICR1eCwstPGW6QxAjKyMs5sIgVaD6DmHcLvf7nKjehUBP9O_Tr9RrINPIblM69vOeoMBjgaiZ0fZunOq0ITrAlJiuGJ3mSi9g0evKQZwwcKOuh8jKhruMblvTrE40IMrpG34k258_qgw=="

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
