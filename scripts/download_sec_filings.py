import requests
import json
import os
import time

def get_latest_10k_filing(ticker):
    # Manually set CIK for Apple (use this for testing)
    cik = "0000320193"  # Hardcoded CIK for AAPL

    print(f"CIK for {ticker}: {cik}")

    time.sleep(2)  # Prevent rate limiting

    # SEC API for company submissions
    filings_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response = requests.get(filings_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve SEC filings for {ticker}. Status Code: {response.status_code}")
        return

    filings = response.json()

    if "filings" not in filings or "recent" not in filings["filings"]:
        print("No filings found.")
        return

    # Find the latest 10-K filing
    for i, form in enumerate(filings["filings"]["recent"]["form"]):
        if form == "10-K":
            filing_folder = filings["filings"]["recent"]["accessionNumber"][i].replace("-", "")
            primary_document = filings["filings"]["recent"]["primaryDocument"][i]

            filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{filing_folder}/{primary_document}"
            print(f"Latest 10-K filing: {filing_url}")

            os.makedirs("../data/raw", exist_ok=True)
            with open(f"../data/raw/{ticker}_10K.txt", "w") as f:
                f.write(filing_url)

            return

    print(f"No 10-K filings found for {ticker}")

# Example usage
get_latest_10k_filing("AAPL")
