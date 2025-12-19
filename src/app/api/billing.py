from flask import Blueprint, jsonify

bp = Blueprint("billing", __name__, url_prefix="/billing")

@bp.route("/upgrade", methods=["GET", "POST"])
def upgrade():
    return jsonify({"error": "Premium Feature – Upgrade Required"}), 402
