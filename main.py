from flask import Flask, jsonify
import time, sys

app = Flask(__name__)

@app.route("/api/status")
def status():
    return jsonify({
        "status": "ok",
        "message": "Minimal Mythiq test",
        "timestamp": time.time()
    })

print("🐉 Minimal Flask is running")
sys.stdout.flush()
