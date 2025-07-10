def reason_symbols(statement):
    if "if" in statement and "then" in statement:
        return "Valid implication detected."
    elif "forall" in statement:
        return "Universal quantifier used."
    else:
        return "Symbolic reasoning complete."
