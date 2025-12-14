from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Backend TalkTranslate en cours de développement"

if __name__ == "__main__":
    app.run(debug=True)
