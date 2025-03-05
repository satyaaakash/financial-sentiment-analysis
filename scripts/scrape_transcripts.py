import requests
from bs4 import BeautifulSoup
import os

def scrape_transcript(ticker):
    url = f"https://www.cnbc.com/quotes/{ticker}/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve transcripts for {ticker}. Status Code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Try to find earnings transcript section
    paragraphs = soup.find_all("p")

    if not paragraphs:
        print("No transcript data found!")
        return
    
    transcript = "\n".join([p.text for p in paragraphs])

    os.makedirs("../data/raw", exist_ok=True)
    with open(f"../data/raw/{ticker}_transcript.txt", "w") as f:
        f.write(transcript)
    
    print(f"Saved transcript for {ticker}")

# Example usage
scrape_transcript("AAPL")
