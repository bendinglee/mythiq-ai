#!/usr/bin/env python3
"""
🧠 Knowledge Base System - Final Fixed Version
==============================================

Advanced knowledge management system for the Ultimate AI Empire.
Provides sophisticated storage, retrieval, and synthesis of information.

Author: Manus AI
Version: 2.1 (Final Fixed)
"""

import sqlite3
import json
import os
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import re
from collections import defaultdict, Counter
import threading
from dataclasses import dataclass, asdict
from enum import Enum

class KnowledgeType(Enum):
    """Types of knowledge that can be stored."""
    FACT = "fact"
    CONCEPT = "concept"
    PROCEDURE = "procedure"
    EXPERIENCE = "experience"
    PREFERENCE = "preference"
    RELATIONSHIP = "relationship"
    PATTERN = "pattern"

@dataclass
class KnowledgeItem:
    """Represents a single piece of knowledge."""
    id: str
    content: str
    knowledge_type: KnowledgeType
    confidence: float
    source: str
    timestamp: datetime
    tags: List[str]
    metadata: Dict[str, Any]
    relationships: List[str]
    access_count: int = 0
    last_accessed: Optional[datetime] = None

class KnowledgeBase:
    """
    Advanced knowledge management system with sophisticated storage,
    retrieval, and synthesis capabilities.
    """
    
    def __init__(self, db_path: str = "knowledge_base.db"):
        """Initialize the knowledge base."""
        self.db_path = db_path
        self.lock = threading.RLock()
        
        # Configuration - SET BEFORE OTHER INITIALIZATION
        self.max_cache_size = 1000
        self.confidence_threshold = 0.7
        self.relationship_threshold = 0.5
        
        # Create directory only if db_path contains a directory
        db_dir = os.path.dirname(db_path)
        if db_dir:  # Only create directory if dirname is not empty
            os.makedirs(db_dir, exist_ok=True)
        
        self._init_database()
        self._load_cache()
        
    def _init_database(self):
        """Initialize the SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_items (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    knowledge_type TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    source TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    relationships TEXT NOT NULL,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_relationships (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    relationship_type TEXT NOT NULL,
                    strength REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (source_id) REFERENCES knowledge_items (id),
                    FOREIGN KEY (target_id) REFERENCES knowledge_items (id)
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_patterns (
                    id TEXT PRIMARY KEY,
                    pattern_type TEXT NOT NULL,
                    pattern_data TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    last_updated TEXT NOT NULL
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS learning_sessions (
                    id TEXT PRIMARY KEY,
                    session_type TEXT NOT NULL,
                    session_data TEXT NOT NULL,
                    performance_metrics TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Create indexes for better performance
            conn.execute('CREATE INDEX IF NOT EXISTS idx_knowledge_type ON knowledge_items (knowledge_type)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_confidence ON knowledge_items (confidence)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON knowledge_items (timestamp)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_relationships_source ON knowledge_relationships (source_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_relationships_target ON knowledge_relationships (target_id)')
            
            conn.commit()
    
    def _load_cache(self):
        """Load frequently accessed knowledge into memory cache."""
        self.cache = {}
        self.access_frequency = defaultdict(int)
        
        # Load most frequently accessed items
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT * FROM knowledge_items 
                ORDER BY access_count DESC 
                LIMIT ?
            ''', (self.max_cache_size,))
            
            for row in cursor:
                item = self._row_to_knowledge_item(row)
                self.cache[item.id] = item
                self.access_frequency[item.id] = item.access_count
    
    def _row_to_knowledge_item(self, row) -> KnowledgeItem:
        """Convert database row to KnowledgeItem object."""
        return KnowledgeItem(
            id=row[0],
            content=row[1],
            knowledge_type=KnowledgeType(row[2]),
            confidence=row[3],
            source=row[4],
            timestamp=datetime.fromisoformat(row[5]),
            tags=json.loads(row[6]),
            metadata=json.loads(row[7]),
            relationships=json.loads(row[8]),
            access_count=row[9],
            last_accessed=datetime.fromisoformat(row[10]) if row[10] else None
        )
    
    def _knowledge_item_to_row(self, item: KnowledgeItem) -> tuple:
        """Convert KnowledgeItem to database row tuple."""
        return (
            item.id,
            item.content,
            item.knowledge_type.value,
            item.confidence,
            item.source,
            item.timestamp.isoformat(),
            json.dumps(item.tags),
            json.dumps(item.metadata),
            json.dumps(item.relationships),
            item.access_count,
            item.last_accessed.isoformat() if item.last_accessed else None
        )
    
    def add_knowledge(self, content: str, knowledge_type: KnowledgeType, 
                     source: str, confidence: float = 0.8, 
                     tags: List[str] = None, metadata: Dict[str, Any] = None) -> str:
        """Add new knowledge to the base."""
        with self.lock:
            # Generate unique ID
            knowledge_id = hashlib.md5(
                f"{content}{knowledge_type.value}{source}{time.time()}".encode()
            ).hexdigest()
            
            # Create knowledge item
            item = KnowledgeItem(
                id=knowledge_id,
                content=content,
                knowledge_type=knowledge_type,
                confidence=confidence,
                source=source,
                timestamp=datetime.now(),
                tags=tags or [],
                metadata=metadata or {},
                relationships=[],
                access_count=0,
                last_accessed=None
            )
            
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO knowledge_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', self._knowledge_item_to_row(item))
                conn.commit()
            
            # Update cache
            self.cache[knowledge_id] = item
            
            # Find and create relationships
            self._discover_relationships(item)
            
            return knowledge_id
    
    def _discover_relationships(self, new_item: KnowledgeItem):
        """Discover relationships between the new item and existing knowledge."""
        # Simple relationship discovery based on content similarity
        for cached_id, cached_item in self.cache.items():
            if cached_id == new_item.id:
                continue
                
            # Calculate similarity
            similarity = self._calculate_similarity(new_item.content, cached_item.content)
            
            if similarity > self.relationship_threshold:
                self._create_relationship(
                    new_item.id, cached_id, "similar_content", similarity
                )
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings."""
        # Simple word-based similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _create_relationship(self, source_id: str, target_id: str, 
                           relationship_type: str, strength: float):
        """Create a relationship between two knowledge items."""
        relationship_id = hashlib.md5(
            f"{source_id}{target_id}{relationship_type}".encode()
        ).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO knowledge_relationships 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                relationship_id, source_id, target_id, 
                relationship_type, strength, datetime.now().isoformat()
            ))
            conn.commit()
    
    def query_knowledge(self, query: str, limit: int = 10) -> List[KnowledgeItem]:
        """Query knowledge base with natural language."""
        with self.lock:
            # Tokenize query
            query_words = set(query.lower().split())
            
            # Search in cache first
            cache_results = []
            for item in self.cache.values():
                content_words = set(item.content.lower().split())
                tag_words = set(' '.join(item.tags).lower().split())
                
                # Calculate relevance score
                content_overlap = len(query_words.intersection(content_words))
                tag_overlap = len(query_words.intersection(tag_words))
                
                relevance = (content_overlap * 2 + tag_overlap) / len(query_words) if query_words else 0
                
                if relevance > 0:
                    cache_results.append((item, relevance))
            
            # Sort by relevance and confidence
            cache_results.sort(key=lambda x: (x[1], x[0].confidence), reverse=True)
            
            # Get database results if cache is insufficient
            if len(cache_results) < limit:
                db_results = self._query_database(query, limit - len(cache_results))
                cache_results.extend(db_results)
            
            # Update access counts
            results = []
            for item, _ in cache_results[:limit]:
                self._update_access_count(item.id)
                results.append(item)
            
            return results
    
    def _query_database(self, query: str, limit: int) -> List[Tuple[KnowledgeItem, float]]:
        """Query the database for knowledge items."""
        results = []
        query_words = set(query.lower().split())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT * FROM knowledge_items 
                WHERE content LIKE ? OR tags LIKE ?
                ORDER BY confidence DESC
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', limit * 2))  # Get more to filter
            
            for row in cursor:
                item = self._row_to_knowledge_item(row)
                
                # Skip if already in cache
                if item.id in self.cache:
                    continue
                
                # Calculate relevance
                content_words = set(item.content.lower().split())
                tag_words = set(' '.join(item.tags).lower().split())
                
                content_overlap = len(query_words.intersection(content_words))
                tag_overlap = len(query_words.intersection(tag_words))
                
                relevance = (content_overlap * 2 + tag_overlap) / len(query_words) if query_words else 0
                
                if relevance > 0:
                    results.append((item, relevance))
        
        # Sort by relevance and confidence
        results.sort(key=lambda x: (x[1], x[0].confidence), reverse=True)
        return results[:limit]
    
    def _update_access_count(self, knowledge_id: str):
        """Update access count for a knowledge item."""
        if knowledge_id in self.cache:
            self.cache[knowledge_id].access_count += 1
            self.cache[knowledge_id].last_accessed = datetime.now()
            self.access_frequency[knowledge_id] += 1
        
        # Update database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE knowledge_items 
                SET access_count = access_count + 1, 
                    last_accessed = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), knowledge_id))
            conn.commit()
    
    def synthesize_knowledge(self, topic: str) -> Dict[str, Any]:
        """Synthesize knowledge about a specific topic."""
        # Query related knowledge
        related_items = self.query_knowledge(topic, limit=20)
        
        if not related_items:
            return {"topic": topic, "synthesis": "No relevant knowledge found.", "confidence": 0.0}
        
        # Categorize knowledge by type
        categorized = defaultdict(list)
        for item in related_items:
            categorized[item.knowledge_type].append(item)
        
        # Generate synthesis
        synthesis_parts = []
        total_confidence = 0
        
        for knowledge_type, items in categorized.items():
            if not items:
                continue
                
            type_synthesis = self._synthesize_by_type(knowledge_type, items)
            synthesis_parts.append(f"{knowledge_type.value.title()}: {type_synthesis}")
            
            # Calculate weighted confidence
            type_confidence = sum(item.confidence for item in items) / len(items)
            total_confidence += type_confidence * len(items)
        
        overall_confidence = total_confidence / len(related_items) if related_items else 0
        
        return {
            "topic": topic,
            "synthesis": " | ".join(synthesis_parts),
            "confidence": overall_confidence,
            "source_count": len(related_items),
            "categories": [kt.value for kt in categorized.keys()]
        }
    
    def _synthesize_by_type(self, knowledge_type: KnowledgeType, items: List[KnowledgeItem]) -> str:
        """Synthesize knowledge items of a specific type."""
        if knowledge_type == KnowledgeType.FACT:
            # Combine facts with highest confidence first
            facts = sorted(items, key=lambda x: x.confidence, reverse=True)
            return "; ".join(item.content for item in facts[:3])
        
        elif knowledge_type == KnowledgeType.CONCEPT:
            # Merge conceptual understanding
            concepts = [item.content for item in items]
            return f"Conceptual understanding includes: {', '.join(concepts[:3])}"
        
        elif knowledge_type == KnowledgeType.EXPERIENCE:
            # Summarize experiences
            experiences = [item.content for item in items]
            return f"Based on experiences: {'; '.join(experiences[:2])}"
        
        elif knowledge_type == KnowledgeType.PREFERENCE:
            # Aggregate preferences
            preferences = [item.content for item in items]
            return f"Preferences indicate: {', '.join(preferences[:3])}"
        
        else:
            # Generic synthesis
            return f"Related {knowledge_type.value}: {items[0].content if items else 'None'}"
    
    def learn_from_interaction(self, user_input: str, ai_response: str, 
                             feedback: Optional[str] = None, rating: Optional[int] = None):
        """Learn from user interactions to improve knowledge base."""
        # Extract potential knowledge from interaction
        interaction_data = {
            "user_input": user_input,
            "ai_response": ai_response,
            "feedback": feedback,
            "rating": rating,
            "timestamp": datetime.now().isoformat()
        }
        
        # Store learning session
        session_id = hashlib.md5(
            f"{user_input}{ai_response}{time.time()}".encode()
        ).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO learning_sessions VALUES (?, ?, ?, ?, ?)
            ''', (
                session_id,
                "interaction",
                json.dumps(interaction_data),
                json.dumps({"rating": rating} if rating else {}),
                datetime.now().isoformat()
            ))
            conn.commit()
        
        # Extract and store new knowledge if feedback is positive
        if rating and rating >= 4:  # Good interaction
            self._extract_knowledge_from_interaction(user_input, ai_response)
    
    def _extract_knowledge_from_interaction(self, user_input: str, ai_response: str):
        """Extract knowledge from successful interactions."""
        # Simple knowledge extraction
        if "?" in user_input:  # Question-answer pair
            self.add_knowledge(
                content=f"Q: {user_input} A: {ai_response}",
                knowledge_type=KnowledgeType.EXPERIENCE,
                source="user_interaction",
                confidence=0.7,
                tags=["interaction", "qa"]
            )
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        with sqlite3.connect(self.db_path) as conn:
            # Total items
            total_items = conn.execute('SELECT COUNT(*) FROM knowledge_items').fetchone()[0]
            
            # Items by type
            type_counts = {}
            for knowledge_type in KnowledgeType:
                count = conn.execute(
                    'SELECT COUNT(*) FROM knowledge_items WHERE knowledge_type = ?',
                    (knowledge_type.value,)
                ).fetchone()[0]
                type_counts[knowledge_type.value] = count
            
            # Average confidence
            avg_confidence = conn.execute(
                'SELECT AVG(confidence) FROM knowledge_items'
            ).fetchone()[0] or 0
            
            # Most accessed items
            most_accessed = conn.execute('''
                SELECT content, access_count FROM knowledge_items 
                ORDER BY access_count DESC LIMIT 5
            ''').fetchall()
            
            # Recent additions
            recent_count = conn.execute('''
                SELECT COUNT(*) FROM knowledge_items 
                WHERE timestamp > ?
            ''', ((datetime.now() - timedelta(days=7)).isoformat(),)).fetchone()[0]
            
            return {
                "total_items": total_items,
                "items_by_type": type_counts,
                "average_confidence": round(avg_confidence, 3),
                "cache_size": len(self.cache),
                "most_accessed": most_accessed,
                "recent_additions": recent_count
            }
    
    def optimize_knowledge_base(self):
        """Optimize the knowledge base by removing low-quality knowledge."""
        with self.lock:
            # Remove low-confidence, rarely accessed items
            cutoff_date = (datetime.now() - timedelta(days=30)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                # Remove items with low confidence and no recent access
                conn.execute('''
                    DELETE FROM knowledge_items 
                    WHERE confidence < ? AND 
                          (last_accessed IS NULL OR last_accessed < ?) AND
                          access_count < 2
                ''', (self.confidence_threshold - 0.2, cutoff_date))
                
                # Clean up orphaned relationships
                conn.execute('''
                    DELETE FROM knowledge_relationships 
                    WHERE source_id NOT IN (SELECT id FROM knowledge_items) OR
                          target_id NOT IN (SELECT id FROM knowledge_items)
                ''')
                
                conn.commit()
            
            # Refresh cache
            self._load_cache()
    
    def export_knowledge(self, filepath: str):
        """Export knowledge base to JSON file."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT * FROM knowledge_items')
            items = []
            
            for row in cursor:
                item = self._row_to_knowledge_item(row)
                items.append(asdict(item))
            
            # Convert datetime objects to strings for JSON serialization
            for item in items:
                item['timestamp'] = item['timestamp'].isoformat()
                if item['last_accessed']:
                    item['last_accessed'] = item['last_accessed'].isoformat()
                item['knowledge_type'] = item['knowledge_type'].value
        
        with open(filepath, 'w') as f:
            json.dump(items, f, indent=2)
    
    def import_knowledge(self, filepath: str):
        """Import knowledge base from JSON file."""
        with open(filepath, 'r') as f:
            items = json.load(f)
        
        with self.lock:
            for item_data in items:
                # Convert back to proper types
                item_data['timestamp'] = datetime.fromisoformat(item_data['timestamp'])
                if item_data['last_accessed']:
                    item_data['last_accessed'] = datetime.fromisoformat(item_data['last_accessed'])
                item_data['knowledge_type'] = KnowledgeType(item_data['knowledge_type'])
                
                item = KnowledgeItem(**item_data)
                
                # Store in database
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute('''
                        INSERT OR REPLACE INTO knowledge_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', self._knowledge_item_to_row(item))
                    conn.commit()
            
            # Refresh cache
            self._load_cache()

def test_knowledge_base():
    """Test the knowledge base functionality."""
    print("🧠 Testing Knowledge Base System...")
    
    # Initialize knowledge base
    kb = KnowledgeBase("test_knowledge.db")
    
    # Add some test knowledge
    print("\n📝 Adding test knowledge...")
    
    kb.add_knowledge(
        "Python is a high-level programming language",
        KnowledgeType.FACT,
        "programming_manual",
        confidence=0.9,
        tags=["python", "programming", "language"]
    )
    
    kb.add_knowledge(
        "Machine learning involves training algorithms on data",
        KnowledgeType.CONCEPT,
        "ai_textbook",
        confidence=0.85,
        tags=["machine learning", "ai", "algorithms"]
    )
    
    kb.add_knowledge(
        "User prefers detailed explanations over brief answers",
        KnowledgeType.PREFERENCE,
        "user_interaction",
        confidence=0.7,
        tags=["user", "preference", "communication"]
    )
    
    # Query knowledge
    print("\n🔍 Querying knowledge...")
    results = kb.query_knowledge("programming language")
    for item in results:
        print(f"- {item.content} (confidence: {item.confidence})")
    
    # Synthesize knowledge
    print("\n🧩 Synthesizing knowledge about 'programming'...")
    synthesis = kb.synthesize_knowledge("programming")
    print(f"Synthesis: {synthesis['synthesis']}")
    print(f"Confidence: {synthesis['confidence']:.2f}")
    
    # Learn from interaction
    print("\n📚 Learning from interaction...")
    kb.learn_from_interaction(
        "What is Python?",
        "Python is a high-level programming language known for its simplicity and readability.",
        "Very helpful!",
        5
    )
    
    # Get statistics
    print("\n📊 Knowledge Base Statistics:")
    stats = kb.get_knowledge_stats()
    for key, value in stats.items():
        print(f"- {key}: {value}")
    
    print("\n✅ Knowledge Base test completed successfully!")

if __name__ == "__main__":
    test_knowledge_base()

