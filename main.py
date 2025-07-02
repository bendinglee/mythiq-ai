from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
import os
import json
import time
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mythiq-simple-key')
CORS(app, origins="*")

# Simple in-memory storage
conversations = {}
stats = {"total_requests": 0, "chat_requests": 0}

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MYTHIQ.AI - Simple Version</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            color: white;
        }
        
        .header {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 2rem;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .status {
            background: #4CAF50;
            color: white;
            padding: 1rem;
            text-align: center;
            font-weight: 500;
        }
        
        .container {
            flex: 1;
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1rem;
            display: flex;
            flex-direction: column;
        }
        
        .chat-box {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            flex: 1;
            min-height: 400px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .messages {
            height: 300px;
            overflow-y: auto;
            margin-bottom: 2rem;
            padding: 1rem;
            background: rgba(0,0,0,0.1);
            border-radius: 15px;
        }
        
        .message {
            margin: 1rem 0;
            padding: 1rem;
            border-radius: 15px;
            max-width: 80%;
        }
        
        .user-message {
            background: rgba(255,255,255,0.2);
            margin-left: auto;
            text-align: right;
        }
        
        .ai-message {
            background: rgba(255,255,255,0.3);
        }
        
        .input-area {
            display: flex;
            gap: 1rem;
        }
        
        #messageInput {
            flex: 1;
            padding: 1rem;
            border: none;
            border-radius: 15px;
            background: rgba(255,255,255,0.2);
            color: white;
            font-size: 1rem;
        }
        
        #messageInput::placeholder {
            color: rgba(255,255,255,0.7);
        }
        
        #sendButton {
            padding: 1rem 2rem;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        #sendButton:hover {
            background: #5a6fd8;
            transform: translateY(-2px);
        }
        
        .features {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .features h3 {
            margin-bottom: 1rem;
        }
        
        .feature-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }
        
        .feature {
            background: rgba(255,255,255,0.1);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .container { margin: 1rem; }
            .input-area { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 MYTHIQ.AI</h1>
        <div class="subtitle">Simple AI Chat Platform - Version 1.0</div>
    </div>
    
    <div class="status">
        ✅ System Online • Simple Chat Active • Ready for Upgrade
    </div>
    
    <div class="container">
        <div class="chat-box">
            <h3>💬 AI Chat</h3>
            <div class="messages" id="messages">
                <div class="ai-message">
                    <strong>MYTHIQ.AI:</strong> Hello! I'm your simple AI assistant. I can chat with you and help with various tasks. This is the basic version - we can upgrade to advanced features anytime! 🚀
                </div>
            </div>
            
            <div class="input-area">
                <input type="text" id="messageInput" placeholder="Type your message here..." />
                <button id="sendButton">Send</button>
            </div>
        </div>
        
        <div class="features">
            <h3>🎯 Current Features</h3>
            <div class="feature-list">
                <div class="feature">
                    <strong>💬 Basic Chat</strong><br>
                    Simple conversation interface
                </div>
                <div class="feature">
                    <strong>📊 API Ready</strong><br>
                    /api/status endpoint working
                </div>
                <div class="feature">
                    <strong>🚀 Railway Deployed</strong><br>
                    Professional hosting
                </div>
                <div class="feature">
                    <strong>⬆️ Upgrade Ready</strong><br>
                    Easy path to advanced features
                </div>
            </div>
        </div>
    </div>

    <script>
        const messages = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        
        let isProcessing = false;
        
        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
            messageDiv.innerHTML = `<strong>${isUser ? 'You' : 'MYTHIQ.AI'}:</strong> ${content}`;
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
        }
        
        async function sendMessage() {
            if (isProcessing) return;
            
            const message = messageInput.value.trim();
            if (!message) return;
            
            addMessage(message, true);
            messageInput.value = '';
            
            isProcessing = true;
            sendButton.disabled = true;
            sendButton.textContent = 'Processing...';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        user_id: 'simple_user_' + Date.now()
                    })
                });
                
                const data = await response.json();
                addMessage(data.response || data.error || 'Sorry, something went wrong!');
                
            } catch (error) {
                addMessage('Connection error. Please try again!');
            } finally {
                isProcessing = false;
                sendButton.disabled = false;
                sendButton.textContent = 'Send';
            }
        }
        
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !isProcessing) sendMessage();
        });
        
        sendButton.addEventListener('click', sendMessage);
        
        // Test connection
        fetch('/api/status')
            .then(response => response.json())
            .then(data => console.log('MYTHIQ.AI Status:', data))
            .catch(error => console.error('Connection error:', error));
    </script>
</body>
</html>
"""

def simple_emotion_detection(text):
    """Simple emotion detection"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['happy', 'great', 'awesome', 'wonderful', 'excited']):
        return 'happy'
    elif any(word in text_lower for word in ['sad', 'upset', 'down', 'depressed']):
        return 'sad'
    elif any(word in text_lower for word in ['help', 'support', 'problem', 'issue']):
        return 'supportive'
    elif any(word in text_lower for word in ['how', 'why', 'what', 'curious']):
        return 'curious'
    else:
        return 'neutral'

def generate_simple_response(user_message, emotion, user_id):
    """Generate simple AI responses"""
    
    if user_id not in conversations:
        conversations[user_id] = []
    
    conversations[user_id].append({
        "user": user_message,
        "emotion": emotion,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 5 conversations
    if len(conversations[user_id]) > 5:
        conversations[user_id] = conversations[user_id][-5:]
    
    responses = {
        'happy': [
            "That's wonderful! I'm so happy to hear that! 😊 Your positive energy is contagious!",
            "Amazing! I love your enthusiasm! What's making you feel so great today?"
        ],
        'sad': [
            "I'm sorry you're feeling down. I'm here to listen and support you. 💙",
            "That sounds tough. Would you like to talk about what's bothering you?"
        ],
        'supportive': [
            "I'm here to help! Let me do my best to assist you with whatever you need. 🤝",
            "I'd be happy to help you work through this. What specific support do you need?"
        ],
        'curious': [
            "Great question! I love curious minds! Let me help you explore this topic. 🤔",
            "That's an interesting question! I'm excited to help you learn more about this."
        ],
        'neutral': [
            "Thanks for chatting with me! I'm here to help with whatever you need. ✨",
            "Hello! I'm MYTHIQ.AI and I'm ready to assist you. What would you like to talk about?"
        ]
    }
    
    import random
    return random.choice(responses.get(emotion, responses['neutral']))

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    """Required status endpoint for Railway"""
    stats["total_requests"] += 1
    
    return jsonify({
        "status": "ok",
        "message": "MYTHIQ.AI Simple Version - All systems operational",
        "version": "1.0-simple",
        "platform": "Railway",
        "features": [
            "basic_chat", "simple_emotion_detection", "conversation_memory", 
            "railway_deployment", "upgrade_ready"
        ],
        "active_conversations": len(conversations),
        "total_requests": stats["total_requests"],
        "upgrade_available": True,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Simple chat API"""
    try:
        stats["total_requests"] += 1
        stats["chat_requests"] += 1
        
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'simple_user')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        if len(user_message) > 1000:
            return jsonify({"error": "Message too long (max 1000 characters)"}), 400
        
        # Simple emotion detection
        emotion = simple_emotion_detection(user_message)
        
        # Generate response
        response = generate_simple_response(user_message, emotion, user_id)
        
        return jsonify({
            "response": response,
            "emotion": emotion,
            "timestamp": datetime.now().isoformat(),
            "conversation_count": len(conversations.get(user_id, [])),
            "version": "1.0-simple",
            "upgrade_available": True
        })
        
    except Exception as e:
        return jsonify({
            "error": "I encountered a small hiccup, but I'm still here to help! Please try again. 🔧",
            "error_type": "temporary_issue",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/test')
def test():
    """Test endpoint"""
    stats["total_requests"] += 1
    
    return jsonify({
        "test": "SUCCESS! 🎉",
        "message": "MYTHIQ.AI Simple Version is working perfectly!",
        "current_features": [
            "✅ Basic chat interface with emotion detection",
            "✅ Simple conversation memory (5 messages)",
            "✅ Railway deployment with health checks",
            "✅ REST API endpoints (/api/status, /api/chat)",
            "✅ Responsive design for mobile and desktop",
            "✅ Error handling and recovery"
        ],
        "upgrade_features": [
            "🚀 Advanced emotion detection (10+ types)",
            "🎨 Stunning animated interface with particles",
            "📚 Professional API documentation",
            "📊 Real-time analytics dashboard",
            "🔧 Flask-API browsable endpoints",
            "💾 Enhanced memory (20+ messages)",
            "🎭 Dynamic personality adaptation"
        ],
        "timestamp": datetime.now().isoformat(),
        "version": "1.0-simple",
        "ready_for_upgrade": True
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

