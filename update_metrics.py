from scholarly import scholarly
from datetime import datetime
import os

# CONFIG
SCHOLAR_ID = "0BtIIxcAAAAJ"  # <-- Replace with your ID
OUTPUT_FILE = "index.html"  # GitHub Pages will serve this

# Fetch Scholar data
author = scholarly.search_author_id(SCHOLAR_ID)
author = scholarly.fill(author, sections=["indices"])
indices = author["indices"]

citations = indices["citations"]["all"]
h_index = indices["hindex"]["all"]
i10_index = indices["i10index"]["all"]

# HTML Template
html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>My Google Scholar Metrics</title>
<style>
body {{ font-family: Arial, sans-serif; }}
.metrics {{ display: flex; gap: 20px; font-size: 18px; }}
.metric {{ background: #f3f3f3; padding: 10px; border-radius: 8px; }}
</style>
</head>
<body>
<h2>Google Scholar Metrics</h2>
<div class="metrics">
    <div class="metric">Citations: <b>{citations}</b></div>
    <div class="metric">h-index: <b>{h_index}</b></div>
    <div class="metric">i10-index: <b>{i10_index}</b></div>
</div>
<p>Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
</body>
</html>
"""

# Save to file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Metrics updated and written to {OUTPUT_FILE}")

