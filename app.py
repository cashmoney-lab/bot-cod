from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = "bot-codigo-aposta-2026"

# ======================
# CÓDIGOS DE ACESSO (PLANOS)
# ======================
# Simulação de planos pagos
CODES = {
    "PLANO1H": 1,
    "PLANO3H": 3,
    "PLANO5H": 5,
    "PLANO10H": 10,
    "PLANO24H": 24
}

# ======================
# LOGIN COM CREDENCIAIS
# ======================
# Tu controlas estas senhas
USERS = {
    "admin": "admin123",
    "cliente": "cliente123"
}

# Histórico em memória
historico = []

def adicionar_historico(tipo):
    historico.append({
        "tipo": tipo,
        "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })

# ======================
# PÁGINA DE LOGIN
# ======================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Pode ser login com usuário/senha ou código de plano
        username = request.form.get("username")
        password = request.form.get("password")
        code = request.form.get("code")

        # LOGIN POR USUÁRIO/SENHA
        if username and password:
            if username in USERS and USERS[username] == password:
                session["user"] = username
                # Para teste, atribuímos plano padrão de 24h
                session["expire_at"] = (datetime.now() + timedelta(hours=24)).isoformat()
                return redirect(url_for("bot"))
            else:
                return render_template("login.html", erro="Credenciais inválidas ❌")

        # LOGIN POR CÓDIGO DE PLANO
        elif code:
            if code in CODES:
                horas = CODES[code]
                session["expire_at"] = (datetime.now() + timedelta(hours=horas)).isoformat()
                return redirect(url_for("bot"))
            else:
                return render_template("login.html", erro="Código inválido ❌")

        else:
            return render_template("login.html", erro="Preencha os campos corretamente ❌")

    return render_template("login.html")

# ======================
# BOT
# ======================
@app.route("/bot")
def bot():
    expire_at = session.get("expire_at")

    if not expire_at:
        return redirect(url_for("login"))

    if datetime.now() > datetime.fromisoformat(expire_at):
        session.clear()
        return redirect(url_for("expired"))

    # EXEMPLO DE SINAIS
    adicionar_historico("VERDE ✅")
    adicionar_historico("ATENÇÃO ⚠️")
    adicionar_historico("VERMELHO ❌")

    tempo_restante = datetime.fromisoformat(expire_at) - datetime.now()

    return render_template(
        "index.html",
        historico=historico[-10:][::-1],
        tempo=str(tempo_restante).split(".")[0]
    )

# ======================
# EXPIRADO
# ======================
@app.route("/expired")
def expired():
    return render_template("expired.html")

# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ======================
# RUN
# ======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
