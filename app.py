#!/usr/bin/env python3
"""A small Flask app that serves the Fibonacci series."""

import os

from flask import Flask, jsonify, request

app = Flask(__name__)

DEFAULT_N = int(os.environ.get("FIB_DEFAULT_N", 10))


def fibonacci_series(n):
    """Return the first n numbers of the Fibonacci series."""
    series = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series


@app.route("/")
def home():
    return jsonify({
        "message": "Fibonacci API",
        "usage": f"GET /fibonacci?n={DEFAULT_N}",
        "health": "/health",
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/fibonacci")
def fibonacci():
    n = request.args.get("n", default=DEFAULT_N, type=int)
    if n is None or n < 0:
        return jsonify({"error": "query param 'n' must be a non-negative integer"}), 400
    if n > 10000:
        return jsonify({"error": "'n' must be <= 10000"}), 400
    return jsonify({"n": n, "series": fibonacci_series(n)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
