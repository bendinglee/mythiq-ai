from branches.math_solver.solver import solve_math_query

def test_basic_equation():
    result = solve_math_query("2x + 5 = 13")
    assert result["success"] and "4" in result["result"], f"Unexpected result: {result}"

def test_trig_expression():
    result = solve_math_query("sin(x) = 0.5")
    assert result["success"], "Trig test failed"

def test_bad_input_handling():
    result = solve_math_query("unknownsymbol$")
    assert not result["success"], "Should fail on bad input"

if __name__ == "__main__":
    test_basic_equation()
    test_trig_expression()
    test_bad_input_handling()
    print("✅ All tests passed.")
