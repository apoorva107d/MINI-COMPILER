import ply.yacc as yacc
from lexer import tokens
from symbol_table import SymbolTable
from tac import TAC

class Parser:
    tokens = tokens  # Explicitly set tokens for PLY

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.tac = TAC()
        self.parser = None
        self.ast = []

    def p_program(self, p):
        '''program : statement_list'''
        p[0] = p[1]
        self.ast = p[1]
        print("[Parser] Parsed program")

    def p_statement_list(self, p):
        '''statement_list : statement
                          | statement_list statement'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
        print("[Parser] Parsed statement list")

    def p_statement(self, p):
        '''statement : declaration
                     | assignment
                     | if_statement
                     | while_statement'''
        p[0] = p[1]
        print("[Parser] Parsed statement")

    def p_declaration(self, p):
        '''declaration : INT ID EQUALS NUMBER SEMICOLON'''
        name, value = p[2], p[4]
        self.symbol_table.add_symbol(name, 'int', value)
        self.tac.emit('=', value, None, name)
        p[0] = ['decl', 'int', name, value]
        print("[Parser] Parsed declaration")

    def p_assignment(self, p):
        '''assignment : ID EQUALS expression SEMICOLON'''
        name, expr = p[1], p[3]
        if not self.symbol_table.lookup(name):
            raise Exception(f"[Semantic Error] Variable {name} not declared")
        if len(expr) == 1:
            self.tac.emit('=', expr[0], None, name)
        else:
            self.tac.emit(expr[0], expr[1], expr[2], expr[3])  # e.g., t3 = x + 2
            self.tac.emit('=', expr[3], None, name)  # e.g., x = t3
        p[0] = ['assign', name, expr]
        print("[Parser] Parsed assignment")

    def p_if_statement(self, p):
        '''if_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE'''
        expr, stmts = p[3], p[6]
        label_true = self.tac.new_label()
        label_end = self.tac.new_label()
        if len(expr) > 1:
            self.tac.emit(expr[0], expr[1], expr[2], expr[3])  # e.g., t0 = x < y
        self.tac.emit('if', f"{expr[-1]} != 0 goto {label_true}")
        self.tac.emit('goto', label_end)
        self.tac.emit('label', label_true)
        for stmt in stmts:
            if stmt[0] == 'assign':
                if len(stmt[2]) == 1:
                    self.tac.emit('=', stmt[2][0], None, stmt[1])
                else:
                    self.tac.emit(stmt[2][0], stmt[2][1], stmt[2][2], stmt[2][3])
                    self.tac.emit('=', stmt[2][3], None, stmt[1])
        self.tac.emit('label', label_end)
        p[0] = ['if', expr, stmts]
        print("[Parser] Parsed if statement")

    def p_while_statement(self, p):
        '''while_statement : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE'''
        expr, stmts = p[3], p[6]
        label_start = self.tac.new_label()
        label_body = self.tac.new_label()
        label_end = self.tac.new_label()
        self.tac.emit('label', label_start)
        if len(expr) > 1:
            self.tac.emit(expr[0], expr[1], expr[2], expr[3])  # e.g., t2 = x < 15
        self.tac.emit('if', f"{expr[-1]} != 0 goto {label_body}")
        self.tac.emit('goto', label_end)
        self.tac.emit('label', label_body)
        for stmt in stmts:
            if stmt[0] == 'assign':
                if len(stmt[2]) == 1:
                    self.tac.emit('=', stmt[2][0], None, stmt[1])
                else:
                    self.tac.emit(stmt[2][0], stmt[2][1], stmt[2][2], stmt[2][3])  # e.g., t3 = x + 2
                    self.tac.emit('=', stmt[2][3], None, stmt[1])  # e.g., x = t3
        self.tac.emit('goto', label_start)
        self.tac.emit('label', label_end)
        p[0] = ['while', expr, stmts]
        print("[Parser] Parsed while statement")

    def p_expression(self, p):
        '''expression : ID
                      | NUMBER
                      | expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression
                      | expression LESS expression
                      | expression GREATER expression'''
        if len(p) == 2:
            p[0] = [p[1]]
            print("[Parser] Parsed expression (single)")
        else:
            op = {'+': '+', '-': '-', '*': '*', '/': '/', '<': '<', '>': '>'}[p[2]]
            temp = self.tac.new_temp()
            p[0] = [op, p[1][-1], p[3][-1], temp]
            print("[Parser] Parsed expression (binary)")

    def p_error(self, p):
        if p:
            raise Exception(f"[Syntax Error] at token {p.type}")
        else:
            raise Exception("[Syntax Error] at EOF")

    def parse(self, token_list):
        if not self.parser:
            self.parser = yacc.yacc(module=self)
        self.ast = []
        self.symbol_table = SymbolTable()
        self.tac = TAC()

        # Convert token_list to PLY-compatible tokens
        from lexer import lexer
        lexer.input("")  # Initialize lexer state
        token_objects = []
        for tok_type, tok_value in token_list:
            tok = lexer.token()  # Create a dummy token to get structure
            if not tok:
                tok = type('LexToken', (), {})()
            tok.type = tok_type
            tok.value = tok_value
            token_objects.append(tok)

        # Mock lexer to feed tokens to yacc
        class MockLexer:
            def __init__(self, tokens):
                self.tokens = tokens
                self.index = 0

            def token(self):
                if self.index < len(self.tokens):
                    tok = self.tokens[self.index]
                    self.index += 1
                    return tok
                return None

        mock_lexer = MockLexer(token_objects)
        self.parser.parse(lexer=mock_lexer)
        return self.ast, self.symbol_table.get_symbols(), self.tac

def parse(token_list):
    parser = Parser()
    return parser.parse(token_list)
