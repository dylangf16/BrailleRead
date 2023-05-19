import ply.lex as lex

lexical_errors = []

# List of token names
tokens = [
    'PROC',
    'NEW',
    'CALL',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'COMMA',
    'NUM',
    'BOOL',
    'COMPARISON_OP',
    'OPERATOR',
    'ID',
    'MASTER'
]

# Regular expression rules for tokens
t_ID = r'[a-zA-Z0-9_@-]+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','
t_PROC ='Proc'

# Ignored characters
t_ignore = '(\t | \n)'


def t_NEW(t):
    r'New'
    return t

def t_CALL(t):
    r'CALL'
    return t


def t_NUM(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'(True|False)'
    if t.value == "True":
        t.value=True
    elif t.value == "False":
        t.value=False
    return t

# Regular expression rule for comments
def t_COMMENT(t):
    r'//.*'
    pass  # Ignore comments

# Rule for operators
def t_OPERATOR(t):
    r'[+\-*/=](?!=)'
    return t

# Rule for comparison operators
def t_COMPARISON_OP(t):
    r'==|!='
    return t

# Error handling rule
def t_error(t):
    lexical_errors.append(f"Invalid token: {t.value[0]}")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

