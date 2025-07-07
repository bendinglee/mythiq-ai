# branches/knowledge/controller.py
# 🧮 WORKING MATH SOLVER WITH WOLFRAM ALPHA

from flask import Blueprint, request, jsonify
import os
import wolframalpha

# Create the blueprint
knowledge_api = Blueprint("knowledge_api", __name__)

# Load Wolfram Alpha App ID from Railway environment variables
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

# Initialize Wolfram Alpha client
if WOLFRAM_APP_ID:
    client = wolframalpha.Client(WOLFRAM_APP_ID)
else:
    client = None

@knowledge_api.route("/api/solve-math", methods=["POST"])
def solve_math():
    """
    Solve mathematical problems using Wolfram Alpha
    """
    try:
        data = request.get_json()
        question = data.get("question", "")
        
        if not question:
            return jsonify({
                "success": False, 
                "error": "No question provided"
            }), 400
        
        # Check if Wolfram Alpha is available
        if not client:
            return jsonify({
                "success": False,
                "error": "Wolfram Alpha not configured",
                "fallback": "Please check WOLFRAM_APP_ID environment variable"
            }), 500
        
        # Query Wolfram Alpha
        res = client.query(question)
        
        # Get the first result
        try:
            answer = next(res.results).text
            return jsonify({
                "success": True,
                "result": answer,
                "query": question,
                "source": "Wolfram Alpha"
            })
        except StopIteration:
            # No results found
            return jsonify({
                "success": False,
                "error": "No solution found",
                "query": question,
                "suggestion": "Try rephrasing your math problem"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "query": question if 'question' in locals() else "unknown"
        }), 500

@knowledge_api.route("/api/ask", methods=["POST"])
def ask_knowledge():
    """
    General knowledge endpoint that can handle math or other questions
    """
    try:
        data = request.get_json()
        question = data.get("question", "")
        
        if not question:
            return jsonify({
                "success": False,
                "error": "No question provided"
            }), 400
        
        # Check if it's a math question
        math_keywords = ['solve', 'calculate', 'integrate', 'derivative', 'equation', '+', '-', '*', '/', '=', 'x', 'y']
        is_math = any(keyword in question.lower() for keyword in math_keywords)
        
        if is_math and client:
            # Try to solve with Wolfram Alpha
            try:
                res = client.query(question)
                answer = next(res.results).text
                return jsonify({
                    "success": True,
                    "response": f"🧮 Math Solution: {answer}",
                    "query": question,
                    "source": "Wolfram Alpha"
                })
            except:
                pass
        
        # Fallback response for non-math or failed math queries
        return jsonify({
            "success": True,
            "response": "I love curious minds! 🧠 I can help with math problems! Try something like 'solve 2x + 5 = 15' or 'calculate 25 * 4 + 10'. For complex math, I use Wolfram Alpha! 📊",
            "query": question,
            "source": "fallback"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@knowledge_api.route("/api/knowledge/status", methods=["GET"])
def knowledge_status():
    """
    Check the status of the knowledge system
    """
    return jsonify({
        "status": "active",
        "wolfram_alpha_available": client is not None,
        "wolfram_app_id_configured": WOLFRAM_APP_ID is not None,
        "endpoints": [
            "/api/solve-math",
            "/api/ask",
            "/api/knowledge/status"
        ],
        "capabilities": [
            "mathematical_computation",
            "equation_solving",
            "calculus",
            "algebra",
            "general_knowledge"
        ]
    })
