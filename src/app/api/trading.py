from flask import Blueprint, render_template, request
from app.core.security import login_required
from app.services.trading_service import buy, sell
from app.services.quote_service import get_quote
from app.services.portfolio_service import get_portfolio

bp = Blueprint("trading", __name__)

@bp.route("/buy", methods=["GET", "POST"])
@login_required
def buy_stock():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares", 0))

        quote = get_quote(symbol)
        if not quote or shares <= 0:
            return render_template("apology.html", message="Invalid input")

        if not buy(symbol, shares, quote["price"]):
            return render_template("apology.html", message="Insufficient funds")

        return render_template("buy.html")

    return render_template("buy.html")

@bp.route("/sell", methods=["GET", "POST"])
@login_required
def sell_stock():
    portfolio = get_portfolio()

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares", 0))

        quote = get_quote(symbol)
        if not quote or shares <= 0:
            return render_template("apology.html", message="Invalid input")

        if not sell(symbol, shares, quote["price"]):
            return render_template("apology.html", message="Not enough shares")

        return render_template("sell.html", stocks=portfolio.keys())

    return render_template("sell.html", stocks=portfolio.keys())
