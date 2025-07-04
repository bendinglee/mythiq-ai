"""
MYTHIQ.AI Knowledge Branch
Enhanced Knowledge Base and Q&A System

This branch handles all knowledge-related operations including:
- Fact retrieval and question answering
- Context-aware search
- Knowledge base expansion
- Intelligent reasoning

Version: 1.5
Status: Active
"""

from .controller import knowledge_api

__version__ = "1.5"
__status__ = "active"
__capabilities__ = [
    "fact_retrieval",
    "question_answering", 
    "context_search",
    "knowledge_expansion"
]

__all__ = ["knowledge_api"]

