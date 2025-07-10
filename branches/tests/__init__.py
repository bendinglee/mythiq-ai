# 🧪 Mythiq Test Suite Package Initialization

__version__ = "1.0.0"
__description__ = "Diagnostic validation tools for Mythiq AI modules"
__author__ = "Mythiq Systems"

from .test_runner import run_all_tests
from .test_config import tests
from .test_utils import call_route, validate_response

def run_tests(verbose=True):
    """Run all registered tests with optional verbosity."""
    run_all_tests(verbose=verbose)

# Optional CLI hook if run directly
if __name__ == "__main__":
    print("🔧 Running Mythiq Diagnostic Test Suite...\n")
    run_all_tests()
