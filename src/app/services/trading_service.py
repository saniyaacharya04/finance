from datetime import datetime
from flask import session
from app.services.portfolio_service import add_stock, remove_stock, get_cash

def _record(txn):
    txns = session.get("transactions", [])
    txns.append(txn)
    session["transactions"] = txns

def buy(symbol, shares, price):
    cost = shares * price
    if get_cash() < cost:
        return False

    add_stock(symbol, shares, price)
    _record({
        "type": "BUY",
        "symbol": symbol,
        "shares": shares,
        "price": price,
        "total": shares * price,
        "timestamp": datetime.utcnow().isoformat()
    })
    return True

def sell(symbol, shares, price):
    if not remove_stock(symbol, shares, price):
        return False

    _record({
        "type": "SELL",
        "symbol": symbol,
        "shares": shares,
        "price": price,
        "total": shares * price,
        "timestamp": datetime.utcnow().isoformat()
    })
    return True
