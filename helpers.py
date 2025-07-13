import requests

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    """Look up quote for symbol using CS50's stock API."""
    url = f"https://finance.cs50.io/quote?symbol={symbol.upper()}"
    print(f"Fetching stock data for: {symbol}")  # ✅ Debugging log

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        quote_data = response.json()

        print("API Response:", quote_data)  # ✅ Debugging log

        if "symbol" in quote_data and "latestPrice" in quote_data and "companyName" in quote_data:
            return {
                "name": quote_data["companyName"],
                "price": quote_data["latestPrice"],
                "symbol": quote_data["symbol"]
            }
        else:
            print("Invalid API response:", quote_data)  # ✅ Debugging log
            return None

    except requests.RequestException as e:
        print(f"Request error: {e}")  # ✅ Debugging log
        return None




def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
