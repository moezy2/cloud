from flask import Flask, jsonify, request
import primp
import re
from urllib.parse import urljoin

app = Flask(__name__)  # required for gunicorn to work

def extract_property_links(url):
    """Extract property links from the given URL"""
    print(f"🔍 Fetching page: {url}")
    
    try:
        client = primp.Client(
            impersonate="chrome_131",
            impersonate_os="windows",
            timeout=30,
            follow_redirects=True
        )

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        resp = client.get(url, headers=headers)

        print(f"✅ Status Code: {resp.status_code}")
        print(f"📄 Content Length: {len(resp.content)} bytes")

        if resp.status_code != 200:
            print(f"❌ Request failed with status {resp.status_code}")
            return [], []

        pattern = r'href="(/programmes-strategies/housing-and-land/homes-londoners/search/property/[^"]*)"'
        matches = re.findall(pattern, resp.text)

        unique_links = []
        seen = set()
        for link in matches:
            if link not in seen:
                unique_links.append(link)
                seen.add(link)

        print(f"🏠 Found {len(unique_links)} unique property links")

        base_url = "https://www.london.gov.uk"
        full_links = [urljoin(base_url, link) for link in unique_links]

        return full_links, unique_links

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return [], []

@app.route("/", methods=["GET"])
def index():
    return "PRIMP Property Extractor API is live."

@app.route("/extract", methods=["GET"])
def extract():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' query parameter"}), 400

    full_links, _ = extract_property_links(url)
    return jsonify({
        "count": len(full_links),
        "links": full_links
    })

