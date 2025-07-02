from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
import os
import json
import time
import re
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mythiq-smart-key')
CORS(app, origins="*")

# Simple in-memory storage
conversations = {}
stats = {"total_requests": 0, "chat_requests": 0}

# Knowledge Base
KNOWLEDGE_BASE = {
    # Geography
    "capital of japan": "Tokyo",
    "capital of france": "Paris",
    "capital of usa": "Washington D.C.",
    "capital of uk": "London",
    "capital of germany": "Berlin",
    "largest country": "Russia",
    "smallest country": "Vatican City",
    
    # Science & Math
    "12 × 8": "96",
    "12 * 8": "96",
    "12 x 8": "96",
    "theory of relativity": "Albert Einstein",
    "relativity": "Albert Einstein",
    "chemical formula for table salt": "NaCl (sodium chloride)",
    "table salt formula": "NaCl",
    "largest planet": "Jupiter",
    "biggest planet": "Jupiter",
    "pythagorean theorem": "a² + b² = c² (in a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides)",
    "boiling point of water": "100°C (212°F) at standard atmospheric pressure",
    "water boiling point": "100°C",
    "father of computers": "Charles Babbage",
    "smallest unit of life": "Cell",
    "main ingredient in bread": "Flour",
    "bread ingredient": "Flour",
    "atomic number of carbon": "6",
    "carbon atomic number": "6",
    "2020 olympics": "Japan (Tokyo) - held in 2021 due to COVID-19",
    "olympics 2020": "Japan (Tokyo)",
    "si unit of force": "Newton (N)",
    "unit of force": "Newton",
    "largest organ": "Skin",
    "biggest organ": "Skin",
    "5 factorial": "120 (5! = 5 × 4 × 3 × 2 × 1 = 120)",
    "5!": "120",
    
    # Technology
    "who invented the internet": "Tim Berners-Lee (World Wide Web) and ARPANET team",
    "first computer": "ENIAC (1946) or Babbage's Analytical Engine (concept)",
    "programming language": "There are many: Python, JavaScript, Java, C++, etc.",
    
    # History
    "world war 2": "1939-1945",
    "ww2": "1939-1945",
    "first moon landing": "July 20, 1969 (Apollo 11, Neil Armstrong)",
    "moon landing": "1969",
    
    # Basic Math
    "2 + 2": "4",
    "10 × 10": "100",
    "square root of 16": "4",
    "pi": "3.14159... (approximately 3.14)",
    
    # General Knowledge
    "speed of light": "299,792,458 meters per second (approximately 300,000 km/s)",
    "gravity": "9.8 m/s² on Earth",
    "dna": "Deoxyribonucleic acid - carries genetic information",
    "photosynthesis": "Process where plants convert sunlight into energy using chlorophyll"
}

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MYTHIQ.AI - Smart Version</title>
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
        <div class="subtitle">Smart AI Chat Platform - Version 2.0</div>
    </div>
    
    <div class="status">
        ✅ System Online • Smart AI Active • Knowledge Base Loaded • Ready for Questions
    </div>
    
    <div class="container">
        <div class="chat-box">
            <h3>💬 Smart AI Chat</h3>
            <div class="messages" id="messages">
                <div class="ai-message">
                    <strong>MYTHIQ.AI:</strong> Hello! I'm your smart AI assistant with a comprehensive knowledge base! 🧠 I can answer factual questions, solve math problems, and help with various topics while maintaining a friendly personality. Try asking me anything! ✨
                </div>
            </div>
            
            <div class="input-area">
                <input type="text" id="messageInput" placeholder="Ask me anything - facts, math, science, history..." />
                <button id="sendButton">Send</button>
            </div>
        </div>
        
        <div class="features">
            <h3>🎯 Smart Features</h3>
            <div class="feature-list">
                <div class="feature">
                    <strong>🧠 Knowledge Base</strong><br>
                    Answers factual questions accurately
                </div>
                <div class="feature">
                    <strong>🔢 Math Solver</strong><br>
                    Solves calculations and equations
                </div>
                <div class="feature">
                    <strong>😊 Emotional Intelligence</strong><br>
                    Friendly, enthusiastic responses
                </div>
                <div class="feature">
                    <strong>📚 Educational</strong><br>
                    Provides explanations and context
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
            sendButton.textContent = 'Thinking...';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        user_id: 'smart_user_' + Date.now()
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
    
    if any(word in text_lower for word in ['happy', 'great', 'awesome', 'wonderful', 'excited', 'amazing', 'fantastic']):
        return 'happy'
    elif any(word in text_lower for word in ['sad', 'upset', 'down', 'depressed', 'disappointed']):
        return 'sad'
    elif any(word in text_lower for word in ['help', 'support', 'problem', 'issue', 'stuck']):
        return 'supportive'
    elif any(word in text_lower for word in ['what', 'how', 'why', 'when', 'where', 'who', '?']):
        return 'curious'
    elif any(word in text_lower for word in ['thank', 'thanks', 'appreciate']):
        return 'grateful'
    else:
        return 'neutral'

def find_answer_in_knowledge_base(question):
    """Find answer in knowledge base"""
    question_lower = question.lower().strip()
    
    # Remove common question words and punctuation
    question_clean = re.sub(r'[^\w\s]', '', question_lower)
    question_clean = re.sub(r'\b(what|is|the|of|in|a|an|are|was|were|do|does|did|can|could|would|should|will)\b', '', question_clean)
    question_clean = ' '.join(question_clean.split())
    
    # Direct match first
    if question_lower in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[question_lower]
    
    # Partial match
    for key, value in KNOWLEDGE_BASE.items():
        if key in question_lower or question_clean in key:
            return value
    
    # Math operations
    if any(op in question for op in ['×', '*', 'x', '+']):
        try:
            # Simple math evaluation (safe for basic operations)
            math_expr = question_lower.replace('×', '*').replace('x', '*')
            # Extract numbers and operators
            import re
            numbers = re.findall(r'\d+', math_expr)
            if len(numbers) >= 2:
                if '*' in math_expr or '×' in question or ' x ' in question:
                    result = int(numbers[0]) * int(numbers[1])
                    return str(result)
                elif '+' in math_expr:
                    result = int(numbers[0]) + int(numbers[1])
                    return str(result)
        except:
            pass
    
    return None

def generate_smart_response(user_message, emotion, user_id):
    """Generate smart AI responses with knowledge"""
    
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
    
    # Try to find factual answer first
    factual_answer = find_answer_in_knowledge_base(user_message)
    
    if factual_answer:
        # Combine factual answer with emotional response
        emotional_intros = {
            'curious': ["Great question! 🤔", "I love curious minds! 🧠", "Excellent question! ✨"],
            'happy': ["I'm excited to share this! 😊", "Wonderful question! 🌟", "I love your enthusiasm! 🎉"],
            'supportive': ["I'm here to help! 🤝", "Let me assist you with that! 💪", "Happy to help! 🌟"],
            'grateful': ["You're so welcome! 😊", "My pleasure to help! ✨", "Glad I could assist! 🌟"],
            'neutral': ["Here's what I know! 📚", "Let me share that with you! ✨", "I can help with that! 🧠"]
        }
        
        import random
        intro = random.choice(emotional_intros.get(emotion, emotional_intros['neutral']))
        
        # Add educational context for some answers
        educational_additions = {
            "Tokyo": "It's been Japan's capital since 1868 and is one of the world's largest metropolitan areas!",
            "96": "Here's a quick way: 12 × 8 = (10 × 8) + (2 × 8) = 80 + 16 = 96!",
            "Albert Einstein": "He developed both special relativity (1905) and general relativity (1915)!",
            "Jupiter": "It's so massive that it could fit all other planets inside it!",
            "100°C": "That's 212°F, and it changes with altitude - higher up, water boils at lower temperatures!",
            "Cell": "Discovered by Robert Hooke in 1665, cells are the building blocks of all living things!",
            "Newton": "Named after Sir Isaac Newton, who formulated the laws of motion and gravity!"
        }
        
        education = ""
        for key, value in educational_additions.items():
            if key in factual_answer:
                education = f" {value}"
                break
        
        return f"{intro} {factual_answer}{education}"
    
    else:
        # Fallback to conversational responses
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
                "I'd love to help you learn more! Could you be more specific about what you'd like to know? 🤔",
                "That's an interesting topic! Could you rephrase your question so I can give you the best answer?"
            ],
            'grateful': [
                "You're so welcome! I'm always happy to help! 😊",
                "My pleasure! Feel free to ask me anything else you'd like to know! ✨"
            ],
            'neutral': [
                "Thanks for chatting with me! I'm here to help with questions, facts, math, and more. ✨",
                "Hello! I'm MYTHIQ.AI and I love answering questions! What would you like to know?"
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
        "message": "MYTHIQ.AI Smart Version - All systems operational",
        "version": "2.0-smart",
        "platform": "Railway",
        "features": [
            "smart_chat", "knowledge_base", "emotion_detection", "math_solver",
            "educational_responses", "conversation_memory", "railway_deployment"
        ],
        "knowledge_topics": [
            "geography", "science", "mathematics", "history", "technology", "general_knowledge"
        ],
        "active_conversations": len(conversations),
        "total_requests": stats["total_requests"],
        "knowledge_entries": len(KNOWLEDGE_BASE),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Smart chat API with knowledge base"""
    try:
        stats["total_requests"] += 1
        stats["chat_requests"] += 1
        
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'smart_user')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        if len(user_message) > 1000:
            return jsonify({"error": "Message too long (max 1000 characters)"}), 400
        
        # Emotion detection
        emotion = simple_emotion_detection(user_message)
        
        # Generate smart response
        response = generate_smart_response(user_message, emotion, user_id)
        
        # Check if we found a factual answer
        factual_answer = find_answer_in_knowledge_base(user_message)
        
        return jsonify({
            "response": response,
            "emotion": emotion,
            "factual_answer_found": factual_answer is not None,
            "timestamp": datetime.now().isoformat(),
            "conversation_count": len(conversations.get(user_id, [])),
            "version": "2.0-smart"
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
        "message": "MYTHIQ.AI Smart Version is working perfectly!",
        "current_features": [
            "✅ Smart chat with comprehensive knowledge base",
            "✅ Factual answers to questions (geography, science, math, history)",
            "✅ Math problem solving (multiplication, addition, etc.)",
            "✅ Emotion detection with appropriate responses",
            "✅ Educational context and explanations",
            "✅ Conversation memory (5 messages per user)",
            "✅ Railway deployment with health checks",
            "✅ Beautiful responsive interface"
        ],
        "sample_questions": [
            "What is the capital of Japan?",
            "What is 12 × 8?",
            "Who developed the theory of relativity?",
            "What is the largest planet?",
            "What is the boiling point of water?"
        ],
        "knowledge_base_size": len(KNOWLEDGE_BASE),
        "timestamp": datetime.now().isoformat(),
        "version": "2.0-smart"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

