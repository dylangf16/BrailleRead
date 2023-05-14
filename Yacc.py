import ply.yacc as yacc
from Lex import tokens

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
        print("Error sintáctico en '%s'" % p.value)
    else:
        print("Error sintáctico en EOF")

parser = yacc.yacc()
