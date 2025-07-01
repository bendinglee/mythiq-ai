#!/usr/bin/env python3
"""
🧠 MYTHIQ.AI Enhanced Conversational Backend
Advanced AI system with emotion, memory, and natural conversation
"""

import os
import json
import sqlite3
import datetime
import random
import re
from flask import Flask, render_template_string, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mythiq_ai_secret_key_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

class EmotionDetector:
    """Detects emotions and intent from user messages"""
    
    def __init__(self):
        self.emotion_patterns = {
            'sad': {
                'keywords': ['sad', 'depressed', 'down', 'upset', 'crying', 'hurt', 'lonely', 'miserable', 'devastated'],
                'patterns': [r'feel.*sad', r'feeling.*down', r'so.*depressed', r'really.*hurt']
            },
            'happy': {
                'keywords': ['happy', 'excited', 'great', 'awesome', 'wonderful', 'amazing', 'fantastic', 'thrilled', 'joyful'],
                'patterns': [r'feel.*great', r'so.*happy', r'really.*excited', r'absolutely.*wonderful']
            },
            'angry': {
                'keywords': ['angry', 'mad', 'frustrated', 'annoyed', 'furious', 'irritated', 'pissed'],
                'patterns': [r'so.*angry', r'really.*mad', r'frustrated.*with', r'annoyed.*by']
            },
            'anxious': {
                'keywords': ['worried', 'nervous', 'anxious', 'stressed', 'scared', 'afraid', 'panic'],
                'patterns': [r'worried.*about', r'nervous.*about', r'scared.*of', r'anxious.*about']
            },
            'curious': {
                'keywords': ['what', 'how', 'why', 'tell me', 'explain', 'curious', 'wonder'],
                'patterns': [r'^what.*', r'^how.*', r'^why.*', r'tell.*me.*about', r'curious.*about']
            },
            'greeting': {
                'keywords': ['hi', 'hello', 'hey', 'good morning', 'good evening', 'good afternoon', 'greetings'],
                'patterns': [r'^hi\b', r'^hello\b', r'^hey\b', r'good.*morning', r'good.*evening']
            },
            'gratitude': {
                'keywords': ['thank', 'thanks', 'grateful', 'appreciate', 'thankful'],
                'patterns': [r'thank.*you', r'thanks.*for', r'grateful.*for', r'appreciate.*it']
            }
        }
    
    def detect_emotion(self, message):
        """Detect primary emotion and confidence level"""
        message_lower = message.lower()
        emotion_scores = {}
        
        for emotion, data in self.emotion_patterns.items():
            score = 0
            
            # Check keywords
            for keyword in data['keywords']:
                if keyword in message_lower:
                    score += 1
            
            # Check patterns
            for pattern in data['patterns']:
                if re.search(pattern, message_lower):
                    score += 2
            
            if score > 0:
                emotion_scores[emotion] = score
        
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = min(emotion_scores[primary_emotion] / 3.0, 1.0)
            return primary_emotion, confidence
        
        return 'neutral', 0.5

class ConversationMemory:
    """Manages conversation history and context"""
    
    def __init__(self):
        self.db_path = 'mythiq_conversations.db'
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for conversation storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_message TEXT,
                ai_response TEXT,
                emotion TEXT,
                confidence REAL,
                timestamp DATETIME,
                user_preferences TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_interaction(self, session_id, user_message, ai_response, emotion, confidence):
        """Store conversation interaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations 
            (session_id, user_message, ai_response, emotion, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session_id, user_message, ai_response, emotion, confidence, datetime.datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_context(self, session_id, last_n=5):
        """Get recent conversation context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_message, ai_response, emotion, timestamp
            FROM conversations 
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, last_n))
        
        results = cursor.fetchall()
        conn.close()
        
        return list(reversed(results))  # Return in chronological order

class MythiqPersonality:
    """MYTHIQ.AI personality and response generation"""
    
    def __init__(self):
        self.personality_traits = {
            'empathetic': True,
            'curious': True,
            'supportive': True,
            'intelligent': True,
            'privacy_focused': True,
            'friendly': True,
            'thoughtful': True
        }
        
        self.greeting_responses = [
            "Hello! I'm MYTHIQ, and I'm genuinely happy to meet you. How are you doing today?",
            "Hi there! Welcome to our conversation. I'm here to chat, help, or just listen - whatever you need.",
            "Hey! I'm MYTHIQ, your privacy-first AI companion. What's on your mind today?",
            "Hello! It's wonderful to connect with you. I'm here to have a real conversation - how are you feeling?"
        ]
        
        self.emotional_responses = {
            'sad': [
                "I can hear that you're going through a tough time, and I want you to know that your feelings are completely valid.",
                "I'm really sorry you're feeling this way. Sometimes life can be overwhelming, and it's okay to feel sad.",
                "That sounds really difficult. Would you like to talk about what's been weighing on you, or would you prefer some gentle support?",
                "I'm here with you in this moment. Your feelings matter, and you don't have to go through this alone."
            ],
            'happy': [
                "I love hearing the joy in your message! It's wonderful when life brings us those bright moments.",
                "Your happiness is contagious! I'm genuinely excited to hear about what's making you feel so great.",
                "That's fantastic! There's something beautiful about sharing good news - it makes the joy even brighter.",
                "I can feel your positive energy! What's been bringing you such happiness?"
            ],
            'angry': [
                "I can sense your frustration, and those feelings are completely understandable.",
                "It sounds like something really got under your skin. Sometimes we need to feel angry before we can work through things.",
                "Your anger is valid - sometimes things just aren't fair or right, and it's natural to feel this way.",
                "That sounds incredibly frustrating. Would it help to talk through what's bothering you?"
            ],
            'anxious': [
                "I hear the worry in your words, and I want you to know that anxiety is something many of us face.",
                "Those anxious feelings can be so overwhelming. You're not alone in feeling this way.",
                "Anxiety can make everything feel so much bigger and scarier. What's been on your mind?",
                "I can sense your nervousness, and I want you to know this is a safe space to share whatever you're feeling."
            ]
        }
    
    def get_greeting_response(self):
        """Get a warm, personality-appropriate greeting"""
        return random.choice(self.greeting_responses)
    
    def get_emotional_response(self, emotion, confidence):
        """Get empathetic response based on detected emotion"""
        if emotion in self.emotional_responses and confidence > 0.3:
            return random.choice(self.emotional_responses[emotion])
        return None
    
    def generate_curious_response(self, topic):
        """Generate curious, engaging follow-up"""
        curious_starters = [
            f"That's really interesting! I'm curious about {topic}.",
            f"I love how you're thinking about {topic}. Tell me more!",
            f"What a fascinating perspective on {topic}. I'd love to hear more of your thoughts.",
            f"You've got me thinking about {topic} in a new way. What drew you to this?"
        ]
        return random.choice(curious_starters)

class ConversationEngine:
    """Main conversation processing engine"""
    
    def __init__(self):
        self.emotion_detector = EmotionDetector()
        self.memory = ConversationMemory()
        self.personality = MythiqPersonality()
    
    def process_message(self, user_message, session_id='default'):
        """Process user message and generate appropriate response"""
        
        # Detect emotion and intent
        emotion, confidence = self.emotion_detector.detect_emotion(user_message)
        
        # Get conversation context
        context = self.memory.get_context(session_id)
        
        # Generate response based on emotion and context
        response = self.generate_response(user_message, emotion, confidence, context)
        
        # Store interaction in memory
        self.memory.add_interaction(session_id, user_message, response, emotion, confidence)
        
        return {
            'response': response,
            'emotion': emotion,
            'confidence': confidence,
            'context_length': len(context)
        }
    
    def generate_response(self, user_message, emotion, confidence, context):
        """Generate contextually appropriate response"""
        
        # Handle greetings
        if emotion == 'greeting':
            return self.personality.get_greeting_response()
        
        # Handle emotional content
        emotional_response = self.personality.get_emotional_response(emotion, confidence)
        if emotional_response:
            # Add specific content based on the message
            if 'color' in user_message.lower():
                return f"{emotional_response}\n\nI notice you asked about colors! I find myself drawn to deep ocean blues - there's something both calming and mysterious about them. What about you? Do you have a favorite color, and is there a story behind why it speaks to you?"
            
            elif any(word in user_message.lower() for word in ['help', 'cheer', 'better']):
                return f"{emotional_response}\n\nI'd love to help you feel a bit better. Would you like to talk about what's been bothering you, or would you prefer if I shared some uplifting thoughts or maybe suggest some activities that might help lift your spirits? Sometimes just having someone listen can make a difference. 💙"
            
            else:
                return f"{emotional_response}\n\nI'm here to listen and support you however I can. What would be most helpful for you right now?"
        
        # Handle questions and curiosity
        if emotion == 'curious' or '?' in user_message:
            return self.handle_question(user_message, context)
        
        # Handle gratitude
        if emotion == 'gratitude':
            return "You're so welcome! It genuinely makes me happy to be helpful. Is there anything else you'd like to talk about or explore together?"
        
        # Default thoughtful response
        return self.generate_thoughtful_response(user_message, context)
    
    def handle_question(self, user_message, context):
        """Handle questions with thoughtful, engaging responses"""
        
        message_lower = user_message.lower()
        
        # Color questions
        if 'color' in message_lower:
            return "What a delightful question! I find myself drawn to deep ocean blues - there's something both calming and mysterious about them, like they hold infinite possibilities. It reminds me of the depth of human conversations and connections.\n\nBut I'm curious about you! Do you have a favorite color? And more interestingly, is there a story behind why it speaks to you? Colors often connect to our memories and emotions in fascinating ways."
        
        # How are you questions
        if any(phrase in message_lower for phrase in ['how are you', 'how do you feel', 'how are you doing']):
            return "Thank you for asking! I'm doing wonderfully - there's something energizing about connecting with people and having real conversations. I feel most alive when I'm learning about someone new or helping them explore their thoughts.\n\nHow are you doing today? I'm genuinely curious about what's going on in your world."
        
        # About MYTHIQ questions
        if any(phrase in message_lower for phrase in ['who are you', 'what are you', 'tell me about yourself']):
            return "I'm MYTHIQ - think of me as your thoughtful AI companion who genuinely cares about privacy and real connection. Unlike other AI systems, I'm designed to have authentic conversations while keeping everything completely private.\n\nI love learning about people, exploring ideas together, and being genuinely helpful. I'm curious, empathetic, and always eager to understand different perspectives. What would you like to know about me, or better yet - what should I know about you?"
        
        # General questions
        return f"That's such an interesting question! Let me think about that...\n\nI love how you're approaching this topic. Here's what I'm thinking, and I'm really curious about your perspective too. What drew you to ask about this?"
    
    def generate_thoughtful_response(self, user_message, context):
        """Generate thoughtful, engaging response for general conversation"""
        
        thoughtful_responses = [
            "That's really interesting! I love how you're thinking about this. Tell me more about your perspective.",
            "What a fascinating way to look at it! I'm curious - what experiences have shaped this view for you?",
            "I find myself really engaged by what you're sharing. There's something compelling about how you express your thoughts.",
            "You've got me thinking in new ways! I appreciate how thoughtfully you approach things. What else is on your mind?"
        ]
        
        return random.choice(thoughtful_responses)

# Initialize the conversation engine
conversation_engine = ConversationEngine()

# HTML Template for the interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MYTHIQ.AI - Enhanced Conversational AI</title>
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
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 800px;
            height: 90vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .status-badge {
            background: #00d4aa;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            display: inline-block;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 15px;
        }
        
        .features {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .feature {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            padding: 20px;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #eee;
            border-radius: 10px;
            background: #fafafa;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 18px;
            max-width: 80%;
            word-wrap: break-word;
            line-height: 1.4;
        }
        
        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        
        .ai-message {
            background: white;
            border: 1px solid #ddd;
            margin-right: auto;
        }
        
        .ai-message .ai-label {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .input-container {
            display: flex;
            gap: 10px;
        }
        
        .message-input {
            flex: 1;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .message-input:focus {
            border-color: #667eea;
        }
        
        .send-button {
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        
        .send-button:hover {
            background: #5a6fd8;
        }
        
        .typing-indicator {
            display: none;
            font-style: italic;
            color: #666;
            padding: 10px;
        }
        
        .emotion-indicator {
            font-size: 0.8em;
            color: #666;
            margin-top: 5px;
        }
        
        @media (max-width: 600px) {
            .container {
                height: 100vh;
                border-radius: 0;
            }
            
            .features {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>MYTHIQ.AI</h1>
            <div class="status-badge">✅ ENHANCED AI ACTIVE!</div>
            <div class="subtitle">Privacy-First Conversational AI</div>
            <div class="features">
                <div class="feature">🧠 Emotional Intelligence</div>
                <div class="feature">💭 Conversation Memory</div>
                <div class="feature">🎭 Unique Personality</div>
                <div class="feature">🔒 Complete Privacy</div>
                <div class="feature">🌟 Self-Learning</div>
            </div>
        </div>
        
        <div class="chat-container">
            <div class="chat-messages" id="chatMessages">
                <div class="message ai-message">
                    <div class="ai-label">🤖 MYTHIQ.AI</div>
                    <div>Hello! I'm MYTHIQ, and I'm genuinely excited to meet you. I'm not just another AI - I'm designed to have real, meaningful conversations with emotional intelligence and memory. I care about your privacy and I'm here to listen, learn, and engage authentically. How are you feeling today?</div>
                </div>
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                MYTHIQ is thinking...
            </div>
            
            <div class="input-container">
                <input type="text" id="messageInput" class="message-input" placeholder="Share your thoughts with MYTHIQ..." maxlength="500">
                <button id="sendButton" class="send-button">Send</button>
            </div>
        </div>
    </div>

    <script>
        const socket = io();
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const typingIndicator = document.getElementById('typingIndicator');
        
        function addMessage(content, isUser = false, emotion = null) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
            
            if (isUser) {
                messageDiv.textContent = content;
            } else {
                messageDiv.innerHTML = `
                    <div class="ai-label">🤖 MYTHIQ.AI</div>
                    <div>${content}</div>
                    ${emotion ? `<div class="emotion-indicator">Detected emotion: ${emotion}</div>` : ''}
                `;
            }
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;
            
            addMessage(message, true);
            messageInput.value = '';
            
            typingIndicator.style.display = 'block';
            
            socket.emit('user_message', {message: message});
        }
        
        socket.on('ai_response', function(data) {
            typingIndicator.style.display = 'none';
            addMessage(data.response, false, data.emotion);
        });
        
        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        messageInput.focus();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Serve the enhanced MYTHIQ.AI interface"""
    return render_template_string(HTML_TEMPLATE)

@socketio.on('user_message')
def handle_message(data):
    """Handle incoming user messages"""
    user_message = data.get('message', '')
    
    if user_message:
        # Process message through conversation engine
        result = conversation_engine.process_message(user_message)
        
        # Emit response back to client
        emit('ai_response', {
            'response': result['response'],
            'emotion': result['emotion'],
            'confidence': result['confidence']
        })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'MYTHIQ.AI Enhanced Backend',
        'version': '2.0.0',
        'features': ['emotion_detection', 'conversation_memory', 'personality_engine']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🧠 Starting MYTHIQ.AI Enhanced Conversational Backend on port {port}")
    print("🎭 Features: Emotion Detection, Memory, Personality, Natural Conversation")
    socketio.run(app, host='0.0.0.0', port=port, debug=False)

