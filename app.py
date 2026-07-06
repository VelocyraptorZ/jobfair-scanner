from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2RDPT2z9XIwjMcC12a5SOdmhFvUiJygtKgVLArmW91QelkB7sSEmXcgO_hJmkP6CxGg/exec"

session = requests.Session()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():

    ticket = request.json.get("ticket","").strip()

    try:

        response = session.get(
            APPS_SCRIPT_URL,
            params={
                "action":"checkin",
                "ticket":ticket
            },
            headers={
                "Accept":"application/json"
            },
            allow_redirects=True,
            timeout=20
        )

        print("=" * 60)
        print("STATUS :", response.status_code)
        print("URL    :", response.url)
        print("TYPE   :", response.headers.get("Content-Type"))
        print("BODY   :")
        print(response.text)
        print("=" * 60)

        data = json.loads(response.text)

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "success":False,
            "message":str(e)
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
    app.run(host="0.0.0.0", port=5000, debug=True)