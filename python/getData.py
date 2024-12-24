
import sys
import yfinance as yf
data = yf.download("AAPL")
with open("response.json", "w") as f:
    f.write(data.to_json(orient="records"))


