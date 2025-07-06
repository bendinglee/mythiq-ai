# 🧮 COMPLETE MATH SOLVER INIT FILE
# File: branches/knowledge/__init__.py
# REPLACE YOUR EXISTING __init__.py WITH THIS VERSION

"""
MYTHIQ.AI Knowledge Branch - Math Solving Module
Provides real mathematical computation using Wolfram Alpha + Python fallbacks
"""

from .controller import knowledge_api

# Branch metadata
BRANCH_NAME = "knowledge"
BRANCH_VERSION = "2.0.0"
BRANCH_DESCRIPTION = "Advanced mathematical computation and problem solving"

# Capabilities
CAPABILITIES = [
    "algebraic_equations",      # solve 2x + 5 = 15
    "arithmetic_operations",    # 25 * 4 + 10
    "calculus_operations",      # derivative of x^2
    "trigonometric_functions",  # sin(pi/2)
    "logarithmic_functions",    # log(100)
    "statistical_calculations", # mean, median, etc.
    "unit_conversions",        # 5 feet to meters
    "mathematical_constants"   # pi, e, etc.
]

# API endpoints provided by this branch
ENDPOINTS = [
    {
        "path": "/api/knowledge/math",
        "method": "POST",
        "description": "Solve mathematical problems",
        "example": {"query": "solve 2x + 5 = 15"}
    },
    {
        "path": "/api/knowledge/status", 
        "method": "GET",
        "description": "Get branch status and capabilities"
    },
    {
        "path": "/api/knowledge/test",
        "method": "GET", 
        "description": "Test math solver with sample problems"
    }
]

def get_branch_info():
    """Get information about this branch"""
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "description": BRANCH_DESCRIPTION,
        "capabilities": CAPABILITIES,
        "endpoints": ENDPOINTS,
        "status": "active"
    }

def initialize_branch():
    """Initialize the knowledge branch"""
    print(f"✅ Initializing {BRANCH_NAME} branch v{BRANCH_VERSION}")
    print(f"📊 Capabilities: {len(CAPABILITIES)} math operations")
    print(f"🔗 Endpoints: {len(ENDPOINTS)} API routes")
    return True

# Export the blueprint and utilities
__all__ = ['knowledge_api', 'get_branch_info', 'initialize_branch']


