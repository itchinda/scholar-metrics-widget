import requests
from datetime import datetime
import os

SCHOLAR_ID = "0BtIIxcAAAAJ"  # your Google Scholar ID
API_KEY = os.getenv("SERPAPI_KEY")

if not API_KEY:
    raise ValueError("Set SERPAPI_KEY as an environment variable or GitHub secret.")

# Fetch metrics via SerpAPI
params = {
    "engine": "google_scholar_author",
    "author_id": SCHOLAR_ID,
    "api_key": API_KEY
}

response = requests.get("https://serpapi.com/search", params=params)
data = response.json()

try:
    citations = data["cited_by"]["all"]        # total citations
    h_index = data["h_index"]["all"]           # h-index
    i10_index = data["i10_index"]["all"]       # i10-index
except KeyError:
    raise ValueError("Cannot parse response from SerpAPI. Check your Scholar ID and API key.")

# Generate index.html
html = f"""
<html>
<head>
<meta charset="UTF-8">
<style>
body {{ font-family: Arial, sans-serif; }}
.metric {{ font-size: 1.2em; margin: 5px 0; }}
</style>
</head>
<body>
<div class="metric"><strong>Citations:</strong> {citations}</div>
<div class="metric"><strong>h-index:</strong> {h_index}</div>
<div class="metric"><strong>i10-index:</strong> {i10_index}</div>
<p>Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Metrics updated: Citations={citations}, h-index={h_index}, i10-index={i10_index}")
