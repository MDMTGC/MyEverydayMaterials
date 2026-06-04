import urllib.request
import ssl

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH2cwrpBjkfddcuRQ8_4o6tiQSVoVI8HNYrPC5RFRTXz7sY5joxhPlT3e6YqT--8bRKpnoXV5qpntG9ispy4oc8v4LmCgVZp3YM4yHvOWEHp7xmFhLEpRk6fFD04Ru5VfaKdNK6ekMQ4odqIw=="

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
