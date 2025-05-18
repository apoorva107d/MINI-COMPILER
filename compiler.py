from lexer import lex_analysis
from myparser import parse
from codegen import CodeGen
from interpreter import TACInterpreter

def compile(code):
    try:
        print("[Compiler] Starting Lexical Analysis")
        tokens = lex_analysis(code)
        print("[Compiler] Lexical Analysis Complete")

        print("[Compiler] Starting Parsing and Analysis")
        ast, symbols, tac_obj = parse(tokens)  # Pass tokens into parser
        print("[Compiler] Parsing and Analysis Complete")

       # print("[Compiler] Optimizing TAC")
       # tac_obj.optimize()

        print("[Compiler] Generating Assembly")
        codegen = CodeGen(tac_obj)
        assembly = codegen.generate()

        print("[Compiler] Executing TAC")
        interpreter = TACInterpreter(tac_obj)
        results = interpreter.execute()

        print("[Compiler] Compilation Complete")
        return {
            "tokens": tokens,
            "ast": ast,
            "symbols": symbols,
            "tac": tac_obj.to_string(),
            "optimized_tac": tac_obj.to_string(),
            "assembly": codegen.to_string(),
            "execution_results": results
        }
    except Exception as e:
        return {"error": str(e)}

# === Example test code ===
if __name__ == "__main__":
    test_code = """
    int x = 5;
    int y = 10;
    if (x < y) {
        x = x + 1;
    }
    while (x < 15) {
        x = x + 2;
    }
    """

    output = compile(test_code)

    if "error" in output:
        print("\n Compilation Error:")
        print(output["error"])
    else:
        print("\n Compilation Results:")
        print("\nTokens:\n", output["tokens"])
        print("\nAST:\n", output["ast"])
        print("\nSymbol Table:\n", output["symbols"])
        print("\nTAC:\n", output["tac"])
        print("\nOptimized TAC:\n", output["optimized_tac"])
        print("\nAssembly:\n", output["assembly"])
        print("\nExecution Results:\n", output["execution_results"])
