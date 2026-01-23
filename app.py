from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = "insurance-baccarat-secret"

# ===== USUÁRIOS =====
USERS = {
    "admin123": {"password": "admin123", "hours": 24},
    "plano1h": {"password": "p1h", "hours": 1},
    "plano3h": {"password": "p3h", "hours": 3},
    "plano5h": {"password": "p5h", "hours": 5},
}

# ===== LOGIN =====
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]

        if user in USERS and USERS[user]["password"] == pw:
            session["user"] = user
            session["expires"] = (
                datetime.now() + timedelta(hours=USERS[user]["hours"])
            ).timestamp()
            return redirect(url_for("index"))
        return render_template("login.html", error=True)

    return render_template("login.html")


# ===== BOT =====
@app.route("/bot")
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    if datetime.now().timestamp() > session["expires"]:
        return render_template("expired.html")

    return render_template("index.html")


# ===== LOGOUT =====
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
