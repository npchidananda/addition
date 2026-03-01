"""
Indian market indices dashboard - Flask web app.
"""
from flask import Flask, jsonify, render_template

from indices import get_indices, get_stocks

app = Flask(__name__)


def _serialize_items(items):
    out = []
    for item in items:
        out.append({
            "name": str(item.get("name", "")),
            "price": float(item["price"]) if item.get("price") is not None else None,
            "change": float(item["change"]) if item.get("change") is not None else None,
            "pct": float(item["pct"]) if item.get("pct") is not None else None,
        })
    return out


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/indices")
def api_indices():
    indices = _serialize_items(get_indices())
    stocks = _serialize_items(get_stocks())
    return jsonify({"indices": indices, "stocks": stocks})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
