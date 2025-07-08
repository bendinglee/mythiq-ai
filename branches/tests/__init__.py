# 🧪 Mythiq Test Suite Package

from .test_runner import run_all_tests
from .test_config import tests
from .test_utils import call_route, validate_response

# Optional CLI hook if run directly
if __name__ == "__main__":
    print("🔧 Running Mythiq Diagnostic Test Suite...\n")
    run_all_tests()
