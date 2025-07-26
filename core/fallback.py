"""
Mythiq AI - Advanced Fallback and Resilience System
Smart AI service routing, circuit breakers, retry logic, and graceful degradation
"""

import time
import asyncio
import random
from typing import Dict, List, Any, Optional, Callable, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ServiceStatus(Enum):
    """Service status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CIRCUIT_OPEN = "circuit_open"

@dataclass
class ServiceConfig:
    """Configuration for an AI service."""
    name: str
    priority: int  # Lower number = higher priority
    timeout: float
    max_retries: int
    circuit_breaker_threshold: int
    circuit_breaker_timeout: float
    rate_limit_per_minute: int
    cost_per_request: float = 0.0
    
@dataclass
class ServiceMetrics:
    """Metrics for an AI service."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    last_request_time: Optional[str] = None
    last_success_time: Optional[str] = None
    last_failure_time: Optional[str] = None
    consecutive_failures: int = 0
    circuit_breaker_open_until: Optional[str] = None
    requests_this_minute: int = 0
    minute_window_start: Optional[str] = None

@dataclass
class FallbackResponse:
    """Response from fallback system."""
    success: bool
    response: Any
    service_used: str
    response_time: float
    fallback_level: int  # 0 = primary, 1 = first fallback, etc.
    error_message: Optional[str] = None
    cost: float = 0.0

class FallbackManager:
    """Advanced fallback and resilience system for AI services."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize fallback manager."""
        self.config = config or {}
        
        # Service configurations
        self.services: Dict[str, ServiceConfig] = {}
        self.service_metrics: Dict[str, ServiceMetrics] = {}
        self.service_handlers: Dict[str, Callable] = {}
        
        # Built-in fallback responses
        self.builtin_fallbacks: Dict[str, Callable] = {
            "chat": self._builtin_chat_fallback,
            "generation": self._builtin_generation_fallback,
            "emotion_detection": self._builtin_emotion_fallback,
            "intent_detection": self._builtin_intent_fallback
        }
        
        # Global settings
        self.global_timeout = self.config.get("global_timeout", 30.0)
        self.max_fallback_levels = self.config.get("max_fallback_levels", 5)
        self.adaptive_routing = self.config.get("adaptive_routing", True)
        
        logger.info("FallbackManager initialized")
    
    def register_service(self, config: ServiceConfig, handler: Callable):
        """Register an AI service with its configuration and handler."""
        self.services[config.name] = config
        self.service_metrics[config.name] = ServiceMetrics()
        self.service_handlers[config.name] = handler
        
        logger.info(f"Registered service {config.name} with priority {config.priority}")
    
    def register_builtin_fallback(self, request_type: str, handler: Callable):
        """Register a built-in fallback handler."""
        self.builtin_fallbacks[request_type] = handler
        logger.info(f"Registered built-in fallback for {request_type}")
    
    async def execute_with_fallback(self, request_type: str, request_data: Dict[str, Any], 
                                  user_preferences: Dict[str, Any] = None) -> FallbackResponse:
        """Execute request with intelligent fallback routing."""
        start_time = time.time()
        user_preferences = user_preferences or {}
        
        # Get ordered list of services to try
        service_order = self._get_service_order(request_type, user_preferences)
        
        last_error = None
        fallback_level = 0
        
        # Try each service in order
        for service_name in service_order:
            if not self._is_service_available(service_name):
                logger.debug(f"Service {service_name} not available, skipping")
                continue
            
            try:
                response = await self._execute_service_request(
                    service_name, request_type, request_data
                )
                
                if response.success:
                    response.fallback_level = fallback_level
                    self._record_success(service_name, time.time() - start_time)
                    return response
                else:
                    last_error = response.error_message
                    self._record_failure(service_name, response.error_message)
                    
            except Exception as e:
                last_error = str(e)
                self._record_failure(service_name, str(e))
                logger.warning(f"Service {service_name} failed: {e}")
            
            fallback_level += 1
            
            # Add delay between service attempts
            if fallback_level < len(service_order):
                await asyncio.sleep(0.1 * fallback_level)  # Progressive delay
        
        # All services failed, use built-in fallback
        logger.warning(f"All services failed for {request_type}, using built-in fallback")
        return await self._execute_builtin_fallback(request_type, request_data, last_error)
    
    def _get_service_order(self, request_type: str, user_preferences: Dict[str, Any]) -> List[str]:
        """Get ordered list of services to try based on preferences and performance."""
        available_services = [
            name for name, config in self.services.items()
            if self._is_service_available(name)
        ]
        
        if not available_services:
            return []
        
        # User preference for speed vs quality
        prefer_speed = user_preferences.get("prefer_speed", False)
        prefer_quality = user_preferences.get("prefer_quality", False)
        
        # Calculate service scores
        service_scores = {}
        for service_name in available_services:
            score = self._calculate_service_score(
                service_name, prefer_speed, prefer_quality
            )
            service_scores[service_name] = score
        
        # Sort by score (higher is better)
        ordered_services = sorted(
            service_scores.keys(),
            key=lambda s: service_scores[s],
            reverse=True
        )
        
        logger.debug(f"Service order for {request_type}: {ordered_services}")
        return ordered_services
    
    def _calculate_service_score(self, service_name: str, prefer_speed: bool, 
                               prefer_quality: bool) -> float:
        """Calculate service score based on performance and preferences."""
        config = self.services[service_name]
        metrics = self.service_metrics[service_name]
        
        # Base score from priority (lower priority number = higher score)
        score = 100 - config.priority
        
        # Success rate factor
        if metrics.total_requests > 0:
            success_rate = metrics.successful_requests / metrics.total_requests
            score *= success_rate
        
        # Response time factor
        if prefer_speed and metrics.average_response_time > 0:
            # Prefer faster services
            speed_factor = max(0.1, 1.0 / metrics.average_response_time)
            score *= speed_factor
        
        # Quality factor (inverse of priority for quality preference)
        if prefer_quality:
            quality_factor = 1.0 / max(1, config.priority)
            score *= quality_factor
        
        # Recent failure penalty
        if metrics.consecutive_failures > 0:
            failure_penalty = 0.9 ** metrics.consecutive_failures
            score *= failure_penalty
        
        # Cost factor (prefer lower cost)
        if config.cost_per_request > 0:
            cost_factor = 1.0 / (1.0 + config.cost_per_request)
            score *= cost_factor
        
        return score
    
    def _is_service_available(self, service_name: str) -> bool:
        """Check if service is available for requests."""
        if service_name not in self.services:
            return False
        
        metrics = self.service_metrics[service_name]
        config = self.services[service_name]
        
        # Check circuit breaker
        if metrics.circuit_breaker_open_until:
            open_until = datetime.fromisoformat(metrics.circuit_breaker_open_until)
            if datetime.now() < open_until:
                return False
            else:
                # Circuit breaker timeout expired, reset
                metrics.circuit_breaker_open_until = None
                metrics.consecutive_failures = 0
        
        # Check rate limiting
        now = datetime.now()
        if metrics.minute_window_start:
            window_start = datetime.fromisoformat(metrics.minute_window_start)
            if now - window_start < timedelta(minutes=1):
                if metrics.requests_this_minute >= config.rate_limit_per_minute:
                    return False
            else:
                # Reset rate limit window
                metrics.requests_this_minute = 0
                metrics.minute_window_start = now.isoformat()
        else:
            metrics.minute_window_start = now.isoformat()
        
        return True
    
    async def _execute_service_request(self, service_name: str, request_type: str, 
                                     request_data: Dict[str, Any]) -> FallbackResponse:
        """Execute request on specific service."""
        config = self.services[service_name]
        metrics = self.service_metrics[service_name]
        handler = self.service_handlers[service_name]
        
        start_time = time.time()
        
        # Update rate limiting
        metrics.requests_this_minute += 1
        metrics.total_requests += 1
        metrics.last_request_time = datetime.now().isoformat()
        
        try:
            # Execute with timeout
            response = await asyncio.wait_for(
                handler(request_type, request_data),
                timeout=config.timeout
            )
            
            response_time = time.time() - start_time
            
            return FallbackResponse(
                success=True,
                response=response,
                service_used=service_name,
                response_time=response_time,
                fallback_level=0,  # Will be set by caller
                cost=config.cost_per_request
            )
            
        except asyncio.TimeoutError:
            response_time = time.time() - start_time
            error_msg = f"Service {service_name} timed out after {config.timeout}s"
            
            return FallbackResponse(
                success=False,
                response=None,
                service_used=service_name,
                response_time=response_time,
                fallback_level=0,
                error_message=error_msg
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            error_msg = f"Service {service_name} error: {str(e)}"
            
            return FallbackResponse(
                success=False,
                response=None,
                service_used=service_name,
                response_time=response_time,
                fallback_level=0,
                error_message=error_msg
            )
    
    async def _execute_builtin_fallback(self, request_type: str, request_data: Dict[str, Any], 
                                      last_error: str) -> FallbackResponse:
        """Execute built-in fallback response."""
        start_time = time.time()
        
        if request_type in self.builtin_fallbacks:
            try:
                response = await self.builtin_fallbacks[request_type](request_data, last_error)
                response_time = time.time() - start_time
                
                return FallbackResponse(
                    success=True,
                    response=response,
                    service_used="builtin_fallback",
                    response_time=response_time,
                    fallback_level=999,  # Highest fallback level
                    cost=0.0
                )
                
            except Exception as e:
                logger.error(f"Built-in fallback failed for {request_type}: {e}")
        
        # Ultimate fallback
        response_time = time.time() - start_time
        return FallbackResponse(
            success=True,
            response=self._ultimate_fallback(request_type, last_error),
            service_used="ultimate_fallback",
            response_time=response_time,
            fallback_level=1000,
            cost=0.0
        )
    
    def _record_success(self, service_name: str, response_time: float):
        """Record successful service request."""
        metrics = self.service_metrics[service_name]
        
        metrics.successful_requests += 1
        metrics.last_success_time = datetime.now().isoformat()
        metrics.consecutive_failures = 0
        
        # Update average response time
        if metrics.average_response_time == 0:
            metrics.average_response_time = response_time
        else:
            # Exponential moving average
            alpha = 0.1
            metrics.average_response_time = (
                alpha * response_time + 
                (1 - alpha) * metrics.average_response_time
            )
        
        logger.debug(f"Recorded success for {service_name}: {response_time:.3f}s")
    
    def _record_failure(self, service_name: str, error_message: str):
        """Record failed service request."""
        metrics = self.service_metrics[service_name]
        config = self.services[service_name]
        
        metrics.failed_requests += 1
        metrics.last_failure_time = datetime.now().isoformat()
        metrics.consecutive_failures += 1
        
        # Check if circuit breaker should open
        if metrics.consecutive_failures >= config.circuit_breaker_threshold:
            open_until = datetime.now() + timedelta(seconds=config.circuit_breaker_timeout)
            metrics.circuit_breaker_open_until = open_until.isoformat()
            logger.warning(f"Circuit breaker opened for {service_name} until {open_until}")
        
        logger.debug(f"Recorded failure for {service_name}: {error_message}")
    
    # Built-in fallback implementations
    async def _builtin_chat_fallback(self, request_data: Dict[str, Any], 
                                   last_error: str) -> Dict[str, Any]:
        """Built-in chat fallback."""
        message = request_data.get("message", "")
        user_id = request_data.get("user_id", "anonymous")
        
        # Simple pattern-based responses
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            response = "Hello! I'm Mythiq AI. I'm here to help you create amazing things! 🌟"
        elif any(word in message_lower for word in ["how", "what", "why", "when", "where"]):
            response = f"That's a great question about '{message}'. I'm processing your request and will have better answers soon! 🤔"
        elif any(word in message_lower for word in ["create", "make", "generate", "build"]):
            response = f"I'd love to help you create something amazing! Your idea about '{message}' sounds fantastic! 🎨"
        elif any(word in message_lower for word in ["sad", "angry", "frustrated", "upset"]):
            response = "I understand you might be feeling down. I'm here to support you and help make things better! 💝"
        elif any(word in message_lower for word in ["happy", "excited", "great", "awesome"]):
            response = "I love your positive energy! Let's channel that excitement into creating something wonderful! 🎉"
        else:
            responses = [
                f"Thanks for sharing '{message}' with me! I'm always learning and improving to help you better! 🚀",
                f"I hear you saying '{message}'. While I'm getting smarter, I'm here to support you however I can! 💫",
                f"Your message '{message}' is important to me. I'm working on understanding you better every day! 🧠"
            ]
            response = random.choice(responses)
        
        return {
            "response": response,
            "detected_emotion": "neutral",
            "detected_intent": "general_chat",
            "confidence": 0.7,
            "fallback_used": True,
            "fallback_reason": last_error or "All AI services unavailable"
        }
    
    async def _builtin_generation_fallback(self, request_data: Dict[str, Any], 
                                         last_error: str) -> Dict[str, Any]:
        """Built-in generation fallback."""
        prompt = request_data.get("prompt", "")
        gen_type = request_data.get("type", "text")
        
        type_responses = {
            "game": f"🎮 I'd love to create a {gen_type} about '{prompt}'! Imagine an interactive experience with your concept - it would be amazing!",
            "image": f"🎨 Your idea for a {gen_type} featuring '{prompt}' sounds visually stunning! I can picture it being beautiful and creative!",
            "video": f"🎬 A {gen_type} based on '{prompt}' would be fantastic! I envision engaging visuals and compelling storytelling!",
            "story": f"📚 I'm inspired by your prompt '{prompt}' for a {gen_type}! It has the potential for a captivating narrative!",
            "text": f"📝 Your request for {gen_type} content about '{prompt}' is excellent! I can see it being informative and engaging!"
        }
        
        response_message = type_responses.get(gen_type, 
            f"✨ Your creative idea for {gen_type} content about '{prompt}' is wonderful! I'm excited to help bring it to life!")
        
        return {
            "message": response_message,
            "type": gen_type,
            "prompt": prompt,
            "status": "conceptual_response",
            "fallback_used": True,
            "fallback_reason": last_error or "Generation services unavailable",
            "inspiration": f"Your {gen_type} about '{prompt}' will be amazing when our full generation capabilities are available!"
        }
    
    async def _builtin_emotion_fallback(self, request_data: Dict[str, Any], 
                                      last_error: str) -> Dict[str, Any]:
        """Built-in emotion detection fallback."""
        text = request_data.get("text", "")
        
        # Simple keyword-based emotion detection
        emotions = {
            "joy": 0.0, "sadness": 0.0, "anger": 0.0, "fear": 0.0,
            "surprise": 0.0, "disgust": 0.0, "trust": 0.0, "anticipation": 0.0
        }
        
        text_lower = text.lower()
        
        # Joy indicators
        if any(word in text_lower for word in ["happy", "joy", "excited", "great", "awesome", "love", "wonderful"]):
            emotions["joy"] = 0.8
        
        # Sadness indicators
        if any(word in text_lower for word in ["sad", "depressed", "down", "unhappy", "crying"]):
            emotions["sadness"] = 0.8
        
        # Anger indicators
        if any(word in text_lower for word in ["angry", "mad", "furious", "hate", "annoyed"]):
            emotions["anger"] = 0.8
        
        # Fear indicators
        if any(word in text_lower for word in ["scared", "afraid", "worried", "anxious", "nervous"]):
            emotions["fear"] = 0.8
        
        # Default to neutral if no strong emotions detected
        if max(emotions.values()) < 0.5:
            emotions["trust"] = 0.6
            emotions["anticipation"] = 0.4
        
        return {
            "emotions": emotions,
            "dominant_emotion": max(emotions.keys(), key=emotions.get),
            "confidence": 0.6,
            "fallback_used": True,
            "method": "keyword_based"
        }
    
    async def _builtin_intent_fallback(self, request_data: Dict[str, Any], 
                                     last_error: str) -> Dict[str, Any]:
        """Built-in intent detection fallback."""
        text = request_data.get("text", "")
        text_lower = text.lower()
        
        # Simple intent classification
        if any(word in text_lower for word in ["create", "make", "generate", "build", "design"]):
            intent = "creative_request"
            confidence = 0.8
        elif any(word in text_lower for word in ["help", "how", "what", "explain", "tell me"]):
            intent = "information_request"
            confidence = 0.7
        elif any(word in text_lower for word in ["hello", "hi", "hey", "greetings"]):
            intent = "greeting"
            confidence = 0.9
        elif any(word in text_lower for word in ["bye", "goodbye", "see you", "farewell"]):
            intent = "farewell"
            confidence = 0.9
        elif any(word in text_lower for word in ["thanks", "thank you", "appreciate"]):
            intent = "gratitude"
            confidence = 0.8
        elif "?" in text:
            intent = "question"
            confidence = 0.6
        else:
            intent = "general_chat"
            confidence = 0.5
        
        return {
            "intent": intent,
            "confidence": confidence,
            "fallback_used": True,
            "method": "keyword_based"
        }
    
    def _ultimate_fallback(self, request_type: str, last_error: str) -> Dict[str, Any]:
        """Ultimate fallback when everything else fails."""
        return {
            "message": "I'm experiencing some technical difficulties, but I'm still here to help! 🤖",
            "status": "fallback_response",
            "request_type": request_type,
            "error_info": last_error,
            "suggestion": "Please try again in a moment, or let me know how else I can assist you!",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all registered services."""
        status = {}
        
        for service_name, config in self.services.items():
            metrics = self.service_metrics[service_name]
            
            # Determine service status
            if metrics.circuit_breaker_open_until:
                service_status = ServiceStatus.CIRCUIT_OPEN
            elif metrics.consecutive_failures >= config.circuit_breaker_threshold // 2:
                service_status = ServiceStatus.DEGRADED
            elif metrics.consecutive_failures > 0:
                service_status = ServiceStatus.DEGRADED
            else:
                service_status = ServiceStatus.HEALTHY
            
            status[service_name] = {
                "status": service_status.value,
                "config": asdict(config),
                "metrics": asdict(metrics),
                "available": self._is_service_available(service_name)
            }
        
        return status
    
    def reset_service_metrics(self, service_name: str) -> bool:
        """Reset metrics for a specific service."""
        if service_name in self.service_metrics:
            self.service_metrics[service_name] = ServiceMetrics()
            logger.info(f"Reset metrics for service {service_name}")
            return True
        return False
    
    def get_fallback_stats(self) -> Dict[str, Any]:
        """Get fallback system statistics."""
        total_requests = sum(m.total_requests for m in self.service_metrics.values())
        total_successes = sum(m.successful_requests for m in self.service_metrics.values())
        total_failures = sum(m.failed_requests for m in self.service_metrics.values())
        
        return {
            "total_requests": total_requests,
            "total_successes": total_successes,
            "total_failures": total_failures,
            "success_rate": total_successes / max(1, total_requests),
            "services_registered": len(self.services),
            "services_healthy": len([
                s for s in self.get_service_status().values()
                if s["status"] == ServiceStatus.HEALTHY.value
            ]),
            "builtin_fallbacks": list(self.builtin_fallbacks.keys()),
            "adaptive_routing_enabled": self.adaptive_routing
        }

