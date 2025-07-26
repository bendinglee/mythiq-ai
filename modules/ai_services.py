"""
Mythiq AI - Multi-AI Service Integration Manager
Coordinates OpenAI, Claude, and Groq APIs with intelligent routing and fallback systems
"""

import os
import asyncio
import aiohttp
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class AIServiceConfig:
    """Configuration for an AI service."""
    name: str
    api_key: str
    base_url: str
    model: str
    max_tokens: int
    temperature: float
    timeout: float
    rate_limit_per_minute: int
    cost_per_1k_tokens: float
    priority: int  # Lower number = higher priority

@dataclass
class AIServiceResponse:
    """Response from an AI service."""
    success: bool
    content: str
    service_name: str
    model_used: str
    tokens_used: int
    response_time: float
    cost: float
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None

class AIServiceManager:
    """Multi-AI service integration manager with intelligent routing."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize AI service manager."""
        self.config = config or {}
        self.services: Dict[str, AIServiceConfig] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Service usage tracking
        self.usage_stats = {}
        self.rate_limits = {}
        
        # Initialize services from environment variables
        self._initialize_services()
        
        logger.info("AIServiceManager initialized")
    
    def _initialize_services(self):
        """Initialize AI services from environment variables."""
        # OpenAI Configuration
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.services["openai"] = AIServiceConfig(
                name="openai",
                api_key=openai_key,
                base_url="https://api.openai.com/v1",
                model="gpt-3.5-turbo",
                max_tokens=1000,
                temperature=0.7,
                timeout=30.0,
                rate_limit_per_minute=60,
                cost_per_1k_tokens=0.002,
                priority=2
            )
            self.usage_stats["openai"] = {"requests": 0, "tokens": 0, "cost": 0.0}
            logger.info("OpenAI service configured")
        
        # Anthropic Claude Configuration
        claude_key = os.getenv("ANTHROPIC_API_KEY")
        if claude_key:
            self.services["claude"] = AIServiceConfig(
                name="claude",
                api_key=claude_key,
                base_url="https://api.anthropic.com/v1",
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0.7,
                timeout=30.0,
                rate_limit_per_minute=50,
                cost_per_1k_tokens=0.00025,
                priority=1  # Highest priority for emotional intelligence
            )
            self.usage_stats["claude"] = {"requests": 0, "tokens": 0, "cost": 0.0}
            logger.info("Claude service configured")
        
        # Groq Configuration
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            self.services["groq"] = AIServiceConfig(
                name="groq",
                api_key=groq_key,
                base_url="https://api.groq.com/openai/v1",
                model="llama3-8b-8192",
                max_tokens=1000,
                temperature=0.7,
                timeout=15.0,
                rate_limit_per_minute=100,
                cost_per_1k_tokens=0.0,  # Free tier
                priority=0  # Highest priority for speed
            )
            self.usage_stats["groq"] = {"requests": 0, "tokens": 0, "cost": 0.0}
            logger.info("Groq service configured")
        
        if not self.services:
            logger.warning("No AI services configured - check environment variables")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def generate_response(self, prompt: str, context: Dict[str, Any] = None,
                              preferences: Dict[str, Any] = None) -> AIServiceResponse:
        """Generate response using the best available AI service."""
        context = context or {}
        preferences = preferences or {}
        
        # Determine service order based on preferences and availability
        service_order = self._get_service_order(preferences)
        
        if not service_order:
            return AIServiceResponse(
                success=False,
                content="",
                service_name="none",
                model_used="none",
                tokens_used=0,
                response_time=0.0,
                cost=0.0,
                error_message="No AI services available"
            )
        
        # Try services in order
        for service_name in service_order:
            try:
                response = await self._call_service(service_name, prompt, context, preferences)
                if response.success:
                    self._update_usage_stats(service_name, response)
                    return response
                else:
                    logger.warning(f"Service {service_name} failed: {response.error_message}")
            except Exception as e:
                logger.error(f"Error calling service {service_name}: {e}")
        
        # All services failed
        return AIServiceResponse(
            success=False,
            content="",
            service_name="failed",
            model_used="none",
            tokens_used=0,
            response_time=0.0,
            cost=0.0,
            error_message="All AI services failed"
        )
    
    def _get_service_order(self, preferences: Dict[str, Any]) -> List[str]:
        """Get ordered list of services to try based on preferences."""
        available_services = list(self.services.keys())
        
        if not available_services:
            return []
        
        # Check preferences
        prefer_speed = preferences.get("prefer_speed", False)
        prefer_quality = preferences.get("prefer_quality", False)
        prefer_free = preferences.get("prefer_free", True)
        
        # Calculate service scores
        service_scores = {}
        for service_name in available_services:
            if not self._is_service_available(service_name):
                continue
                
            config = self.services[service_name]
            score = 100 - config.priority  # Lower priority number = higher score
            
            # Apply preference modifiers
            if prefer_speed and service_name == "groq":
                score += 50  # Groq is fastest
            
            if prefer_quality and service_name == "claude":
                score += 30  # Claude is best for emotional intelligence
            
            if prefer_free and config.cost_per_1k_tokens == 0.0:
                score += 20  # Free services get bonus
            
            # Recent performance factor
            stats = self.usage_stats.get(service_name, {})
            if stats.get("requests", 0) > 0:
                # Simple success rate boost (could be more sophisticated)
                score += 10
            
            service_scores[service_name] = score
        
        # Sort by score (highest first)
        ordered_services = sorted(
            service_scores.keys(),
            key=lambda s: service_scores[s],
            reverse=True
        )
        
        logger.debug(f"Service order: {ordered_services}")
        return ordered_services
    
    def _is_service_available(self, service_name: str) -> bool:
        """Check if service is available (not rate limited)."""
        if service_name not in self.services:
            return False
        
        # Check rate limiting (simplified)
        current_time = datetime.now()
        rate_limit_key = f"{service_name}_{current_time.strftime('%Y%m%d%H%M')}"
        
        if rate_limit_key not in self.rate_limits:
            self.rate_limits[rate_limit_key] = 0
        
        config = self.services[service_name]
        if self.rate_limits[rate_limit_key] >= config.rate_limit_per_minute:
            return False
        
        return True
    
    async def _call_service(self, service_name: str, prompt: str, 
                          context: Dict[str, Any], preferences: Dict[str, Any]) -> AIServiceResponse:
        """Call specific AI service."""
        config = self.services[service_name]
        start_time = datetime.now()
        
        # Update rate limiting
        current_time = datetime.now()
        rate_limit_key = f"{service_name}_{current_time.strftime('%Y%m%d%H%M')}"
        self.rate_limits[rate_limit_key] = self.rate_limits.get(rate_limit_key, 0) + 1
        
        # Prepare request based on service type
        if service_name == "claude":
            response = await self._call_claude(config, prompt, context, preferences)
        else:  # OpenAI-compatible (OpenAI, Groq)
            response = await self._call_openai_compatible(config, prompt, context, preferences)
        
        response.response_time = (datetime.now() - start_time).total_seconds()
        return response
    
    async def _call_claude(self, config: AIServiceConfig, prompt: str,
                         context: Dict[str, Any], preferences: Dict[str, Any]) -> AIServiceResponse:
        """Call Anthropic Claude API."""
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        # Build messages for Claude
        messages = []
        
        # Add context if available
        if context.get("conversation_history"):
            for msg in context["conversation_history"][-5:]:  # Last 5 messages
                role = "user" if msg.get("role") == "user" else "assistant"
                messages.append({"role": role, "content": msg.get("content", "")})
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": config.model,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "messages": messages
        }
        
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.post(
                f"{config.base_url}/messages",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=config.timeout)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    content = data["content"][0]["text"]
                    tokens_used = data["usage"]["input_tokens"] + data["usage"]["output_tokens"]
                    cost = (tokens_used / 1000) * config.cost_per_1k_tokens
                    
                    return AIServiceResponse(
                        success=True,
                        content=content,
                        service_name=config.name,
                        model_used=config.model,
                        tokens_used=tokens_used,
                        response_time=0.0,  # Will be set by caller
                        cost=cost,
                        metadata={"usage": data["usage"]}
                    )
                else:
                    error_text = await response.text()
                    return AIServiceResponse(
                        success=False,
                        content="",
                        service_name=config.name,
                        model_used=config.model,
                        tokens_used=0,
                        response_time=0.0,
                        cost=0.0,
                        error_message=f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            return AIServiceResponse(
                success=False,
                content="",
                service_name=config.name,
                model_used=config.model,
                tokens_used=0,
                response_time=0.0,
                cost=0.0,
                error_message=str(e)
            )
    
    async def _call_openai_compatible(self, config: AIServiceConfig, prompt: str,
                                    context: Dict[str, Any], preferences: Dict[str, Any]) -> AIServiceResponse:
        """Call OpenAI-compatible API (OpenAI, Groq)."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.api_key}"
        }
        
        # Build messages
        messages = []
        
        # Add system message for context
        system_message = "You are Mythiq AI, an emotionally intelligent and creative AI assistant."
        if context.get("ai_personality"):
            personality = context["ai_personality"]
            system_message += f" You are currently in {personality} mode."
        
        messages.append({"role": "system", "content": system_message})
        
        # Add conversation history
        if context.get("conversation_history"):
            for msg in context["conversation_history"][-5:]:  # Last 5 messages
                role = msg.get("role", "user")
                if role in ["user", "assistant"]:
                    messages.append({"role": role, "content": msg.get("content", "")})
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": config.model,
            "messages": messages,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "stream": False
        }
        
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.post(
                f"{config.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=config.timeout)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    content = data["choices"][0]["message"]["content"]
                    tokens_used = data["usage"]["total_tokens"]
                    cost = (tokens_used / 1000) * config.cost_per_1k_tokens
                    
                    return AIServiceResponse(
                        success=True,
                        content=content,
                        service_name=config.name,
                        model_used=config.model,
                        tokens_used=tokens_used,
                        response_time=0.0,  # Will be set by caller
                        cost=cost,
                        metadata={"usage": data["usage"]}
                    )
                else:
                    error_text = await response.text()
                    return AIServiceResponse(
                        success=False,
                        content="",
                        service_name=config.name,
                        model_used=config.model,
                        tokens_used=0,
                        response_time=0.0,
                        cost=0.0,
                        error_message=f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            return AIServiceResponse(
                success=False,
                content="",
                service_name=config.name,
                model_used=config.model,
                tokens_used=0,
                response_time=0.0,
                cost=0.0,
                error_message=str(e)
            )
    
    def _update_usage_stats(self, service_name: str, response: AIServiceResponse):
        """Update usage statistics for a service."""
        if service_name not in self.usage_stats:
            self.usage_stats[service_name] = {"requests": 0, "tokens": 0, "cost": 0.0}
        
        stats = self.usage_stats[service_name]
        stats["requests"] += 1
        stats["tokens"] += response.tokens_used
        stats["cost"] += response.cost
        
        logger.debug(f"Updated stats for {service_name}: {stats}")
    
    async def generate_creative_content(self, prompt: str, content_type: str,
                                      context: Dict[str, Any] = None) -> AIServiceResponse:
        """Generate creative content with specialized prompting."""
        context = context or {}
        
        # Enhanced prompt for creative content
        creative_prompts = {
            "game": f"Create an engaging game concept based on: {prompt}. Include gameplay mechanics, objectives, and what makes it fun.",
            "image": f"Describe a vivid, detailed image based on: {prompt}. Include visual elements, style, composition, and mood.",
            "video": f"Outline a compelling video concept for: {prompt}. Include scenes, visual style, pacing, and narrative structure.",
            "story": f"Write a captivating story inspired by: {prompt}. Include characters, plot, setting, and emotional depth.",
            "music": f"Describe a musical composition inspired by: {prompt}. Include genre, instruments, mood, and structure."
        }
        
        enhanced_prompt = creative_prompts.get(content_type, 
            f"Create compelling {content_type} content based on: {prompt}")
        
        # Prefer creative-focused services
        preferences = {
            "prefer_quality": True,
            "creativity_focus": True
        }
        
        return await self.generate_response(enhanced_prompt, context, preferences)
    
    async def generate_emotional_response(self, message: str, emotion_context: Dict[str, Any],
                                        context: Dict[str, Any] = None) -> AIServiceResponse:
        """Generate emotionally intelligent response."""
        context = context or {}
        
        # Build emotion-aware prompt
        dominant_emotion = emotion_context.get("dominant_emotion", "neutral")
        emotion_intensity = emotion_context.get("emotion_intensity", 0.5)
        
        emotional_prompt = f"""
        The user is expressing {dominant_emotion} with intensity {emotion_intensity:.1f}/1.0.
        Their message: "{message}"
        
        Respond with appropriate emotional intelligence, empathy, and support.
        Match their emotional state while being helpful and caring.
        """
        
        # Prefer Claude for emotional intelligence
        preferences = {
            "prefer_quality": True,
            "emotional_focus": True
        }
        
        # Add emotional context
        context["emotional_state"] = emotion_context
        
        return await self.generate_response(emotional_prompt, context, preferences)
    
    async def generate_informational_response(self, query: str, complexity_level: str,
                                            context: Dict[str, Any] = None) -> AIServiceResponse:
        """Generate informational response with appropriate complexity."""
        context = context or {}
        
        # Adjust response based on complexity
        complexity_prompts = {
            "simple": f"Explain in simple, easy-to-understand terms: {query}",
            "moderate": f"Provide a clear and detailed explanation of: {query}",
            "complex": f"Give a comprehensive, technical explanation of: {query}",
            "expert": f"Provide an expert-level analysis and explanation of: {query}"
        }
        
        enhanced_prompt = complexity_prompts.get(complexity_level,
            f"Explain clearly: {query}")
        
        # Prefer fast, accurate services for information
        preferences = {
            "prefer_speed": True,
            "accuracy_focus": True
        }
        
        return await self.generate_response(enhanced_prompt, context, preferences)
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all AI services."""
        status = {}
        
        for service_name, config in self.services.items():
            stats = self.usage_stats.get(service_name, {})
            
            status[service_name] = {
                "configured": True,
                "model": config.model,
                "priority": config.priority,
                "cost_per_1k_tokens": config.cost_per_1k_tokens,
                "available": self._is_service_available(service_name),
                "usage_stats": stats
            }
        
        return {
            "services": status,
            "total_services": len(self.services),
            "total_requests": sum(s.get("requests", 0) for s in self.usage_stats.values()),
            "total_cost": sum(s.get("cost", 0.0) for s in self.usage_stats.values())
        }
    
    def get_usage_summary(self) -> Dict[str, Any]:
        """Get usage summary across all services."""
        total_requests = sum(s.get("requests", 0) for s in self.usage_stats.values())
        total_tokens = sum(s.get("tokens", 0) for s in self.usage_stats.values())
        total_cost = sum(s.get("cost", 0.0) for s in self.usage_stats.values())
        
        service_breakdown = {}
        for service_name, stats in self.usage_stats.items():
            if stats.get("requests", 0) > 0:
                service_breakdown[service_name] = {
                    "requests": stats["requests"],
                    "tokens": stats["tokens"],
                    "cost": stats["cost"],
                    "avg_tokens_per_request": stats["tokens"] / stats["requests"],
                    "percentage_of_requests": (stats["requests"] / max(1, total_requests)) * 100
                }
        
        return {
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "average_tokens_per_request": total_tokens / max(1, total_requests),
            "service_breakdown": service_breakdown,
            "most_used_service": max(self.usage_stats.keys(), 
                                   key=lambda s: self.usage_stats[s].get("requests", 0))
            if self.usage_stats else None
        }
    
    async def test_all_services(self) -> Dict[str, Any]:
        """Test all configured AI services."""
        test_prompt = "Hello! Please respond with a brief, friendly greeting."
        results = {}
        
        for service_name in self.services.keys():
            try:
                # Temporarily override service order to test specific service
                original_services = dict(self.services)
                self.services = {service_name: self.services[service_name]}
                
                response = await self.generate_response(test_prompt)
                
                results[service_name] = {
                    "success": response.success,
                    "response_time": response.response_time,
                    "model_used": response.model_used,
                    "tokens_used": response.tokens_used,
                    "cost": response.cost,
                    "error": response.error_message if not response.success else None
                }
                
                # Restore original services
                self.services = original_services
                
            except Exception as e:
                results[service_name] = {
                    "success": False,
                    "error": str(e)
                }
        
        return results

