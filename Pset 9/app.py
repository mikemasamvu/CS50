import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    total_shares = 0
    company_info = db.execute(
        "SELECT company.name, symbol, SUM(shares) FROM purchases JOIN company ON purchases.company_id = company.id WHERE purchases.person_id = ? GROUP BY symbol", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    for info in company_info:
        price = lookup(info["symbol"])["price"]
        total = price * info["SUM(shares)"]
        info["price"] = usd(price)
        info["total"] = usd(total)
        total_shares += total

    return render_template("index.html", company_info=company_info, cash=usd(cash), total=usd(total_shares + cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        dict = lookup(request.form.get("symbol"))
        row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if dict == None:
            return apology("stock symbol doesn't exist", 400)
        try:
            if int(request.form.get("shares")) <= 0:
                return apology("Input valid shares", 400)
        except ValueError:
            return apology("Input valid shares", 400)

        if len(row) != 0:
            if row[0]["cash"] < dict["price"] * int(request.form.get("shares")):
                return apology("cannot afford shares", 400)
            company = db.execute("SELECT * FROM company WHERE symbol = ?", dict["symbol"])
            if len(company) == 0:
                db.execute("INSERT INTO company(name, price, symbol) VALUES(?, ?, ?)", dict["name"], dict["price"], dict["symbol"])

            company = db.execute("SELECT * FROM company WHERE symbol = ?", dict["symbol"])
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            db.execute("INSERT INTO purchases(person_id, company_id, shares, status, date) VALUEs(?, ?, ?, ?, ?)",
                       session["user_id"], company[0]["id"], int(request.form.get("shares")), "BOUGHT", date_time)
            db.execute("UPDATE users SET cash = cash - (? * ?) WHERE id = ?",
                       float(dict["price"]), int(request.form.get("shares")), session["user_id"])

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    company_info = db.execute(
        "SELECT symbol, shares, shares * price,status, date FROM purchases JOIN company ON purchases.company_id = company.id WHERE person_id = ?", session["user_id"])

    for info in company_info:
        info["money_transacted"] = usd(info["shares * price"])
    return render_template("history.html", company_info=company_info)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        dict = lookup(request.form.get("symbol"))
        if dict == None:
            return apology("stock symbol doesn't exist", 400)
        else:
            return render_template("quoted.html", name=dict["name"], price=usd(dict["price"]), symbol=dict["symbol"])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("The passwords must match", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            if rows[0]["username"] == request.form.get("username"):
                return apology("username already exists", 400)
        db.execute("INSERT INTO users(username, hash) VALUES(?,?)",
                   request.form.get("username"), generate_password_hash(request.form.get("password")))

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Input symbol")
        if not request.form.get("shares"):
            return apology("Input shares")

        info = db.execute("SELECT symbol, SUM(shares), company.id FROM purchases JOIN company ON purchases.company_id = company.id WHERE person_id = ? AND symbol = ?",
                          session["user_id"], request.form.get("symbol"))
        if int(request.form.get("shares")) > info[0]["SUM(shares)"]:
            return apology("Overselling shares")

        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
        db.execute("UPDATE users SET cash = cash + (? * ?) WHERE id = ?",
                   usd(lookup(request.form.get("symbol"))["price"]), int(request.form.get("shares")), session["user_id"])

        db.execute("INSERT INTO purchases(person_id, company_id, shares, status, date) VALUEs(?, ?, ?, ?, ?)",
                   session["user_id"], info[0]["id"], -int(request.form.get("shares")), "SOLD", date_time)
        return redirect("/")

    else:
        info = db.execute(
            "SELECT symbol FROM purchases JOIN company ON purchases.company_id = company.id WHERE person_id = ? GROUP BY symbol", session["user_id"])
        return render_template("sell.html", symbols=info)


@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    """Add cash"""
    if request.method == "POST":
        if not request.form.get("cash"):
            return apology("Input cash amount")

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        cash += float(request.form.get("cash"))
        db.execute("UPDATE users SET cash = ?", cash)

        return redirect("/")

    else:
        return render_template("cash.html")