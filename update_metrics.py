import requests
from datetime import datetime
import os
import sys

# -----------------------------
# CONFIG
# -----------------------------
SCHOLAR_ID = "0BtIIxcAAAAJ"  # Replace with your Scholar ID
API_KEY = os.getenv("SERPAPI_KEY")  # Must be set locally or in GitHub Actions
OUTPUT_FILE = "index.html"

if not API_KEY:
    print("❌ SERPAPI_KEY not set. Set it as an environment variable or GitHub secret.")
    sys.exit(1)

# -----------------------------
# FETCH DATA FROM SERPAPI
# -----------------------------
params = {
    "engine": "google_scholar_author",
    "author_id": SCHOLAR_ID,
    "api_key": API_KEY
}

try:
    response = requests.get("https://serpapi.com/search", params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.RequestException as e:
    print(f"❌ HTTP error: {e}")
    sys.exit(1)
except ValueError:
    print("❌ Failed to parse JSON from SerpAPI.")
    sys.exit(1)

# -----------------------------
# SAFE PARSING OF METRICS
# -----------------------------
cited_table = data.get("cited_by", {}).get("table", [])

def get_all(metric_name):
    """Return the 'all' value from the cited_by table for the given metric."""
    for entry in cited_table:
        if metric_name in entry:
            return entry[metric_name].get("all", "N/A")
    return "N/A"

citations = get_all("citations")
h_index = get_all("h_index")
i10_index = get_all("i10_index")

# -----------------------------
# GENERATE HTML
# -----------------------------
html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{ font-family: Arial, sans-serif; }}
.metric {{ font-size: 1.2em; margin: 5px 0; }}
.container {{ display: flex; gap: 15px; }}
</style>
</head>
<body>
<h3>Google Scholar Metrics</h3>
<div class="container">
    <div class="metric"><strong>Citations:</strong> {citations}</div>
    <div class="metric"><strong>h-index:</strong> {h_index}</div>
    <div class="metric"><strong>i10-index:</strong> {i10_index}</div>
</div>
<p>Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
</body>
</html>
"""

try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Metrics updated: Citations={citations}, h-index={h_index}, i10-index={i10_index}")
except Exception as e:
    print(f"❌ Failed to write {OUTPUT_FILE}: {e}")
    sys.exit(1)
