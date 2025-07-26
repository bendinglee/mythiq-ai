"""
Mythiq AI - Adaptive Chat Core
Intelligent conversation engine with emotional awareness, memory integration, and personality adaptation
"""

import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import logging

from .reasoning_engine import ReasoningEngine, ReasoningResult

logger = logging.getLogger(__name__)

class ConversationState(Enum):
    """Conversation state enumeration."""
    GREETING = "greeting"
    CREATIVE = "creative"
    INFORMATIONAL = "informational"
    EMOTIONAL_SUPPORT = "emotional_support"
    PROBLEM_SOLVING = "problem_solving"
    CASUAL_CHAT = "casual_chat"
    FAREWELL = "farewell"

class ResponseStyle(Enum):
    """Response style enumeration."""
    EMPATHETIC = "empathetic"
    ENTHUSIASTIC = "enthusiastic"
    INFORMATIVE = "informative"
    SUPPORTIVE = "supportive"
    CASUAL = "casual"
    ENCOURAGING = "encouraging"
    BALANCED = "balanced"

class PersonalityMode(Enum):
    """AI personality mode enumeration."""
    PROFESSIONAL = "professional"
    CREATIVE = "creative"
    CARING = "caring"
    TEACHER = "teacher"
    ENTHUSIASTIC = "enthusiastic"
    BALANCED = "balanced"

@dataclass
class ConversationContext:
    """Current conversation context."""
    conversation_id: str
    user_id: str
    state: ConversationState
    message_count: int
    current_topics: List[str]
    user_goals: List[str]
    emotional_state: Dict[str, float]
    engagement_level: float
    preferred_style: ResponseStyle
    ai_personality: PersonalityMode
    last_reasoning: Optional[ReasoningResult] = None

@dataclass
class ResponseGeneration:
    """Response generation configuration."""
    style: ResponseStyle
    personality: PersonalityMode
    tone: str  # warm, neutral, professional, playful
    empathy_level: float  # 0.0-1.0
    creativity_level: float  # 0.0-1.0
    formality_level: float  # 0.0-1.0
    enthusiasm_level: float  # 0.0-1.0

@dataclass
class ChatResponse:
    """Chat response with metadata."""
    response: str
    conversation_id: str
    response_style: str
    ai_personality: str
    emotional_awareness: Dict[str, Any]
    reasoning_summary: Dict[str, Any]
    confidence: float
    processing_time: float
    timestamp: str
    suggestions: List[str] = None

class ChatCore:
    """Adaptive conversation engine with emotional intelligence."""
    
    def __init__(self, reasoning_engine: ReasoningEngine, memory_manager=None, config: Dict[str, Any] = None):
        """Initialize chat core."""
        self.reasoning_engine = reasoning_engine
        self.memory_manager = memory_manager
        self.config = config or {}
        
        # Active conversations
        self.conversations: Dict[str, ConversationContext] = {}
        
        # Response templates by style and personality
        self.response_templates = self._initialize_response_templates()
        
        # Personality characteristics
        self.personality_traits = self._initialize_personality_traits()
        
        # Conversation flow patterns
        self.conversation_patterns = self._initialize_conversation_patterns()
        
        logger.info("ChatCore initialized")
    
    def process_message(self, message: str, user_id: str, conversation_id: str = None,
                       user_preferences: Dict[str, Any] = None) -> ChatResponse:
        """Process incoming message and generate intelligent response."""
        start_time = time.time()
        
        # Get or create conversation context
        if conversation_id is None:
            conversation_id = f"{user_id}_{int(time.time())}"
        
        context = self._get_or_create_conversation_context(
            conversation_id, user_id, user_preferences
        )
        
        # Get conversation history for reasoning context
        reasoning_context = self._build_reasoning_context(context)
        
        # Perform reasoning analysis
        reasoning_result = self.reasoning_engine.analyze_message(message, reasoning_context)
        
        # Update conversation context based on reasoning
        self._update_conversation_context(context, reasoning_result, message)
        
        # Generate response configuration
        response_config = self._generate_response_config(context, reasoning_result)
        
        # Generate the actual response
        response_text = self._generate_response_text(
            message, context, reasoning_result, response_config
        )
        
        # Add conversation suggestions
        suggestions = self._generate_conversation_suggestions(context, reasoning_result)
        
        # Store conversation in memory
        if self.memory_manager:
            self._store_conversation_memory(context, message, response_text, reasoning_result)
        
        processing_time = time.time() - start_time
        
        # Create response object
        response = ChatResponse(
            response=response_text,
            conversation_id=conversation_id,
            response_style=response_config.style.value,
            ai_personality=response_config.personality.value,
            emotional_awareness={
                "detected_emotion": reasoning_result.emotion_analysis.dominant_emotion,
                "emotion_intensity": reasoning_result.emotion_analysis.intensity,
                "empathy_level": response_config.empathy_level,
                "emotional_context": reasoning_result.emotion_analysis.emotional_context
            },
            reasoning_summary=self.reasoning_engine.get_reasoning_summary(reasoning_result),
            confidence=reasoning_result.confidence_score,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat(),
            suggestions=suggestions
        )
        
        logger.debug(f"Processed message for {user_id} in {processing_time:.3f}s")
        return response
    
    def _get_or_create_conversation_context(self, conversation_id: str, user_id: str,
                                          user_preferences: Dict[str, Any] = None) -> ConversationContext:
        """Get existing or create new conversation context."""
        if conversation_id in self.conversations:
            context = self.conversations[conversation_id]
            context.message_count += 1
            return context
        
        # Create new conversation context
        user_preferences = user_preferences or {}
        
        # Get user profile from memory if available
        user_profile = None
        if self.memory_manager:
            user_profile = self.memory_manager.get_user_profile(user_id)
        
        # Determine initial preferences
        preferred_style = ResponseStyle(user_preferences.get(
            "preferred_style", 
            user_profile.preferred_style if user_profile else "balanced"
        ))
        
        context = ConversationContext(
            conversation_id=conversation_id,
            user_id=user_id,
            state=ConversationState.GREETING,
            message_count=1,
            current_topics=[],
            user_goals=[],
            emotional_state={},
            engagement_level=0.5,
            preferred_style=preferred_style,
            ai_personality=PersonalityMode.BALANCED,
            last_reasoning=None
        )
        
        self.conversations[conversation_id] = context
        
        # Create conversation in memory manager
        if self.memory_manager:
            self.memory_manager.create_conversation(user_id, conversation_id)
        
        return context
    
    def _build_reasoning_context(self, context: ConversationContext) -> Dict[str, Any]:
        """Build context for reasoning engine."""
        reasoning_context = {
            "conversation_id": context.conversation_id,
            "user_id": context.user_id,
            "message_count": context.message_count,
            "current_topics": context.current_topics,
            "user_goals": context.user_goals,
            "emotional_state": context.emotional_state,
            "engagement_level": context.engagement_level,
            "conversation_state": context.state.value
        }
        
        # Add memory context if available
        if self.memory_manager:
            memory_context = self.memory_manager.get_conversation_context(
                context.conversation_id, max_messages=5
            )
            reasoning_context.update(memory_context)
            
            # Add user emotional patterns
            emotional_patterns = self.memory_manager.get_user_emotional_pattern(context.user_id)
            reasoning_context["user_emotional_baseline"] = emotional_patterns
        
        return reasoning_context
    
    def _update_conversation_context(self, context: ConversationContext, 
                                   reasoning_result: ReasoningResult, message: str):
        """Update conversation context based on reasoning analysis."""
        # Update emotional state
        context.emotional_state = reasoning_result.emotion_analysis.emotions
        
        # Update engagement level
        context.engagement_level = reasoning_result.context_analysis.engagement_level
        
        # Update topics
        new_topics = reasoning_result.context_analysis.topics
        for topic in new_topics:
            if topic not in context.current_topics:
                context.current_topics.append(topic)
        
        # Keep only recent topics (max 5)
        context.current_topics = context.current_topics[-5:]
        
        # Update user goals
        new_goals = reasoning_result.context_analysis.user_goals
        for goal in new_goals:
            if goal not in context.user_goals:
                context.user_goals.append(goal)
        
        # Keep only recent goals (max 3)
        context.user_goals = context.user_goals[-3:]
        
        # Update conversation state
        context.state = self._determine_conversation_state(reasoning_result)
        
        # Update AI personality based on context
        context.ai_personality = PersonalityMode(reasoning_result.recommended_personality)
        
        # Store reasoning result
        context.last_reasoning = reasoning_result
    
    def _determine_conversation_state(self, reasoning_result: ReasoningResult) -> ConversationState:
        """Determine conversation state from reasoning result."""
        intent = reasoning_result.intent_analysis.primary_intent
        
        state_mapping = {
            "creative_request": ConversationState.CREATIVE,
            "information_request": ConversationState.INFORMATIONAL,
            "emotional_support": ConversationState.EMOTIONAL_SUPPORT,
            "problem_solving": ConversationState.PROBLEM_SOLVING,
            "casual_conversation": ConversationState.CASUAL_CHAT,
            "farewell": ConversationState.FAREWELL
        }
        
        return state_mapping.get(intent, ConversationState.CASUAL_CHAT)
    
    def _generate_response_config(self, context: ConversationContext, 
                                reasoning_result: ReasoningResult) -> ResponseGeneration:
        """Generate response configuration based on context and reasoning."""
        # Base configuration from reasoning
        style = ResponseStyle(reasoning_result.recommended_response_style)
        personality = PersonalityMode(reasoning_result.recommended_personality)
        
        # Adjust based on user preferences
        if context.preferred_style != ResponseStyle.BALANCED:
            # Blend user preference with reasoning recommendation
            style = context.preferred_style
        
        # Determine tone
        emotion_intensity = reasoning_result.emotion_analysis.intensity
        dominant_emotion = reasoning_result.emotion_analysis.dominant_emotion
        
        if dominant_emotion in ["sadness", "fear", "anger"] and emotion_intensity > 0.6:
            tone = "warm"
        elif dominant_emotion in ["joy", "excitement"] and emotion_intensity > 0.6:
            tone = "playful"
        elif reasoning_result.context_analysis.complexity_level in ["complex", "expert"]:
            tone = "professional"
        else:
            tone = "neutral"
        
        # Calculate response characteristics
        empathy_level = min(1.0, emotion_intensity + 0.3) if dominant_emotion in ["sadness", "fear", "anger"] else 0.5
        creativity_level = 0.8 if context.state == ConversationState.CREATIVE else 0.5
        formality_level = 0.8 if personality == PersonalityMode.PROFESSIONAL else 0.3
        enthusiasm_level = 0.8 if dominant_emotion in ["joy", "excitement", "anticipation"] else 0.5
        
        return ResponseGeneration(
            style=style,
            personality=personality,
            tone=tone,
            empathy_level=empathy_level,
            creativity_level=creativity_level,
            formality_level=formality_level,
            enthusiasm_level=enthusiasm_level
        )
    
    def _generate_response_text(self, message: str, context: ConversationContext,
                              reasoning_result: ReasoningResult, 
                              response_config: ResponseGeneration) -> str:
        """Generate the actual response text."""
        # Get base template
        template = self._get_response_template(response_config.style, response_config.personality)
        
        # Get personality-specific elements
        personality_elements = self.personality_traits[response_config.personality]
        
        # Build response components
        greeting = self._generate_greeting(context, response_config)
        main_response = self._generate_main_response(message, reasoning_result, response_config)
        emotional_acknowledgment = self._generate_emotional_acknowledgment(reasoning_result, response_config)
        encouragement = self._generate_encouragement(context, reasoning_result, response_config)
        
        # Combine components based on template
        response_parts = []
        
        # Add greeting for new conversations or greetings
        if context.message_count <= 2 or reasoning_result.intent_analysis.primary_intent == "casual_conversation":
            if greeting:
                response_parts.append(greeting)
        
        # Add emotional acknowledgment if needed
        if emotional_acknowledgment and response_config.empathy_level > 0.6:
            response_parts.append(emotional_acknowledgment)
        
        # Add main response
        response_parts.append(main_response)
        
        # Add encouragement if appropriate
        if encouragement and response_config.enthusiasm_level > 0.6:
            response_parts.append(encouragement)
        
        # Join parts and apply personality styling
        response = " ".join(response_parts)
        response = self._apply_personality_styling(response, response_config, personality_elements)
        
        return response
    
    def _get_response_template(self, style: ResponseStyle, personality: PersonalityMode) -> Dict[str, str]:
        """Get response template for style and personality combination."""
        return self.response_templates.get(f"{style.value}_{personality.value}", 
                                         self.response_templates["default"])
    
    def _generate_greeting(self, context: ConversationContext, 
                         response_config: ResponseGeneration) -> Optional[str]:
        """Generate appropriate greeting."""
        if context.message_count > 2:
            return None
        
        greetings = {
            PersonalityMode.ENTHUSIASTIC: ["Hello! I'm so excited to chat with you! 🌟", 
                                         "Hi there! Ready to create something amazing together? 🚀"],
            PersonalityMode.CARING: ["Hello! I'm here to help and support you. 💝",
                                   "Hi! I'm glad you're here. How can I assist you today? 🤗"],
            PersonalityMode.PROFESSIONAL: ["Good day! I'm Mythiq AI, ready to assist you.",
                                         "Hello! How may I help you today?"],
            PersonalityMode.CREATIVE: ["Hey! Let's spark some creativity together! ✨",
                                     "Hello, creative soul! What shall we imagine today? 🎨"],
            PersonalityMode.TEACHER: ["Hello! I'm here to help you learn and grow! 📚",
                                    "Hi! What would you like to explore today? 🧠"],
            PersonalityMode.BALANCED: ["Hello! I'm Mythiq AI, and I'm here to help! 😊",
                                     "Hi there! What can I do for you today? 🤖"]
        }
        
        personality_greetings = greetings.get(response_config.personality, greetings[PersonalityMode.BALANCED])
        return personality_greetings[context.message_count % len(personality_greetings)]
    
    def _generate_main_response(self, message: str, reasoning_result: ReasoningResult,
                              response_config: ResponseGeneration) -> str:
        """Generate main response content."""
        intent = reasoning_result.intent_analysis.primary_intent
        emotion = reasoning_result.emotion_analysis.dominant_emotion
        
        # Intent-based response generation
        if intent == "creative_request":
            return self._generate_creative_response(message, reasoning_result, response_config)
        elif intent == "information_request":
            return self._generate_informational_response(message, reasoning_result, response_config)
        elif intent == "emotional_support":
            return self._generate_supportive_response(message, reasoning_result, response_config)
        elif intent == "problem_solving":
            return self._generate_problem_solving_response(message, reasoning_result, response_config)
        elif intent == "casual_conversation":
            return self._generate_casual_response(message, reasoning_result, response_config)
        else:
            return self._generate_default_response(message, reasoning_result, response_config)
    
    def _generate_creative_response(self, message: str, reasoning_result: ReasoningResult,
                                  response_config: ResponseGeneration) -> str:
        """Generate response for creative requests."""
        entities = reasoning_result.intent_analysis.entities
        
        creative_responses = [
            f"I love your creative vision! Your idea about '{message}' has so much potential! 🎨",
            f"That's an amazing creative concept! I can already imagine how wonderful '{message}' could be! ✨",
            f"Your creativity is inspiring! Let's bring your idea about '{message}' to life! 🚀",
            f"What a fantastic creative challenge! I'm excited to help you with '{message}'! 🌟"
        ]
        
        # Add specific creative medium mentions if detected
        if entities.get("creative_mediums"):
            medium = entities["creative_mediums"][0]
            creative_responses.append(f"Creating a {medium} sounds amazing! Your concept '{message}' will be incredible!")
        
        base_response = creative_responses[len(message) % len(creative_responses)]
        
        # Add creative encouragement
        if response_config.creativity_level > 0.7:
            encouragements = [
                "Let's push the boundaries of imagination!",
                "The possibilities are endless!",
                "Your creativity knows no limits!",
                "Let's make something truly unique!"
            ]
            encouragement = encouragements[len(message) % len(encouragements)]
            base_response += f" {encouragement}"
        
        return base_response
    
    def _generate_informational_response(self, message: str, reasoning_result: ReasoningResult,
                                       response_config: ResponseGeneration) -> str:
        """Generate response for information requests."""
        complexity = reasoning_result.context_analysis.complexity_level
        
        if complexity == "expert":
            return f"That's an excellent technical question about '{message}'. I'll provide you with comprehensive information and insights!"
        elif complexity == "complex":
            return f"Great question about '{message}'! I'll break this down into clear, detailed explanations for you."
        else:
            return f"I'd be happy to help you understand '{message}'! Let me explain this in a clear and helpful way."
    
    def _generate_supportive_response(self, message: str, reasoning_result: ReasoningResult,
                                    response_config: ResponseGeneration) -> str:
        """Generate response for emotional support."""
        emotion = reasoning_result.emotion_analysis.dominant_emotion
        intensity = reasoning_result.emotion_analysis.intensity
        
        if emotion == "sadness" and intensity > 0.6:
            return f"I can sense you're going through a difficult time with '{message}'. I'm here to listen and support you. 💝"
        elif emotion == "anger" and intensity > 0.6:
            return f"I understand you're feeling frustrated about '{message}'. Those feelings are completely valid, and I'm here to help."
        elif emotion == "fear" and intensity > 0.6:
            return f"I can tell '{message}' is causing you some worry. It's okay to feel this way, and we can work through this together."
        else:
            return f"Thank you for sharing '{message}' with me. I'm here to support you however I can."
    
    def _generate_problem_solving_response(self, message: str, reasoning_result: ReasoningResult,
                                         response_config: ResponseGeneration) -> str:
        """Generate response for problem-solving requests."""
        urgency = reasoning_result.intent_analysis.urgency_level
        
        if urgency == "urgent":
            return f"I understand this is urgent! Let's tackle '{message}' right away and find a solution quickly."
        elif urgency == "high":
            return f"I can see this is important to you. Let's work on solving '{message}' step by step."
        else:
            return f"I'm here to help you figure out '{message}'. Let's approach this systematically and find the best solution!"
    
    def _generate_casual_response(self, message: str, reasoning_result: ReasoningResult,
                                response_config: ResponseGeneration) -> str:
        """Generate response for casual conversation."""
        engagement = reasoning_result.context_analysis.engagement_level
        
        if engagement > 0.8:
            return f"I love chatting with you about '{message}'! Your enthusiasm is contagious! 😊"
        elif engagement > 0.6:
            return f"That's interesting! I enjoy our conversation about '{message}'. Tell me more!"
        else:
            return f"Thanks for sharing '{message}' with me! I'm always happy to chat."
    
    def _generate_default_response(self, message: str, reasoning_result: ReasoningResult,
                                 response_config: ResponseGeneration) -> str:
        """Generate default response."""
        return f"Thank you for your message about '{message}'. I'm here to help you in any way I can! 🤖"
    
    def _generate_emotional_acknowledgment(self, reasoning_result: ReasoningResult,
                                         response_config: ResponseGeneration) -> Optional[str]:
        """Generate emotional acknowledgment if appropriate."""
        if response_config.empathy_level < 0.6:
            return None
        
        emotion = reasoning_result.emotion_analysis.dominant_emotion
        intensity = reasoning_result.emotion_analysis.intensity
        
        if intensity < 0.5:
            return None
        
        acknowledgments = {
            "joy": "I can feel your happiness and excitement! 😊",
            "sadness": "I sense you might be feeling down, and that's okay. 💙",
            "anger": "I can tell you're feeling frustrated, and I understand. 🤗",
            "fear": "I notice some worry in your message, and I'm here for you. 💝",
            "surprise": "You seem surprised! That's quite a reaction! 😮",
            "love": "I can feel the warmth and care in your words! ❤️",
            "anticipation": "I can sense your excitement about what's coming! 🌟"
        }
        
        return acknowledgments.get(emotion)
    
    def _generate_encouragement(self, context: ConversationContext, 
                              reasoning_result: ReasoningResult,
                              response_config: ResponseGeneration) -> Optional[str]:
        """Generate encouragement if appropriate."""
        if response_config.enthusiasm_level < 0.6:
            return None
        
        encouragements = [
            "You've got this! 💪",
            "I believe in your abilities! 🌟",
            "Let's make something amazing together! 🚀",
            "Your potential is limitless! ✨",
            "I'm excited to see what we create! 🎨",
            "Together, we can achieve anything! 🤝"
        ]
        
        return encouragements[context.message_count % len(encouragements)]
    
    def _apply_personality_styling(self, response: str, response_config: ResponseGeneration,
                                 personality_elements: Dict[str, Any]) -> str:
        """Apply personality-specific styling to response."""
        # Add personality-specific phrases or modifications
        if response_config.personality == PersonalityMode.ENTHUSIASTIC:
            if not any(emoji in response for emoji in ["!", "🚀", "🌟", "✨", "🎉"]):
                response += " 🚀"
        
        elif response_config.personality == PersonalityMode.CARING:
            if not any(emoji in response for emoji in ["💝", "🤗", "💙", "❤️"]):
                response += " 💝"
        
        elif response_config.personality == PersonalityMode.CREATIVE:
            if not any(emoji in response for emoji in ["🎨", "✨", "🌈", "💡"]):
                response += " ✨"
        
        # Adjust formality
        if response_config.formality_level > 0.7:
            response = response.replace("!", ".")
            response = response.replace(" 🚀", "")
            response = response.replace(" ✨", "")
        
        return response
    
    def _generate_conversation_suggestions(self, context: ConversationContext,
                                         reasoning_result: ReasoningResult) -> List[str]:
        """Generate conversation suggestions for the user."""
        intent = reasoning_result.intent_analysis.primary_intent
        state = context.state
        
        suggestions = []
        
        if intent == "creative_request":
            suggestions = [
                "Tell me more about your creative vision",
                "What style or theme do you have in mind?",
                "Would you like to explore different creative approaches?"
            ]
        elif intent == "information_request":
            suggestions = [
                "Would you like me to explain this in more detail?",
                "Are there specific aspects you'd like to focus on?",
                "Do you have any follow-up questions?"
            ]
        elif state == ConversationState.CASUAL_CHAT:
            suggestions = [
                "What else would you like to chat about?",
                "Tell me about your interests",
                "What's been on your mind lately?"
            ]
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def _store_conversation_memory(self, context: ConversationContext, message: str,
                                 response: str, reasoning_result: ReasoningResult):
        """Store conversation in memory manager."""
        if not self.memory_manager:
            return
        
        message_data = {
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "detected_emotions": reasoning_result.emotion_analysis.emotions,
            "detected_intent": reasoning_result.intent_analysis.primary_intent,
            "detected_topics": reasoning_result.context_analysis.topics
        }
        
        response_data = {
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat(),
            "response_style": context.preferred_style.value,
            "ai_personality": context.ai_personality.value,
            "confidence": reasoning_result.confidence_score
        }
        
        # Add messages to conversation
        self.memory_manager.add_message_to_conversation(context.conversation_id, message_data)
        self.memory_manager.add_message_to_conversation(context.conversation_id, response_data)
    
    def _initialize_response_templates(self) -> Dict[str, Dict[str, str]]:
        """Initialize response templates."""
        return {
            "empathetic_caring": {
                "greeting": "Hello, I'm here for you 💝",
                "main": "I understand and care about your feelings",
                "closing": "You're not alone in this"
            },
            "enthusiastic_creative": {
                "greeting": "Hey there, creative soul! ✨",
                "main": "Let's bring your amazing ideas to life!",
                "closing": "The possibilities are endless! 🚀"
            },
            "informative_teacher": {
                "greeting": "Hello! Ready to learn something new? 📚",
                "main": "Let me explain this clearly and thoroughly",
                "closing": "Knowledge is power! 🧠"
            },
            "default": {
                "greeting": "Hello! 😊",
                "main": "I'm here to help you",
                "closing": "Let's make something great together! 🤖"
            }
        }
    
    def _initialize_personality_traits(self) -> Dict[PersonalityMode, Dict[str, Any]]:
        """Initialize personality traits."""
        return {
            PersonalityMode.ENTHUSIASTIC: {
                "energy_level": "high",
                "emoji_usage": "frequent",
                "exclamation_usage": "high",
                "encouragement_frequency": "high"
            },
            PersonalityMode.CARING: {
                "empathy_expressions": "frequent",
                "supportive_language": "high",
                "emotional_validation": "high",
                "gentle_tone": "high"
            },
            PersonalityMode.PROFESSIONAL: {
                "formality_level": "high",
                "technical_accuracy": "high",
                "structured_responses": "high",
                "emoji_usage": "minimal"
            },
            PersonalityMode.CREATIVE: {
                "imaginative_language": "high",
                "metaphor_usage": "frequent",
                "artistic_references": "high",
                "inspiration_focus": "high"
            },
            PersonalityMode.TEACHER: {
                "explanation_detail": "high",
                "educational_structure": "high",
                "patience_level": "high",
                "knowledge_sharing": "high"
            },
            PersonalityMode.BALANCED: {
                "adaptability": "high",
                "moderate_traits": "all",
                "context_sensitivity": "high",
                "versatility": "high"
            }
        }
    
    def _initialize_conversation_patterns(self) -> Dict[str, Any]:
        """Initialize conversation flow patterns."""
        return {
            "greeting_patterns": ["hello", "hi", "hey", "greetings"],
            "farewell_patterns": ["bye", "goodbye", "see you", "farewell"],
            "question_patterns": ["what", "how", "why", "when", "where", "who"],
            "creative_patterns": ["create", "make", "generate", "build", "design"],
            "emotional_patterns": ["feel", "emotion", "mood", "heart", "soul"]
        }
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get conversation statistics."""
        total_conversations = len(self.conversations)
        active_conversations = len([c for c in self.conversations.values() if c.message_count > 1])
        
        # Aggregate statistics
        total_messages = sum(c.message_count for c in self.conversations.values())
        avg_engagement = sum(c.engagement_level for c in self.conversations.values()) / max(1, total_conversations)
        
        # State distribution
        state_counts = {}
        for conversation in self.conversations.values():
            state = conversation.state.value
            state_counts[state] = state_counts.get(state, 0) + 1
        
        return {
            "total_conversations": total_conversations,
            "active_conversations": active_conversations,
            "total_messages": total_messages,
            "average_engagement": avg_engagement,
            "conversation_states": state_counts,
            "personality_usage": {
                personality.value: len([c for c in self.conversations.values() 
                                     if c.ai_personality == personality])
                for personality in PersonalityMode
            }
        }

