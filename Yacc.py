import ply.yacc as yacc
from Lex import tokens, lexer
errores_sintacticos = []

precedence = (
    ('left', 'PLUS', 'MINUS'),
)

def p_expression(p):
    '''
    expression : expression PLUS term
               | expression MINUS term
               | term
    '''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        else:
            p[0] = p[1] - p[3]
    else:
        p[0] = p[1]

def p_term(p):
    '''
    term : NUMBER
    '''
    p[0] = p[1]

def p_error(p):
    if p:
        line = p.lineno if p else lexer.lineno  # obtiene el número de línea del token actual o del lexer
        errores_sintacticos.append("Error sintáctico en la línea %d: '%s'" % (line, p.value))
    else:
        errores_sintacticos.append("Error sintáctico en EOF")

parser = yacc.yacc()
