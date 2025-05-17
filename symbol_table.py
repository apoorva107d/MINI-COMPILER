class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scope = 0

    def add(self, name, type_, scope):
        """Add a variable to the symbol table."""
        if (name, scope) in self.symbols:
            raise Exception(f"Error: Variable {name} already declared in scope {scope}")
        self.symbols[(name, scope)] = {"type": type_, "scope": scope}
        print(f"[Semantic Analysis] Added variable '{name}' with type '{type_}' in scope {scope}")
        return {"name": name, "type": type_, "scope": scope}

    def lookup(self, name, scope):
        """Look up a variable in current or parent scopes."""
        for s in range(scope, -1, -1):
            if (name, s) in self.symbols:
                print(f"[Semantic Analysis] Found variable '{name}' in scope {s}")
                return self.symbols[(name, s)]
        raise Exception(f"Error: Variable {name} not declared")

    def enter_scope(self):
        """Enter a new scope."""
        self.scope += 1
        print(f"[Semantic Analysis] Entered new scope: {self.scope}")
        return self.scope

    def exit_scope(self):
        """Exit the current scope and remove its variables."""
        keys_to_remove = [k for k in self.symbols if k[1] == self.scope]
        for k in keys_to_remove:
            print(f"[Semantic Analysis] Removed variable '{k[0]}' from scope {k[1]}")
            del self.symbols[k]
        self.scope -= 1
        print(f"[Semantic Analysis] Exited scope, current scope: {self.scope}")
        return self.scope

    def get_symbols(self):
        """Return current symbol table state."""
        return [{"name": k[0], "type": v["type"], "scope": v["scope"]} for k, v in self.symbols.items()]
