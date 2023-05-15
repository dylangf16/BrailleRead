import ply.lex as lex
errores_lexicos = []
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
)

t_PLUS = r'\+'
t_MINUS = r'-'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    errores_lexicos.append("Error léxico en la línea %d: Carácter ilegal '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)

def get_line_number(t):
    return t.lexer.lexdata[:t.lexpos].count('\n') + 1

lexer = lex.lex()
