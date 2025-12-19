from flask import session
from datetime import date

def _today():
    return date.today().isoformat()

def get_usage():
    usage = session.get("usage", {})
    today = _today()
    return usage.get(today, {"quotes": 0})

def increment_quotes():
    usage = session.get("usage", {})
    today = _today()

    if today not in usage:
        usage[today] = {"quotes": 0}

    usage[today]["quotes"] += 1
    session["usage"] = usage

def quotes_used_today():
    return get_usage().get("quotes", 0)
