import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

from helpers import usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

income = 0



# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Show recent transactions and other dashboard information"""
    fin_info = db.execute(
        "SELECT transaction_id, date, amount, balance FROM transactions ORDER BY date ASC LIMIT 5")
    income = db.execute("SELECT SUM(amount) FROM transactions WHERE amount > 0 GROUP BY amount")[0]["SUM(amount)"]
    expenses = db.execute("SELECT SUM(amount) FROM transactions WHERE amount < 0 GROUP BY amount")[0]["SUM(amount)"]
    balance = income + expenses

    overearn = db.execute(
        "SELECT COUNT(*) FROM transactions WHERE amount > 300")[0]["COUNT(*)"]
    overspend = db.execute(
        "SELECT COUNT(*) FROM transactions WHERE amount < -300")[0]["COUNT(*)"]

    return render_template("index.html",
    fin_info=fin_info, total_income = usd(income), total_expenses = usd(-expenses), total_balance = usd(balance), overearn = overearn, overspend = overspend)


@app.route("/analytics", methods=["GET", "POST"])
def analytics():
    """Show history of transactions"""

    if request.method == "POST":
        date = request.form.get("date")
        fin_info = db.execute(
        "SELECT transaction_id, date, amount, balance FROM transactions WHERE date = ?", date)


        return render_template("analytics.html", fin_info=fin_info)
    else:
        fin_info = db.execute(
        "SELECT transaction_id, date, amount, balance FROM transactions ORDER BY date DESC")
        return render_template("analytics.html", fin_info=fin_info)





@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    """Add transaction"""
    if request.method == "POST":
        balance = float(request.form.get("balance"))
        amount = float(request.form.get("amount"))
        date = request.form.get("date")
        transaction_type = request.form.get("transaction_type")
        

        if transaction_type == "Income":
            db.execute("INSERT INTO transactions(date, amount, balance) VALUES(?, ?, ?)", date, amount, balance+amount)

        if transaction_type == "Expense":
            db.execute("INSERT INTO transactions(balance, amount, date) VALUES(?, ?, ?)", balance-amount, -amount, date)

        return redirect("/")

    else:
        return render_template("transactions.html")