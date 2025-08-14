import signal
import sys
from scholarly import scholarly

# CONFIG — your Google Scholar author ID (the part after "user=" in your profile URL)
SCHOLAR_ID = "0BtIIxcAAAAJ"

# Timeout handler
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

# Set a max execution time (seconds)
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(20)  # 20 sec timeout

try:
    # Search and fetch only indices (fast mode)
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=["indices"])

    citations = author["citedby"]
    h_index = author["hindex"]
    i10_index = author["i10index"]

    # Build HTML output
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="86400"> <!-- refresh daily -->
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .metric {{ font-size: 1.2em; margin: 5px 0; }}
        </style>
    </head>
    <body>
        <div class="metric"><strong>Citations:</strong> {citations}</div>
        <div class="metric"><strong>h-index:</strong> {h_index}</div>
        <div class="metric"><strong>i10-index:</strong> {i10_index}</div>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Metrics updated: Citations={citations}, h-index={h_index}, i10-index={i10_index}")

except TimeoutException:
    print("⏳ Fetching metrics took too long — skipping update.")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error fetching metrics: {e}")
    sys.exit(1)
finally:
    signal.alarm(0)  # Cancel timeout
