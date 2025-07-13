from helpers import apology, login_required, lookup, usd
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
import os
import logging
logging.basicConfig(level=logging.DEBUG)


# Configure application
app = Flask(__name__)

# Custom filter for USD formatting
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Get user's current cash balance
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Get stocks owned by the user
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        user_id
    )

    # Calculate stock values
    total_value = cash
    for stock in stocks:
        stock_info = lookup(stock["symbol"])
        stock["name"] = stock_info["name"]
        stock["price"] = stock_info["price"]
        stock["total"] = stock["price"] * stock["total_shares"]
        total_value += stock["total"]

    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote"""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Please enter a stock symbol.", 400)

        symbol = symbol.strip().upper()

        stock = lookup(symbol)

        if not stock:
            return apology("Invalid stock symbol!", 400)

        return render_template("quote.html", stock=stock)

    return render_template("quote.html", stock=None)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return apology("Stock symbol and shares are required!", 400)

        if not shares.isdigit() or int(shares) <= 0:
            return apology("Shares must be a positive integer!", 400)

        symbol = symbol.upper()
        stock = lookup(symbol)

        if not stock:
            return apology("Invalid stock symbol!", 400)

        cost = stock["price"] * int(shares)
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        if cost > user_cash:
            return apology("Insufficient funds!", 400)

        # Update database
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, int(shares), stock["price"])
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])

        flash(f"Successfully bought {shares} shares of {symbol}!", "success")
        return redirect("/")

    return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", user_id)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return apology("Stock symbol and shares are required!", 400)

        if not shares.isdigit() or int(shares) <= 0:
            return apology("Shares must be a positive integer!", 400)

        shares = int(shares)
        user_shares = db.execute(
            "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)[0]["total_shares"]

        if shares > user_shares:
            return apology("Not enough shares!", 400)

        stock = lookup(symbol)
        total_sale = stock["price"] * shares

        # Update database
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, -shares, stock["price"])
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale, user_id)

        flash(f"Successfully sold {shares} shares of {symbol}!", "success")
        return redirect("/")

    return render_template("sell.html", stocks=stocks)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("All fields are required!", 400)

        if password != confirmation:
            return apology("Passwords do not match!", 400)

        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            return apology("Username already exists!", 400)

        # Hash password and store user in DB
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        flash("Registered successfully! Please log in.", "success")
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Invalid username and/or password!", 400)

        session["user_id"] = rows[0]["id"]
        flash("Logged in successfully!", "success")
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect("/login")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow users to change password"""
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]

        if not check_password_hash(user["hash"], current_password):
            return apology("Incorrect password", 400)

        new_hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, session["user_id"])

        flash("Password successfully changed", "success")
        return redirect("/")

    return render_template("change_password.html")
