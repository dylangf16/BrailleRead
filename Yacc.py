import ply.yacc as yacc
import ply.lex as lex
import sys

#Lex ---------------------
lexical_errors = []

# List of token names
tokens = ['MASTER','ID', 'SEMICOLON', 'INTEGER', 'BOOL', 'MAQ', 'MEQ', 'EQUAL', 'DIFFERENT', 'MEQEQUAL', 'MAQEQUAL', 'ARROBA',
          'COMA', 'LPARENT', 'RPARENT', 'ADD', 'SUB', 'MUL', 'DIV', 'COMMENT', 'TYPE', 'STRING'
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
    'BREAK'
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
t_BREAK = r'break'

def t_MASTER(t):
    r'@Master'
    return t

def t_ID(t):
    r'[@][a-zA-Z0-9_#]+'
    if t.value.upper() in reserved:
        t.value = t.value.upper()
        t.type = t.value
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t


def t_TYPE(t):
    r'(Num|Bool)'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMMENT(t):
    r'//.*'
    pass


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

# Dictionary of names
procs = []
variables_locales = {}
variables_globales = {}
syntax_errors = []
master = 0
proc_en_analisis = ''

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
)

def p_master(p):
    '''master : MASTER LPARENT master_sentences RPARENT SEMICOLON
                | empty'''
    # Acción semántica: Realizar las acciones correspondientes al análisis sintáctico de @Master
    print("pasó proc_master")
    global master
    master += 1
    if master != 1:
        syntax_errors.append(f'Debe existir solamente un @Master, hay otra declaración en la línea: {p.lineno}')
    p[0] = ('master', p[3])


# Esto es para lidiar con las variables globales
def p_master_sentences(p):
    '''master_sentences : master_sentence
                        | master_sentences master_sentence'''

def p_master_sentence(p):
    '''master_sentence : master_var'''

def p_master_var(p):
    '''master_var : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON
                    | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON'''
    if len(p[2]) > 2 and len(p[2]) < 12:
        if p[5] == 'Num' and isinstance(p[7], int):
            variables_globales[p[2]] = [p[5], p[7]]
        elif p[5] == 'Bool' and isinstance(p[7], bool):
            variables_globales[p[2]] = [p[5], p[7]]
        else:
            syntax_errors.append(
                f'Error en línea {p.lineno}, posición {p.lexpos}, valor dado no corresponde al tipado seleccionado')
    else:
        syntax_errors.append(
            f'Error en línea {p.lineno}, posición {p.lexpos}, tamaño de nombre de variable no cumple con el estándar')

def p_procedure(p):
    '''procedure : PROC ID LPARENT sentences RPARENT SEMICOLON'''
    # Acción semántica: Realizar las acciones correspondientes al análisis sintáctico
    # de un procedimiento
    if p[2] not in procs:
        procs.append(p[2])
        print(str(p[2]) + " agregado a la lista de procs")
    print("Función analizando: " + p[2])
    print("Sentencias detectadas: ")
    for rule in p[4]:
        print(rule)

    p[0] = ('procedure', p[2], p[4])


# Recursividad para agarrar todas las sentencias
def p_sentences(p):
    '''sentences : sentence
                 | sentences sentence'''


# Aquí se van agregando todas las sentencias, así como vamos
# TODO toda sentence que se agregue aquí, se tiene que agregar a master_sentence
def p_sentence(p):
    '''sentence : sentence1
                | sentence2
                | sentence3
                | sentence4
                | sentence5
                | sentence6
                | sentence7
                | sentence8
                | sentence9
                | sentence10
                | sentence11
                | sentence12
                | sentence13
                | sentence14
                | sentence15 '''
    p[0] = p[1]


# Estructura en el diccionario de variables = ID [nombreProc, tipo, valor]
def p_sentence1(p):
    '''sentence1 : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON
                | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON'''
    if len(p[2]) > 2 and len(p[2]) < 12:
        if p[5] == 'Num' and isinstance(p[7], int):
            variables_locales[p[2]] = [proc_en_analisis, [5], p[7]]
        elif p[5] == 'Bool' and isinstance(p[7], bool):
            variables_locales[p[2]] = [proc_en_analisis, [5], p[7]]
        else:
            syntax_errors.append(
                f'Error en línea {p.lineno}, posición {p.lexpos}, valor dado no corresponde al tipado seleccionado')
    else:
        syntax_errors.append(
            f'Error en línea {p.lineno}, posición {p.lexpos}, tamaño de nombre de variable no cumple con el estándar')


def p_sentence2(p):
    '''sentence2 : VALUES LPARENT ID COMA INTEGER RPARENT SEMICOLON
                 | VALUES LPARENT ID COMA BOOL RPARENT SEMICOLON'''
    if p[3] in variables_locales:
        if isinstance(p[5], int) and variables_locales[p[3]][0] == 'Num':
            variables_locales[p[3]][1] = p[5]
        elif isinstance(p[5], bool) and variables_locales[p[3]][0] == 'Bool':
            variables_locales[p[3]][1] = p[5]
        else:
            syntax_errors.append(
                f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[3]}')
    elif p[3] in variables_globales:
        if isinstance(p[5], int) and variables_globales[p[3]][0] == 'Num':
            variables_globales[p[3]][1] = p[5]
        elif isinstance(p[5], bool) and variables_globales[p[3]][0] == 'Bool':
            variables_globales[p[3]][1] = p[5]
        else:
            syntax_errors.append(
                f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[3]}')
    else:
        syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def p_sentence3(p):
    '''sentence3 : CALL LPARENT ID RPARENT SEMICOLON'''

    if p[3] in procs:
        # Aquí puedes llamar a la función correspondiente
        # Por ejemplo, si las funciones están definidas como funciones normales de Python:
        return procs[p[3]]()


def p_sentence4(p):
    '''sentence4 : PRINTVALUES RPARENT STRING RPARENT'''
    print(p[3])


# Estructura en el diccionario de variables = ID [nombreProc, tipo, valor]
def p_sentence5(p):
    '''sentence5 : ALTER LPARENT ID COMA ADD COMA INTEGER RPARENT SEMICOLON
                | ALTER LPARENT ID COMA SUB COMA INTEGER RPARENT SEMICOLON
                | ALTER LPARENT ID COMA MUL COMA INTEGER RPARENT SEMICOLON
                | ALTER LPARENT ID COMA DIV COMA INTEGER RPARENT SEMICOLON'''

    if p[5] == "ADD":
        if p[3] in variables_globales:
            valor_actual = variables_globales[p[3]]
            nuevo_valor = (valor_actual[0], valor_actual[1] + p[7])
            variables_globales[p[3]] = nuevo_valor
            for clave, (dato1, dato2, dato3) in variables_locales.items():
                if clave == p[3]:
                    if dato1 == proc_en_analisis:
                        valor_actual = variables_locales[p[2]]
                        nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] + p[7])
                        variables_locales[p[3]] = nuevo_valor
                    else:
                        syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                else:
                    syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')
    if p[5] == "SUB":
        if p[3] in variables_globales:
            valor_actual = variables_globales[p[3]]
            nuevo_valor = (valor_actual[0], valor_actual[1] - p[7])
            variables_globales[p[3]] = nuevo_valor
            for clave, (dato1, dato2, dato3) in variables_locales.items():
                if clave == p[3]:
                    if dato1 == proc_en_analisis:
                        valor_actual = variables_locales[p[2]]
                        nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] - p[7])
                        variables_locales[p[3]] = nuevo_valor
                    else:
                        syntax_errors.append(
                            f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                else:
                    syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')
    if p[5] == "MUL":
        if p[3] in variables_globales:
            valor_actual = variables_globales[p[3]]
            nuevo_valor = (valor_actual[0], valor_actual[1] * p[7])
            variables_globales[p[3]] = nuevo_valor
        for clave, (dato1, dato2, dato3) in variables_locales.items():
            if clave == p[3]:
                if dato1 == proc_en_analisis:
                    valor_actual = variables_locales[p[2]]
                    nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] * p[7])
                    variables_locales[p[3]] = nuevo_valor
                else:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')
    if p[5] == "DIV":
        if p[3] in variables_globales:
            valor_actual = variables_globales[p[3]]
            nuevo_valor = (valor_actual[0], valor_actual[1] / p[7])
            variables_globales[p[3]] = nuevo_valor
        for clave, (dato1, dato2, dato3) in variables_locales.items():
            if clave == p[3]:
                if dato1 == proc_en_analisis:
                    valor_actual = variables_locales[p[2]]
                    nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] / p[7])
                    variables_locales[p[3]] = nuevo_valor
                else:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')
    else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

def p_sentence6(p):
    '''sentence6 : ALTERB LPARENT ID COMA ADD COMA INTEGER RPARENT SEMICOLON'''
    for clave, (dato1, dato2) in variables_globales.items():
        if clave == p[3]:
            valor_actual = variables_globales[p[3]]
            if dato2 == True:
                nuevo_valor = (valor_actual[0], False)
                variables_globales[p[3]] = nuevo_valor
            else:
                nuevo_valor = (valor_actual[0], True)
                variables_globales[p[3]] = nuevo_valor

    for clave, (dato1, dato2, dato3) in variables_locales.items():
        if clave == p[3]:
            if dato1 == proc_en_analisis:
                if dato3 == True:
                    valor_actual = variables_locales[p[2]]
                    nuevo_valor = (valor_actual[0], valor_actual[1], False)
                    variables_locales[p[3]] = nuevo_valor
                else:
                    valor_actual = variables_locales[p[2]]
                    nuevo_valor = (valor_actual[0], valor_actual[1], True)
                    variables_locales[p[3]] = nuevo_valor
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

def p_sentence7(p):
    '''sentence7 : ID MAQ INTEGER'''
    for clave, (dato1, dato2) in variables_globales.items():
        if clave == p[1]:
            valor_actual = variables_globales[p[1]]
            if p[3] > dato2:
                return True
            else:
                return False
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

    for clave, (dato1, dato2, dato3) in variables_locales.items():
        if clave == p[1]:
            if dato1 == proc_en_analisis:
                if p[3] > dato3:
                    return True
                else:
                    return False
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

def p_sentence8(p):
    '''sentence8 : ID MEQ INTEGER'''

    for clave, (dato1, dato2) in variables_globales.items():
        if clave == p[1]:
            valor_actual = variables_globales[p[1]]
            if p[3] < dato2:
                return True
            else:
                return False
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

    for clave, (dato1, dato2, dato3) in variables_locales.items():
        if clave == p[1]:
            if dato1 == proc_en_analisis:
                if p[3] < dato3:
                    return True
                else:
                    return False
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

def p_sentence9(p):
    '''sentence9 : ID EQUAL INTEGER'''

    for clave, (dato1, dato2) in variables_globales.items():
        if clave == p[1]:
            valor_actual = variables_globales[p[1]]
            if p[3] == dato2:
                return True
            else:
                return False
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

    for clave, (dato1, dato2, dato3) in variables_locales.items():
        if clave == p[1]:
            if dato1 == proc_en_analisis:
                if p[3] == dato3:
                    return True
                else:
                    return False
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def p_sentence10(p):
    '''sentence10 : ID DIFFERENT INTEGER'''

    for clave, (dato1, dato2) in variables_globales.items():
        if clave == p[1]:
            valor_actual = variables_globales[p[1]]
            if p[3] != dato2:
                return True
            else:
                return False
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

    for clave, (dato1, dato2, dato3) in variables_locales.items():
        if clave == p[1]:
            if dato1 == proc_en_analisis:
                if p[3] != dato3:
                    return True
                else:
                    return False
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

def p_sentence11(p):
    '''sentence11 : ID MEQEQUAL INTEGER'''

    for clave, (dato1, dato2) in variables_globales.items():
        if clave == p[1]:
            valor_actual = variables_globales[p[1]]
            if p[3] <= dato2:
                return True
            else:
                return False
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

    for clave, (dato1, dato2, dato3) in variables_locales.items():
        if clave == p[1]:
            if dato1 == proc_en_analisis:
                if p[3] <= dato3:
                    return True
                else:
                    return False
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

def p_sentence12(p):
    '''sentence12 : ID MAQEQUAL INTEGER'''

    for clave, (dato1, dato2) in variables_globales.items():
        if clave == p[1]:
            valor_actual = variables_globales[p[1]]
            if p[3] >= dato2:
                return True
            else:
                return False
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

    for clave, (dato1, dato2, dato3) in variables_locales.items():
        if clave == p[1]:
            if dato1 == proc_en_analisis:
                if p[3] >= dato3:
                    return True
                else:
                    return False
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

def p_sentence13(p):
    '''sentence13 : ISTRUE LPARENT ID RPARENT SEMICOLON'''

    for clave, (dato1, dato2) in variables_globales.items():
        if clave == p[1]:
            valor_actual = variables_globales[p[1]]
            if dato2:
                return True
            else:
                return False
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

    for clave, (dato1, dato2, dato3) in variables_locales.items():
        if clave == p[1]:
            if dato1 == proc_en_analisis:
                if dato3:
                    return True
                else:
                    return False
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def p_sentence14(p):
    '''sentence14 : REPEAT LPARENT sentences BREAK RPARENT SEMICOLON'''

def p_sentence15(p):
    '''sentence15 : UNTIL LPARENT instructions RPARENT sentences SEMICOLON'''
    if p[5] == True:
        return 0

def p_instructions(p):
    '''instructions : sentence'''
    p[0] = [p[1]]

def p_instructions_recursive(p):
    '''instructions : sentence sentences'''
    p[0] = [p[1]] + p[3]

def p_empty(p):
    '''empty :'''

    p[0] = None

# Error handling rule
def p_error(p):
    if p:
        syntax_errors.append(f"Error sintáctico: Token inesperado '{p.value}' en línea {p.lineno}, posición {p.lexpos}")
    else:
        syntax_errors.append("Error sintáctico: Fin de archivo inesperado")


with open('prueba.txt', 'r') as file:
    input_text = file.read()


print("Ejecutando análisis")
lexer = lex.lex()
lexer.input(input_text)
for token in lexer:
    print(token)
# Print the lexical errors
if lexical_errors:
    print("\nLexical errors:")
    for error in lexical_errors:
        print(error)

# Build the parser
parser = yacc.yacc()


result = parser.parse(input_text)

# Print the syntax errors
if syntax_errors:
    print("Syntax errors:")
    for error in syntax_errors:
        print(error)
else:
    print(result)
    
