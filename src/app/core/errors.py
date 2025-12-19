from flask import render_template

def forbidden(e):
    return render_template("apology.html", message=str(e)), 403
