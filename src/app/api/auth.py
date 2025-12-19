from flask import Blueprint, render_template, request, redirect, session

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Placeholder: real logic will be restored later
        session["user_id"] = 1
        return redirect("/")
    return render_template("login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Placeholder: real logic will be restored later
        return redirect("/login")
    return render_template("register.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
