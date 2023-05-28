import ply.yacc as yacc
from Lex import tokens

# dictionary of names
procs = []
variables_locales = {}
variables_globales = {}
syntax_errors = []
master = 0

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
)


def p_program(p):
    global master
    '''program : proc_master proc_list'''
    # Acción semántica: Realizar las acciones correspondientes al análisis sintáctico del programa completo
    if master != 1:
        syntax_errors.append(f'Debe existir solamente un @Master, hay otra declaración en la línea: {p.lineno}')


def p_proc_master(p):
    global master
    '''proc_master : MASTER LPARENT sentence RPARENT SEMICOLON'''
    # Acción semántica: Realizar las acciones correspondientes al análisis sintáctico de @Master
    master += 1
    if master != 1:
        syntax_errors.append(f'Debe existir solamente un @Master, hay otra declaración en la línea: {p.lineno}')


def p_proc_list(p):
    '''proc_list : proc
                 | proc_list proc'''
    # Acción semántica: Realizar las acciones correspondientes al análisis sintáctico de la lista de procedimientos


def p_proc(p):
    '''proc : PROC ID LPARENT sentence RPARENT SEMICOLON'''
    # Acción semántica: Realizar las acciones correspondientes al análisis sintáctico
    # de un procedimiento


# Estructura en el diccionario de variables= ID [tipo,valor]
def p_sentence1(p):
    '''sentence : NEW ID LPARENT TYPE COMA INTEGER RPARENT SEMICOLON
                | NEW ID LPARENT TYPE COMA BOOL RPARENT SEMICOLON'''
    if len(p[2]) > 2 and len(p[2]) < 12:
        if p[4] == 'Num' and isinstance(p[6], int):
            variables_locales[p[2]] = [p[4], p[6]]
        if p[4] == 'Bool' and isinstance(p[6], bool):
            variables_locales[p[2]] = [p[4], p[6]]
        else:
            syntax_errors.append(f'Error en línea: {p.lineno}, valor dado no corresponde al tipado seleccionado')
    else:
        syntax_errors.append(f'Error en línea: {p.lineno}, tamaño de nombre de variable no cumple con estándar')


def p_sentence2(p):
    '''sentence : VALUES LPARENT ID COMA INTEGER RPARENT SEMICOLON
                | VALUES LPARENT ID COMA BOOL RPARENT SEMICOLON'''

    if p[3] in variables_locales or p[3] in variables_globales:
        if type(p[5]) == type(variables_locales[p[3][1]]):
            variables_locales[p[3][1]] = p[5]
        else:
            syntax_errors.append(f'Error en línea: {p.lineno}, tipo de valor a cambiar no coincide con tipo de valor ya en variable')
    else:
        syntax_errors.append(f'Error en línea: {p.lineno}, variable no existente')


# Error handling rule
def p_error(p):
    if p:
        syntax_errors.append(f'Syntax error at line {p.lineno}: Unexpected token {p.value}')
    else:
        syntax_errors.append('Syntax error: Unexpected end of input')


# Build the parser
parser = yacc.yacc()


input_code = '''
@Master(
New @variable1,(Num,5);
CALL(pro1)
);

Proc pro1(
Values(@variable1, 89)
);
'''

result = parser.parse(input_code)

# Print the syntax errors
if syntax_errors:
    print("Syntax errors:")
    for error in syntax_errors:
        print(error)
else:
    print(result)