from flask import Flask, request
from flask_cors import CORS
import requests
import os
import whisper

app = Flask(__name__)
CORS(app)
model = whisper.load_model("base")

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

@app.route("/process", methods=["POST"])
def process():
    data = request.json

    if data is None:
        return "Aucune donnée reçue", 400
    
    text = data.get("text", "")
    target_lang = data.get("target_lang","en")

    transcription = text.lower().strip()

    try:
        response = requests.post(
            "https://libretranslate.com/translate",
            json={
                "q": transcription,
                "source": "auto",
                "target": target_lang,
                "format": "text"
            },
            timeout=5
        )

        translated_text = response.json().get(
            "translatedText",
            f"[{target_lang}] {transcription}"
        )

    except Exception as e:
        print("Traduction indisponible :", e)
        translated_text = f"[{target_lang}] {transcription}"

    return {
        "original": text,
        "transcription": transcription,
        "translated": translated_text,
        "target_lang": target_lang
    }

@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return {"error": "Aucun fichier audio reçu"}, 400
        
    audio_file = request.files["audio"]

    os.makedirs("uploads", exist_ok=True)
    save_path = os.path.join("uploads", audio_file.filename)
    audio_file.save(save_path)

    try:
        result = model.transcribe(save_path)
        transcription = result["text"]
    except Exception as e:
        print("Erreur Whisper :", e)
        transcription = "[Erreur lors de la transcription]"

    return {
        "message": "Audio reçu avec succès",
        "filename": audio_file.filename,
        "transcription": transcription
    }

if __name__ == "__main__":
    app.run(debug=True)
