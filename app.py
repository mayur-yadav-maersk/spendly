from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import init_db, create_user, get_user_by_email, get_user_by_username, get_user_by_id

app = Flask(__name__)
app.secret_key = "spendly-dev-secret-key"

init_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return render_template("register.html", error="All fields are required.")
        if len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters.")
        if get_user_by_email(email):
            return render_template("register.html", error="An account with that email already exists.")
        if get_user_by_username(name):
            return render_template("register.html", error="That username is already taken.")

        pw_hash = generate_password_hash(password)
        create_user(name, email, pw_hash)
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            return render_template("login.html", error="All fields are required.")

        user = get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid email or password.")

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("profile"))

    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("1.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    db_user = get_user_by_id(session["user_id"])
    if db_user is None:
        abort(404)

    from datetime import datetime
    try:
        member_since = datetime.strptime(db_user["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y")
    except (ValueError, TypeError):
        member_since = db_user["created_at"]

    user = {
        "username": db_user["username"],
        "email": db_user["email"],
        "member_since": member_since,
    }
    stats = {
        "total_spent": "₹12,450.00",
        "transaction_count": 24,
        "top_category": "Food",
    }
    transactions = [
        {"date": "Apr 15, 2026", "description": "Lunch at café",        "category": "Food",      "amount": "₹350.00"},
        {"date": "Apr 14, 2026", "description": "Monthly bus pass",     "category": "Transport", "amount": "₹1,200.00"},
        {"date": "Apr 12, 2026", "description": "Netflix subscription", "category": "Utilities", "amount": "₹649.00"},
        {"date": "Apr 10, 2026", "description": "Grocery shopping",     "category": "Food",      "amount": "₹2,100.00"},
        {"date": "Apr 08, 2026", "description": "Dinner with friends",  "category": "Food",      "amount": "₹890.00"},
    ]
    categories = [
        {"name": "Food",      "amount": "₹6,540.00", "percent": 52},
        {"name": "Transport", "amount": "₹2,400.00", "percent": 19},
        {"name": "Utilities", "amount": "₹1,948.00", "percent": 16},
        {"name": "Shopping",  "amount": "₹1,562.00", "percent": 13},
    ]
    return render_template("profile.html",
                           user=user, stats=stats,
                           transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
