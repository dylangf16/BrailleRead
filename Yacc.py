import ply.yacc as yacc
from Lex import tokens, lexer, lexical_errors

# Dictionary of names
procs = []
variables_locales = {}
variables_globales = {}
syntax_errors = []
master = 0

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
)

def p_master(p):
    global master
    '''p_master : MASTER LPARENT sentence RPARENT SEMICOLON'''
    # Acción semántica: Realizar las acciones correspondientes al análisis sintáctico de @Master
    print("pasó proc_master")
    master += 1
    if master != 1:
        syntax_errors.append(f'Debe existir solamente un @Master, hay otra declaración en la línea: {p.lineno}')
    p[0] = ('master', p[3])


def p_procedure_list(p):
    '''procedure_list : procedure
                      | procedure_list procedure'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_procedure(p):
    '''procedure : PROC ID LPARENT sentence RPARENT SEMICOLON'''
    # Acción semántica: Realizar las acciones correspondientes al análisis sintáctico
    # de un procedimiento
    if p[2] not in procs:
        procs.append(p[2])
        print(str(p[2]) + " agregado a la lista de procs")

    p[0] = ('procedure', p[2], p[4])


# Estructura en el diccionario de variables = ID [tipo, valor]
def p_sentence1(p):
    '''sentence : NEW ID LPARENT TYPE COMA INTEGER RPARENT SEMICOLON
                | NEW ID LPARENT TYPE COMA BOOL RPARENT SEMICOLON'''
    if len(p[2]) > 2 and len(p[2]) < 12:
        if p[4] == 'Num' and isinstance(p[6], int):
            variables_locales[p[2]] = [p[4], p[6]]
        elif p[4] == 'Bool' and isinstance(p[6], bool):
            variables_locales[p[2]] = [p[4], p[6]]
        else:
            syntax_errors.append(f'Error en línea: {p.lineno}, valor dado no corresponde al tipado seleccionado')
    else:
        syntax_errors.append(f'Error en línea: {p.lineno}, tamaño de nombre de variable no cumple con el estándar')


def p_sentence2(p):
    '''sentence : VALUES LPARENT ID COMA INTEGER RPARENT SEMICOLON
                | VALUES LPARENT ID COMA BOOL RPARENT SEMICOLON'''

    if p[3] in variables_locales or p[3] in variables_globales:
        if type(p[5]) == type(variables_locales[p[3]][1]):
            variables_locales[p[3]][1] = p[5]
        else:
            syntax_errors.append(f'Error en línea: {p.lineno}, tipo de valor a cambiar no coincide con tipo de valor ya en variable')
    else:
        syntax_errors.append(f'Error en línea: {p.lineno}, variable no existente')


def p_sentence3(p):
    '''sentence : CALL LPARENT ID RPARENT SEMICOLON'''

    if p[3] in procs:
        # Aquí puedes llamar a la función correspondiente
        # Por ejemplo, si las funciones están definidas como funciones normales de Python:
        return procs[p[3]]()


def p_sentence4(p):
    '''sentence : PRINTVALUES RPARENT STRING RPARENT'''
    print(p[3])


# Error handling rule
def p_error(p):
    if p:
        syntax_errors.append(f'Syntax error at line {p.lineno}: Unexpected token {p.value}')
    else:
        syntax_errors.append('Syntax error: Unexpected end of input')


# Build the parser
parser = yacc.yacc()

código_prueba = '''
// Procedure definitions

Proc @Procedure1 (

    Values(@variable1, 456789);
    PrintValues(@variable1);

);

@Master(
    New @variable1,(Num, 15);
    PrintValues(@variable1);
    CALL (@Procedure1);
);
'''

print("Ejecutando análisis")
lexer.input(código_prueba)
for token in lexer:
    print(token)
# Print the lexical errors
if lexical_errors:
    print("\nLexical errors:")
    for error in lexical_errors:
        print(error)

result = parser.parse(código_prueba, lexer=lexer)
# Print the syntax errors
if syntax_errors:
    print("Syntax errors:")
    for error in syntax_errors:
        print(error)
else:
    print(result)
