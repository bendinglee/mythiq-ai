"""
Mythiq AI - Reflector Module
Self-improvement, learning from interactions, and system optimization
"""

import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)

@dataclass
class InteractionAnalysis:
    """Analysis of a user interaction."""
    interaction_id: str
    user_id: str
    conversation_id: str
    user_message: str
    ai_response: str
    user_feedback: Optional[Dict[str, Any]]
    reasoning_data: Dict[str, Any]
    response_quality_score: float
    emotional_appropriateness: float
    user_satisfaction_indicators: List[str]
    improvement_suggestions: List[str]
    timestamp: str

@dataclass
class LearningPattern:
    """A learned pattern from user interactions."""
    pattern_id: str
    pattern_type: str  # emotional_response, conversation_flow, creative_approach
    context_triggers: Dict[str, Any]
    successful_approach: Dict[str, Any]
    confidence_score: float
    usage_count: int
    success_rate: float
    last_updated: str
    user_feedback_summary: Dict[str, Any]

@dataclass
class SystemInsight:
    """System-level insight for improvement."""
    insight_id: str
    category: str  # performance, user_experience, emotional_intelligence
    description: str
    evidence: List[str]
    recommended_actions: List[str]
    priority: str  # low, medium, high, critical
    impact_estimate: str
    implementation_complexity: str
    timestamp: str

@dataclass
class ReflectionReport:
    """Comprehensive reflection and improvement report."""
    report_id: str
    time_period: str
    interactions_analyzed: int
    key_insights: List[SystemInsight]
    learning_patterns: List[LearningPattern]
    performance_metrics: Dict[str, float]
    user_satisfaction_trends: Dict[str, float]
    improvement_recommendations: List[str]
    generated_at: str

class ReflectorModule:
    """AI self-improvement and learning system."""
    
    def __init__(self, memory_manager=None, ai_service_manager=None, config: Dict[str, Any] = None):
        """Initialize reflector module."""
        self.memory_manager = memory_manager
        self.ai_service_manager = ai_service_manager
        self.config = config or {}
        
        # Learning data storage
        self.interaction_analyses: deque = deque(maxlen=1000)  # Recent analyses
        self.learning_patterns: Dict[str, LearningPattern] = {}
        self.system_insights: List[SystemInsight] = []
        
        # Performance tracking
        self.performance_metrics = defaultdict(list)
        self.user_satisfaction_scores = defaultdict(list)
        
        # Learning configuration
        self.min_interactions_for_pattern = self.config.get("min_interactions_for_pattern", 5)
        self.confidence_threshold = self.config.get("confidence_threshold", 0.7)
        self.reflection_interval = self.config.get("reflection_interval", 3600)  # 1 hour
        
        # Last reflection time
        self.last_reflection = time.time()
        
        logger.info("ReflectorModule initialized")
    
    def analyze_interaction(self, user_message: str, ai_response: str, 
                          reasoning_data: Dict[str, Any], user_id: str,
                          conversation_id: str, user_feedback: Dict[str, Any] = None) -> InteractionAnalysis:
        """Analyze a user interaction for learning opportunities."""
        interaction_id = f"{user_id}_{conversation_id}_{int(time.time())}"
        
        # Analyze response quality
        quality_score = self._analyze_response_quality(user_message, ai_response, reasoning_data)
        
        # Analyze emotional appropriateness
        emotional_score = self._analyze_emotional_appropriateness(
            user_message, ai_response, reasoning_data
        )
        
        # Extract satisfaction indicators
        satisfaction_indicators = self._extract_satisfaction_indicators(
            user_message, ai_response, user_feedback
        )
        
        # Generate improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(
            user_message, ai_response, reasoning_data, quality_score, emotional_score
        )
        
        analysis = InteractionAnalysis(
            interaction_id=interaction_id,
            user_id=user_id,
            conversation_id=conversation_id,
            user_message=user_message,
            ai_response=ai_response,
            user_feedback=user_feedback,
            reasoning_data=reasoning_data,
            response_quality_score=quality_score,
            emotional_appropriateness=emotional_score,
            user_satisfaction_indicators=satisfaction_indicators,
            improvement_suggestions=improvement_suggestions,
            timestamp=datetime.now().isoformat()
        )
        
        # Store analysis
        self.interaction_analyses.append(analysis)
        
        # Update performance metrics
        self._update_performance_metrics(analysis)
        
        # Check for immediate learning opportunities
        self._check_for_learning_patterns(analysis)
        
        logger.debug(f"Analyzed interaction {interaction_id}")
        return analysis
    
    def _analyze_response_quality(self, user_message: str, ai_response: str,
                                reasoning_data: Dict[str, Any]) -> float:
        """Analyze the quality of the AI response."""
        quality_score = 0.5  # Base score
        
        # Length appropriateness
        user_length = len(user_message)
        response_length = len(ai_response)
        
        if user_length < 50 and 50 <= response_length <= 200:
            quality_score += 0.1  # Good length for short queries
        elif user_length >= 50 and 100 <= response_length <= 400:
            quality_score += 0.1  # Good length for longer queries
        
        # Intent matching
        detected_intent = reasoning_data.get("reasoning_summary", {}).get("primary_intent")
        if detected_intent:
            intent_keywords = {
                "creative_request": ["create", "generate", "make", "design"],
                "information_request": ["explain", "information", "details", "facts"],
                "emotional_support": ["understand", "support", "help", "care"],
                "problem_solving": ["solve", "solution", "fix", "resolve"]
            }
            
            keywords = intent_keywords.get(detected_intent, [])
            if any(keyword in ai_response.lower() for keyword in keywords):
                quality_score += 0.2
        
        # Emotional awareness
        if reasoning_data.get("emotional_awareness", {}).get("empathy_level", 0) > 0.5:
            emotional_words = ["understand", "feel", "care", "support", "here for you"]
            if any(word in ai_response.lower() for word in emotional_words):
                quality_score += 0.1
        
        # Helpfulness indicators
        helpful_phrases = ["help", "assist", "support", "guide", "show you"]
        if any(phrase in ai_response.lower() for phrase in helpful_phrases):
            quality_score += 0.1
        
        # Avoid repetition
        if ai_response.lower() not in user_message.lower():
            quality_score += 0.1
        
        return min(1.0, quality_score)
    
    def _analyze_emotional_appropriateness(self, user_message: str, ai_response: str,
                                         reasoning_data: Dict[str, Any]) -> float:
        """Analyze emotional appropriateness of the response."""
        emotional_score = 0.5  # Base score
        
        emotional_awareness = reasoning_data.get("emotional_awareness", {})
        detected_emotion = emotional_awareness.get("detected_emotion", "neutral")
        emotion_intensity = emotional_awareness.get("emotion_intensity", 0.5)
        
        # Check for appropriate emotional response
        if detected_emotion in ["sadness", "fear", "anger"] and emotion_intensity > 0.6:
            # Should be empathetic
            empathetic_words = ["understand", "sorry", "care", "support", "here", "help"]
            if any(word in ai_response.lower() for word in empathetic_words):
                emotional_score += 0.3
            
            # Should avoid being too cheerful
            cheerful_words = ["exciting", "amazing", "awesome", "fantastic"]
            if not any(word in ai_response.lower() for word in cheerful_words):
                emotional_score += 0.2
        
        elif detected_emotion in ["joy", "excitement"] and emotion_intensity > 0.6:
            # Should match enthusiasm
            enthusiastic_words = ["great", "amazing", "exciting", "wonderful", "fantastic"]
            if any(word in ai_response.lower() for word in enthusiastic_words):
                emotional_score += 0.3
        
        # Check for emotional validation
        if emotion_intensity > 0.5:
            validation_phrases = ["that's", "i can", "i understand", "makes sense"]
            if any(phrase in ai_response.lower() for phrase in validation_phrases):
                emotional_score += 0.2
        
        return min(1.0, emotional_score)
    
    def _extract_satisfaction_indicators(self, user_message: str, ai_response: str,
                                       user_feedback: Dict[str, Any] = None) -> List[str]:
        """Extract indicators of user satisfaction."""
        indicators = []
        
        # Explicit feedback
        if user_feedback:
            if user_feedback.get("rating", 0) >= 4:
                indicators.append("high_rating")
            if user_feedback.get("helpful", False):
                indicators.append("marked_helpful")
            if user_feedback.get("positive_comment"):
                indicators.append("positive_feedback")
        
        # Implicit indicators from user message
        user_lower = user_message.lower()
        
        # Positive language
        positive_words = ["thank", "great", "awesome", "perfect", "exactly", "love"]
        if any(word in user_lower for word in positive_words):
            indicators.append("positive_language")
        
        # Follow-up questions (engagement)
        if "?" in user_message and len(user_message) > 20:
            indicators.append("engaged_follow_up")
        
        # Specific requests (trust)
        if any(word in user_lower for word in ["can you", "please", "help me"]):
            indicators.append("trust_indicators")
        
        return indicators
    
    def _generate_improvement_suggestions(self, user_message: str, ai_response: str,
                                        reasoning_data: Dict[str, Any], quality_score: float,
                                        emotional_score: float) -> List[str]:
        """Generate suggestions for improving the response."""
        suggestions = []
        
        # Quality improvements
        if quality_score < 0.7:
            if len(ai_response) < 50:
                suggestions.append("Provide more detailed and comprehensive responses")
            
            detected_intent = reasoning_data.get("reasoning_summary", {}).get("primary_intent")
            if detected_intent == "creative_request" and "create" not in ai_response.lower():
                suggestions.append("More explicitly address creative requests with action words")
            
            if detected_intent == "information_request" and "explain" not in ai_response.lower():
                suggestions.append("Use more explanatory language for information requests")
        
        # Emotional improvements
        if emotional_score < 0.7:
            emotion = reasoning_data.get("emotional_awareness", {}).get("detected_emotion")
            if emotion in ["sadness", "fear", "anger"]:
                suggestions.append("Increase empathetic language for negative emotions")
            elif emotion in ["joy", "excitement"]:
                suggestions.append("Match user enthusiasm with more energetic language")
        
        # Engagement improvements
        if "?" not in ai_response and len(user_message) > 50:
            suggestions.append("Ask follow-up questions to maintain engagement")
        
        # Personalization improvements
        if "you" not in ai_response.lower():
            suggestions.append("Use more personalized language addressing the user directly")
        
        return suggestions
    
    def _update_performance_metrics(self, analysis: InteractionAnalysis):
        """Update performance metrics based on interaction analysis."""
        timestamp = datetime.now().isoformat()
        
        # Quality metrics
        self.performance_metrics["response_quality"].append({
            "value": analysis.response_quality_score,
            "timestamp": timestamp
        })
        
        # Emotional appropriateness
        self.performance_metrics["emotional_appropriateness"].append({
            "value": analysis.emotional_appropriateness,
            "timestamp": timestamp
        })
        
        # User satisfaction (based on indicators)
        satisfaction_score = len(analysis.user_satisfaction_indicators) / 5.0  # Normalize to 0-1
        self.performance_metrics["user_satisfaction"].append({
            "value": min(1.0, satisfaction_score),
            "timestamp": timestamp
        })
        
        # Keep only recent metrics (last 100 entries)
        for metric_name in self.performance_metrics:
            if len(self.performance_metrics[metric_name]) > 100:
                self.performance_metrics[metric_name] = self.performance_metrics[metric_name][-100:]
    
    def _check_for_learning_patterns(self, analysis: InteractionAnalysis):
        """Check for emerging learning patterns."""
        # Look for patterns in successful interactions
        if (analysis.response_quality_score > 0.8 and 
            analysis.emotional_appropriateness > 0.8 and
            len(analysis.user_satisfaction_indicators) >= 2):
            
            # Extract pattern context
            context = {
                "intent": analysis.reasoning_data.get("reasoning_summary", {}).get("primary_intent"),
                "emotion": analysis.reasoning_data.get("emotional_awareness", {}).get("detected_emotion"),
                "complexity": analysis.reasoning_data.get("reasoning_summary", {}).get("complexity_level"),
                "user_message_length": len(analysis.user_message),
                "response_style": analysis.reasoning_data.get("response_style")
            }
            
            # Create pattern signature
            pattern_signature = f"{context['intent']}_{context['emotion']}_{context['complexity']}"
            
            if pattern_signature in self.learning_patterns:
                # Update existing pattern
                pattern = self.learning_patterns[pattern_signature]
                pattern.usage_count += 1
                pattern.success_rate = (pattern.success_rate * (pattern.usage_count - 1) + 1.0) / pattern.usage_count
                pattern.last_updated = datetime.now().isoformat()
            else:
                # Create new pattern
                pattern = LearningPattern(
                    pattern_id=pattern_signature,
                    pattern_type="successful_interaction",
                    context_triggers=context,
                    successful_approach={
                        "response_length": len(analysis.ai_response),
                        "key_phrases": self._extract_key_phrases(analysis.ai_response),
                        "emotional_tone": analysis.reasoning_data.get("emotional_awareness", {}),
                        "satisfaction_indicators": analysis.user_satisfaction_indicators
                    },
                    confidence_score=0.7,
                    usage_count=1,
                    success_rate=1.0,
                    last_updated=datetime.now().isoformat(),
                    user_feedback_summary={}
                )
                self.learning_patterns[pattern_signature] = pattern
                
                logger.info(f"New learning pattern identified: {pattern_signature}")
    
    def _extract_key_phrases(self, response: str) -> List[str]:
        """Extract key phrases from a successful response."""
        # Simple keyword extraction (could be enhanced with NLP)
        words = response.lower().split()
        
        # Look for helpful phrases
        key_phrases = []
        helpful_patterns = [
            "i understand", "i can help", "let me", "here's how", "you can",
            "i'd be happy", "great question", "that's interesting", "i love"
        ]
        
        for pattern in helpful_patterns:
            if pattern in response.lower():
                key_phrases.append(pattern)
        
        return key_phrases[:5]  # Limit to top 5
    
    def perform_reflection(self, force: bool = False) -> ReflectionReport:
        """Perform comprehensive system reflection and generate insights."""
        current_time = time.time()
        
        if not force and current_time - self.last_reflection < self.reflection_interval:
            logger.debug("Reflection interval not reached, skipping")
            return None
        
        logger.info("Performing system reflection...")
        
        # Analyze recent interactions
        recent_analyses = list(self.interaction_analyses)[-50:]  # Last 50 interactions
        
        if len(recent_analyses) < 5:
            logger.warning("Insufficient interaction data for meaningful reflection")
            return None
        
        # Generate insights
        insights = self._generate_system_insights(recent_analyses)
        
        # Update learning patterns
        self._update_learning_patterns(recent_analyses)
        
        # Calculate performance metrics
        performance_summary = self._calculate_performance_summary()
        
        # Generate improvement recommendations
        recommendations = self._generate_improvement_recommendations(insights, performance_summary)
        
        # Create reflection report
        report = ReflectionReport(
            report_id=f"reflection_{int(current_time)}",
            time_period=f"Last {len(recent_analyses)} interactions",
            interactions_analyzed=len(recent_analyses),
            key_insights=insights,
            learning_patterns=list(self.learning_patterns.values())[-10:],  # Recent patterns
            performance_metrics=performance_summary,
            user_satisfaction_trends=self._calculate_satisfaction_trends(),
            improvement_recommendations=recommendations,
            generated_at=datetime.now().isoformat()
        )
        
        self.last_reflection = current_time
        logger.info(f"Reflection completed: {len(insights)} insights, {len(recommendations)} recommendations")
        
        return report
    
    def _generate_system_insights(self, analyses: List[InteractionAnalysis]) -> List[SystemInsight]:
        """Generate system-level insights from interaction analyses."""
        insights = []
        
        if not analyses:
            return insights
        
        # Performance insight
        avg_quality = sum(a.response_quality_score for a in analyses) / len(analyses)
        if avg_quality < 0.7:
            insights.append(SystemInsight(
                insight_id=f"performance_{int(time.time())}",
                category="performance",
                description=f"Average response quality is {avg_quality:.2f}, below optimal threshold of 0.7",
                evidence=[f"Analyzed {len(analyses)} interactions", f"Quality scores range from {min(a.response_quality_score for a in analyses):.2f} to {max(a.response_quality_score for a in analyses):.2f}"],
                recommended_actions=["Improve response relevance", "Enhance intent detection accuracy", "Provide more comprehensive answers"],
                priority="high",
                impact_estimate="Improved user satisfaction and engagement",
                implementation_complexity="medium",
                timestamp=datetime.now().isoformat()
            ))
        
        # Emotional intelligence insight
        avg_emotional = sum(a.emotional_appropriateness for a in analyses) / len(analyses)
        if avg_emotional < 0.7:
            insights.append(SystemInsight(
                insight_id=f"emotional_{int(time.time())}",
                category="emotional_intelligence",
                description=f"Emotional appropriateness is {avg_emotional:.2f}, indicating room for improvement",
                evidence=[f"Emotional scores below 0.7 in {sum(1 for a in analyses if a.emotional_appropriateness < 0.7)} interactions"],
                recommended_actions=["Enhance emotion detection", "Improve empathetic responses", "Better match user emotional state"],
                priority="medium",
                impact_estimate="Better emotional connection with users",
                implementation_complexity="medium",
                timestamp=datetime.now().isoformat()
            ))
        
        # User satisfaction insight
        satisfaction_counts = [len(a.user_satisfaction_indicators) for a in analyses]
        avg_satisfaction = sum(satisfaction_counts) / len(satisfaction_counts)
        if avg_satisfaction < 2.0:
            insights.append(SystemInsight(
                insight_id=f"satisfaction_{int(time.time())}",
                category="user_experience",
                description=f"Average satisfaction indicators per interaction: {avg_satisfaction:.1f}, suggesting low user satisfaction",
                evidence=[f"Only {sum(1 for count in satisfaction_counts if count >= 2)} out of {len(analyses)} interactions showed strong satisfaction"],
                recommended_actions=["Increase engagement", "Provide more helpful responses", "Ask follow-up questions"],
                priority="high",
                impact_estimate="Higher user retention and positive feedback",
                implementation_complexity="low",
                timestamp=datetime.now().isoformat()
            ))
        
        return insights
    
    def _update_learning_patterns(self, analyses: List[InteractionAnalysis]):
        """Update learning patterns based on recent analyses."""
        # Group analyses by pattern signature
        pattern_groups = defaultdict(list)
        
        for analysis in analyses:
            context = analysis.reasoning_data.get("reasoning_summary", {})
            signature = f"{context.get('primary_intent', 'unknown')}_{context.get('dominant_emotion', 'neutral')}"
            pattern_groups[signature].append(analysis)
        
        # Update patterns with sufficient data
        for signature, group_analyses in pattern_groups.items():
            if len(group_analyses) >= self.min_interactions_for_pattern:
                if signature in self.learning_patterns:
                    pattern = self.learning_patterns[signature]
                    
                    # Calculate success rate
                    successful = sum(1 for a in group_analyses 
                                   if a.response_quality_score > 0.7 and a.emotional_appropriateness > 0.7)
                    pattern.success_rate = successful / len(group_analyses)
                    pattern.usage_count += len(group_analyses)
                    pattern.last_updated = datetime.now().isoformat()
                    
                    # Update confidence based on success rate and usage
                    pattern.confidence_score = min(1.0, pattern.success_rate * (1 + pattern.usage_count / 100))
    
    def _calculate_performance_summary(self) -> Dict[str, float]:
        """Calculate performance summary metrics."""
        summary = {}
        
        for metric_name, metric_data in self.performance_metrics.items():
            if metric_data:
                recent_values = [entry["value"] for entry in metric_data[-20:]]  # Last 20 entries
                summary[f"{metric_name}_avg"] = sum(recent_values) / len(recent_values)
                summary[f"{metric_name}_trend"] = self._calculate_trend(recent_values)
        
        return summary
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend direction (-1 to 1, where 1 is improving)."""
        if len(values) < 2:
            return 0.0
        
        # Simple trend calculation
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        return min(1.0, max(-1.0, (second_avg - first_avg) * 2))  # Scale to -1 to 1
    
    def _calculate_satisfaction_trends(self) -> Dict[str, float]:
        """Calculate user satisfaction trends."""
        satisfaction_data = self.performance_metrics.get("user_satisfaction", [])
        
        if not satisfaction_data:
            return {}
        
        recent_values = [entry["value"] for entry in satisfaction_data[-20:]]
        
        return {
            "current_satisfaction": sum(recent_values) / len(recent_values),
            "satisfaction_trend": self._calculate_trend(recent_values),
            "satisfaction_consistency": 1.0 - (max(recent_values) - min(recent_values))  # Lower variance = higher consistency
        }
    
    def _generate_improvement_recommendations(self, insights: List[SystemInsight],
                                            performance_summary: Dict[str, float]) -> List[str]:
        """Generate actionable improvement recommendations."""
        recommendations = []
        
        # From insights
        for insight in insights:
            if insight.priority in ["high", "critical"]:
                recommendations.extend(insight.recommended_actions)
        
        # From performance trends
        for metric_name, trend in performance_summary.items():
            if metric_name.endswith("_trend") and trend < -0.3:  # Declining trend
                base_metric = metric_name.replace("_trend", "")
                if base_metric == "response_quality":
                    recommendations.append("Focus on improving response relevance and completeness")
                elif base_metric == "emotional_appropriateness":
                    recommendations.append("Enhance emotional intelligence and empathy in responses")
                elif base_metric == "user_satisfaction":
                    recommendations.append("Increase user engagement and helpfulness")
        
        # Learning pattern recommendations
        high_confidence_patterns = [p for p in self.learning_patterns.values() if p.confidence_score > 0.8]
        if high_confidence_patterns:
            recommendations.append(f"Apply {len(high_confidence_patterns)} high-confidence learned patterns more consistently")
        
        return list(set(recommendations))  # Remove duplicates
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of learning progress."""
        return {
            "total_interactions_analyzed": len(self.interaction_analyses),
            "learning_patterns_identified": len(self.learning_patterns),
            "high_confidence_patterns": len([p for p in self.learning_patterns.values() if p.confidence_score > 0.8]),
            "system_insights_generated": len(self.system_insights),
            "last_reflection": datetime.fromtimestamp(self.last_reflection).isoformat(),
            "performance_metrics_tracked": list(self.performance_metrics.keys()),
            "average_response_quality": sum(entry["value"] for entry in self.performance_metrics.get("response_quality", [{}])[-10:]) / max(1, len(self.performance_metrics.get("response_quality", [])[-10:])),
            "learning_status": "active" if len(self.interaction_analyses) > 10 else "initializing"
        }
    
    def apply_learned_patterns(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply learned patterns to improve response generation."""
        # Find matching patterns
        intent = context.get("primary_intent")
        emotion = context.get("dominant_emotion")
        complexity = context.get("complexity_level")
        
        pattern_signature = f"{intent}_{emotion}_{complexity}"
        
        if pattern_signature in self.learning_patterns:
            pattern = self.learning_patterns[pattern_signature]
            
            if pattern.confidence_score > self.confidence_threshold:
                # Apply learned approach
                return {
                    "apply_pattern": True,
                    "pattern_id": pattern.pattern_id,
                    "suggested_approach": pattern.successful_approach,
                    "confidence": pattern.confidence_score,
                    "usage_count": pattern.usage_count
                }
        
        # Look for partial matches
        partial_matches = []
        for pattern_id, pattern in self.learning_patterns.items():
            if (pattern.context_triggers.get("intent") == intent or
                pattern.context_triggers.get("emotion") == emotion):
                partial_matches.append((pattern, pattern.confidence_score))
        
        if partial_matches:
            # Use highest confidence partial match
            best_pattern = max(partial_matches, key=lambda x: x[1])[0]
            if best_pattern.confidence_score > 0.6:
                return {
                    "apply_pattern": True,
                    "pattern_id": best_pattern.pattern_id,
                    "suggested_approach": best_pattern.successful_approach,
                    "confidence": best_pattern.confidence_score * 0.8,  # Reduced for partial match
                    "match_type": "partial"
                }
        
        return {"apply_pattern": False}

