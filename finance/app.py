import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date

from helpers import apology, login_required, lookup, usd

# export API_KEY=pk_c5b85687c31a499e8231e2ac1d833dff

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded


app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'
# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use POSTGRES database
db = SQL("sqlite:///finance.db")
# db = SQL(os.getenv("DATABASE_URI"))

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    stocks = db.execute(
        'SELECT symbol, name, price, SUM(shares) as TotalShares FROM transactions WHERE user_id = ? GROUP BY symbol', user_id)
    cash = db.execute('SELECT cash FROM users WHERE id = ?', user_id)[0]["cash"]

    total = cash

    for stock in stocks:
        total += stock["price"] * stock["TotalShares"]

    return render_template("index.html", stocks=stocks, cash=cash, usd=usd, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        # get the info from the form
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))  # converting shares from str into int
        db_symbol = lookup(symbol)
        # check if symbol and shares were entered correctly
        if symbol == "":
            return apology("The symbol is blank.")
        elif not db_symbol:
            return apology("Invalid symbol.")
        elif shares <= 0:
            return apology("The amount of shares should be positive.")
        else:
            # getting the info about the share from database
            symbol_name = db_symbol["name"]
            price = db_symbol["price"]
            # symbol = session["symbol"]
            user_id = session["user_id"]

            cash = db.execute('SELECT cash FROM users WHERE id = ?', user_id)[0]['cash']

            if cash < price:
                return apology("Not enough cash to buy the share.")
            else:
                remain = cash - price * shares
                # deduct order cost from user's remaining balance
                db.execute("UPDATE users SET cash = ? WHERE id = ?", remain, user_id)
                db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)",
                           user_id, symbol_name, shares, price, 'buy', symbol)

    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    query = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY id DESC", session["user_id"])
    return render_template("history.html", query=query)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        check = lookup(symbol)
        if not check:
            return render_template("quote.html")
        return render_template("quoted.html", name=check["name"], price=usd(check["price"]), symbol=check["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # getting the data from the form
        name = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        if name == "":
            return apology("The name is blank.")
        elif len(db.execute('SELECT username FROM users WHERE username = ?', name)) > 0:
            return apology("This username already exists.")
        elif password == "":
            return apology("The password is blank.")
        elif password != confirm:
            return apology("Confirmation doesn't match the password.")
        # add user to a database
        db.execute('INSERT INTO users (username, hash) VALUES (?, ?)', name, generate_password_hash(password))
        # start the session (log user in)
        user = db.execute('SELECT * FROM users WHERE username = ?', name)
        session["user_id"] = user[0]["id"]
        # return to a home page (index)
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols = db.execute('SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol', user_id)
        return render_template("sell.html", symbols=symbols)
    else:
        user_id = session["user_id"]
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if shares <= 0:
            return apology("Shares must be a possitive number.")
        share_price = lookup(symbol)["price"]
        share_name = lookup(symbol)["name"]
        price = shares * share_price
        # check if the user has a share in the transactions db
        shares_owned = db.execute('SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol',
                                  user_id, symbol)[0]['shares']

        if shares_owned < shares:
            return apology("You don't have this many shares.")
        # update the cash user has
        current_cash = db.execute('SELECT cash FROM users WHERE id = ?', user_id)[0]['cash']
        db.execute('UPDATE users SET cash = ? WHERE id = ?', current_cash + price, user_id)

        # update the transactions table
        db.execute('INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)',
                   user_id, share_name, -shares, share_price, 'sel', symbol)

        return redirect("/")


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    if request.method == "GET":
        return render_template("addcash.html")
    else:
        amount = request.form.get("amount")
        if amount == None:
            return apology("Invalid input")
        else:
            capital = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            db.execute("UPDATE users SET cash = ? WHERE id = ?", (float(capital[0]["cash"]) + float(amount)), session["user_id"])
            flash('Cash added sucessfully!')
            return redirect("/")