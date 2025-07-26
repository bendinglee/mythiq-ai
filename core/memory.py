"""
Mythiq AI - Advanced Memory Management System
Handles user profiles, conversation history, emotional patterns, and learning data
"""

import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class UserProfile:
    """User profile with preferences and emotional patterns."""
    user_id: str
    name: Optional[str] = None
    preferred_style: str = "balanced"  # casual, formal, creative, technical, balanced
    emotional_baseline: Dict[str, float] = None
    interests: List[str] = None
    conversation_count: int = 0
    first_interaction: str = None
    last_interaction: str = None
    total_interactions: int = 0
    
    def __post_init__(self):
        if self.emotional_baseline is None:
            self.emotional_baseline = {
                "joy": 0.5, "sadness": 0.2, "anger": 0.1, "fear": 0.2,
                "surprise": 0.3, "disgust": 0.1, "trust": 0.6, "anticipation": 0.4,
                "love": 0.4, "optimism": 0.5, "submission": 0.3, "awe": 0.3
            }
        if self.interests is None:
            self.interests = []
        if self.first_interaction is None:
            self.first_interaction = datetime.now().isoformat()

@dataclass
class ConversationMemory:
    """Individual conversation memory with context and emotions."""
    conversation_id: str
    user_id: str
    messages: List[Dict[str, Any]]
    emotional_journey: List[Dict[str, float]]
    topics: List[str]
    user_goals: List[str]
    ai_personality_used: str
    satisfaction_score: Optional[float] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

@dataclass
class LearningData:
    """Learning data for AI improvement."""
    pattern_id: str
    pattern_type: str  # emotional_response, conversation_flow, user_preference
    input_context: Dict[str, Any]
    successful_response: Dict[str, Any]
    user_feedback: Optional[Dict[str, Any]] = None
    confidence_score: float = 0.5
    usage_count: int = 0
    last_used: str = None
    
    def __post_init__(self):
        if self.last_used is None:
            self.last_used = datetime.now().isoformat()

class MemoryManager:
    """Advanced memory management for Mythiq AI."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize memory manager with data directory."""
        self.data_dir = data_dir
        self.user_profiles: Dict[str, UserProfile] = {}
        self.conversations: Dict[str, ConversationMemory] = {}
        self.learning_data: Dict[str, LearningData] = {}
        self.emotional_patterns: Dict[str, List[Dict]] = {}
        
        # Memory limits to prevent excessive storage
        self.max_conversations_per_user = 50
        self.max_learning_patterns = 1000
        self.memory_cleanup_interval = 3600  # 1 hour
        self.last_cleanup = time.time()
        
        logger.info("MemoryManager initialized")
    
    def get_user_profile(self, user_id: str) -> UserProfile:
        """Get or create user profile."""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(user_id=user_id)
            logger.info(f"Created new user profile for {user_id}")
        
        return self.user_profiles[user_id]
    
    def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> UserProfile:
        """Update user profile with new information."""
        profile = self.get_user_profile(user_id)
        
        for key, value in updates.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        profile.last_interaction = datetime.now().isoformat()
        profile.total_interactions += 1
        
        logger.info(f"Updated profile for user {user_id}")
        return profile
    
    def create_conversation(self, user_id: str, conversation_id: str = None) -> ConversationMemory:
        """Create new conversation memory."""
        if conversation_id is None:
            conversation_id = f"{user_id}_{int(time.time())}"
        
        conversation = ConversationMemory(
            conversation_id=conversation_id,
            user_id=user_id,
            messages=[],
            emotional_journey=[],
            topics=[],
            user_goals=[],
            ai_personality_used="balanced"
        )
        
        self.conversations[conversation_id] = conversation
        
        # Update user profile
        profile = self.get_user_profile(user_id)
        profile.conversation_count += 1
        
        logger.info(f"Created conversation {conversation_id} for user {user_id}")
        return conversation
    
    def add_message_to_conversation(self, conversation_id: str, message: Dict[str, Any]) -> bool:
        """Add message to conversation memory."""
        if conversation_id not in self.conversations:
            logger.warning(f"Conversation {conversation_id} not found")
            return False
        
        conversation = self.conversations[conversation_id]
        conversation.messages.append({
            **message,
            "timestamp": datetime.now().isoformat()
        })
        conversation.updated_at = datetime.now().isoformat()
        
        # Extract topics and emotions if present
        if "detected_topics" in message:
            for topic in message["detected_topics"]:
                if topic not in conversation.topics:
                    conversation.topics.append(topic)
        
        if "detected_emotions" in message:
            conversation.emotional_journey.append(message["detected_emotions"])
        
        logger.debug(f"Added message to conversation {conversation_id}")
        return True
    
    def get_conversation_context(self, conversation_id: str, max_messages: int = 10) -> Dict[str, Any]:
        """Get conversation context for AI processing."""
        if conversation_id not in self.conversations:
            return {"messages": [], "topics": [], "emotional_state": {}}
        
        conversation = self.conversations[conversation_id]
        recent_messages = conversation.messages[-max_messages:] if conversation.messages else []
        
        # Calculate current emotional state
        current_emotions = {}
        if conversation.emotional_journey:
            latest_emotions = conversation.emotional_journey[-1]
            current_emotions = latest_emotions
        
        return {
            "conversation_id": conversation_id,
            "messages": recent_messages,
            "topics": conversation.topics,
            "user_goals": conversation.user_goals,
            "emotional_state": current_emotions,
            "ai_personality": conversation.ai_personality_used,
            "message_count": len(conversation.messages)
        }
    
    def get_user_emotional_pattern(self, user_id: str) -> Dict[str, float]:
        """Get user's emotional patterns over time."""
        profile = self.get_user_profile(user_id)
        user_conversations = [conv for conv in self.conversations.values() if conv.user_id == user_id]
        
        if not user_conversations:
            return profile.emotional_baseline
        
        # Aggregate emotional data from recent conversations
        emotion_totals = {}
        emotion_counts = {}
        
        for conversation in user_conversations[-10:]:  # Last 10 conversations
            for emotion_snapshot in conversation.emotional_journey:
                for emotion, intensity in emotion_snapshot.items():
                    if emotion not in emotion_totals:
                        emotion_totals[emotion] = 0
                        emotion_counts[emotion] = 0
                    emotion_totals[emotion] += intensity
                    emotion_counts[emotion] += 1
        
        # Calculate averages
        emotional_pattern = {}
        for emotion in profile.emotional_baseline.keys():
            if emotion in emotion_totals and emotion_counts[emotion] > 0:
                emotional_pattern[emotion] = emotion_totals[emotion] / emotion_counts[emotion]
            else:
                emotional_pattern[emotion] = profile.emotional_baseline[emotion]
        
        return emotional_pattern
    
    def store_learning_pattern(self, pattern_type: str, input_context: Dict, 
                             successful_response: Dict, user_feedback: Dict = None) -> str:
        """Store successful interaction pattern for learning."""
        pattern_id = hashlib.md5(
            f"{pattern_type}_{json.dumps(input_context, sort_keys=True)}".encode()
        ).hexdigest()
        
        if pattern_id in self.learning_data:
            # Update existing pattern
            pattern = self.learning_data[pattern_id]
            pattern.usage_count += 1
            pattern.last_used = datetime.now().isoformat()
            if user_feedback:
                pattern.user_feedback = user_feedback
                # Adjust confidence based on feedback
                if user_feedback.get("positive", False):
                    pattern.confidence_score = min(1.0, pattern.confidence_score + 0.1)
                else:
                    pattern.confidence_score = max(0.0, pattern.confidence_score - 0.1)
        else:
            # Create new pattern
            pattern = LearningData(
                pattern_id=pattern_id,
                pattern_type=pattern_type,
                input_context=input_context,
                successful_response=successful_response,
                user_feedback=user_feedback
            )
            self.learning_data[pattern_id] = pattern
        
        logger.info(f"Stored learning pattern {pattern_id} of type {pattern_type}")
        return pattern_id
    
    def find_similar_patterns(self, pattern_type: str, context: Dict, 
                            min_confidence: float = 0.6) -> List[LearningData]:
        """Find similar successful patterns for current context."""
        similar_patterns = []
        
        for pattern in self.learning_data.values():
            if (pattern.pattern_type == pattern_type and 
                pattern.confidence_score >= min_confidence):
                
                # Simple similarity check (can be enhanced with ML)
                similarity_score = self._calculate_context_similarity(
                    context, pattern.input_context
                )
                
                if similarity_score > 0.7:  # 70% similarity threshold
                    similar_patterns.append(pattern)
        
        # Sort by confidence and usage
        similar_patterns.sort(
            key=lambda p: (p.confidence_score, p.usage_count), 
            reverse=True
        )
        
        return similar_patterns[:5]  # Return top 5 matches
    
    def _calculate_context_similarity(self, context1: Dict, context2: Dict) -> float:
        """Calculate similarity between two contexts."""
        # Simple implementation - can be enhanced with semantic similarity
        common_keys = set(context1.keys()) & set(context2.keys())
        if not common_keys:
            return 0.0
        
        matches = 0
        for key in common_keys:
            if context1[key] == context2[key]:
                matches += 1
        
        return matches / len(common_keys)
    
    def cleanup_old_data(self) -> Dict[str, int]:
        """Clean up old conversations and learning data."""
        if time.time() - self.last_cleanup < self.memory_cleanup_interval:
            return {"conversations_cleaned": 0, "patterns_cleaned": 0}
        
        conversations_cleaned = 0
        patterns_cleaned = 0
        cutoff_date = datetime.now() - timedelta(days=30)  # 30 days old
        
        # Clean old conversations (keep recent ones per user)
        user_conversations = {}
        for conv_id, conversation in list(self.conversations.items()):
            user_id = conversation.user_id
            if user_id not in user_conversations:
                user_conversations[user_id] = []
            user_conversations[user_id].append((conv_id, conversation))
        
        for user_id, conversations in user_conversations.items():
            # Sort by creation date, keep most recent
            conversations.sort(key=lambda x: x[1].created_at, reverse=True)
            
            # Remove excess conversations
            if len(conversations) > self.max_conversations_per_user:
                for conv_id, _ in conversations[self.max_conversations_per_user:]:
                    del self.conversations[conv_id]
                    conversations_cleaned += 1
        
        # Clean low-confidence learning patterns
        for pattern_id, pattern in list(self.learning_data.items()):
            if (pattern.confidence_score < 0.3 and 
                pattern.usage_count < 2 and
                datetime.fromisoformat(pattern.last_used) < cutoff_date):
                del self.learning_data[pattern_id]
                patterns_cleaned += 1
        
        self.last_cleanup = time.time()
        logger.info(f"Cleaned {conversations_cleaned} conversations and {patterns_cleaned} patterns")
        
        return {
            "conversations_cleaned": conversations_cleaned,
            "patterns_cleaned": patterns_cleaned
        }
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics."""
        total_messages = sum(len(conv.messages) for conv in self.conversations.values())
        
        return {
            "users": len(self.user_profiles),
            "conversations": len(self.conversations),
            "total_messages": total_messages,
            "learning_patterns": len(self.learning_data),
            "average_messages_per_conversation": total_messages / max(1, len(self.conversations)),
            "memory_usage": "optimal",  # Could add actual memory usage calculation
            "last_cleanup": datetime.fromtimestamp(self.last_cleanup).isoformat()
        }
    
    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """Export all data for a specific user (GDPR compliance)."""
        profile = self.user_profiles.get(user_id)
        user_conversations = [conv for conv in self.conversations.values() if conv.user_id == user_id]
        
        return {
            "user_profile": asdict(profile) if profile else None,
            "conversations": [asdict(conv) for conv in user_conversations],
            "emotional_patterns": self.get_user_emotional_pattern(user_id),
            "export_timestamp": datetime.now().isoformat()
        }
    
    def delete_user_data(self, user_id: str) -> bool:
        """Delete all data for a specific user (GDPR compliance)."""
        try:
            # Remove user profile
            if user_id in self.user_profiles:
                del self.user_profiles[user_id]
            
            # Remove user conversations
            conversations_to_remove = [
                conv_id for conv_id, conv in self.conversations.items() 
                if conv.user_id == user_id
            ]
            for conv_id in conversations_to_remove:
                del self.conversations[conv_id]
            
            # Remove user-specific learning patterns
            patterns_to_remove = [
                pattern_id for pattern_id, pattern in self.learning_data.items()
                if pattern.input_context.get("user_id") == user_id
            ]
            for pattern_id in patterns_to_remove:
                del self.learning_data[pattern_id]
            
            logger.info(f"Deleted all data for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting user data for {user_id}: {e}")
            return False

