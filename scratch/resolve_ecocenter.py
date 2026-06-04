import urllib.request
import ssl

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHkuatalerRif5Bk5LifRlf0wOm2z1ekFjXq0AgsCx8DPfy4UOaIcK455avxWVFq58bDkjbDVSxBLSmwSmxVLsBav4eEo5h63LGVY1qOeSu4uYEjI_qWeP6tZ1f8ZaPia7C_Rp8Xr6yziYg13Low1u9ABZEPJ1DO2YLPGCDEFLGczEPfw=="

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
