from app.services.portfolio_service import add_stock, remove_stock, get_cash

def buy(symbol, shares, price):
    cost = shares * price
    if get_cash() < cost:
        return False
    add_stock(symbol, shares, price)
    return True

def sell(symbol, shares, price):
    return remove_stock(symbol, shares, price)
