from flask import Blueprint, render_template, request
from app.core.security import login_required
from app.services.quote_service import get_quote

bp = Blueprint("quotes", __name__)

@bp.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = get_quote(symbol)

        if not quote:
            return render_template("apology.html", message="Invalid symbol")

        return render_template("quote.html", quote=quote)

    return render_template("quote.html")
