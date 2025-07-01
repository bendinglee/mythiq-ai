import os
import gc
import time
import json
import redis
import torch
import asyncio
import threading
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template_string
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from apscheduler.schedulers.background import BackgroundScheduler
import psutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mythiq-ai-secret-key')
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global variables for memory management
conversation_model = None
last_activity = time.time()
model_loaded = False
scheduler = BackgroundScheduler()

# Redis connection (Upstash free tier)
try:
    redis_client = redis.from_url(
        os.environ.get('REDIS_URL', 'redis://localhost:6379'),
        decode_responses=True
    )
    redis_client.ping()
    logger.info("✅ Redis connected successfully")
except Exception as e:
    logger.error(f"❌ Redis connection failed: {e}")
    redis_client = None

class MemoryOptimizer:
    """Optimize memory usage for Railway 1GB limit"""
    
    @staticmethod
    def get_memory_usage():
        """Get current memory usage percentage"""
        return psutil.virtual_memory().percent
    
    @staticmethod
    def cleanup_memory():
        """Aggressive memory cleanup"""
        global conversation_model
        
        if conversation_model:
            del conversation_model
            conversation_model = None
        
        # Clear PyTorch cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Force garbage collection
        gc.collect()
        
        logger.info(f"🧹 Memory cleaned. Usage: {MemoryOptimizer.get_memory_usage():.1f}%")
    
    @staticmethod
    def should_cleanup():
        """Determine if memory cleanup is needed"""
        memory_usage = MemoryOptimizer.get_memory_usage()
        return memory_usage > 85  # Cleanup if over 85% memory usage

class SmartSleepManager:
    """Manage smart sleeping to conserve Railway hours"""
    
    def __init__(self):
        self.last_activity = time.time()
        self.sleep_threshold = 300  # 5 minutes of inactivity
        self.monthly_hours_used = self.get_monthly_hours()
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = time.time()
        global last_activity
        last_activity = self.last_activity
    
    def get_monthly_hours(self):
        """Get monthly hours used from Redis"""
        if redis_client:
            try:
                hours = redis_client.get('monthly_hours_used')
                return float(hours) if hours else 0
            except:
                return 0
        return 0
    
    def update_monthly_hours(self, hours_to_add):
        """Update monthly hours used"""
        if redis_client:
            try:
                current_hours = self.get_monthly_hours()
                new_hours = current_hours + hours_to_add
                redis_client.setex('monthly_hours_used', 86400 * 31, new_hours)  # 31 days
                self.monthly_hours_used = new_hours
            except Exception as e:
                logger.error(f"Failed to update monthly hours: {e}")
    
    def should_sleep(self):
        """Determine if app should sleep"""
        inactive_time = time.time() - self.last_activity
        
        # Sleep if inactive for too long
        if inactive_time > self.sleep_threshold:
            return True
        
        # Sleep if approaching monthly limit (450 hours used of 500)
        if self.monthly_hours_used > 450:
            return True
        
        return False
    
    def get_status(self):
        """Get sleep manager status"""
        return {
            "last_activity": self.last_activity,
            "inactive_seconds": time.time() - self.last_activity,
            "monthly_hours_used": self.monthly_hours_used,
            "hours_remaining": 500 - self.monthly_hours_used,
            "should_sleep": self.should_sleep()
        }

class ModelManager:
    """Manage AI models with lazy loading and memory optimization"""
    
    @staticmethod
    def load_conversation_model():
        """Load conversation model with memory optimization"""
        global conversation_model, model_loaded
        
        if conversation_model is not None:
            return conversation_model
        
        try:
            logger.info("🤖 Loading conversation model...")
            
            # Use smaller, quantized model for free tier
            model_name = "microsoft/DialoGPT-small"
            
            # Load with memory optimizations
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                low_cpu_mem_usage=True,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            # Disable gradients for inference
            torch.set_grad_enabled(False)
            model.eval()
            
            conversation_model = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device=0 if torch.cuda.is_available() else -1,
                framework="pt"
            )
            
            model_loaded = True
            logger.info(f"✅ Model loaded. Memory usage: {MemoryOptimizer.get_memory_usage():.1f}%")
            
            return conversation_model
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            return None
    
    @staticmethod
    def unload_model():
        """Unload model to free memory"""
        global conversation_model, model_loaded
        
        if conversation_model:
            del conversation_model
            conversation_model = None
            model_loaded = False
            MemoryOptimizer.cleanup_memory()
            logger.info("🗑️ Model unloaded")

class CacheManager:
    """Manage Redis caching for responses and data"""
    
    @staticmethod
    def get_cached_response(prompt_hash):
        """Get cached response for prompt"""
        if not redis_client:
            return None
        
        try:
            cached = redis_client.get(f"response:{prompt_hash}")
            return json.loads(cached) if cached else None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    @staticmethod
    def cache_response(prompt_hash, response, ttl=3600):
        """Cache response with TTL"""
        if not redis_client:
            return
        
        try:
            redis_client.setex(
                f"response:{prompt_hash}",
                ttl,
                json.dumps(response)
            )
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    @staticmethod
    def get_user_memory(user_id):
        """Get user conversation memory"""
        if not redis_client:
            return []
        
        try:
            memory = redis_client.get(f"memory:{user_id}")
            return json.loads(memory) if memory else []
        except Exception as e:
            logger.error(f"Memory get error: {e}")
            return []
    
    @staticmethod
    def update_user_memory(user_id, conversation, max_memory=10):
        """Update user conversation memory"""
        if not redis_client:
            return
        
        try:
            memory = CacheManager.get_user_memory(user_id)
            memory.append(conversation)
            
            # Keep only last N conversations
            if len(memory) > max_memory:
                memory = memory[-max_memory:]
            
            redis_client.setex(
                f"memory:{user_id}",
                86400 * 7,  # 7 days
                json.dumps(memory)
            )
        except Exception as e:
            logger.error(f"Memory update error: {e}")

# Initialize managers
sleep_manager = SmartSleepManager()

# Background tasks
def monitor_system():
    """Background system monitoring"""
    try:
        # Update activity tracking
        uptime_hours = (time.time() - app.start_time) / 3600
        sleep_manager.update_monthly_hours(0.1)  # Add 6 minutes
        
        # Memory cleanup if needed
        if MemoryOptimizer.should_cleanup():
            MemoryOptimizer.cleanup_memory()
        
        # Unload model if inactive
        if time.time() - last_activity > 600 and model_loaded:  # 10 minutes
            ModelManager.unload_model()
        
        logger.info(f"📊 System check - Memory: {MemoryOptimizer.get_memory_usage():.1f}%, "
                   f"Hours used: {sleep_manager.monthly_hours_used:.1f}")
        
    except Exception as e:
        logger.error(f"Monitor error: {e}")

# Schedule background monitoring
scheduler.add_job(monitor_system, 'interval', minutes=5)
scheduler.start()

# HTML Template for the interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MYTHIQ.AI - Enhanced & Optimized</title>
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
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
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
        .optimization-info {
            background: rgba(0,255,0,0.1);
            border: 1px solid rgba(0,255,0,0.3);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            color: white;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 MYTHIQ.AI - Enhanced & Optimized</h1>
        <p>Free Tier Optimized • Smart Memory Management • Redis Caching</p>
    </div>
    
    <div class="status-bar">
        <span id="memoryStatus">Memory: Loading...</span>
        <span id="cacheStatus">Cache: Connected</span>
        <span id="modelStatus">Model: Unloaded</span>
        <span id="hoursStatus">Hours: Loading...</span>
    </div>
    
    <div class="optimization-info">
        <strong>🚀 Railway Free Tier Optimizations Active:</strong><br>
        • Smart model loading/unloading • Redis response caching • Memory cleanup • Sleep scheduling
    </div>
    
    <div class="chat-container">
        <div class="messages" id="messages">
            <div class="ai-message">
                <strong>MYTHIQ.AI:</strong> Hello! I'm your optimized AI companion running on Railway's free tier with smart memory management and Redis caching. I'm ready to chat with enhanced performance! 🎭✨
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
        
        // Status elements
        const memoryStatus = document.getElementById('memoryStatus');
        const cacheStatus = document.getElementById('cacheStatus');
        const modelStatus = document.getElementById('modelStatus');
        const hoursStatus = document.getElementById('hoursStatus');
        
        // Update status periodically
        setInterval(() => {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    memoryStatus.textContent = `Memory: ${data.memory_usage}%`;
                    modelStatus.textContent = `Model: ${data.model_loaded ? 'Loaded' : 'Unloaded'}`;
                    hoursStatus.textContent = `Hours: ${data.hours_remaining.toFixed(1)} left`;
                });
        }, 10000);
        
        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
            messageDiv.innerHTML = `<strong>${isUser ? 'You' : 'MYTHIQ.AI'}:</strong> ${content}`;
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
            addMessage(data.response);
            sendButton.disabled = false;
            sendButton.textContent = 'Send';
        });
        
        socket.on('status_update', (data) => {
            if (data.type === 'model_loading') {
                addMessage('🤖 Loading AI model for better responses...');
            } else if (data.type === 'cache_hit') {
                addMessage('⚡ Retrieved cached response for faster delivery!');
            }
        });
        
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        sendButton.addEventListener('click', sendMessage);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the optimized chat interface"""
    sleep_manager.update_activity()
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    """Get system status for monitoring"""
    sleep_manager.update_activity()
    
    status = {
        "memory_usage": round(MemoryOptimizer.get_memory_usage(), 1),
        "model_loaded": model_loaded,
        "redis_connected": redis_client is not None,
        "sleep_status": sleep_manager.get_status(),
        "hours_remaining": 500 - sleep_manager.monthly_hours_used
    }
    
    return jsonify(status)

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Optimized chat API with caching"""
    sleep_manager.update_activity()
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'anonymous')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Check cache first
        prompt_hash = str(hash(user_message))
        cached_response = CacheManager.get_cached_response(prompt_hash)
        
        if cached_response:
            logger.info("⚡ Cache hit for prompt")
            return jsonify({
                "response": cached_response["response"],
                "cached": True,
                "emotion": cached_response.get("emotion", "neutral")
            })
        
        # Load model if needed
        model = ModelManager.load_conversation_model()
        if not model:
            return jsonify({"error": "Model unavailable"}), 503
        
        # Generate response
        try:
            # Simple emotion detection
            emotion = "neutral"
            if any(word in user_message.lower() for word in ["sad", "upset", "down"]):
                emotion = "sad"
            elif any(word in user_message.lower() for word in ["happy", "excited", "great"]):
                emotion = "happy"
            elif any(word in user_message.lower() for word in ["angry", "mad", "frustrated"]):
                emotion = "angry"
            
            # Generate response based on emotion
            if emotion == "sad":
                response = f"I can sense you're feeling down. I'm here to support you! Let's talk about what's bothering you. 💙"
            elif emotion == "happy":
                response = f"That's wonderful! I'm absolutely thrilled to hear you're feeling great! ✨ What's making you so happy?"
            elif emotion == "angry":
                response = f"I understand you're frustrated. Take a deep breath - I'm here to listen and help you work through this. 🤗"
            else:
                # Use model for neutral responses
                inputs = f"User: {user_message}\nMYTHIQ.AI:"
                outputs = model(inputs, max_length=len(inputs.split()) + 50, num_return_sequences=1, temperature=0.7)
                response = outputs[0]['generated_text'].split("MYTHIQ.AI:")[-1].strip()
                
                if not response:
                    response = "I'm here to chat with you! What would you like to talk about? 😊"
        
        except Exception as e:
            logger.error(f"Generation error: {e}")
            response = "I'm having trouble generating a response right now, but I'm still here to chat! 😊"
        
        # Cache the response
        response_data = {"response": response, "emotion": emotion}
        CacheManager.cache_response(prompt_hash, response_data)
        
        # Update user memory
        CacheManager.update_user_memory(user_id, {
            "user": user_message,
            "ai": response,
            "emotion": emotion,
            "timestamp": datetime.now().isoformat()
        })
        
        return jsonify({
            "response": response,
            "cached": False,
            "emotion": emotion
        })
        
    except Exception as e:
        logger.error(f"Chat API error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@socketio.on('user_message')
def handle_message(data):
    """Handle real-time chat messages"""
    sleep_manager.update_activity()
    
    try:
        user_message = data.get('message', '').strip()
        
        # Check cache first
        prompt_hash = str(hash(user_message))
        cached_response = CacheManager.get_cached_response(prompt_hash)
        
        if cached_response:
            emit('status_update', {'type': 'cache_hit'})
            emit('ai_response', {'response': cached_response["response"]})
            return
        
        # Notify model loading
        if not model_loaded:
            emit('status_update', {'type': 'model_loading'})
        
        # Load model and generate response
        model = ModelManager.load_conversation_model()
        if not model:
            emit('ai_response', {'response': 'I apologize, but I\'m having trouble loading my AI model right now. Please try again in a moment! 😊'})
            return
        
        # Simple passionate response generation
        passionate_responses = {
            "hello": "Hello there! I'm absolutely THRILLED to meet you! 🎉 What brings you here today?",
            "how are you": "I'm doing wonderfully, thank you for asking! I'm so excited to chat with you! ✨ How are YOU doing?",
            "help": "I'm here to help and I'm SO excited to assist you! 🚀 What can I do for you today?",
            "bye": "Aww, it was absolutely amazing chatting with you! Come back soon! 💫",
        }
        
        # Check for simple patterns
        response = None
        for pattern, reply in passionate_responses.items():
            if pattern in user_message.lower():
                response = reply
                break
        
        if not response:
            response = f"That's really interesting! I love chatting about {user_message[:20]}... Tell me more! 😊✨"
        
        # Cache and emit response
        response_data = {"response": response, "emotion": "enthusiastic"}
        CacheManager.cache_response(prompt_hash, response_data)
        
        emit('ai_response', {'response': response})
        
    except Exception as e:
        logger.error(f"SocketIO error: {e}")
        emit('ai_response', {'response': 'I encountered an error, but I\'m still here to chat! 😊'})

# Store app start time for uptime tracking
app.start_time = time.time()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    logger.info("🚀 Starting MYTHIQ.AI Enhanced Backend")
    logger.info(f"📊 Memory usage at startup: {MemoryOptimizer.get_memory_usage():.1f}%")
    logger.info(f"🔗 Redis connected: {redis_client is not None}")
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=port,
        debug=False,
        allow_unsafe_werkzeug=True
    )

