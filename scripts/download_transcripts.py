import yfinance as yf
import json
import os

ticker = "TSLA"  # Change to any ticker

# Fetch earnings data
stock = yf.Ticker(ticker)

# Extract Net Income and convert timestamps to strings
earnings = stock.income_stmt.loc["Net Income"].rename(lambda x: str(x)).to_dict()

# Create directory if not exists
os.makedirs("../data/raw", exist_ok=True)

# Save data as JSON
with open(f"../data/raw/{ticker}_earnings.json", "w") as f:
    json.dump(earnings, f, indent=4)

print(f"Earnings data saved to ../data/raw/{ticker}_earnings.json")
