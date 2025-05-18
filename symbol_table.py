class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scope_stack = [0]
        self.current_scope = 0

    def enter_scope(self):
        self.current_scope += 1
        self.scope_stack.append(self.current_scope)
        print(f"[Symbol Table] Entering scope {self.current_scope}")

    def exit_scope(self):
        self.scope_stack.pop()
        self.current_scope = self.scope_stack[-1]
        symbols_to_remove = [key for key, value in self.symbols.items() if value['scope'] == self.current_scope]
        for key in symbols_to_remove:
            del self.symbols[key]
        print(f"[Symbol Table] Exiting scope {self.current_scope}")

    def add_symbol(self, name, type, value=None):
        self.symbols[name] = {'type': type, 'scope': self.current_scope, 'value': value}
        print(f"[Symbol Table] Added symbol: {name}, type: {type}, scope: {self.current_scope}")

    def lookup(self, name):
        return self.symbols.get(name)

    def get_symbols(self):
        return [{'name': k, 'type': v['type'], 'scope': v['scope'], 'value': v['value']} for k, v in self.symbols.items()]
