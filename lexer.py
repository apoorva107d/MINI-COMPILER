import ply.lex as lex

tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'ID', 'EQUALS', 'SEMICOLON', 'LBRACE', 'RBRACE', 'LESS', 'GREATER',
    'IF', 'WHILE', 'INT'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LESS = r'<'
t_GREATER = r'>'

reserved = {
    'if': 'IF',
    'while': 'WHILE',
    'int': 'INT'
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
    print(f"[Lexical Error] Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def lex_analysis(code):
    lexer.input(code)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append([tok.type, tok.value])
    return tokens
