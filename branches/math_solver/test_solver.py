from branches.math_solver.solver import solve_math_query

def run_tests():
    tests = {
        "2x + 5 = 13": "x = 4",
        "x^2 - 4 = 0": "x = ±2",
        "sin(x) = 0.5": "x ≈ 30° or x ≈ π/6",
        "unknownsymbol$": None
    }

    for query, expected in tests.items():
        result = solve_math_query(query)
        if expected:
            assert result["success"] and expected.lower() in result["result"].lower(), f"Test failed for: {query}"
        else:
            assert not result["success"], f"Unexpected success for: {query}"

    print("✅ All math solver tests passed.")

if __name__ == "__main__":
    run_tests()
