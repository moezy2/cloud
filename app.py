#!/usr/bin/env python3
"""
PRIMP Property Links Extractor
Extracts property links from London.gov.uk housing search page
"""

import primp
import re
from urllib.parse import urljoin

def extract_property_links(url):
    """Extract property links from the given URL"""
    
    print(f"🔍 Fetching page: {url}")
    
    try:
        # Create client with Chrome impersonation
        client = primp.Client(
            impersonate="chrome_131",
            impersonate_os="windows",
            timeout=30,
            follow_redirects=True
        )
        
        # Add realistic headers
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        # Make the request
        resp = client.get(url, headers=headers)
        
        print(f"✅ Status Code: {resp.status_code}")
        print(f"📄 Content Length: {len(resp.content)} bytes")
        
        if resp.status_code != 200:
            print(f"❌ Request failed with status {resp.status_code}")
            return []
        
        # Extract property links using regex
        pattern = r'href="(/programmes-strategies/housing-and-land/homes-londoners/search/property/[^"]*)"'
        matches = re.findall(pattern, resp.text)
        
        # Remove duplicates while preserving order
        unique_links = []
        seen = set()
        for link in matches:
            if link not in seen:
                unique_links.append(link)
                seen.add(link)
        
        print(f"🏠 Found {len(unique_links)} unique property links")
        
        # Convert relative URLs to absolute URLs
        base_url = "https://www.london.gov.uk"
        full_links = [urljoin(base_url, link) for link in unique_links]
        
        return full_links, unique_links
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return [], []

def main():
    """Main function"""
    print("🚀 PRIMP Property Links Extractor")
    print("=" * 50)
    
    # The URL you provided
    url = "https://www.london.gov.uk/programmes-strategies/housing-and-land/homes-londoners/search/to-rent/property?location=Barfield+Avenue%2C+London+N20+0DE&search-area=15&minimum-bedrooms=2&min-monthly-rent=none&max-monthly-rent=none&lat=51.6267984&lng=-0.1587195&outside=0&show-advanced-form=0"
    
    # Extract the links
    full_links, relative_links = extract_property_links(url)
    
    if full_links:
        print("\n📋 PROPERTY LINKS FOUND:")
        print("=" * 50)
        
        for i, (full_link, relative_link) in enumerate(zip(full_links, relative_links), 1):
            print(f"{i:2d}. {relative_link}")
            print(f"    Full URL: {full_link}")
            print()
        
        # Save to file
        with open('property_links.txt', 'w') as f:
            f.write("Property Links Found:\n")
            f.write("=" * 50 + "\n\n")
            f.write("Relative Links:\n")
            for link in relative_links:
                f.write(f"{link}\n")
            f.write("\nFull URLs:\n")
            for link in full_links:
                f.write(f"{link}\n")
        
        print(f"💾 Links saved to 'property_links.txt'")
        
        # Return the links for further processing
        return full_links
    
    else:
        print("\n❌ No property links found")
        print("\nPossible reasons:")
        print("1. The page uses JavaScript to load content dynamically")
        print("2. The site is blocking the request")
        print("3. The URL structure has changed")
        print("4. No properties match the search criteria")
        
        return []

if __name__ == "__main__":
    links = main()
    
    # Print summary
    print(f"\n🎯 SUMMARY: Found {len(links)} property links")