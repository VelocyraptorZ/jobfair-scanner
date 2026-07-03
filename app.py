from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# GANTI DENGAN URL APPS SCRIPT ANDA
APPS_SCRIPT_URL = "https://script.google.com/macros/s/XXXX/exec"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():

    data = request.get_json()

    ticket = data.get("ticket")

    if not ticket:
        return jsonify({
            "success": False,
            "message": "Ticket kosong"
        })

    try:

        r = requests.get(
            APPS_SCRIPT_URL,
            params={
                "action": "checkin",
                "ticket": ticket
            },
            timeout=10
        )

        return jsonify(r.json())

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })


@app.route("/dashboard")
def dashboard():

    try:

        r = requests.get(
            APPS_SCRIPT_URL,
            params={"action": "dashboard"},
            timeout=10
        )

        return jsonify(r.json())

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)