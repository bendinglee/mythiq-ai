from .router import math_solver_route

BRANCH_NAME = "Math Solver"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"➗ Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return True

__all__ = ["math_solver_route", "initialize_branch"]
