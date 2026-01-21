from flask import Flask, render_template, request, redirect, url_for
import time

app = Flask(__name__)

# ===== CONFIGURAÇÃO =====
PIN_VALIDO = "1234"
DURACAO_PIN = 3600  # 1 hora (em segundos)

sessions = {}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pin = request.form.get("pin")

        if pin == PIN_VALIDO:
            sessions[pin] = time.time() + DURACAO_PIN
            return redirect(url_for("bot", pin=pin))
        else:
            return render_template("index.html", erro="❌ PIN inválido")

    return render_template("index.html")

@app.route("/bot")
def bot():
    pin = request.args.get("pin")

    if pin not in sessions:
        return "⛔ Acesso negado", 403

    restante = int(sessions[pin] - time.time())

    if restante <= 0:
        sessions.pop(pin, None)
        return "⏱️ Tempo expirado. Acesso encerrado."

    return render_template("index.html", autorizado=True, remaining=restante)

if __name__ == "__main__":
    app.run(debug=True)
