import ply.lex as lex
import ply.yacc as yacc

# Lex ---------------------
lexical_errors = []

# Lista de nombres de tokens
tokens = ['MASTER', 'ID', 'SEMICOLON', 'INTEGER', 'BOOL', 'MAQ', 'MEQ', 'EQUAL', 'DIFFERENT', 'MEQEQUAL', 'MAQEQUAL',
          'ARROBA',
          'COMA', 'LPARENT', 'RPARENT', 'ADD', 'SUB', 'MUL', 'DIV', 'COMMENT', 'TYPE', 'STRING', 'PLUS'
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
    'BREAK',
    'CUT',
    'RECUT',
    'SLEEP'
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
t_PLUS = r'\+'

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
t_BREAK = r'Break'
t_CUT = 'Cut'
t_RECUT = 'ReCut'
t_SLEEP = 'Sleep'

#Token reservado para la funcion master
def t_MASTER(t):
    r'@Master'
    return t

# Tokens id
# Cualquier combinacion de caracteres que inicien con @
def t_ID(t):
    r'[@][a-zA-Z0-9_#]+'
    if t.value.upper() in reserved:
        t.value = t.value.upper()
        t.type = t.value
    return t

# Token de string
# Cualquier combinacion de caracteres que se encuentren entre " "
def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

# Token de tipo de variables
# Puede ser token Num, Bool y String
def t_TYPE(t):
    r'(Num|Bool|Str)'
    return t

# Token para reconocer new line
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Token de comentarios
# Siempre que la linea empiece con //
def t_COMMENT(t):
    r'//.*'
    pass

# Token para integers
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Token para bools
def t_BOOL(t):
    r'(True|False)'
    if t.value == "True":
        t.value = True
    elif t.value == "False":
        t.value = False
    return t


# Token para administrar errores lexicos
def t_error(t):
    lexical_errors.append(f"Invalid token at line {t.lexer.lineno}: {t.value[0]}")
    t.lexer.skip(1)



lexer = lex.lex()

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
'''


