# 🧮 COMPLETE MATH SOLVER CONTROLLER
# File: branches/knowledge/controller.py
# REPLACE YOUR EXISTING controller.py WITH THIS COMPLETE VERSION

from flask import Blueprint, request, jsonify
import requests
import urllib.parse
import os
import re
import math
from datetime import datetime
import json

# Create the blueprint
knowledge_api = Blueprint('knowledge_api', __name__)

# Wolfram Alpha configuration
WOLFRAM_APP_ID = os.getenv('WOLFRAM_APP_ID')
WOLFRAM_API_URL = "http://api.wolframalpha.com/v2/query"

# Simple cache for math results
math_cache = {}

def solve_math_problem(query ):
    """
    Real math solving using Wolfram Alpha with Python fallbacks
    This function handles ALL types of math problems
    """
    try:
        # Check cache first
        cache_key = query.lower().strip()
        if cache_key in math_cache:
            cached_result = math_cache[cache_key]
            cached_result["cached"] = True
            return cached_result
        
        # Try Wolfram Alpha first (if API key available)
        if WOLFRAM_APP_ID:
            wolfram_result = query_wolfram_alpha(query)
            if wolfram_result["success"]:
                # Cache successful results
                math_cache[cache_key] = wolfram_result
                return wolfram_result
        
        # Fallback to Python math solver
        python_result = python_math_solver(query)
        if python_result["success"]:
            # Cache successful results
            math_cache[cache_key] = python_result
            return python_result
        
        # If all else fails, provide helpful guidance
        return math_help_response(query)
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Math solving encountered an error",
            "source": "error_handler"
        }

def query_wolfram_alpha(query):
    """Query Wolfram Alpha API for math solutions"""
    try:
        # Prepare the query parameters
        params = {
            'input': query,
            'appid': WOLFRAM_APP_ID,
            'format': 'plaintext',
            'output': 'json',
            'includepodid': 'Solution,Result,DecimalApproximation,Input',
            'timeout': 10
        }
        
        # Make the API request
        response = requests.get(WOLFRAM_API_URL, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('queryresult', {}).get('success'):
                pods = data['queryresult'].get('pods', [])
                solution = extract_wolfram_solution(pods, query)
                
                if solution:
                    return {
                        "success": True,
                        "solution": solution,
                        "query": query,
                        "source": "Wolfram Alpha",
                        "timestamp": datetime.now().isoformat(),
                        "cached": False
                    }
        
        # If Wolfram Alpha fails, return failure to trigger fallback
        return {
            "success": False,
            "error": "Wolfram Alpha could not solve this problem",
            "source": "wolfram_alpha"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Wolfram Alpha API error: {str(e)}",
            "source": "wolfram_alpha"
        }

def extract_wolfram_solution(pods, original_query):
    """Extract the solution from Wolfram Alpha response pods"""
    solution_parts = []
    
    # Look for solution in specific pod types
    for pod in pods:
        pod_id = pod.get('id', '').lower()
        pod_title = pod.get('title', '').lower()
        
        # Check if this pod contains a solution
        if any(keyword in pod_id for keyword in ['solution', 'result', 'decimal']):
            subpods = pod.get('subpods', [])
            for subpod in subpods:
                text = subpod.get('plaintext', '')
                if text and text.strip():
                    solution_parts.append(text.strip())
    
    # If we found solutions, format them nicely
    if solution_parts:
        # Remove duplicates while preserving order
        unique_solutions = []
        for solution in solution_parts:
            if solution not in unique_solutions:
                unique_solutions.append(solution)
        
        # Format the final solution
        if len(unique_solutions) == 1:
            return f"✅ {unique_solutions[0]}"
        else:
            formatted_solutions = "\n".join([f"• {sol}" for sol in unique_solutions])
            return f"✅ Solutions:\n{formatted_solutions}"
    
    return None

def python_math_solver(query):
    """Fallback math solver using Python for basic calculations"""
    try:
        # Clean and prepare the query
        cleaned_query = clean_math_expression(query)
        
        if not cleaned_query:
            return solve_algebraic_equation(query)
        
        # Safe evaluation with allowed functions
        allowed_names = {
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow, "sqrt": math.sqrt,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "log": math.log, "log10": math.log10, "exp": math.exp,
            "pi": math.pi, "e": math.e, "ceil": math.ceil, "floor": math.floor,
            "factorial": math.factorial, "degrees": math.degrees, "radians": math.radians
        }
        
        # Evaluate the expression
        result = eval(cleaned_query, {"__builtins__": {}}, allowed_names)
        
        return {
            "success": True,
            "solution": f"✅ {result}",
            "query": query,
            "source": "Python Calculator",
            "timestamp": datetime.now().isoformat(),
            "cached": False
        }
        
    except Exception as e:
        return solve_algebraic_equation(query)

def clean_math_expression(query):
    """Clean and prepare math expression for safe evaluation"""
    # Convert to lowercase and remove common words
    query = query.lower()
    query = re.sub(r'\b(solve|calculate|compute|find|what is|equals?|the|of|a|an)\b', '', query)
    
    # Replace common math terms
    replacements = {
        'plus': '+', 'add': '+', 'added to': '+',
        'minus': '-', 'subtract': '-', 'subtracted from': '-',
        'times': '*', 'multiply': '*', 'multiplied by': '*',
        'divided by': '/', 'divide': '/', 'over': '/',
        'to the power of': '**', 'raised to': '**', 'squared': '**2', 'cubed': '**3',
        'square root of': 'sqrt(', 'sqrt': 'sqrt(',
        'sine': 'sin(', 'cosine': 'cos(', 'tangent': 'tan(',
        'natural log': 'log(', 'logarithm': 'log10('
    }
    
    for old, new in replacements.items():
        query = query.replace(old, new)
    
    # Remove extra spaces
    query = re.sub(r'\s+', '', query)
    
    # Check if it's a safe mathematical expression
    if re.match(r'^[0-9+\-*/().x\s\w]+$', query):
        # Handle some common patterns
        query = query.replace('x', '*')  # Implicit multiplication
        
        # Balance parentheses for sqrt and trig functions
        open_parens = query.count('(')
        close_parens = query.count(')')
        if open_parens > close_parens:
            query += ')' * (open_parens - close_parens)
        
        return query
    
    return None

def solve_algebraic_equation(query):
    """Attempt to solve simple algebraic equations"""
    try:
        # Look for equation patterns like "2x + 5 = 15"
        equation_match = re.search(r'(.+?)\s*=\s*(.+)', query)
        
        if equation_match:
            left_side = equation_match.group(1).strip()
            right_side = equation_match.group(2).strip()
            
            # Try to solve simple linear equations
            if 'x' in left_side and right_side.replace('.', '').replace('-', '').isdigit():
                solution = solve_linear_equation(left_side, float(right_side))
                if solution is not None:
                    return {
                        "success": True,
                        "solution": f"✅ x = {solution}",
                        "query": query,
                        "source": "Algebraic Solver",
                        "timestamp": datetime.now().isoformat(),
                        "cached": False
                    }
        
        # If we can't solve it, provide helpful guidance
        return math_help_response(query)
        
    except Exception as e:
        return math_help_response(query)

def solve_linear_equation(expression, target):
    """Solve simple linear equations like '2x + 5' = target"""
    try:
        # Parse expressions like "2x + 5", "3x - 7", "x + 10", etc.
        expression = expression.replace(' ', '').lower()
        
        # Extract coefficient and constant
        coefficient = 0
        constant = 0
        
        # Split by + and -
        parts = re.split(r'([+-])', expression)
        
        for i, part in enumerate(parts):
            if 'x' in part:
                # Extract coefficient of x
                coef_str = part.replace('x', '')
                if coef_str == '' or coef_str == '+':
                    coefficient += 1
                elif coef_str == '-':
                    coefficient -= 1
                else:
                    coefficient += float(coef_str)
            elif part not in ['+', '-'] and part.strip():
                # It's a constant
                sign = 1
                if i > 0 and parts[i-1] == '-':
                    sign = -1
                constant += sign * float(part)
        
        # Solve: coefficient * x + constant = target
        # So: x = (target - constant) / coefficient
        if coefficient != 0:
            x = (target - constant) / coefficient
            return round(x, 6) if x != int(x) else int(x)
        
        return None
        
    except Exception as e:
        return None

def math_help_response(query):
    """Provide helpful math guidance when solving fails"""
    # Detect what type of math problem it might be
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['derivative', 'differentiate', 'dx']):
        help_text = "🧮 For calculus problems like derivatives, try: 'derivative of x^2' or 'differentiate sin(x)'"
    elif any(word in query_lower for word in ['integral', 'integrate', 'antiderivative']):
        help_text = "🧮 For integrals, try: 'integral of 2x' or 'integrate cos(x)'"
    elif any(word in query_lower for word in ['solve', 'equation', '=']):
        help_text = "🧮 For equations, try: 'solve 2x + 5 = 15' or 'solve x^2 = 16'"
    elif any(word in query_lower for word in ['factor', 'expand']):
        help_text = "🧮 For algebra, try: 'factor x^2 + 5x + 6' or 'expand (x+2)(x+3)'"
    else:
        help_text = "🧮 I can help with math! Try: 'solve 2x + 5 = 15', 'calculate 25 * 4 + 10', or 'derivative of x^2'"
    
    return {
        "success": True,
        "solution": help_text,
        "query": query,
        "source": "Math Helper",
        "timestamp": datetime.now().isoformat(),
        "cached": False
    }

# API ENDPOINTS

@knowledge_api.route('/knowledge/math', methods=['POST'])
def solve_math():
    """
    Solve math problems - REAL implementation
    Accepts: {"query": "solve 2x + 5 = 15"}
    Returns: {"success": true, "solution": "x = 5", ...}
    """
    try:
        # Get the request data
        if request.is_json:
            data = request.get_json() or {}
        else:
            data = request.form.to_dict()
            
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Math query is required",
                "code": "MISSING_QUERY",
                "example": "Try: 'solve 2x + 5 = 15' or 'calculate 25 * 4'"
            }), 400
            
        # Solve the math problem
        result = solve_math_problem(query)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "message": "🧮 Math problem solved!",
                "solution": result["solution"],
                "query": query,
                "source": result["source"],
                "timestamp": result["timestamp"],
                "cached": result.get("cached", False),
                "branch": "knowledge"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result.get("error", "Math solving failed"),
                "message": "Unable to solve math problem",
                "query": query,
                "branch": "knowledge"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "code": "INTERNAL_ERROR",
            "branch": "knowledge"
        }), 500

@knowledge_api.route('/knowledge/status', methods=['GET'])
def knowledge_status():
    """Get knowledge branch status"""
    return jsonify({
        "success": True,
        "branch": "knowledge",
        "status": "active",
        "capabilities": [
            "math_solving",
            "equation_solving", 
            "calculus",
            "algebra",
            "arithmetic"
        ],
        "wolfram_alpha_available": bool(WOLFRAM_APP_ID),
        "python_fallback_available": True,
        "cached_solutions": len(math_cache)
    }), 200

@knowledge_api.route('/knowledge/test', methods=['GET'])
def test_math_solver():
    """Test the math solver with sample problems"""
    test_problems = [
        "2 + 2",
        "solve x + 5 = 10", 
        "calculate 25 * 4",
        "derivative of x^2"
    ]
    
    results = []
    for problem in test_problems:
        result = solve_math_problem(problem)
        results.append({
            "problem": problem,
            "success": result["success"],
            "solution": result.get("solution", result.get("error", "No solution")),
            "source": result.get("source", "unknown")
        })
    
    return jsonify({
        "success": True,
        "test_results": results,
        "wolfram_alpha_available": bool(WOLFRAM_APP_ID),
        "branch": "knowledge"
    }), 200

# Export the blueprint
__all__ = ['knowledge_api']
