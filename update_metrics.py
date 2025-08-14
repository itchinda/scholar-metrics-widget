import requests
from datetime import datetime
import os
import sys

# -----------------------------
# CONFIG
# -----------------------------
SCHOLAR_ID = "0BtIIxcAAAAJ"  # Replace with your Scholar ID
API_KEY = os.getenv("SERPAPI_KEY")
OUTPUT_FILE = "index.html"

if not API_KEY:
    print("❌ SERPAPI_KEY environment variable not set.")
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
try:
    # New SerpAPI structure
    author = data.get("author", {})
    cited_by = author.get("cited_by", {})
    citations = cited_by.get("total", "N/A")
    h_index = author.get("h_index", "N/A")
    i10_index = author.get("i10_index", "N/A")
except Exception as e:
    print(f"❌ Error parsing metrics: {e}")
    print(data)  # full JSON for debugging
    sys.exit(1)

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
