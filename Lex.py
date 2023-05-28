import ply.lex as lex

lexical_errors = []


# List of token names
tokens = ['ID', 'SEMICOLON', 'INTEGER', 'BOOL', 'MAQ', 'MEQ', 'EQUAL', 'DIFFERENT', 'MEQEQUAL', 'MAQEQUAL', 'ARROBA',
          'COMA', 'LPARENT', 'RPARENT', 'ADD', 'SUB', 'MUL', 'DIV', 'COMMENT', 'TYPE'
          ]

reserved = [
    'PROC',
    'NEW',
    'VALUES',
    'ALTER',
    'ALTERB',
    'SIGNAL',
    'VIEWSIGNAL',
    'ISTRUE',
    'REPEAT',
    'UNTIL',
    'WHILE',
    'CASE',
    'WHEN',
    'THEN',
    'ELSE',
    'PRINTVALUES',
    'CALL',
    'MASTER'
]

tokens = tokens + reserved

t_ignore = r'[ \t]|\n'
t_MAQ = r'>'
t_MEQ = r'<'
t_EQUAL = r'=='
t_DIFFERENT = r'<>'
t_MEQEQUAL = r'<='
t_MAQEQUAL = r'>='
t_ARROBA = r'@'
t_COMA = r','
t_SEMICOLON = r';'
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_ADD = r'ADD'
t_SUB = r'SUB'
t_MUL = r'MUL'
t_DIV = r'DIV'

t_PROC = r'Proc'
t_NEW = r'New'
t_VALUES = r'Values'
t_ALTER = r'Alter'
t_ALTERB = r'AlterB'
t_SIGNAL = r'Signal'
t_VIEWSIGNAL = r'ViewSignal'
t_ISTRUE = r'IsTrue'
t_REPEAT = r'Repeat'
t_UNTIL = r'Until'
t_WHILE = r'While'
t_CASE = r'Case'
t_WHEN = r'When'
t_THEN = r'Then'
t_ELSE = r'Else'
t_PRINTVALUES = r'PrintValues'
t_CALL = r'CALL'

def t_MASTER(t):
    r'[@][Master]+'
    return t

def t_ID(t):
    r'[@][a-zA-Z0-9_#]+'
    if t.value.upper() in reserved:
        t.value = t.value.upper()
        t.type = t.value
    return t


def t_TYPE(t):
    r'(Num|Bool)'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'//.*'
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'(True|False)'
    if t.value == "True":
        t.value = True
    elif t.value == "False":
        t.value = False
    return t


# Error handling rule
def t_error(t):
    lexical_errors.append(f"Invalid token at line {t.lexer.lineno}: {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()

# Test input code
input_code = '''
// Sample code to test lexical analysis and parsing
// Procedure definitions
@Master
(
    @variable1,
    (Num, 5);
);
Proc @Procedure1
(
    @variable1,
    (Num, 5);
    @variable2,
    (Bool, True);
);

// Variable definition outside of any procedure
New @variable3,
(Num, 10);

// Invalid procedure definition
Proc @Procedure1
(
    @variable3,
    (Num, 15);
);
// Invalid variable definition
New @variable4,
(Num, 20);

// Invalid syntax
Proc Procedure3
(
    CALL(@Procedure1);
    CALL(@Procedure2);
    
    Else
);

// Invalid token
@var5 = 25;

Proc @Procedure4
(
    @variable4,
    (Num, 30)
);
'''

# Run the lexer
lexer.input(input_code)
# Print the tokens
for token in lexer:
    print(token)
# Print the lexical errors
if lexical_errors:
    print("\nLexical errors:")
    for error in lexical_errors:
        print(error)
