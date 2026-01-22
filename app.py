from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "insurance-baccarat-secret"

# ===== USUÁRIOS E PLANOS =====
USERS = {
    "admin123": {"password": "admin123", "hours": 9999},
    "plano1h": {"password": "1234", "hours": 1},
    "plano3h": {"password": "1234", "hours": 3},
    "plano5h": {"password": "1234", "hours": 5},
}

# ===== HISTÓRICO GLOBAL =====
HISTORICO = []

# ===== LOGIN =====
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")

        if user in USERS and USERS[user]["password"] == pwd:
            session["user"] = user
            session["expire"] = (datetime.now() + timedelta(hours=USERS[user]["hours"])).isoformat()
            return redirect(url_for("index"))

        return render_template("login.html", error="Credenciais inválidas")

    return render_template("login.html")


# ===== PROTEÇÃO DE SESSÃO =====
def session_valid():
    if "user" not in session:
        return False
    expire = datetime.fromisoformat(session["expire"])
    return datetime.now() < expire


@app.route("/expired")
def expired():
    return render_template("expired.html")


# ===== PÁGINA PRINCIPAL =====
@app.route("/index")
def index():
    if not session_valid():
        return redirect(url_for("expired"))
    return render_template("index.html")


# ===== LÓGICA DO BOT (EXATA E CONSERVADORA) =====
def analisar_historico(hist):
    if len(hist) < 6:
        return {
            "acao": "AGUARDAR",
            "probabilidade": 0,
            "mensagem": "⏳ Histórico insuficiente",
            "cor": "yellow"
        }

    ultimos = hist[-6:]

    # Evitar sequência perigosa
    if ultimos[-1] == ultimos[-2] == ultimos[-3]:
        return {
            "acao": "AGUARDAR",
            "probabilidade": 40,
            "mensagem": "😟 Sequência longa detectada. Aguardar.",
            "cor": "red"
        }

    banker = ultimos.count("B")
    player = ultimos.count("P")

    score_banker = banker * 1.06
    score_player = player * 1.00

    total = score_banker + score_player
    prob_banker = round((score_banker / total) * 100)

    if prob_banker >= 65:
        return {
            "acao": "APOSTAR",
            "probabilidade": prob_banker,
            "mensagem": "😄 Apostar BANKER + proteção no EMPATE",
            "cor": "green"
        }

    return {
        "acao": "AGUARDAR",
        "probabilidade": prob_banker,
        "mensagem": "😐 Sem vantagem clara. Aguardar.",
        "cor": "yellow"
    }


# ===== RECEBER RESULTADOS =====
@app.route("/add", methods=["POST"])
def add_result():
    if not session_valid():
        return jsonify({"error": "expired"})

    res = request.json.get("resultado")

    if res not in ["P", "B", "T"]:
        return jsonify({"error": "inválido"})

    HISTORICO.append(res)

    analise = analisar_historico(HISTORICO)

    return jsonify({
        "historico": " ".join(HISTORICO),
        **analise
    })


# ===== START =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
