import ply.yacc as yacc
import ply.lex as lex
from collections import deque
from arduino import manipulacion_arduino
import time
from functools import partial

# Lex ---------------------
lexical_errors = []

# List of token names
tokens = ['MASTER', 'ID', 'SEMICOLON', 'INTEGER', 'BOOL', 'MAQ', 'MEQ', 'EQUAL', 'DIFFERENT', 'MEQEQUAL', 'MAQEQUAL',
          'ARROBA',
          'COMA', 'LPARENT', 'RPARENT', 'ADD', 'SUB', 'MUL', 'DIV', 'COMMENT', 'TYPE', 'STRING', 'PLUS', 'NEWLINE'
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
processingMaster = True
called_procs = []
procs = []
variables_locales = {}
variables_globales = {}
syntax_errors = []
master = 0
proc_en_analisis = ''
condition_flag = True
else_flag = False
while_flag = False
while_list = []

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
)


def p_start(p):
    '''start : master procedures
            | master'''
    p[0] = p[1]


def p_declare_procedure(p):
    '''declare_procedure : PROC ID'''
    global procs, proc_en_analisis
    if p[2] not in procs:
        procs.append(p[2])
        print(str(p[2]) + " agregado a la lista de procs")
        proc_en_analisis = p[2]
    else:
        syntax_errors.append(f'Ya hay un procedure con este nombre, hay otra declaración en la línea: {p.lineno}')


def p_procedures(p):
    '''procedures : procedure
                    | procedures procedure'''


def p_procedure(p):
    '''procedure : declare_procedure LPARENT sentences RPARENT SEMICOLON'''
    # Acción semántica: Realizar las acciones correspondientes al análisis sintáctico
    # de un procedimiento
    for element in procs:
        if element in called_procs:
            called_procs.remove(element)
    p[0] = ('procedure', p[2], p[4])


def p_master(p):
    '''master : MASTER LPARENT master_sentences RPARENT SEMICOLON'''
    # Acción semántica: Realizar las aciones correspondientes al análisis sintáctico de @Master
    print("pasó master")
    global master, processingMaster
    master += 1
    if master != 1:
        syntax_errors.append(f'Debe existir solamente un @Master, hay otra declaración en la línea: {p.lineno}')
    processingMaster = False


# Esto es para lidiar con las variables globales
def p_master_sentences(p):
    '''master_sentences : master_sentence
                        | master_sentences master_sentence'''
    if len(p) == 2:
        p[0] = [p[1]]  # Create a list with a single item
    else:
        p[0] = p[1] + [p[2]]  # Append the new item to the existing list


def p_master_sentence(p):
    '''master_sentence : master_var
                       | values
                       | case
                       | call
                       | print_values
                       | alter
                       | alterB
                       | signal
                       | viewsignal
                       | sentence7
                       | sentence8
                       | sentence9
                       | sentence10
                       | sentence11
                       | sentence12
                       | isTrue
                       | while
                       | empty'''
    p[0] = p[1]  # Assign the value of the matched alternative to p[0]


def p_master_var(p):
    '''master_var : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON
                    | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON'''
    if 2 < len(p[2]) < 12:
        if p[5] == 'Num' and isinstance(p[7], int):
            variables_globales[p[2]] = [p[5], p[7]]
            print(f'Variable Global Creada: Nombre: {p[2]} // Valor: {p[7]}')
        elif p[5] == 'Bool' and isinstance(p[7], bool):
            variables_globales[p[2]] = [p[5], p[7]]
            print(f'Variable Global Creada: Nombre: {p[2]} // Valor: {p[7]}')
        else:
            syntax_errors.append(
                f'Error en línea {p.lineno}, posición {p.lexpos}, valor dado no corresponde al tipado seleccionado')
    else:
        syntax_errors.append(
            f'Error en línea {p.lineno}, posición {p.lexpos}, tamaño de nombre de variable no cumple con el estándar')


# Recursividad para agarrar todas las sentencias
def p_sentences(p):
    '''sentences : sentence
                 | sentences sentence'''


# Aquí se van agregando todas las sentencias, así como vamos
# TODO toda sentence que se agregue aquí, se tiene que agregar a master_sentence
def p_sentence(p):
    '''sentence : local_variable
                | values
                | case
                | call
                | print_values
                | alter
                | alterB
                | signal
                | viewsignal
                | sentence7
                | sentence8
                | sentence9
                | sentence10
                | sentence11
                | sentence12
                | isTrue
                | while
                | empty'''
    p[0] = p[1]


# Estructura en el diccionario de variables = ID [nombreProc, tipo, valor]
def p_local_variable(p):
    '''local_variable : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON
                | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON'''
    if proc_en_analisis in called_procs:
        print("Paso variable local")
        if len(p[2]) > 2 and len(p[2]) < 12:
            if p[5] == 'Num' and isinstance(p[7], int):
                variables_locales[p[2]] = [proc_en_analisis, p[5], p[7]]
            elif p[5] == 'Bool' and isinstance(p[7], bool):
                variables_locales[p[2]] = [proc_en_analisis, p[5], p[7]]
            else:
                syntax_errors.append(
                    f'Error en línea {p.lineno}, posición {p.lexpos}, valor dado no corresponde al tipado seleccionado')
        else:
            syntax_errors.append(
                f'Error en línea {p.lineno}, posición {p.lexpos}, tamaño de nombre de variable no cumple con el estándar')


def p_values(p):
    '''values : VALUES LPARENT ID COMA INTEGER RPARENT SEMICOLON
                 | VALUES LPARENT ID COMA BOOL RPARENT SEMICOLON'''
    if proc_en_analisis in called_procs or processingMaster:
        if p[3] in variables_locales:
            if isinstance(p[5], int) and variables_locales[p[3]][1] == 'Num':
                variables_locales[p[3]][2] = p[5]
            elif isinstance(p[5], bool) and variables_locales[p[3]][1] == 'Bool':
                variables_locales[p[3]][2] = p[5]
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


def p_call(p):
    '''call : CALL LPARENT ID RPARENT SEMICOLON'''
    if proc_en_analisis in called_procs or processingMaster:
        called_procs.append(p[3])


def find_local_variable_value(variable_name):
    for var_name, (var_proc, var_type, var_value) in variables_locales.items():
        if var_name == variable_name:
            return var_value
    return None  # Variable not found


def find_global_variable_value(variable_name):
    for var_name, var_value in variables_globales.items():
        if var_name == variable_name:
            print(f'Variable GLOBAL buscada: {var_name} // Valor: {var_value}')
            return var_value[1]
    return None  # Variable not found


def p_print_values(p):
    '''print_values : PRINTVALUES LPARENT printable_sentences RPARENT SEMICOLON'''


# Recursividad para agarrar todas las sentencias

def p_printable_sentences(p):
    '''printable_sentences : printable_sentence_var
                | printable_sentence_string
                | printable_sentence_var PLUS printable_sentence_var
                | printable_sentence_string PLUS printable_sentence_string
                | printable_sentence_var PLUS printable_sentence_string
                | printable_sentence_string PLUS printable_sentence_var
                | PLUS printable_sentences PLUS printable_sentence_var
                | PLUS printable_sentences PLUS printable_sentence_string'''


def p_printable_sentence_var(p):
    '''printable_sentence_var : ID '''
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_locales:
            print(find_local_variable_value(p[1]))
        elif p[1] in variables_globales:
            print(variables_globales[p[1]][1])
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def p_printable_sentence_string(p):
    '''printable_sentence_string : STRING '''
    if proc_en_analisis in called_procs or processingMaster:
        print(p[1])


# Estructura en el diccionario de variables = ID [nombreProc, tipo, valor]
def p_alter(p):
    '''alter : ALTER LPARENT ID COMA ADD COMA INTEGER RPARENT SEMICOLON
                | ALTER LPARENT ID COMA SUB COMA INTEGER RPARENT SEMICOLON
                | ALTER LPARENT ID COMA MUL COMA INTEGER RPARENT SEMICOLON
                | ALTER LPARENT ID COMA DIV COMA INTEGER RPARENT SEMICOLON'''

    global while_flag, while_list
    if proc_en_analisis in called_procs or processingMaster:
        operador = "ADD"
        id = p[3]
        integer = p[7]
        alter_aux(operador, id, integer)

        if while_flag and (lambda: alter_aux not in while_list):
            while_list.append(lambda: alter_aux(operador, id, integer))


def alter_aux(operador, id, integer):
    if operador == "ADD":
        if id in variables_globales:
            valor_actual = variables_globales[id]
            nuevo_valor = (valor_actual[0], valor_actual[1] + integer)
            variables_globales[id] = nuevo_valor
            print(f'Valor cambiado: {variables_globales[id]}')
        elif id in variables_locales:
            for var_name, (var_proc, var_type, var_value) in variables_locales.items():
                if var_type == 'Num':
                    if var_name == id:
                        if var_proc == proc_en_analisis:
                            valor_actual = variables_locales[id]
                            nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] + integer)
                            variables_locales[id] = nuevo_valor
                        else:
                            syntax_errors.append(
                                f'Error en línea , posición : variable local no existe en proc {proc_en_analisis}')
                else:
                    syntax_errors.append(
                        f'Error en línea , posición : valor dado no corresponde al tipado seleccionado {id}')
        else:
            syntax_errors.append(f'Error en línea , posición : Variable: {id} no existe')
    elif operador == "SUB":
        if id in variables_globales:
            valor_actual = variables_globales[id]
            nuevo_valor = (valor_actual[0], valor_actual[1] - integer)
            variables_globales[id] = nuevo_valor
        elif id in variables_locales:
            for var_name, (var_proc, var_type, var_value) in variables_locales.items():
                if var_type == 'Num':
                    if var_name == id:
                        if var_proc == proc_en_analisis:
                            valor_actual = variables_locales[id]
                            nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] - integer)
                            variables_locales[id] = nuevo_valor
                            print(find_local_variable_value(id))
                        else:
                            syntax_errors.append(
                                f'Error en línea , posición : variable local no existe en proc {proc_en_analisis}')
                else:
                    syntax_errors.append(
                        f'Error en línea , posición : valor dado no corresponde al tipado seleccionado {id}')
        else:
            syntax_errors.append(f'Error en línea , posición : Variable: {id} no existe')
    elif operador == "MUL":
        if id in variables_globales:
            valor_actual = variables_globales[id]
            nuevo_valor = (valor_actual[0], valor_actual[1] * integer)
            variables_globales[id] = nuevo_valor
            print(variables_globales[id][1])
        elif id in variables_locales:
            for var_name, (var_proc, var_type, var_value) in variables_locales.items():
                if var_type == 'Num':
                    if var_name == id:
                        if var_proc == proc_en_analisis:
                            valor_actual = variables_locales[id]
                            nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] * integer)
                            variables_locales[id] = nuevo_valor
                            print(find_local_variable_value(id))
                        else:
                            syntax_errors.append(
                                f'Error en línea , posición : variable local no existe en proc {proc_en_analisis}')
                else:
                    syntax_errors.append(
                        f'Error en línea , posición : valor dado no corresponde al tipado seleccionado {id}')
        else:
            syntax_errors.append(f'Error en línea , posición : Variable: {id} no existe')
    elif operador == "DIV":
        if id in variables_globales:
            valor_actual = variables_globales[id]
            nuevo_valor = (valor_actual[0], valor_actual[1] / integer)
            variables_globales[id] = nuevo_valor
            print(variables_globales[id][1])
        elif id in variables_locales:
            for var_name, (var_proc, var_type, var_value) in variables_locales.items():
                if var_type == 'Num':
                    if var_name == id:
                        if var_proc == proc_en_analisis:
                            valor_actual = variables_locales[id]
                            nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] / integer)
                            variables_locales[id] = nuevo_valor
                            print(find_local_variable_value(id))
                        else:
                            syntax_errors.append(
                                f'Error en línea , posición : variable local no existe en proc {proc_en_analisis}')
                else:
                    syntax_errors.append(
                        f'Error en línea , posición : valor dado no corresponde al tipado seleccionado {id}')
    else:
        syntax_errors.append(f'Error en línea , posición : Variable: {id} no existe')


def p_alterB(p):
    '''alterB : ALTERB LPARENT ID RPARENT SEMICOLON'''
    if proc_en_analisis in called_procs or processingMaster:
        if p[3] in variables_globales:
            for clave, (dato1, dato2) in variables_globales.items():
                if clave == p[3]:
                    valor_actual = variables_globales[p[3]]
                    if dato2 == True:
                        nuevo_valor = (valor_actual[0], False)
                        variables_globales[p[3]] = nuevo_valor
                    else:
                        nuevo_valor = (valor_actual[0], True)
                        variables_globales[p[3]] = nuevo_valor
        elif p[3] in variables_locales:
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
                        syntax_errors.append(
                            f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                else:
                    syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def p_sentence7(p):
    '''sentence7 : ID MAQ INTEGER'''
    if proc_en_analisis in called_procs or processingMaster:
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
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def p_sentence8(p):
    '''sentence8 : ID MEQ INTEGER'''
    if proc_en_analisis in called_procs or processingMaster:
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
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def p_sentence9(p):
    '''sentence9 : ID EQUAL INTEGER'''
    if proc_en_analisis in called_procs or processingMaster:
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
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def p_sentence10(p):
    '''sentence10 : ID DIFFERENT INTEGER'''
    if proc_en_analisis in called_procs or processingMaster:
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
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def p_sentence11(p):
    '''sentence11 : ID MEQEQUAL INTEGER'''
    if proc_en_analisis in called_procs or processingMaster:
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
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def p_sentence12(p):
    '''sentence12 : ID MAQEQUAL INTEGER'''
    if proc_en_analisis in called_procs or processingMaster:
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
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def p_isTrue(p):
    '''isTrue : ISTRUE LPARENT ID RPARENT SEMICOLON'''

    global condition_flag, while_flag
    if proc_en_analisis in called_procs or processingMaster:
        if p[3] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_name == p[3]:
                    if var_type == 'Bool':
                        if var_value:
                            print("True")
                            condition_flag = True
                            while_flag = True
                            return True
                        else:
                            print("False")
                            condition_flag = False
                            while_flag = False
                            return False
                    elif index == len(variables_globales) - 1:
                        syntax_errors.append(
                            f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[3]}')
        elif p[3] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_name == p[3]:
                    if var_proc == proc_en_analisis:
                        if var_value:
                            print(True)
                            return True
                        else:
                            print(False)
                            return False
                    elif index == len(variables_locales) - 1:
                        syntax_errors.append(
                            f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def p_while(p):
    '''while : WHILE sentences LPARENT sentences RPARENT SEMICOLON'''

    global while_flag, while_list
    print("llegó a while")
    while while_flag:
        for func in while_list:
            func()
            time.sleep(2)


def p_case(p):
    '''case : CASE expression recursive_conditions SEMICOLON'''

    global condition_flag
    condition_flag = True
    pass


def p_else_condition(p):
    '''else_condition : LPARENT sentences RPARENT'''

    global condition_flag, else_flag
    if not condition_flag:
        else_flag = True

    pass


def p_recursive_conditions(p):
    '''recursive_conditions : recursive_condition
                            | recursive_conditions recursive_condition'''
    pass


def p_recursive_condition(p):
    '''recursive_condition :  condition LPARENT sentences RPARENT'''
    pass


def p_expression(p):
    'expression : ID'
    global id_case, condition_flag, else_flag
    id_case = p[1]
    condition_flag = True
    else_flag = False


def p_condition(p):
    'condition : WHEN INTEGER THEN '

    global id_case, condition_flag
    variable_name = id_case
    condition_value = p[2]
    if variable_name in variables_globales:
        if find_global_variable_value(variable_name) == condition_value:
            # Set the condition flag to True to execute the following sentences
            print("PASÓ RITEVE")
            condition_flag = True
        else:
            # Set the condition flag to False to skip the following sentences
            print("No coindició CASE")
            condition_flag = False


def p_signal(p):
    '''signal : SIGNAL LPARENT INTEGER COMA INTEGER RPARENT SEMICOLON
            | SIGNAL LPARENT ID COMA INTEGER RPARENT SEMICOLON'''

    global condition_flag, while_flag, while_list
    position = p[3]
    estado = p[5]

    if condition_flag:
        if isinstance(position, int):
            if 6 >= position >= 1:
                signal_handler(position, estado)
        else:
            pos = find_global_variable_value(position)
            signal_handler(pos, estado)

    if while_flag and (lambda: signal_handler not in while_list):
        while_list.append(lambda: signal_handler(position, estado))

    else:
        pass


def signal_handler(position, estado):
    if isinstance(position, int):
        pass
    if not isinstance(position, int):
        position = find_global_variable_value(position)
    if position == 1:
        manipulacion_arduino("morado", estado)
    if position == 2:
        manipulacion_arduino("verde", estado)
    if position == 3:
        manipulacion_arduino("naranja", estado)
    if position == 4:
        manipulacion_arduino("blanco", estado)
    if position == 5:
        manipulacion_arduino("azul", estado)
    if position == 6:
        manipulacion_arduino("amarillo", estado)


def p_viewsignal(p):
    '''viewsignal : VIEWSIGNAL LPARENT INTEGER RPARENT SEMICOLON'''
    position = p[3]
    print("Implementación con código Josepa")


def p_empty(p):
    '''empty :'''

    p[0] = None


# Error handling rule
def p_error(p):
    if p:
        syntax_errors.append(f"Error sintáctico: Token inesperado '{p.value}' en línea {p.lineno}, posición {p.lexpos}")
    else:
        syntax_errors.append("Error sintáctico: Fin de archivo inesperado")


with open('prueba2.txt', 'r') as file:
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
