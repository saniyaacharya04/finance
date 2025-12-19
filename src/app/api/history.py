from flask import Blueprint, render_template, session
from app.core.security import login_required
from app.services.portfolio_service import get_portfolio, get_cash

bp = Blueprint("history", __name__)

@bp.route("/")
@login_required
def index():
    portfolio = get_portfolio()
    cash = get_cash()

    total = cash
    holdings = []

    for symbol, shares in portfolio.items():
        holdings.append({
            "symbol": symbol,
            "shares": shares,
            "price": 0,   # placeholder, no live lookup here
            "total": 0
        })

    return render_template(
        "index.html",
        portfolio=holdings,
        cash=cash,
        total=total
    )

@bp.route("/history")
@login_required
def history():
    transactions = session.get("transactions", [])
    return render_template("history.html", transactions=transactions)
