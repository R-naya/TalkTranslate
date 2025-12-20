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

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.json

    if data is None:
        return "Aucune donnée reçue", 400

    text = data.get("text", "")

    transcription = text.lower().strip()

    return {
        "original": text,
        "transcription": transcription
    }

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json

    if data is None:
        return "Aucune donnée reçue", 400

    text = data.get("text", "")
    target_lang = data.get("target_lang", "en")

    translated_text = f"[{target_lang}] {text}"

    return {
        "original": text,
        "translated": translated_text,
        "target_lang": target_lang
    }

if __name__ == "__main__":
    app.run(debug=True)
