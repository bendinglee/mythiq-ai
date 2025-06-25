#!/usr/bin/env python3
"""
🚀 MYTHIQ.AI Backend - Railway Optimized
The Ultimate Self-Learning AI Empire Backend System
"""

import os
import sys
import json
import time
import uuid
import sqlite3
import threading
from datetime import datetime
from pathlib import Path

# Flask and extensions
from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit

# Import knowledge base
try:
    from knowledge_base_final_fixed import KnowledgeBase
    KNOWLEDGE_BASE_AVAILABLE = True
    print("✅ Knowledge Base imported successfully")
except ImportError as e:
    KNOWLEDGE_BASE_AVAILABLE = False
    print(f"⚠️ Knowledge Base import failed: {e}")

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mythiq-ai-secret-key-2024')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables
knowledge_base = None
conversation_db = None
user_preferences = {}

class ConversationDatabase:
    """Manages conversation history and user data"""
    
    def __init__(self, db_path="conversations.db"):
        self.db_path = db_path
        self.lock = threading.RLock()
        self._init_database()
    
    def _init_database(self):
        """Initialize the conversation database"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_rating INTEGER DEFAULT NULL
                )
            ''')
            
            # Create user preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    session_id TEXT PRIMARY KEY,
                    preferences TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
    
    def save_conversation(self, session_id, user_message, ai_response):
        """Save a conversation to the database"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO conversations (session_id, user_message, ai_response)
                VALUES (?, ?, ?)
            ''', (session_id, user_message, ai_response))
            conn.commit()
            conn.close()
    
    def get_conversation_history(self, session_id, limit=10):
        """Get recent conversation history for a session"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_message, ai_response, timestamp
                FROM conversations
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (session_id, limit))
            results = cursor.fetchall()
            conn.close()
            return list(reversed(results))  # Return in chronological order

class MythiqAICore:
    """Core AI processing system"""
    
    def __init__(self):
        self.knowledge_base = knowledge_base
        self.conversation_db = conversation_db
        
    def process_message(self, message, session_id="default"):
        """Process a user message and generate response"""
        
        # Get conversation context
        history = self.conversation_db.get_conversation_history(session_id, limit=5)
        context = self._build_context(history)
        
        # Process with knowledge base if available
        if self.knowledge_base and KNOWLEDGE_BASE_AVAILABLE:
            response = self._process_with_knowledge_base(message, context, session_id)
        else:
            response = self._process_basic(message, context, session_id)
        
        # Save conversation
        self.conversation_db.save_conversation(session_id, message, response)
        
        # Learn from interaction
        if self.knowledge_base and KNOWLEDGE_BASE_AVAILABLE:
            self._learn_from_interaction(message, response, session_id)
        
        return response
    
    def _build_context(self, history):
        """Build conversation context from history"""
        if not history:
            return ""
        
        context_parts = []
        for user_msg, ai_msg, timestamp in history[-3:]:  # Last 3 exchanges
            context_parts.append(f"User: {user_msg}")
            context_parts.append(f"AI: {ai_msg}")
        
        return "\n".join(context_parts)
    
    def _process_with_knowledge_base(self, message, context, session_id):
        """Process message using knowledge base"""
        try:
            # Query knowledge base
            relevant_knowledge = self.knowledge_base.query(message)
            
            # Check for special commands
            if message.lower().startswith(('help', 'what can you do')):
                return self._get_help_response()
            elif message.lower().startswith('remember'):
                return self._handle_remember_command(message, session_id)
            elif message.lower().startswith('what do you know'):
                return self._handle_knowledge_query(message, session_id)
            
            # Generate contextual response
            response = self._generate_contextual_response(message, relevant_knowledge, context)
            
            return response
            
        except Exception as e:
            print(f"⚠️ Knowledge base processing error: {e}")
            return self._process_basic(message, context, session_id)
    
    def _process_basic(self, message, context, session_id):
        """Basic processing without knowledge base"""
        
        message_lower = message.lower()
        
        # Greeting responses
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm MYTHIQ.AI, your self-learning AI assistant. I grow smarter with every conversation! How can I help you create something amazing today?"
        
        # Help responses
        elif any(word in message_lower for word in ['help', 'what can you do', 'capabilities']):
            return self._get_help_response()
        
        # About responses
        elif any(word in message_lower for word in ['about', 'who are you', 'what are you']):
            return "I'm MYTHIQ.AI - The Ultimate Human-AI Creative Engine. I'm a self-learning AI that grows smarter with every conversation. I can help with creative projects, answer questions, and learn your preferences over time!"
        
        # Learning responses
        elif 'learn' in message_lower or 'remember' in message_lower:
            return "I'm constantly learning from our conversations! Every interaction helps me understand you better and provide more personalized assistance. What would you like me to remember about you?"
        
        # Creative responses
        elif any(word in message_lower for word in ['create', 'generate', 'make', 'build']):
            return "I'd love to help you create something! While my full creative capabilities are still initializing, I can assist with planning, brainstorming, and providing guidance. What kind of project are you working on?"
        
        # Default intelligent response
        else:
            return f"That's interesting! I'm processing your message: '{message}'. As a self-learning AI, I'm continuously improving my responses. Could you tell me more about what you're looking for, or would you like to know about my capabilities?"
    
    def _generate_contextual_response(self, message, knowledge, context):
        """Generate a contextual response using available knowledge"""
        
        if knowledge:
            # Use the most relevant knowledge
            top_knowledge = knowledge[0] if isinstance(knowledge, list) else knowledge
            knowledge_text = getattr(top_knowledge, 'content', str(top_knowledge))
            
            response = f"Based on what I've learned: {knowledge_text}\n\nRegarding your message about '{message}', I can help you explore this further. What specific aspect interests you most?"
        else:
            response = f"I'm learning about '{message}' from our conversation. This is a new topic for me, so I'm adding it to my knowledge base. Could you tell me more so I can better assist you in the future?"
        
        return response
    
    def _get_help_response(self):
        """Generate help response"""
        return """🚀 **MYTHIQ.AI Capabilities**

I'm your self-learning AI that grows smarter with every conversation! Here's what I can do:

💬 **Intelligent Conversation**
- Natural language understanding
- Context-aware responses
- Learning from every interaction

🧠 **Self-Learning System**
- Remember your preferences
- Build knowledge from conversations
- Improve responses over time

🎨 **Creative Assistance**
- Help with brainstorming
- Project planning and guidance
- Creative problem solving

📚 **Knowledge Management**
- Store and recall information
- Connect related concepts
- Provide personalized insights

**Try saying:**
- "Remember that I love science fiction"
- "What do you know about my interests?"
- "Help me create something amazing"

I'm continuously learning and improving! What would you like to explore together?"""
    
    def _handle_remember_command(self, message, session_id):
        """Handle remember commands"""
        try:
            # Extract what to remember
            remember_text = message.lower().replace('remember', '').strip()
            if remember_text.startswith('that'):
                remember_text = remember_text[4:].strip()
            
            if self.knowledge_base:
                # Add to knowledge base
                self.knowledge_base.add_knowledge(
                    content=remember_text,
                    knowledge_type='preference',
                    context=f"User preference from session {session_id}",
                    confidence=0.9
                )
                
                return f"✅ I'll remember that: {remember_text}\n\nThis information is now part of my knowledge base and will help me provide more personalized assistance!"
            else:
                return f"I'll try to remember: {remember_text}\n\nNote: My full memory system is still initializing, but I'm learning from our conversation!"
                
        except Exception as e:
            return f"I understand you want me to remember something, but I had trouble processing that. Could you rephrase it? (Error: {str(e)})"
    
    def _handle_knowledge_query(self, message, session_id):
        """Handle knowledge queries"""
        try:
            if self.knowledge_base:
                # Get user-specific knowledge
                user_knowledge = self.knowledge_base.query(f"session {session_id}")
                
                if user_knowledge:
                    knowledge_summary = []
                    for item in user_knowledge[:5]:  # Top 5 items
                        content = getattr(item, 'content', str(item))
                        knowledge_summary.append(f"• {content}")
                    
                    return f"Here's what I know about you:\n\n" + "\n".join(knowledge_summary) + "\n\nI'm continuously learning more about your preferences and interests!"
                else:
                    return "I'm still learning about you! As we continue our conversations, I'll build up knowledge about your preferences, interests, and needs. Try telling me something you'd like me to remember!"
            else:
                return "My knowledge system is still initializing, but I'm learning from our conversation! Each interaction helps me understand you better."
                
        except Exception as e:
            return f"I'm still building my knowledge about you. Let's continue our conversation so I can learn more! (System note: {str(e)})"
    
    def _learn_from_interaction(self, message, response, session_id):
        """Learn from the interaction"""
        try:
            if self.knowledge_base:
                # Add interaction as experience
                self.knowledge_base.add_knowledge(
                    content=f"Q: {message} A: {response}",
                    knowledge_type='experience',
                    context=f"Conversation with session {session_id}",
                    confidence=0.8
                )
                
                # Extract and store any factual information
                if any(indicator in message.lower() for indicator in ['is', 'are', 'was', 'were', 'fact', 'true']):
                    self.knowledge_base.add_knowledge(
                        content=message,
                        knowledge_type='fact',
                        context=f"User statement from session {session_id}",
                        confidence=0.7
                    )
        except Exception as e:
            print(f"⚠️ Learning error: {e}")

# Initialize core systems
def initialize_systems():
    """Initialize all core systems"""
    global knowledge_base, conversation_db
    
    print("🧠 Initializing MYTHIQ.AI systems...")
    
    # Initialize knowledge base
    if KNOWLEDGE_BASE_AVAILABLE:
        try:
            knowledge_base = KnowledgeBase("mythiq_knowledge.db")
            print("🧠 Knowledge Base initialized successfully")
        except Exception as e:
            print(f"⚠️ Knowledge Base initialization failed: {e}")
            knowledge_base = None
    
    # Initialize conversation database
    try:
        conversation_db = ConversationDatabase("mythiq_conversations.db")
        print("💾 Conversation database initialized")
    except Exception as e:
        print(f"⚠️ Conversation database initialization failed: {e}")
        conversation_db = None
    
    # Load user preferences
    global user_preferences
    user_preferences = {}
    print("⚙️ User preferences loaded")

# Initialize AI core
mythiq_core = None

def get_ai_core():
    """Get or create AI core instance"""
    global mythiq_core
    if mythiq_core is None:
        mythiq_core = MythiqAICore()
    return mythiq_core

# Web interface HTML template
WEB_INTERFACE_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 MYTHIQ.AI - Ultimate AI Creative Engine</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 1rem 2rem;
            text-align: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .header h1 {
            color: white;
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .header p {
            color: rgba(255, 255, 255, 0.8);
            font-size: 1rem;
        }
        
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 800px;
            margin: 2rem auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        .chat-messages {
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
            max-height: 500px;
            min-height: 300px;
        }
        
        .message {
            margin-bottom: 1rem;
            padding: 1rem;
            border-radius: 15px;
            max-width: 80%;
            word-wrap: break-word;
        }
        
        .user-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-left: auto;
        }
        
        .ai-message {
            background: #f8f9fa;
            color: #333;
            border: 1px solid #e9ecef;
        }
        
        .chat-input-container {
            padding: 1.5rem;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 1rem;
        }
        
        .chat-input {
            flex: 1;
            padding: 1rem;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .chat-input:focus {
            border-color: #667eea;
        }
        
        .send-button {
            padding: 1rem 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .send-button:hover {
            transform: translateY(-2px);
        }
        
        .send-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .status {
            text-align: center;
            padding: 1rem;
            color: #666;
            font-style: italic;
        }
        
        .examples {
            padding: 1rem 2rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .examples h3 {
            color: white;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .example-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: center;
        }
        
        .example-button {
            padding: 0.5rem 1rem;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s;
        }
        
        .example-button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        @media (max-width: 768px) {
            .chat-container {
                margin: 1rem;
                border-radius: 15px;
            }
            
            .header h1 {
                font-size: 1.5rem;
            }
            
            .chat-input-container {
                flex-direction: column;
            }
            
            .send-button {
                align-self: stretch;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 MYTHIQ.AI</h1>
        <p>The Ultimate Self-Learning AI Creative Engine</p>
    </div>
    
    <div class="chat-container">
        <div class="chat-messages" id="chatMessages">
            <div class="ai-message message">
                <strong>🚀 MYTHIQ.AI:</strong> Hello! I'm your self-learning AI assistant. I grow smarter with every conversation and remember what you tell me. How can I help you create something amazing today?
            </div>
        </div>
        
        <div class="chat-input-container">
            <input type="text" class="chat-input" id="chatInput" placeholder="Type your message here..." maxlength="500">
            <button class="send-button" id="sendButton">Send</button>
        </div>
    </div>
    
    <div class="examples">
        <h3>💡 Try These Examples:</h3>
        <div class="example-buttons">
            <div class="example-button" onclick="sendExample('Hello MYTHIQ.AI! What can you do?')">What can you do?</div>
            <div class="example-button" onclick="sendExample('Remember that I love science fiction')">Remember my interests</div>
            <div class="example-button" onclick="sendExample('What do you know about me?')">What do you know about me?</div>
            <div class="example-button" onclick="sendExample('Help me create something amazing')">Help me create</div>
            <div class="example-button" onclick="sendExample('Tell me about your learning capabilities')">Learning capabilities</div>
        </div>
    </div>
    
    <script>
        const socket = io();
        const chatMessages = document.getElementById('chatMessages');
        const chatInput = document.getElementById('chatInput');
        const sendButton = document.getElementById('sendButton');
        
        let sessionId = 'web_' + Math.random().toString(36).substr(2, 9);
        
        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
            
            if (isUser) {
                messageDiv.innerHTML = `<strong>You:</strong> ${content}`;
            } else {
                messageDiv.innerHTML = `<strong>🚀 MYTHIQ.AI:</strong> ${content.replace(/\\n/g, '<br>')}`;
            }
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function sendMessage() {
            const message = chatInput.value.trim();
            if (!message) return;
            
            addMessage(message, true);
            chatInput.value = '';
            sendButton.disabled = true;
            sendButton.textContent = 'Thinking...';
            
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: sessionId
                })
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response || 'Sorry, I had trouble processing that.');
            })
            .catch(error => {
                addMessage('Sorry, I encountered an error. Please try again.');
                console.error('Error:', error);
            })
            .finally(() => {
                sendButton.disabled = false;
                sendButton.textContent = 'Send';
                chatInput.focus();
            });
        }
        
        function sendExample(text) {
            chatInput.value = text;
            sendMessage();
        }
        
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        sendButton.addEventListener('click', sendMessage);
        
        // Focus input on load
        chatInput.focus();
    </script>
</body>
</html>
'''

# Routes
@app.route('/')
def index():
    """Main web interface"""
    return render_template_string(WEB_INTERFACE_HTML)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'MYTHIQ.AI',
        'version': '1.0.0',
        'knowledge_base': KNOWLEDGE_BASE_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Process message with AI core
        ai_core = get_ai_core()
        response = ai_core.process_message(message, session_id)
        
        return jsonify({
            'response': response,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'learning_active': KNOWLEDGE_BASE_AVAILABLE
        })
        
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'I encountered an error processing your message. Please try again.'
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        stats = {
            'system': 'MYTHIQ.AI',
            'status': 'operational',
            'knowledge_base_active': KNOWLEDGE_BASE_AVAILABLE,
            'timestamp': datetime.now().isoformat()
        }
        
        if knowledge_base and KNOWLEDGE_BASE_AVAILABLE:
            try:
                kb_stats = knowledge_base.get_statistics()
                stats['knowledge_base_stats'] = kb_stats
            except:
                stats['knowledge_base_stats'] = 'unavailable'
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('status', {'message': 'Connected to MYTHIQ.AI', 'timestamp': datetime.now().isoformat()})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle real-time chat messages"""
    try:
        message = data.get('message', '').strip()
        session_id = data.get('session_id', 'socket_user')
        
        if message:
            ai_core = get_ai_core()
            response = ai_core.process_message(message, session_id)
            
            emit('chat_response', {
                'response': response,
                'timestamp': datetime.now().isoformat(),
                'learning_active': KNOWLEDGE_BASE_AVAILABLE
            })
    except Exception as e:
        emit('error', {'message': 'Error processing message'})

# Initialize systems on startup
print("🚀 Starting MYTHIQ.AI Integrated Backend...")
initialize_systems()

print("📡 API endpoints available at /api/")
print("🔌 WebSocket available at /")
print(f"💾 Knowledge Base: {'✅ Available' if KNOWLEDGE_BASE_AVAILABLE else '⚠️ Fallback Mode'}")
print("🎯 Ready to serve MYTHIQ.AI frontend!")

# Create output directories
os.makedirs("outputs/images", exist_ok=True)
os.makedirs("outputs/audio", exist_ok=True)
os.makedirs("outputs/videos", exist_ok=True)
os.makedirs("outputs/games", exist_ok=True)

if __name__ == "__main__":
    # This will only run in local development
    # Railway uses main.py as the entry point
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)

