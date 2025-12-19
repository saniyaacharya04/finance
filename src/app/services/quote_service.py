from app.integrations.market_data import lookup

def get_quote(symbol):
    return lookup(symbol)
