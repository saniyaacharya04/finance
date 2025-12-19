from flask import session

DEFAULT_CASH = 10000

def get_portfolio():
    if "portfolio" not in session:
        session["portfolio"] = {}
    return session["portfolio"]

def get_cash():
    return session.get("cash", DEFAULT_CASH)

def set_cash(amount):
    session["cash"] = amount

def add_stock(symbol, shares, price):
    portfolio = get_portfolio()
    portfolio[symbol] = portfolio.get(symbol, 0) + shares
    set_cash(get_cash() - shares * price)
    session["portfolio"] = portfolio

def remove_stock(symbol, shares, price):
    portfolio = get_portfolio()

    if symbol not in portfolio or portfolio[symbol] < shares:
        return False

    portfolio[symbol] -= shares
    if portfolio[symbol] == 0:
        del portfolio[symbol]

    set_cash(get_cash() + shares * price)
    session["portfolio"] = portfolio
    return True
