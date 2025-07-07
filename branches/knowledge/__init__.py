# branches/knowledge/__init__.py
# 🧮 KNOWLEDGE BRANCH INITIALIZATION

"""
MYTHIQ AI Knowledge Branch
Provides mathematical computation and general knowledge capabilities
"""

from .controller import knowledge_api

__version__ = "1.0.0"
__author__ = "MYTHIQ AI Team"

# Branch information
BRANCH_NAME = "Knowledge"
BRANCH_VERSION = "1.0.0"
BRANCH_DESCRIPTION = "Mathematical computation and general knowledge processing"

# Export the blueprint
__all__ = ['knowledge_api']
