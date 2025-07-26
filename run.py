"""
Mythiq AI - FREE Version Main Application
100% Free AI platform with Groq and Hugging Face - No credit card required!
"""

import os
import asyncio
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

# Import FREE version modules
from core.memory import MemoryManager
from core.diagnostics import DiagnosticsManager
from core.fallback import FallbackManager
from modules.reasoning_engine import ReasoningEngine
from modules.chat_core import ChatCore
from ai_services_free import FreeAIServiceManager  # FREE version!
from modules.reflector import ReflectorModule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global managers (will be initialized in main)
memory_manager = None
diagnostics_manager = None
fallback_manager = None
reasoning_engine = None
chat_core = None
ai_service_manager = None
reflector_module = None

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with FREE version information."""
    return jsonify({
        "message": "🆓 Mythiq AI - FREE Version: Emotional Intelligence Platform",
        "version": "2.0.0-FREE",
        "stage": "Stage 2 - AI Intelligence (FREE)",
        "cost": "💰 $0.00 - Completely FREE!",
        "features": [
            "🧠 Advanced Reasoning Engine",
            "💝 Emotional Intelligence (12 emotion types)",
            "🆓 FREE AI Integration (Groq + Hugging Face)",
            "💾 Advanced Memory System",
            "🔄 Self-Improvement & Learning",
            "📊 Real-time Performance Monitoring",
            "🛡️ Intelligent Fallback Systems"
        ],
        "free_services": {
            "groq": "14,400 requests/day - Lightning fast!",
            "huggingface": "30,000 requests/month - Great models!",
            "local": "Unlimited - Always available!"
        },
        "endpoints": {
            "/api/chat": "Intelligent conversation with emotional awareness",
            "/api/generate": "Creative content generation",
            "/api/status": "System health and FREE service status",
            "/api/reflection": "AI self-improvement insights",
            "/api/memory": "Memory and learning statistics"
        },
        "upgrade_info": "🚀 Upgrade to paid services when successful for even better AI!",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get comprehensive FREE system status."""
    try:
        # Collect status from all managers
        status = {
            "system": {
                "status": "online",
                "stage": "Stage 2 - AI Intelligence (FREE)",
                "version": "2.0.0-FREE",
                "cost": "$0.00 - Completely FREE!",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Memory system status
        if memory_manager:
            status["memory"] = memory_manager.get_memory_stats()
        
        # Diagnostics status
        if diagnostics_manager:
            status["diagnostics"] = diagnostics_manager.get_health_status()
            status["performance"] = diagnostics_manager.get_performance_summary(hours=1)
        
        # FREE AI services status
        if ai_service_manager:
            status["ai_services"] = ai_service_manager.get_service_status()
        
        # Chat core status
        if chat_core:
            status["chat"] = chat_core.get_conversation_stats()
        
        # Reflector status
        if reflector_module:
            status["learning"] = reflector_module.get_learning_summary()
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({
            "error": "Failed to get system status",
            "message": str(e),
            "note": "🆓 System is FREE - no costs involved!"
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """FREE intelligent chat endpoint with emotional awareness."""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Missing required field: message",
                "note": "🆓 This service is completely FREE!"
            }), 400
        
        message = data['message']
        user_id = data.get('user_id', 'anonymous')
        conversation_id = data.get('conversation_id')
        user_preferences = data.get('preferences', {})
        
        # Record request metrics
        start_time = datetime.now()
        
        if diagnostics_manager:
            diagnostics_manager.record_request("chat", 0, True)
        
        # Process message through chat core
        if not chat_core:
            return jsonify({
                "error": "Chat system not initialized",
                "note": "🆓 This service is completely FREE!"
            }), 500
        
        # Generate intelligent response using FREE services
        response = chat_core.process_message(
            message=message,
            user_id=user_id,
            conversation_id=conversation_id,
            user_preferences=user_preferences
        )
        
        # Record interaction for learning
        if reflector_module:
            try:
                reflector_module.analyze_interaction(
                    user_message=message,
                    ai_response=response.response,
                    reasoning_data=response.reasoning_summary,
                    user_id=user_id,
                    conversation_id=response.conversation_id,
                    user_feedback=data.get('feedback')
                )
            except Exception as e:
                logger.warning(f"Failed to record interaction for learning: {e}")
        
        # Update response time metrics
        response_time = (datetime.now() - start_time).total_seconds()
        if diagnostics_manager:
            diagnostics_manager.record_request("chat", response_time, True)
        
        return jsonify({
            "response": response.response,
            "conversation_id": response.conversation_id,
            "metadata": {
                "response_style": response.response_style,
                "ai_personality": response.ai_personality,
                "emotional_awareness": response.emotional_awareness,
                "reasoning_summary": response.reasoning_summary,
                "confidence": response.confidence,
                "processing_time": response.processing_time,
                "suggestions": response.suggestions,
                "free_service": True,
                "cost": "$0.00"
            },
            "free_info": {
                "service_used": "FREE AI services",
                "cost": "$0.00",
                "message": "🆓 This response was generated completely FREE!"
            },
            "timestamp": response.timestamp
        })
        
    except Exception as e:
        logger.error(f"Error in FREE chat endpoint: {e}")
        if diagnostics_manager:
            diagnostics_manager.record_request("chat", 0, False)
        
        return jsonify({
            "error": "Failed to process chat message",
            "message": str(e),
            "note": "🆓 This service is completely FREE - no charges apply!"
        }), 500

@app.route('/api/generate', methods=['POST'])
def generate():
    """FREE creative content generation endpoint."""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                "error": "Missing required field: prompt",
                "note": "🆓 This service is completely FREE!"
            }), 400
        
        prompt = data['prompt']
        content_type = data.get('type', 'text')
        user_id = data.get('user_id', 'anonymous')
        
        start_time = datetime.now()
        
        if diagnostics_manager:
            diagnostics_manager.record_request("generate", 0, True)
        
        # Use FREE AI service manager for creative generation
        if not ai_service_manager:
            return jsonify({
                "error": "AI services not initialized",
                "note": "🆓 This service is completely FREE!"
            }), 500
        
        # Generate creative content using FREE services
        async def generate_content():
            return await ai_service_manager.generate_response(
                prompt=f"Create {content_type} content based on: {prompt}",
                context={"user_id": user_id, "content_type": content_type},
                preferences={"prefer_creativity": True}
            )
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ai_response = loop.run_until_complete(generate_content())
        loop.close()
        
        response_time = (datetime.now() - start_time).total_seconds()
        
        if ai_response.success:
            if diagnostics_manager:
                diagnostics_manager.record_request("generate", response_time, True)
            
            return jsonify({
                "content": ai_response.content,
                "type": content_type,
                "prompt": prompt,
                "metadata": {
                    "service_used": ai_response.service_name,
                    "model_used": ai_response.model_used,
                    "tokens_used": ai_response.tokens_used,
                    "cost": ai_response.cost,
                    "response_time": ai_response.response_time,
                    "free_service": True
                },
                "free_info": {
                    "service_used": f"FREE {ai_response.service_name}",
                    "cost": "$0.00",
                    "message": "🆓 This content was generated completely FREE!"
                },
                "timestamp": datetime.now().isoformat()
            })
        else:
            if diagnostics_manager:
                diagnostics_manager.record_request("generate", response_time, False)
            
            return jsonify({
                "error": "Failed to generate content",
                "message": ai_response.error_message,
                "note": "🆓 This service is completely FREE - no charges apply!"
            }), 500
        
    except Exception as e:
        logger.error(f"Error in FREE generate endpoint: {e}")
        if diagnostics_manager:
            diagnostics_manager.record_request("generate", 0, False)
        
        return jsonify({
            "error": "Failed to generate content",
            "message": str(e),
            "note": "🆓 This service is completely FREE!"
        }), 500

@app.route('/api/reflection', methods=['GET'])
def get_reflection():
    """Get FREE AI self-improvement reflection report."""
    try:
        if not reflector_module:
            return jsonify({
                "error": "Reflection system not initialized",
                "note": "🆓 This service is completely FREE!"
            }), 500
        
        # Force reflection if requested
        force = request.args.get('force', 'false').lower() == 'true'
        
        reflection_report = reflector_module.perform_reflection(force=force)
        
        if reflection_report:
            return jsonify({
                "reflection_report": {
                    "report_id": reflection_report.report_id,
                    "time_period": reflection_report.time_period,
                    "interactions_analyzed": reflection_report.interactions_analyzed,
                    "key_insights": [
                        {
                            "category": insight.category,
                            "description": insight.description,
                            "priority": insight.priority,
                            "recommended_actions": insight.recommended_actions
                        }
                        for insight in reflection_report.key_insights
                    ],
                    "performance_metrics": reflection_report.performance_metrics,
                    "user_satisfaction_trends": reflection_report.user_satisfaction_trends,
                    "improvement_recommendations": reflection_report.improvement_recommendations,
                    "generated_at": reflection_report.generated_at
                },
                "learning_summary": reflector_module.get_learning_summary(),
                "free_info": {
                    "cost": "$0.00",
                    "message": "🆓 AI self-improvement is completely FREE!"
                }
            })
        else:
            return jsonify({
                "message": "Reflection not performed - insufficient data or interval not reached",
                "learning_summary": reflector_module.get_learning_summary(),
                "free_info": {
                    "cost": "$0.00",
                    "message": "🆓 This service is completely FREE!"
                }
            })
        
    except Exception as e:
        logger.error(f"Error in FREE reflection endpoint: {e}")
        return jsonify({
            "error": "Failed to get reflection report",
            "message": str(e),
            "note": "🆓 This service is completely FREE!"
        }), 500

@app.route('/api/memory', methods=['GET'])
def get_memory_stats():
    """Get FREE memory and learning statistics."""
    try:
        if not memory_manager:
            return jsonify({
                "error": "Memory system not initialized",
                "note": "🆓 This service is completely FREE!"
            }), 500
        
        stats = memory_manager.get_memory_stats()
        
        # Add learning patterns if reflector is available
        if reflector_module:
            learning_summary = reflector_module.get_learning_summary()
            stats["learning"] = learning_summary
        
        # Add FREE service info
        stats["free_info"] = {
            "cost": "$0.00",
            "message": "🆓 Memory and learning are completely FREE!"
        }
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error getting FREE memory stats: {e}")
        return jsonify({
            "error": "Failed to get memory statistics",
            "message": str(e),
            "note": "🆓 This service is completely FREE!"
        }), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback for FREE learning."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No feedback data provided",
                "note": "🆓 This service is completely FREE!"
            }), 400
        
        user_id = data.get('user_id', 'anonymous')
        conversation_id = data.get('conversation_id')
        feedback = data.get('feedback', {})
        
        # Store feedback in memory if available
        if memory_manager and conversation_id:
            feedback_message = {
                "role": "feedback",
                "content": feedback,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id
            }
            
            memory_manager.add_message_to_conversation(conversation_id, feedback_message)
        
        # Use feedback for learning if reflector is available
        if reflector_module:
            logger.info(f"Received FREE feedback from {user_id}: {feedback}")
        
        return jsonify({
            "message": "Feedback received and will be used for improvement",
            "timestamp": datetime.now().isoformat(),
            "free_info": {
                "cost": "$0.00",
                "message": "🆓 Feedback processing is completely FREE!"
            }
        })
        
    except Exception as e:
        logger.error(f"Error submitting FREE feedback: {e}")
        return jsonify({
            "error": "Failed to submit feedback",
            "message": str(e),
            "note": "🆓 This service is completely FREE!"
        }), 500

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify FREE functionality."""
    return jsonify({
        "test": "✅ SUCCESS!",
        "stage": "Stage 2 - AI Intelligence (FREE)",
        "message": "All FREE systems operational! 🆓🧠🚀",
        "cost": "$0.00",
        "services": "Groq + Hugging Face + Local",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/free-status', methods=['GET'])
def get_free_status():
    """Get detailed FREE service status."""
    try:
        if not ai_service_manager:
            return jsonify({
                "error": "AI services not initialized",
                "note": "🆓 This service is completely FREE!"
            }), 500
        
        # Test all FREE services
        async def test_services():
            return await ai_service_manager.test_all_free_services()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        test_results = loop.run_until_complete(test_services())
        loop.close()
        
        return jsonify({
            "free_services_status": test_results,
            "service_status": ai_service_manager.get_service_status(),
            "usage_summary": ai_service_manager.get_usage_summary(),
            "message": "🆓 All services are completely FREE!",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting FREE service status: {e}")
        return jsonify({
            "error": "Failed to get FREE service status",
            "message": str(e),
            "note": "🆓 This service is completely FREE!"
        }), 500

def initialize_free_managers():
    """Initialize all FREE AI managers and systems."""
    global memory_manager, diagnostics_manager, fallback_manager
    global reasoning_engine, chat_core, ai_service_manager, reflector_module
    
    try:
        logger.info("🆓 Initializing Mythiq AI FREE systems...")
        
        # Initialize core systems
        logger.info("📊 Initializing diagnostics manager...")
        diagnostics_manager = DiagnosticsManager()
        diagnostics_manager.start_monitoring()
        
        logger.info("💾 Initializing memory manager...")
        memory_manager = MemoryManager()
        
        logger.info("🛡️ Initializing fallback manager...")
        fallback_manager = FallbackManager()
        
        # Initialize AI modules
        logger.info("🧠 Initializing reasoning engine...")
        reasoning_engine = ReasoningEngine()
        
        logger.info("🆓 Initializing FREE AI service manager...")
        ai_service_manager = FreeAIServiceManager()  # FREE version!
        
        logger.info("💬 Initializing chat core...")
        chat_core = ChatCore(
            reasoning_engine=reasoning_engine,
            memory_manager=memory_manager
        )
        
        logger.info("🔄 Initializing reflector module...")
        reflector_module = ReflectorModule(
            memory_manager=memory_manager,
            ai_service_manager=ai_service_manager
        )
        
        logger.info("✅ All FREE systems initialized successfully!")
        
        # Add health checks
        if diagnostics_manager:
            diagnostics_manager.add_health_check("memory", lambda: memory_manager is not None)
            diagnostics_manager.add_health_check("reasoning", lambda: reasoning_engine is not None)
            diagnostics_manager.add_health_check("chat", lambda: chat_core is not None)
            diagnostics_manager.add_health_check("free_ai_services", lambda: ai_service_manager is not None)
            diagnostics_manager.add_health_check("reflector", lambda: reflector_module is not None)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize FREE managers: {e}")
        return False

def main():
    """Main FREE application entry point."""
    print("🌐 Starting Mythiq AI Platform - FREE Version...")
    print("✅ Stage 2: Emotional Intelligence & Advanced AI")
    print("🆓 Cost: $0.00 - Completely FREE!")
    print("🧠 Features: Reasoning, Memory, FREE AI, Self-Improvement")
    print("🔗 Server starting at http://0.0.0.0:8080")
    print("🎉 Ready to receive FREE requests!")
    
    # Initialize all FREE systems
    if not initialize_free_managers():
        print("❌ Failed to initialize FREE systems. Exiting.")
        return
    
    # Get port from environment
    port = int(os.environ.get('PORT', 8080))
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )

if __name__ == '__main__':
    main()
