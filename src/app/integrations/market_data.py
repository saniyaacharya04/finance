import os
import requests

def lookup(symbol):
    api_key = os.getenv("API_KEY")
    if not api_key:
        return None

    url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "price" not in data:
        return None

    return {
        "name": data.get("name", symbol),
        "price": float(data["price"]),
        "symbol": symbol.upper()
    }
