import random
import time

import pandas as pd
from bs4 import BeautifulSoup
from curl_cffi import requests as cffi_requests

# 1. Target: electricians in Greenacres, FL on YellowPages
BASE_URL = "https://www.yellowpages.com/search"
HOMEPAGE = "https://www.yellowpages.com/"
SEARCH_WHAT = "electricians"
SEARCH_WHERE = "Greenacres, FL"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": HOMEPAGE,
    "Upgrade-Insecure-Requests": "1",
}

# Session impersonates Chrome's TLS fingerprint and carries cookies
session = cffi_requests.Session(impersonate="chrome")

all_leads = []
seen = set()  # (name, phone) dedupe — same business appears in organic + paid slots
total_pages_to_scrape = 3  # Each YP page holds ~30 listings


def pick(parent, selectors):
    """Try a list of (tag, class) selectors, return the first match."""
    for tag, cls in selectors:
        el = parent.find(tag, class_=cls)
        if el:
            return el
    return None


# Warm up the session on the homepage to collect cookies first
warmup = session.get(HOMEPAGE, headers=HEADERS, timeout=15)
print(f"Session warmup: {warmup.status_code}, cookies: {len(session.cookies)}")
time.sleep(2)

for page in range(1, total_pages_to_scrape + 1):
    print(f"Scraping page {page}...")

    # YellowPages pagination uses ?page=N
    params = {
        "search_terms": SEARCH_WHAT,
        "geo_location_terms": SEARCH_WHERE,
        "page": page,
    }

    try:
        response = session.get(
            BASE_URL, headers=HEADERS, params=params, timeout=15
        )
        if response.status_code != 200:
            print(f"Failed to load page {page}. Status: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # 2. Listing container on YellowPages: div.result (organic listings)
        listings = soup.find_all("div", class_="result")

        if not listings:
            print("No listings found — selectors may be stale or the page is blocked.")
            break

        for business in listings:
            # 3. Business name — YP uses a.business-name; fall back to h2 link
            name_el = pick(business, [("a", "business-name")])
            if not name_el:
                h2 = business.find("h2")
                name_el = h2.find("a") if h2 else None
            name = name_el.get_text(strip=True) if name_el else "N/A"
            if name == "N/A":
                continue  # Skip ad/banner blocks with no business name

            # 4. Phone number
            phone_el = pick(business, [
                ("div", "phones phone primary"),
                ("div", "phones"),
                ("div", "phone"),
            ])
            phone = phone_el.get_text(strip=True) if phone_el else "N/A"

            if (name, phone) in seen:
                continue  # Same business already captured from another slot
            seen.add((name, phone))

            # 5. Address (street + city/state/zip)
            street_el = pick(business, [
                ("div", "street-address"),
                ("span", "street-address"),
            ])
            locality_el = pick(business, [
                ("div", "locality"),
                ("span", "locality"),
            ])
            parts = [
                el.get_text(strip=True)
                for el in (street_el, locality_el)
                if el
            ]
            address = ", ".join(parts) if parts else "N/A"

            # 6. Website detection (verified against live YP markup):
            #    the real website link always has anchor text "Website".
            #    Organic listings carry no class; paid use track-visit-website.
            #    localsearch.com = YP-hosted template page -> NOT a real site.
            website_url = "None"
            website_status = "No Website"
            for a in business.find_all("a", href=True):
                text = a.get_text(strip=True).lower()
                cls = " ".join(a.get("class", []))
                href = a["href"]
                if text != "website" and "track-visit-website" not in cls:
                    continue
                if not href.startswith("http") or "yellowpages.com" in href:
                    continue
                if "localsearch.com" in href:
                    website_status = "Template Site (YP-hosted)"
                    website_url = href
                    break
                website_status = "Has Website"
                website_url = href
                break

            all_leads.append({
                "Business Name": name,
                "Phone": phone,
                "Address": address,
                "Website Status": website_status,
                "Website URL": website_url,
            })

        # Randomized delay to look human and avoid IP flagging
        time.sleep(3 + random.uniform(0, 2))

    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Save the filtered targets to CSV
df = pd.DataFrame(all_leads)
# Prime leads = no real website (includes YP-hosted template sites)
no_website_df = (
    df[df["Website Status"] != "Has Website"] if not df.empty else df
)

df.to_csv("all_scraped_leads.csv", index=False)
no_website_df.to_csv("local_leads_without_websites.csv", index=False)

print("\nScraping complete!")
print(f"Total leads saved: {len(df)}")
print(f"Leads without real websites saved: {len(no_website_df)}")
if not df.empty:
    print(df["Website Status"].value_counts().to_string())
