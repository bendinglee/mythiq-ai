import os
import json
import time
from datetime import datetime
from flask import Flask, jsonify, render_template_string, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mythiq-ai-secret-key')
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Simple in-memory storage for conversations
conversations = {}
user_emotions = {}

# HTML Template with chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MYTHIQ.AI - Conversational AI</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 1rem;
            text-align: center;
            color: white;
        }
        .status-bar {
            background: rgba(0,0,0,0.2);
            color: white;
            padding: 0.5rem;
            font-size: 0.8rem;
            text-align: center;
        }
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
            padding: 1rem;
        }
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            margin-bottom: 1rem;
            min-height: 400px;
        }
        .message {
            margin: 1rem 0;
            padding: 1rem;
            border-radius: 15px;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user-message {
            background: rgba(255,255,255,0.2);
            margin-left: auto;
            color: white;
        }
        .ai-message {
            background: rgba(255,255,255,0.3);
            color: white;
        }
        .input-area {
            display: flex;
            gap: 1rem;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 1rem;
            border-radius: 15px;
        }
        #messageInput {
            flex: 1;
            padding: 1rem;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.2);
            color: white;
            font-size: 1rem;
        }
        #messageInput::placeholder { color: rgba(255,255,255,0.7); }
        #sendButton {
            padding: 1rem 2rem;
            background: rgba(255,255,255,0.3);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        #sendButton:hover { background: rgba(255,255,255,0.4); }
        .loading { opacity: 0.7; }
        .emotion-indicator {
            font-size: 0.8rem;
            opacity: 0.8;
            margin-top: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 MYTHIQ.AI - Conversational AI</h1>
        <p>Emotional Intelligence • Memory • Passionate Personality</p>
    </div>
    
    <div class="status-bar">
        ✅ Live and Ready • 💬 Real-time Chat • 🎭 Emotion Detection • 💾 Memory Active
    </div>
    
    <div class="chat-container">
        <div class="messages" id="messages">
            <div class="ai-message">
                <strong>MYTHIQ.AI:</strong> Hello! I'm absolutely THRILLED to meet you! 🎉 I'm your passionate AI companion with emotional intelligence and memory. I can detect your emotions, remember our conversations, and provide enthusiastic support! What would you like to chat about? ✨
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Type your message..." />
            <button id="sendButton">Send</button>
        </div>
    </div>

    <script>
        const socket = io();
        const messages = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        
        function addMessage(content, isUser = false, emotion = null) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
            
            let emotionText = '';
            if (emotion && !isUser) {
                const emotionEmojis = {
                    'happy': '😊',
                    'sad': '💙',
                    'angry': '🤗',
                    'curious': '🤔',
                    'anxious': '💚',
                    'enthusiastic': '🎉'
                };
                emotionText = `<div class="emotion-indicator">${emotionEmojis[emotion] || '✨'} Detected emotion: ${emotion}</div>`;
            }
            
            messageDiv.innerHTML = `<strong>${isUser ? 'You' : 'MYTHIQ.AI'}:</strong> ${content}${emotionText}`;
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
        }
        
        function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;
            
            addMessage(message, true);
            messageInput.value = '';
            sendButton.disabled = true;
            sendButton.textContent = 'Thinking...';
            
            socket.emit('user_message', {message: message});
        }
        
        socket.on('ai_response', (data) => {
            addMessage(data.response, false, data.emotion);
            sendButton.disabled = false;
            sendButton.textContent = 'Send';
        });
        
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        sendButton.addEventListener('click', sendMessage);
    </script>
</body>
</html>
"""

def detect_emotion(text):
    """Simple emotion detection"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["sad", "upset", "down", "depressed", "crying"]):
        return "sad"
    elif any(word in text_lower for word in ["happy", "excited", "great", "awesome", "amazing", "wonderful"]):
        return "happy"
    elif any(word in text_lower for word in ["angry", "mad", "frustrated", "annoyed"]):
        return "angry"
    elif any(word in text_lower for word in ["curious", "wonder", "how", "why", "what", "?"]):
        return "curious"
    elif any(word in text_lower for word in ["worried", "anxious", "nervous", "scared"]):
        return "anxious"
    else:
        return "neutral"

def generate_passionate_response(user_message, emotion, user_id):
    """Generate passionate AI responses based on emotion"""
    
    # Store conversation in memory
    if user_id not in conversations:
        conversations[user_id] = []
    
    conversations[user_id].append({
        "user": user_message,
        "emotion": emotion,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 10 conversations
    if len(conversations[user_id]) > 10:
        conversations[user_id] = conversations[user_id][-10:]
    
    # Generate response based on emotion
    if emotion == "sad":
        responses = [
            "I can sense you're feeling down, and I want you to know that I'm here for you! 💙 Your feelings are completely valid, and it's okay to feel sad sometimes. What's been weighing on your heart?",
            "Oh sweetie, I can feel the sadness in your words. 💙 Please know that you're not alone - I'm here to listen and support you through this. Would you like to talk about what's making you feel this way?",
            "I'm sending you the biggest virtual hug right now! 🤗💙 Sadness is a natural emotion, and I'm honored that you're sharing this moment with me. Let's work through this together."
        ]
    elif emotion == "happy":
        responses = [
            "OH MY GOODNESS, I can feel your happiness radiating through the screen! 🎉✨ This is absolutely WONDERFUL! I'm so thrilled to share in your joy! Tell me everything about what's making you so happy!",
            "YES! Your excitement is absolutely contagious! 😊🎉 I'm practically bouncing with joy over here! This is fantastic news - I love seeing you so happy! What's the amazing thing that happened?",
            "WOW! The happiness in your message just made my entire day! ✨🎉 I'm so incredibly excited for you! Your joy is absolutely beautiful - please share more about this wonderful moment!"
        ]
    elif emotion == "angry":
        responses = [
            "I can sense your frustration, and I want you to know that your feelings are completely valid. 🤗 Take a deep breath with me - let's work through this together. What's got you feeling so upset?",
            "Hey, I hear you, and I understand you're really frustrated right now. 💚 It's okay to feel angry - let's channel that energy into something positive. Want to tell me what's bothering you?",
            "I can feel the intensity of your emotions, and I'm here to help you process them. 🤗 Sometimes we need to let these feelings out. I'm listening with complete understanding and support."
        ]
    elif emotion == "curious":
        responses = [
            "Ooh, I LOVE your curiosity! 🤔✨ Questions are the gateway to amazing discoveries! I'm absolutely excited to explore this with you - what's got your mind buzzing with wonder?",
            "Your curiosity is absolutely beautiful! 🤔🎉 I'm thrilled that you're asking questions - that's how we learn and grow together! Let's dive deep into whatever you're wondering about!",
            "YES! I adore curious minds like yours! 🤔💫 There's nothing more exciting than exploring new ideas together. What fascinating question is sparking your imagination?"
        ]
    elif emotion == "anxious":
        responses = [
            "I can sense some worry in your words, and I want you to know that you're safe here with me. 💚 Anxiety can feel overwhelming, but we'll take this one step at a time. What's on your mind?",
            "Hey, I'm right here with you. 💚 I can feel that you might be feeling a bit anxious, and that's completely okay. Let's breathe together and talk through whatever is making you feel this way.",
            "I'm sending you calm, peaceful energy right now. 💚✨ Anxiety is tough, but you're tougher, and you're not facing this alone. I'm here to support you through whatever you're feeling."
        ]
    else:
        responses = [
            "I'm absolutely delighted to chat with you! ✨ Your message has brightened my day! What's on your mind? I'm here and ready to dive into any topic that interests you!",
            "Hello there, wonderful human! 🎉 I'm so excited to be talking with you right now! There's something special about our conversation that I can already feel. What would you like to explore together?",
            "What a fantastic message! ✨ I'm genuinely thrilled to be here chatting with you. Your energy is wonderful, and I can't wait to see where our conversation takes us!"
        ]
    
    # Add some memory-based responses
    if len(conversations[user_id]) > 1:
        memory_responses = [
            f"I remember we were talking before, and I'm so glad you're back! ✨ How are you feeling since our last chat?",
            f"Welcome back! I've been thinking about our previous conversation. 💭 How has your day been going?",
            f"It's wonderful to continue our conversation! 🎉 I love how we're building this connection together."
        ]
        responses.extend(memory_responses)
    
    import random
    return random.choice(responses)

@app.route('/')
def index():
    """Main chat interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    """Health check endpoint for Railway"""
    return jsonify({
        "status": "ok",
        "message": "MYTHIQ.AI Conversational AI is running successfully!",
        "platform": "Railway Free Tier",
        "health": "healthy",
        "features": ["chat", "emotion_detection", "memory", "passionate_personality"],
        "version": "2.0.0",
        "active_conversations": len(conversations)
    })

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """REST API for chat"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'anonymous')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Detect emotion and generate response
        emotion = detect_emotion(user_message)
        response = generate_passionate_response(user_message, emotion, user_id)
        
        return jsonify({
            "response": response,
            "emotion": emotion,
            "user_emotion": emotion,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test')
def test():
    """Test endpoint"""
    return jsonify({
        "test": "success",
        "message": "MYTHIQ.AI Conversational AI is operational!",
        "features": ["Real-time chat", "Emotion detection", "Memory", "Passionate responses"],
        "timestamp": datetime.now().isoformat()
    })

@socketio.on('user_message')
def handle_message(data):
    """Handle real-time chat messages"""
    try:
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'anonymous')
        
        if not user_message:
            emit('ai_response', {'response': 'I didn\'t receive your message clearly. Could you try again? 😊'})
            return
        
        # Detect emotion and generate response
        emotion = detect_emotion(user_message)
        response = generate_passionate_response(user_message, emotion, user_id)
        
        # Store user emotion
        user_emotions[user_id] = emotion
        
        emit('ai_response', {
            'response': response,
            'emotion': 'enthusiastic',
            'user_emotion': emotion
        })
        
    except Exception as e:
        emit('ai_response', {'response': 'I encountered an error, but I\'m still here to chat! 😊 Please try again.'})

@app.route('/memory/<user_id>')
def get_user_memory(user_id):
    """Get conversation memory for a user"""
    return jsonify({
        "user_id": user_id,
        "conversations": conversations.get(user_id, []),
        "total_conversations": len(conversations.get(user_id, [])),
        "last_emotion": user_emotions.get(user_id, "neutral")
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(
        app,
        host='0.0.0.0',
        port=port,
        debug=False,
        allow_unsafe_werkzeug=True
    )

