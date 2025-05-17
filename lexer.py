import ply.lex as lex

# Token definitions
tokens = (
    'INT', 'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE', 'SEMI', 'EQ', 'LT', 'GT', 'IF', 'WHILE'
)

# Regular expressions for tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_EQ = r'='
t_LT = r'<'
t_GT = r'>'

# Reserved keywords
reserved = {
    'int': 'INT',
    'if': 'IF',
    'while': 'WHILE'
}

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"[Lexical Analysis] Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Create lexer
lexer = lex.lex()

def lex_analysis(code):
    """Perform lexical analysis and return tokens."""
    lexer.input(code)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value))
        print(f"[Lexical Analysis] Token: {tok.type} ({tok.value})")
    return tokens
