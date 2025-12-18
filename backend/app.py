from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return "Backend TalkTranslate en cours de développement"

@app.route("/ping")
def ping():
    return "pong"

@app.route("/echo", methods=["POST"])
def echo():
    data = request.json

    if data is None:
        return "Aucune donnée reçue", 400
    
    message = data.get("message", "")

    return {
        "received": message
    }

if __name__ == "__main__":
    app.run(debug=True)
