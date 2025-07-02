import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Simple HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>MYTHIQ.AI - Working!</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 50px;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            max-width: 600px;
            margin: 0 auto;
        }
        a { color: #ffeb3b; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 MYTHIQ.AI is Live!</h1>
        <p>Your optimized AI is running successfully on Railway!</p>
        <p><strong>Status:</strong> ✅ Healthy and Ready</p>
        <p><strong>Platform:</strong> Railway Free Tier</p>
        <p><strong>Region:</strong> Europe West</p>
        <br>
        <p><a href="/api/status">📊 Check API Status</a></p>
        <p><a href="/test">🧪 Test Endpoint</a></p>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    """Health check endpoint for Railway"""
    return jsonify({
        "status": "ok",
        "message": "MYTHIQ.AI is running successfully!",
        "platform": "Railway Free Tier",
        "health": "healthy",
        "version": "1.0.0"
    })

@app.route('/test')
def test():
    """Test endpoint"""
    return jsonify({
        "test": "success",
        "message": "All systems operational!",
        "timestamp": "2025-01-02"
    })

@app.route('/health')
def health():
    """Alternative health check"""
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

