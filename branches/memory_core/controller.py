# 🧠 SELF-LEARNING AI BRAIN
# This makes your AI remember and learn from users

from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime
from sentence_transformers import SentenceTransformer
import sqlite3

# Create the brain blueprint
memory_api = Blueprint('memory_api', __name__)

# Initialize the learning model (free!)
try:
    learning_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("🧠 Learning brain loaded successfully!")
except:
    learning_model = None
    print("⚠️ Learning brain not loaded - will use basic memory")

# Database setup
def init_memory_database():
    """Create the memory database if it doesn't exist"""
    conn = sqlite3.connect('ai_memory.db')
    cursor = conn.cursor()
    
    # Create conversations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            feedback TEXT DEFAULT 'neutral',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            plugin_used TEXT,
            confidence_score REAL DEFAULT 0.5
        )
    ''')
    
    # Create learning patterns table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_type TEXT NOT NULL,
            pattern_data TEXT NOT NULL,
            success_rate REAL DEFAULT 0.5,
            usage_count INTEGER DEFAULT 1,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("🗄️ Memory database initialized!")

# Initialize database when module loads
init_memory_database()

@memory_api.route('/memory/learn', methods=['POST'])
def learn_from_interaction():
    """
    🧠 LEARNING ENDPOINT
    Saves user interactions and learns from them
    """
    try:
        data = request.get_json() or {}
        
        user_input = data.get('user_input', '')
        ai_response = data.get('ai_response', '')
        feedback = data.get('feedback', 'neutral')  # positive, negative, neutral
        plugin_used = data.get('plugin_used', 'unknown')
        
        if not user_input or not ai_response:
            return jsonify({
                "success": False,
                "error": "Both user_input and ai_response are required"
            }), 400
        
        # Save to memory database
        conn = sqlite3.connect('ai_memory.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations 
            (user_input, ai_response, feedback, plugin_used)
            VALUES (?, ?, ?, ?)
        ''', (user_input, ai_response, feedback, plugin_used))
        
        conn.commit()
        conversation_id = cursor.lastrowid
        conn.close()
        
        # Learn from the interaction
        learning_result = analyze_and_learn(user_input, ai_response, feedback)
        
        return jsonify({
            "success": True,
            "message": "🧠 AI learned from this interaction!",
            "conversation_id": conversation_id,
            "learning_insights": learning_result,
            "memory_status": "updated"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Learning failed: {str(e)}"
        }), 500

@memory_api.route('/memory/recall', methods=['POST'])
def recall_similar_conversations():
    """
    🔍 MEMORY RECALL
    Finds similar past conversations to help answer new questions
    """
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        limit = data.get('limit', 5)
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Query is required"
            }), 400
        
        # Find similar conversations
        similar_conversations = find_similar_conversations(query, limit)
        
        # Get learning insights
        insights = get_learning_insights(query)
        
        return jsonify({
            "success": True,
            "query": query,
            "similar_conversations": similar_conversations,
            "learning_insights": insights,
            "total_memories": len(similar_conversations)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Memory recall failed: {str(e)}"
        }), 500

@memory_api.route('/memory/feedback', methods=['POST'])
def update_feedback():
    """
    👍👎 FEEDBACK SYSTEM
    Users can rate AI responses to improve learning
    """
    try:
        data = request.get_json() or {}
        conversation_id = data.get('conversation_id')
        feedback = data.get('feedback')  # 'positive', 'negative', 'neutral'
        
        if not conversation_id or not feedback:
            return jsonify({
                "success": False,
                "error": "conversation_id and feedback are required"
            }), 400
        
        # Update feedback in database
        conn = sqlite3.connect('ai_memory.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE conversations 
            SET feedback = ?, confidence_score = ?
            WHERE id = ?
        ''', (feedback, get_confidence_score(feedback), conversation_id))
        
        conn.commit()
        conn.close()
        
        # Update learning patterns
        update_learning_patterns(conversation_id, feedback)
        
        return jsonify({
            "success": True,
            "message": f"🧠 Feedback recorded: {feedback}",
            "conversation_id": conversation_id,
            "learning_status": "updated"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Feedback update failed: {str(e)}"
        }), 500

@memory_api.route('/memory/stats', methods=['GET'])
def memory_statistics():
    """
    📊 LEARNING STATISTICS
    Shows how much the AI has learned
    """
    try:
        conn = sqlite3.connect('ai_memory.db')
        cursor = conn.cursor()
        
        # Get conversation stats
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total_conversations = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM conversations WHERE feedback = "positive"')
        positive_feedback = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM conversations WHERE feedback = "negative"')
        negative_feedback = cursor.fetchone()[0]
        
        cursor.execute('SELECT plugin_used, COUNT(*) FROM conversations GROUP BY plugin_used')
        plugin_usage = dict(cursor.fetchall())
        
        cursor.execute('SELECT AVG(confidence_score) FROM conversations')
        avg_confidence = cursor.fetchone()[0] or 0.5
        
        conn.close()
        
        # Calculate learning metrics
        learning_rate = (positive_feedback / max(total_conversations, 1)) * 100
        improvement_score = min(100, learning_rate + (avg_confidence * 50))
        
        return jsonify({
            "success": True,
            "learning_statistics": {
                "total_conversations": total_conversations,
                "positive_feedback": positive_feedback,
                "negative_feedback": negative_feedback,
                "learning_rate": round(learning_rate, 2),
                "improvement_score": round(improvement_score, 2),
                "average_confidence": round(avg_confidence, 3),
                "plugin_usage": plugin_usage,
                "memory_status": "active",
                "learning_model_loaded": learning_model is not None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Statistics failed: {str(e)}"
        }), 500

def analyze_and_learn(user_input, ai_response, feedback):
    """Analyze interaction and extract learning patterns"""
    try:
        insights = {
            "input_length": len(user_input),
            "response_length": len(ai_response),
            "feedback_type": feedback,
            "learning_points": []
        }
        
        # Analyze input patterns
        if len(user_input) < 10:
            insights["learning_points"].append("Short queries detected")
        elif len(user_input) > 100:
            insights["learning_points"].append("Complex queries detected")
        
        # Analyze feedback patterns
        if feedback == "positive":
            insights["learning_points"].append("Successful response pattern identified")
        elif feedback == "negative":
            insights["learning_points"].append("Response improvement needed")
        
        # Store learning pattern
        conn = sqlite3.connect('ai_memory.db')
        cursor = conn.cursor()
        
        pattern_data = json.dumps({
            "input_type": classify_input_type(user_input),
            "response_quality": feedback,
            "context": user_input[:50] + "..." if len(user_input) > 50 else user_input
        })
        
        cursor.execute('''
            INSERT INTO learning_patterns (pattern_type, pattern_data)
            VALUES (?, ?)
        ''', ("interaction_analysis", pattern_data))
        
        conn.commit()
        conn.close()
        
        return insights
        
    except Exception as e:
        return {"error": str(e)}

def find_similar_conversations(query, limit=5):
    """Find conversations similar to the current query"""
    try:
        conn = sqlite3.connect('ai_memory.db')
        cursor = conn.cursor()
        
        # Simple keyword-based similarity for now
        # In production, you'd use embeddings
        cursor.execute('''
            SELECT user_input, ai_response, feedback, timestamp
            FROM conversations
            WHERE user_input LIKE ? OR ai_response LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))
        
        results = cursor.fetchall()
        conn.close()
        
        similar_conversations = []
        for row in results:
            similar_conversations.append({
                "user_input": row[0],
                "ai_response": row[1],
                "feedback": row[2],
                "timestamp": row[3],
                "similarity_score": calculate_similarity(query, row[0])
            })
        
        return similar_conversations
        
    except Exception as e:
        return []

def get_learning_insights(query):
    """Get insights about what the AI has learned"""
    try:
        conn = sqlite3.connect('ai_memory.db')
        cursor = conn.cursor()
        
        # Get patterns related to this type of query
        input_type = classify_input_type(query)
        
        cursor.execute('''
            SELECT pattern_data, success_rate, usage_count
            FROM learning_patterns
            WHERE pattern_type = ?
            ORDER BY usage_count DESC
            LIMIT 3
        ''', (input_type,))
        
        patterns = cursor.fetchall()
        conn.close()
        
        insights = {
            "query_type": input_type,
            "learned_patterns": len(patterns),
            "recommendations": []
        }
        
        for pattern in patterns:
            try:
                pattern_info = json.loads(pattern[0])
                insights["recommendations"].append({
                    "pattern": pattern_info.get("context", "Unknown"),
                    "success_rate": pattern[1],
                    "usage_count": pattern[2]
                })
            except:
                pass
        
        return insights
        
    except Exception as e:
        return {"error": str(e)}

def classify_input_type(user_input):
    """Classify the type of user input"""
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ['solve', 'calculate', 'math', '=', '+', '-', '*', '/']):
        return "math_query"
    elif any(word in user_input_lower for word in ['create', 'generate', 'make', 'image', 'picture']):
        return "creation_query"
    elif any(word in user_input_lower for word in ['video', 'animation', 'movie']):
        return "video_query"
    elif '?' in user_input:
        return "question"
    else:
        return "general_query"

def calculate_similarity(query1, query2):
    """Simple similarity calculation"""
    words1 = set(query1.lower().split())
    words2 = set(query2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)

def get_confidence_score(feedback):
    """Convert feedback to confidence score"""
    if feedback == "positive":
        return 0.9
    elif feedback == "negative":
        return 0.1
    else:
        return 0.5

def update_learning_patterns(conversation_id, feedback):
    """Update learning patterns based on feedback"""
    try:
        # This would update the AI's understanding
        # For now, just log the learning event
        print(f"🧠 Learning from conversation {conversation_id}: {feedback}")
        
        # In a more advanced system, you'd:
        # 1. Update model weights
        # 2. Adjust response strategies
        # 3. Improve prompt engineering
        
    except Exception as e:
        print(f"Learning update failed: {e}")

# Export the blueprint
__all__ = ['memory_api']
