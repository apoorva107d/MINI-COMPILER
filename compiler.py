from lexer import lex_analysis
from myparser import parse

def compile(code):
    """Run the full compilation process."""
    try:
        # Lexical Analysis
        print("[Compiler] Starting Lexical Analysis")
        tokens = lex_analysis(code)
        print("[Compiler] Lexical Analysis Complete")

        # Syntax, Semantic Analysis, and TAC Generation
        print("[Compiler] Starting Parsing and Analysis")
        ast, symbols, tac = parse(code)
        print("[Compiler] Compilation Complete")
        return {
            "tokens": tokens,
            "ast": ast,
            "symbols": symbols,
            "tac": tac
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    code = """
    int x = 4;
    int y = 100;
    if (x < y) {
        x = x - 1;
    }
    while (x < 15) {
        x = x + 2;
    }
    """
    result = compile(code)
    print("Tokens:", result.get("tokens", []))
    print("AST:", result.get("ast", []))
    print("Symbol Table:", result.get("symbols", []))
    print("TAC:\n", result.get("tac", ""))
