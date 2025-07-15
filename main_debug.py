from flask import Flask

app = Flask(__name__)

@app.route("/api/status")
def status():
    return "Mythiq is alive 🔥", 200
