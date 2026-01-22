from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "segredo_super_simples"

USERS = {
    "admin123": "admin123",
    "basic001": "basic001",
    "pro001": "pro001"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")

        if user in USERS and USERS[user] == pwd:
            session["user"] = user
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Credenciais inválidas")

    return render_template("login.html")

@app.route("/index")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
