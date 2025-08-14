import json
import requests
from datetime import datetime

# -----------------------------
# CONFIGURATION
# -----------------------------
SCHOLAR_ID = "0BtIIxcAAAAJ"  # Replace with your Scholar ID
SERPAPI_KEY = "YOUR_SERPAPI_KEY"  # Or use os.environ["SERPAPI_KEY"]

# -----------------------------
# FETCH DATA FROM SerpAPI
# -----------------------------
url = f"https://serpapi.com/search.json?engine=google_scholar_author&author_id={SCHOLAR_ID}&hl=en&api_key={SERPAPI_KEY}"
resp = requests.get(url)
data = resp.json()

# -----------------------------
# EXTRACT METRICS
# -----------------------------
try:
    citations = data["cited_by"]["table"][0]["citations"]["all"]
    h_index   = data["cited_by"]["table"][1]["h_index"]["all"]
    i10_index = data["cited_by"]["table"][2]["i10_index"]["all"]
except (KeyError, IndexError, TypeError):
    citations = h_index = i10_index = "N/A"

# -----------------------------
# GENERATE HTML TABLE
# -----------------------------
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}}
.table-container {{
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 10px 15px;
    background-color: #f9f9f9;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    text-align: center;
}}
th, td {{
    padding: 8px 12px;
    border-bottom: 1px solid #ddd;
}}
th {{
    background-color: #0078d7;
    color: white;
    font-weight: bold;
}}
.metric-row td {{
    font-size: 1.1em;
}}
.last-updated {{
    margin-top: 8px;
    font-size: 0.85em;
    color: #555;
    text-align: right;
}}
</style>
</head>
<body>
<div class="table-container">
    <table>
        <tr>
            <th>Metric</th>
            <th>Value</th>
        </tr>
        <tr class="metric-row">
            <td>Citations</td>
            <td>{citations}</td>
        </tr>
        <tr class="metric-row">
            <td>h-index</td>
            <td>{h_index}</td>
        </tr>
        <tr class="metric-row">
            <td>i10-index</td>
            <td>{i10_index}</td>
        </tr>
    </table>
    <div class="last-updated">
        Last updated: {now}
    </div>
</div>
</body>
</html>
"""

# -----------------------------
# WRITE HTML FILE
# -----------------------------
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Metrics updated: Citations={citations}, h-index={h_index}, i10-index={i10_index}")
