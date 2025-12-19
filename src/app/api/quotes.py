from flask import Blueprint, render_template, request, abort, session
from app.core.security import login_required
from app.services.quote_service import get_quote
from app.services.usage_service import increment_quotes, quotes_used_today
from app.services.portfolio_service import get_user_plan
from app.domain.plan import PLAN_LIMITS

bp = Blueprint("quotes", __name__)

@bp.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    user_id = session.get("user_id")
    plan = get_user_plan(user_id)

    if request.method == "POST":
        used = quotes_used_today()
        limit = PLAN_LIMITS[plan]["quotes_per_day"]

        if used >= limit:
            abort(403, description="Free tier limit reached. Upgrade to continue.")

        symbol = request.form.get("symbol")
        quote = get_quote(symbol)

        if not quote:
            return render_template("apology.html", message="Invalid symbol")

        increment_quotes()
        return render_template("quote.html", quote=quote)

    return render_template("quote.html")
