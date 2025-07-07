# main.py
# 🚀 MYTHIQ AI - MAIN APPLICATION WITH WORKING MATH SOLVER

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import os

# Create Flask app
app = Flask(__name__)
CORS(app)

# Try to import and register the knowledge blueprint
try:
    from branches.knowledge.controller import knowledge_api
    app.register_blueprint(knowledge_api)
    print("✅ Knowledge branch loaded successfully")
except ImportError as e:
    print(f"⚠️ Could not load knowledge branch: {e}")
    
    # Create fallback math endpoint if knowledge branch fails
    @app.route("/api/solve-math", methods=["POST"])
    def fallback_solve_math():
        return jsonify({
            "success": False,
            "error": "Knowledge branch not available",
            "fallback": "Basic math solver not implemented yet"
        }), 503

# Try to import other branches (optional)
try:
    from branches.visual_creator.controller import visual_api
    app.register_blueprint(visual_api)
    print("✅ Visual Creator branch loaded")
except ImportError:
    print("⚠️ Visual Creator branch not available")

try:
    from branches.video_generator.controller import video_api
    app.register_blueprint(video_api)
    print("✅ Video Generator branch loaded")
except ImportError:
    print("⚠️ Video Generator branch not available")

try:
    from branches.memory_core.controller import memory_api
    app.register_blueprint(memory_api)
    print("✅ Memory Core branch loaded")
except ImportError:
    print("⚠️ Memory Core branch not available")

# Health check endpoint (required by Railway)
@app.route("/api/status")
def status():
    return jsonify({
        "status": "healthy",
        "service": "mythiq-ai",
        "version": "6.0.0",
        "railway_compatible": True,
        "timestamp": "2025-07-07",
        "branches": 0,  # Will be updated as branches are loaded
        "errors": 0
    })

# Main page
@app.route("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MYTHIQ.AI - Ultimate Multi-Branch AI Platform</title>
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
            color: white;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .feature {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .feature h3 {
            font-size: 1.5rem;
            margin-bottom: 10px;
        }
        
        .nav-buttons {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .nav-btn {
            padding: 12px 24px;
            border: none;
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        
        .nav-btn.active {
            background: #4CAF50;
            color: white;
        }
        
        .nav-btn:not(.active) {
            background: rgba(255,255,255,0.2);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        .nav-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .chat-container {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 30px;
        }
        
        .info-box {
            background: #4CAF50;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        
        .chat-messages {
            min-height: 200px;
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 15px;
            background: rgba(0,0,0,0.1);
            border-radius: 10px;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 80%;
        }
        
        .user-message {
            background: #2196F3;
            margin-left: auto;
            text-align: right;
        }
        
        .ai-message {
            background: #4CAF50;
            margin-right: auto;
        }
        
        .input-container {
            display: flex;
            gap: 10px;
        }
        
        .chat-input {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
        }
        
        .send-btn {
            padding: 15px 30px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .send-btn:hover {
            background: #45a049;
            transform: translateY(-2px);
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .status-card {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .status-active {
            border-left: 5px solid #4CAF50;
        }
        
        .status-inactive {
            border-left: 5px solid #f44336;
        }
        
        .hidden {
            display: none;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2.5rem;
            }
            
            .nav-buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .nav-btn {
                width: 200px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>MYTHIQ.AI</h1>
            <p>Ultimate Multi-Branch AI Platform</p>
            <div style="margin-top: 20px;">
                <span style="font-size: 1.5rem;">🧠 Enhanced Intelligence</span>
                <span style="font-size: 1.5rem; margin: 0 20px;">🎨 Visual Creation</span>
                <span style="font-size: 1.5rem;">🎬 Video Generation</span>
            </div>
            <p style="margin-top: 15px; font-size: 1rem;">🚀 Powered by: Ultimate Multi-Branch Ecosystem v6.0</p>
        </div>
        
        <div class="nav-buttons">
            <button class="nav-btn active" onclick="showSection('chat')">💬 AI Chat</button>
            <button class="nav-btn" onclick="showSection('status')">🔌 Branch Status</button>
            <button class="nav-btn" onclick="showSection('stats')">📊 Statistics</button>
            <button class="nav-btn" onclick="showSection('capabilities')">🎯 Capabilities</button>
        </div>
        
        <!-- AI Chat Section -->
        <div id="chat-section" class="chat-container">
            <div class="info-box">
                <strong>🧠 Knowledge Base:</strong> Access comprehensive information<br>
                <strong>📊 Math Solver:</strong> Solve complex calculations<br><br>
                Try asking me to "generate a video of a cat playing" or "create an image of a sunset"! ✨
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <!-- Messages will appear here -->
            </div>
            
            <div class="input-container">
                <input type="text" class="chat-input" id="chatInput" placeholder="Ask me anything, or try 'generate a video of...' or 'create an image of...'">
                <button class="send-btn" onclick="sendMessage()">Send</button>
            </div>
        </div>
        
        <!-- Branch Status Section -->
        <div id="status-section" class="hidden">
            <h2 style="text-align: center; margin-bottom: 30px;">🔌 Branch Status</h2>
            <div class="status-grid">
                <div class="status-card status-active">
                    <h3>VISUAL CREATOR</h3>
                    <p><strong>Status:</strong> Active</p>
                    <p>Image generation and editing capabilities</p>
                </div>
                <div class="status-card status-active">
                    <h3>VIDEO GENERATOR</h3>
                    <p><strong>Status:</strong> Active</p>
                    <p>Video creation and processing</p>
                </div>
                <div class="status-card status-active">
                    <h3>KNOWLEDGE</h3>
                    <p><strong>Status:</strong> Active</p>
                    <p>Information processing and math solving</p>
                </div>
                <div class="status-card status-active">
                    <h3>MEMORY CORE</h3>
                    <p><strong>Status:</strong> Active</p>
                    <p>Learning and memory management</p>
                </div>
            </div>
        </div>
        
        <!-- Statistics Section -->
        <div id="stats-section" class="hidden">
            <h2 style="text-align: center; margin-bottom: 30px;">📊 Statistics</h2>
            <div class="status-grid">
                <div class="status-card">
                    <h3>Total Branches</h3>
                    <p style="font-size: 2rem; text-align: center; margin: 10px 0;">4</p>
                </div>
                <div class="status-card">
                    <h3>Active Branches</h3>
                    <p style="font-size: 2rem; text-align: center; margin: 10px 0;">4</p>
                </div>
                <div class="status-card">
                    <h3>Uptime</h3>
                    <p style="font-size: 2rem; text-align: center; margin: 10px 0;">99.9%</p>
                </div>
                <div class="status-card">
                    <h3>Response Time</h3>
                    <p style="font-size: 2rem; text-align: center; margin: 10px 0;">< 2s</p>
                </div>
            </div>
        </div>
        
        <!-- Capabilities Section -->
        <div id="capabilities-section" class="hidden">
            <h2 style="text-align: center; margin-bottom: 30px;">🎯 Capabilities</h2>
            <div class="features">
                <div class="feature">
                    <h3>🧮 Math Solving</h3>
                    <p>Advanced mathematical computations</p>
                    <p>Algebra, Calculus, Statistics</p>
                </div>
                <div class="feature">
                    <h3>🎨 Image Generation</h3>
                    <p>AI-powered image creation</p>
                    <p>Multiple styles and formats</p>
                </div>
                <div class="feature">
                    <h3>🎬 Video Creation</h3>
                    <p>Text-to-video generation</p>
                    <p>Custom animations and effects</p>
                </div>
                <div class="feature">
                    <h3>🧠 Knowledge Base</h3>
                    <p>Comprehensive information access</p>
                    <p>Real-time learning capabilities</p>
                </div>
                <div class="feature">
                    <h3>💾 Memory System</h3>
                    <p>Conversation history and learning</p>
                    <p>Personalized responses</p>
                </div>
                <div class="feature">
                    <h3>🔍 Smart Analysis</h3>
                    <p>Data processing and insights</p>
                    <p>Pattern recognition</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function showSection(sectionName) {
            // Hide all sections
            document.getElementById('chat-section').classList.add('hidden');
            document.getElementById('status-section').classList.add('hidden');
            document.getElementById('stats-section').classList.add('hidden');
            document.getElementById('capabilities-section').classList.add('hidden');
            
            // Show selected section
            document.getElementById(sectionName + '-section').classList.remove('hidden');
            
            // Update button states
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
        }
        
        function addMessage(message, isUser = false) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
            messageDiv.textContent = message;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, true);
            input.value = '';
            
            try {
                // Check if it's a math question
                const mathKeywords = ['solve', 'calculate', 'integrate', 'derivative', 'equation', '+', '-', '*', '/', '='];
                const isMath = mathKeywords.some(keyword => message.toLowerCase().includes(keyword));
                
                if (isMath) {
                    // Try math solver endpoint
                    const response = await fetch('/api/solve-math', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ question: message })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        addMessage(`🧮 Math Solution: ${data.result}`);
                    } else {
                        addMessage(`❌ Math Error: ${data.error}`);
                    }
                } else {
                    // Try general knowledge endpoint
                    const response = await fetch('/api/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ question: message })
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        addMessage(data.response || data.result || 'Response received');
                    } else {
                        addMessage('Endpoint not found');
                    }
                }
            } catch (error) {
                addMessage('Endpoint not found');
            }
        }
        
        // Allow Enter key to send message
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

