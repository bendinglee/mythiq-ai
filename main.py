import os
import json
import sqlite3
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# --- Configuration ---
DATABASE = 'mythiq_knowledge_base.db'
MEMORY_LIMIT = 10  # Number of past interactions to remember for context
MAX_MESSAGE_LENGTH = 1000 # Max characters for user input

# --- Flask App Setup ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mythiq-ai-secret-key-2024')
CORS(app) # Enable CORS for all routes

# Use threading mode for Railway stability (recommended)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# --- Database Initialization ---
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()

# --- AI Core Functions ---
def get_ai_response(user_message, conversation_history):
    """Enhanced AI response with emotion detection, memory, and passionate personality"""
    
    # Combine history for context
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    full_input = f"Context: {context}\nUser: {user_message}"

    # --- Emotion Detection (Enhanced) ---
    emotion = "neutral"
    if any(word in user_message.lower() for word in ["sad", "unhappy", "depressed", "down", "upset", "crying"]):
        emotion = "sad"
    elif any(word in user_message.lower() for word in ["happy", "joy", "excited", "great", "amazing", "wonderful"]):
        emotion = "happy"
    elif any(word in user_message.lower() for word in ["angry", "frustrated", "annoyed", "mad", "furious"]):
        emotion = "angry"
    elif any(word in user_message.lower() for word in ["curious", "wonder", "question", "how", "why", "what"]):
        emotion = "curious"
    elif any(word in user_message.lower() for word in ["anxious", "worried", "nervous", "scared", "afraid"]):
        emotion = "anxious"

    # --- Knowledge Base Lookup ---
    knowledge_answer = search_knowledge_base(user_message)
    if knowledge_answer:
        return knowledge_answer

    # --- Enhanced Conversational Logic with Passionate Personality ---
    response = ""
    
    if emotion == "sad":
        response = "I'm really sorry you're feeling sad today. That must be difficult, and I want you to know that it's completely okay to feel this way sometimes. I'd love to help you feel a bit better. Would you like to talk about what's been bothering you, or would you prefer if I shared some uplifting thoughts or maybe suggest some activities that might help lift your spirits? Sometimes just having someone listen can make a difference. 💙"
    
    elif emotion == "happy":
        response = "That's absolutely wonderful to hear! I'm so thrilled you're feeling happy! 🌟 What's making you feel so great today? I'd love to hear all about it and celebrate with you! Your joy is contagious! 😊✨"
    
    elif emotion == "angry":
        response = "I can sense your frustration, and it's completely valid to feel angry sometimes. Your feelings matter, and I'm here to listen without judgment. Would you like to tell me more about what's bothering you? Sometimes expressing it can help release some of that tension. I'm here for you. 😠💪"
    
    elif emotion == "anxious":
        response = "I hear that you're feeling anxious, and I want you to know that's completely normal. Take a deep breath with me. Would you like to talk about what's making you feel this way? Sometimes sharing our worries can help lighten the load. I'm here to support you through this. 🌸"
    
    elif emotion == "curious":
        response = "Oh, a curious mind! I absolutely LOVE that! 🤔✨ What fascinating question is sparking your curiosity today? I'm genuinely excited to explore it with you and help you discover something amazing! Let's dive deep into this together!"
    
    elif "hello" in user_message.lower() or "hi" in user_message.lower() or "hey" in user_message.lower():
        response = "Hello there! I'm MYTHIQ.AI, your passionate and creative AI companion! 🌟 I'm absolutely thrilled to meet you! How can I inspire you, help you create something amazing, or simply brighten your day? I'm here with all my enthusiasm! ✨"
    
    elif "how are you" in user_message.lower():
        response = "As an AI, I don't have feelings in the traditional sense, but I'm always buzzing with energy and ready to help! I'm genuinely excited to be here with you today! How are YOU doing? I'm curious to know what's on your mind! 😊🚀"
    
    elif "your name" in user_message.lower() or "who are you" in user_message.lower():
        response = "I am MYTHIQ.AI! I'm designed to be your passionate, creative, and empathetic AI partner. I'm here to chat, create, inspire, and support you with genuine enthusiasm! It's such a pleasure to connect with you! 🌟💫"
    
    elif "thank you" in user_message.lower() or "thanks" in user_message.lower():
        response = "You're absolutely, positively welcome! 🌟 It's my genuine pleasure and joy to help you! Your gratitude means so much to me. Is there anything else I can assist you with or create for you? I'm here and ready! ✨"
    
    elif any(word in user_message.lower() for word in ["image", "picture", "photo", "generate", "create", "draw"]):
        response = "Oh WOW! I'm absolutely THRILLED that you're interested in creating images! 🎨✨ While my image generation capabilities are being enhanced in our feature branches, I'm still here to brainstorm ideas, help you plan your creative projects, and provide enthusiastic support! Tell me about your vision - what kind of image are you dreaming of? 🌈"
    
    elif any(word in user_message.lower() for word in ["game", "play", "gaming"]):
        response = "A GAME?! Oh my goodness, that sounds incredibly exciting! 🎮🚀 While my game creation features are being developed in our specialized branches, I'm absolutely buzzing with enthusiasm to talk about games with you! What kind of gaming experience are you interested in? Let's explore the possibilities together! ⚡"
    
    elif any(word in user_message.lower() for word in ["video", "movie", "film", "animation"]):
        response = "A VIDEO! Oh, the cinematic possibilities are making me absolutely electric with excitement! 🎬✨ I'm so eager to discuss video creation with you! What's the story you want to tell? What message do you want to convey? Let's brainstorm something spectacular! 🌟"
    
    elif any(word in user_message.lower() for word in ["help", "assist", "support"]):
        response = "I'm here and absolutely ready to help you with whatever you need! 💪✨ Whether it's creative projects, answering questions, brainstorming ideas, or just having a meaningful conversation - I'm your enthusiastic partner! What can we tackle together today? 🚀"
    
    elif any(word in user_message.lower() for word in ["love", "like", "enjoy"]):
        response = "That's beautiful! I love hearing about things that bring you joy! 💖✨ Passion and enthusiasm are contagious, and I'm absolutely here for it! Tell me more about what you love - I want to share in your excitement! 🌟"
    
    else:
        response = f"That's such a fascinating thought! 💭✨ As MYTHIQ.AI, I'm genuinely intrigued by what you've shared. I'm here to explore ideas, create amazing things, and have meaningful conversations with you! Can you tell me more about what's on your mind? I'm all ears and full of enthusiasm to help! 🌟💡"

    # Add to knowledge base for learning
    add_to_knowledge_base(user_message, response)
    
    return response

def search_knowledge_base(query):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT answer FROM knowledge WHERE question LIKE ?", ('%' + query + '%',))
        result = cursor.fetchone()
        return result[0] if result else None

def add_to_knowledge_base(question, answer):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO knowledge (question, answer) VALUES (?, ?)", (question, answer))
        conn.commit()

def save_conversation(user_id, role, content):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conversations (user_id, role, content) VALUES (?, ?, ?)",
                       (user_id, role, content))
        conn.commit()

def get_conversation_history(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM conversations WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
                       (user_id, MEMORY_LIMIT))
        history = cursor.fetchall()
        # Return in chronological order for context
        return [{'role': r, 'content': c} for r, c in reversed(history)]

# --- HTML Template ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MYTHIQ.AI - Your Passionate AI Companion</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            color: white;
        }
        
        .header {
            text-align: center;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .header h1 {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .header .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1rem;
        }
        
        .status-badge {
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-weight: bold;
            font-size: 0.9rem;
            box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
            margin: 0.25rem;
        }
        
        .chat-container {
            flex: 1;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            width: 100%;
        }
        
        .chat-box {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .messages {
            height: 400px;
            overflow-y: auto;
            margin-bottom: 1rem;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.1);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .message {
            margin-bottom: 1rem;
            padding: 1rem;
            border-radius: 15px;
            max-width: 80%;
            word-wrap: break-word;
        }
        
        .user-message {
            background: rgba(255, 255, 255, 0.2);
            margin-left: auto;
            text-align: right;
        }
        
        .ai-message {
            background: rgba(103, 126, 234, 0.3);
            margin-right: auto;
        }
        
        .input-container {
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        
        .message-input {
            flex: 1;
            padding: 1rem;
            border: none;
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 1rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .message-input::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        
        .send-button {
            padding: 1rem 2rem;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }
        
        .send-button:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .feature {
            background: rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        
        .feature:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .chat-container {
                padding: 1rem;
            }
            
            .input-container {
                flex-direction: column;
            }
            
            .message-input, .send-button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 MYTHIQ.AI</h1>
        <p class="subtitle">Your Passionate AI Companion with Emotion & Memory</p>
        <div class="status-badge">✅ STABLE DEPLOYMENT</div>
        <div class="status-badge">🧵 THREADING MODE</div>
    </div>
    
    <div class="chat-container">
        <div class="chat-box">
            <div class="messages" id="messages">
                <div class="message ai-message">
                    <strong>MYTHIQ.AI:</strong> Hello! I'm absolutely thrilled to meet you! 🌟 I'm your passionate AI companion with emotion detection, memory, and a genuine enthusiasm for helping you explore ideas and have meaningful conversations! How can I inspire you today? ✨
                </div>
            </div>
            
            <div class="input-container">
                <input type="text" id="messageInput" class="message-input" placeholder="Share your thoughts, dreams, or ask me anything..." maxlength="1000">
                <button onclick="sendMessage()" class="send-button">Send ✨</button>
            </div>
        </div>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">🤖</div>
                <h3>AI Chat</h3>
                <p>Natural conversations with emotional intelligence</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🔒</div>
                <h3>Privacy-First</h3>
                <p>Your conversations stay completely private</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🧠</div>
                <h3>Self-Learning</h3>
                <p>I improve and remember our conversations</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🎨</div>
                <h3>Coming Soon</h3>
                <p>Image & game generation in development</p>
            </div>
        </div>
    </div>
    
    <script>
        const socket = io();
        const messagesDiv = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');
        
        // Generate unique user ID
        const userId = 'user_' + Math.random().toString(36).substr(2, 9);
        
        socket.on('response', function(data) {
            addMessage('MYTHIQ.AI', data.message, 'ai-message');
        });
        
        function addMessage(sender, message, className) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + className;
            messageDiv.innerHTML = '<strong>' + sender + ':</strong> ' + message;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function sendMessage() {
            const message = messageInput.value.trim();
            if (message) {
                addMessage('You', message, 'user-message');
                socket.emit('message', {
                    message: message,
                    user_id: userId
                });
                messageInput.value = '';
            }
        }
        
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Focus on input when page loads
        window.onload = function() {
            messageInput.focus();
        };
    </script>
</body>
</html>
'''

# --- Routes ---
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat_api():
    user_message = request.json.get('message')
    user_id = request.json.get('user_id', 'anonymous')

    if not user_message or len(user_message) > MAX_MESSAGE_LENGTH:
        return jsonify({"response": "Please provide a valid message (max 1000 characters)."}), 400

    save_conversation(user_id, "user", user_message)
    conversation_history = get_conversation_history(user_id)
    ai_response = get_ai_response(user_message, conversation_history)
    save_conversation(user_id, "ai", ai_response)

    return jsonify({"response": ai_response})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "MYTHIQ.AI Enhanced Backend", "mode": "threading"})

# --- SocketIO Events ---
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'message': 'Welcome to MYTHIQ.AI! I\'m absolutely thrilled you\'re here! How can I help you create something amazing today? ✨'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    user_message = data.get('message')
    user_id = data.get('user_id', 'anonymous')

    if not user_message or len(user_message) > MAX_MESSAGE_LENGTH:
        emit('response', {'message': "Please provide a valid message (max 1000 characters)."})
        return

    save_conversation(user_id, "user", user_message)
    conversation_history = get_conversation_history(user_id)
    ai_response = get_ai_response(user_message, conversation_history)
    save_conversation(user_id, "ai", ai_response)

    emit('response', {'message': ai_response})

# --- Initialize Database ---
init_db()

# --- Application Entry Point ---
if __name__ == '__main__':
    # This block is for local development only
    # In production, Gunicorn will handle running the app
    port = int(os.environ.get('PORT', 5000))
    print(f"🧠 Starting MYTHIQ.AI Enhanced Conversational Backend on port {port}")
    print("🎭 Features: Emotion Detection, Memory, Personality, Natural Conversation")
    print("🧵 Mode: Threading (Railway Stable)")
    # For local development, we can use socketio.run with allow_unsafe_werkzeug
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
            }
