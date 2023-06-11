import ply.yacc as yacc
import ply.lex as lex
from collections import deque
from arduino import manipulacion_arduino
import time

# Lex ---------------------
lexical_errors = []

# List of token names
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
    'RECUT'
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
t_CUT = 'Cut'
t_RECUT = 'ReCut'


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
    r'(Num|Bool|Str)'
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

while_flag = False
while_list = []
first_pasada = False

id_case = None
condition_flag = True
else_flag = False

var_queValida_while = None

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
)


def p_start(p):
    '''start : master
            | master procedures
            | master master_vars procedures
            | master_vars master
            | master_vars master master_vars
            | master_vars master master_vars procedures
            | master_vars master master_vars procedures master_vars
            | master_vars master procedures
            | master_vars master procedures master_vars '''
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
    if proc_en_analisis in called_procs:
        called_procs.remove(proc_en_analisis)
    # for element in procs:
    #   if element in called_procs:
    #      called_procs.remove(element)
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
                       | call
                       | print_values
                       | alter
                       | alterB
                       | comparisson_maq
                       | comparisson_meq
                       | comparisson_equal
                       | comparisson_dif
                       | comparisson_meqequal
                       | comparisson_maqequal
                       | isTrue
                       | signal
                       | viewsignal
                       | cut
                       | recut
                       | case
                       | while
                       | empty'''
    p[0] = p[1]  # Assign the value of the matched alternative to p[0]


def p_master_vars(p):
    '''master_vars : master_var
                    | master_vars master_var'''


def p_master_var(p):
    '''master_var : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON
                    | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON
                    | NEW ID COMA LPARENT TYPE COMA STRING RPARENT SEMICOLON'''
    if 2 < len(p[2]) < 12:
        if p[5] == 'Num' and isinstance(p[7], int):
            variables_globales[p[2]] = [p[5], p[7]]
            print(f'Variable Global Creada: Nombre: {p[2]} // Valor: {p[7]}')
        elif p[5] == 'Bool' and isinstance(p[7], bool):
            variables_globales[p[2]] = [p[5], p[7]]
            print(f'Variable Global Creada: Nombre: {p[2]} // Valor: {p[7]}')
        elif p[5] == 'Str' and isinstance(p[7], str):
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


def p_sentence(p):
    '''sentence : local_variable
                | values
                | call
                | print_values
                | alter
                | alterB
                | comparisson_maq
                | comparisson_meq
                | comparisson_equal
                | comparisson_dif
                | comparisson_meqequal
                | comparisson_maqequal
                | isTrue
                | signal
                | viewsignal
                | cut
                | recut
                | case
                | while
                | empty'''
    p[0] = p[1]


def p_return_statement(p):
    '''return_statement : isTrue
                        | comparisson_maqequal
                        | comparisson_meqequal
                        | comparisson_dif
                        | comparisson_equal
                        | comparisson_meq
                        | comparisson_maq
                        | alterB
                        | alter'''


def local_variable_aux(id, type, value):
    print("paso variable local " + id)
    global variables_locales
    errorFlag = False
    if id in variables_locales and variables_locales[id][0] == proc_en_analisis:
        errorFlag = True
    if not errorFlag:
        if 2 < len(id) < 12:
            if type == 'Num' and isinstance(value, int):
                variables_locales[id] = [proc_en_analisis, type, value]
            elif type == 'Bool' and isinstance(value, bool):
                variables_locales[id] = [proc_en_analisis, type, value]
            elif type == 'Str' and isinstance(value, str):
                variables_locales[id] = [proc_en_analisis, type, value]
            else:
                syntax_errors.append(
                    f'Error en {proc_en_analisis}, en definicion de variable: {id} valor dado no corresponde al tipado seleccionado')
        else:
            syntax_errors.append(
                f'Error en {proc_en_analisis}, tamaño de nombre de variable: {id} no cumple con el estándar')
    else:
        syntax_errors.append(
            f'Error en procedure: {proc_en_analisis}, definicion multiple de variable local: {id}')


# Estructura en el diccionario de variables = ID [nombreProc, tipo, valor]
def p_local_variable(p):
    '''local_variable : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON
                | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON
                | NEW ID COMA LPARENT TYPE COMA STRING RPARENT SEMICOLON'''
    global condition_flag, while_flag, while_list, first_pasada
    id = p[2]
    type = p[5]
    value = p[7]
    if first_pasada:
        if while_flag and (lambda: local_variable_aux not in while_list):
            while_list.append(lambda: local_variable_aux(id, type, value))
    elif condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            local_variable_aux(id, type, value)


def values_aux(id, value):
    if id in variables_locales:
        if isinstance(value, int) and variables_locales[id][1] == 'Num':
            variables_locales[id][2] = value
        elif isinstance(value, bool) and variables_locales[id][1] == 'Bool':
            variables_locales[id][2] = value
        elif isinstance(value, str) and variables_locales[id][1] == 'Str':
            variables_locales[id][2] = value
        else:
            syntax_errors.append(
                f'Error en procedure: {proc_en_analisis}, variable: {id}, valor dado no corresponde al tipado')
            return
        return variables_locales[id][2]
    elif id in variables_globales:
        if isinstance(value, int) and variables_globales[id][0] == 'Num':
            variables_globales[id][1] = value
        elif isinstance(value, bool) and variables_globales[id][0] == 'Bool':
            variables_globales[id][1] = value
        elif isinstance(value, str) and variables_globales[id][0] == 'Str':
            variables_globales[id][1] = value
        else:
            syntax_errors.append(
                f'Error en procedure: {proc_en_analisis}, variable: {id}, valor dado no corresponde al tipado')
            return
        return variables_globales[id][1]
    else:
        syntax_errors.append(f'Error en procedure: {proc_en_analisis}, Variable: {id} no existe')


def p_values(p):
    '''values : VALUES LPARENT ID COMA INTEGER RPARENT SEMICOLON
                 | VALUES LPARENT ID COMA BOOL RPARENT SEMICOLON
                 | VALUES LPARENT ID COMA return_statement RPARENT SEMICOLON'''
    global condition_flag, while_flag, while_list, first_pasada
    id = p[3]
    new_value = p[5]
    if first_pasada:
        if while_flag and (lambda: values_aux not in while_list):
            while_list.append(lambda: values_aux(id, new_value))
    elif condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            values_aux(id, new_value)


def p_call(p):
    '''call : CALL LPARENT ID RPARENT SEMICOLON'''
    if proc_en_analisis in called_procs or processingMaster:
        called_procs.append(p[3])


def find_local_variable_value(variable_name):
    for var_name, (var_proc, var_type, var_value) in variables_locales.items():
        if var_name == variable_name:
            print(f'Variable LOCAL buscada: {var_name} // Valor: {var_value} // Proc donde está: {var_proc}')
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
                | printable_sentence_var COMA printable_sentence_var
                | printable_sentence_string COMA printable_sentence_string
                | printable_sentence_var COMA printable_sentence_string
                | printable_sentence_string COMA printable_sentence_var
                | printable_sentences COMA printable_sentence_var
                | printable_sentences COMA printable_sentence_string
                | COMA printable_sentences COMA printable_sentence_var
                | COMA printable_sentences COMA printable_sentence_string'''


def printable_sentence_var_aux(id):
    if id in variables_locales:
        print(find_local_variable_value(id))
    elif id in variables_globales:
        print(variables_globales[id][1])
    else:
        syntax_errors.append(f'Error en procedure: {proc_en_analisis}, variable: {id} no existe')


def p_printable_sentence_var(p):
    '''printable_sentence_var : ID '''
    global condition_flag, while_flag, while_list, first_pasada
    if first_pasada:
        if while_flag and (lambda: printable_sentence_var_aux not in while_list):
            while_list.append(lambda: printable_sentence_var_aux(p[1]))
    elif condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            printable_sentence_var_aux(p[1])


def printable_sentence_string_aux(id):
    if proc_en_analisis in called_procs or processingMaster:
        print(id)


def p_printable_sentence_string(p):
    '''printable_sentence_string : STRING '''
    global condition_flag, while_flag, while_list, first_pasada
    if first_pasada:
        if while_flag and (lambda: printable_sentence_string_aux not in while_list):
            while_list.append(lambda: printable_sentence_string_aux(p[1]))
    elif condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            printable_sentence_string_aux(p[1])


def alter_aux(id, action, integer):
    if action == "ADD":
        if id in variables_globales:
            if variables_globales[id][0] == 'Num':
                valor_actual = variables_globales[id]
                nuevo_valor = (valor_actual[0], valor_actual[1] + integer)
                variables_globales[id] = nuevo_valor
                return variables_globales[id][1]
            else:
                syntax_errors.append(
                    f'Error en procedure {proc_en_analisis}, valor dado no corresponde al tipado {id}')
        elif id in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == id:
                        if var_proc == proc_en_analisis:
                            valor_actual = variables_locales[id]
                            nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] + integer)
                            variables_locales[id] = nuevo_valor
                            return variables_locales[id][2]
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'Error en procedure: {proc_en_analisis}, variable local: {id} no existe')
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'Error en procedure {proc_en_analisis}, valor dado no corresponde al tipado {id}')
        else:
            syntax_errors.append(f'Error en procedure {proc_en_analisis}, variable: {id} no existe')
    elif action == "SUB":
        if id in variables_globales:
            if variables_globales[id][0] == 'Num':
                valor_actual = variables_globales[id]
                nuevo_valor = (valor_actual[0], valor_actual[1] - integer)
                variables_globales[id] = nuevo_valor
                return variables_globales[id][1]
            else:
                syntax_errors.append(
                    f'Error en procedure {proc_en_analisis}, valor dado no corresponde al tipado {id}')
        elif id in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == id:
                        if var_proc == proc_en_analisis:
                            valor_actual = variables_locales[id]
                            nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] - integer)
                            variables_locales[id] = nuevo_valor
                            return variables_locales[id][2]
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'Error en procedure: {proc_en_analisis}, variable local: {id} no existe')
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'Error en procedure {proc_en_analisis}, valor dado no corresponde al tipado {id}')
        else:
            syntax_errors.append(f'Error en procedure {proc_en_analisis}, variable: {id} no existe')
    elif action == 'MUL':
        if id in variables_globales:
            if variables_globales[id][0] == 'Num':
                valor_actual = variables_globales[id]
                nuevo_valor = (valor_actual[0], valor_actual[1] * integer)
                variables_globales[id] = nuevo_valor
                return variables_globales[id][1]
            else:
                syntax_errors.append(
                    f'Error en procedure {proc_en_analisis}, valor dado no corresponde al tipado {id}')
        elif id in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == id:
                        if var_proc == proc_en_analisis:
                            valor_actual = variables_locales[id]
                            nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] * integer)
                            variables_locales[id] = nuevo_valor
                            return variables_locales[id][2]
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'Error en procedure: {proc_en_analisis}, variable local: {id} no existe')
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'Error en procedure {proc_en_analisis}, valor dado no corresponde al tipado {id}')
        else:
            syntax_errors.append(f'Error en procedure {proc_en_analisis}, variable: {id} no existe')
    elif action == 'DIV':
        if id in variables_globales:
            if variables_globales[id][0] == 'Num':
                valor_actual = variables_globales[id]
                nuevo_valor = (valor_actual[0], valor_actual[1] / integer)
                variables_globales[id] = nuevo_valor
                return variables_globales[id][1]
            else:
                syntax_errors.append(
                    f'Error en procedure {proc_en_analisis}, valor dado no corresponde al tipado {id}')
        elif id in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == id:
                        if var_proc == proc_en_analisis:
                            valor_actual = variables_locales[id]
                            nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] / integer)
                            variables_locales[id] = nuevo_valor
                            return variables_locales[id][2]
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'Error en procedure: {proc_en_analisis}, variable local: {id} no existe')
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'Error en procedure {proc_en_analisis}, valor dado no corresponde al tipado {id}')
        else:
            syntax_errors.append(f'Error en procedure {proc_en_analisis}, variable: {id} no existe')


# Estructura en el diccionario de variables = ID [nombreProc, tipo, valor]
def p_alter(p):
    '''alter : ALTER LPARENT ID COMA ADD COMA INTEGER RPARENT SEMICOLON
                | ALTER LPARENT ID COMA SUB COMA INTEGER RPARENT SEMICOLON
                | ALTER LPARENT ID COMA MUL COMA INTEGER RPARENT SEMICOLON
                | ALTER LPARENT ID COMA DIV COMA INTEGER RPARENT SEMICOLON'''
    global condition_flag, while_flag, while_list, first_pasada
    if first_pasada:
        if while_flag and (lambda: alter_aux not in while_list):
            while_list.append(lambda: alter_aux(p[3], p[5], p[7]))
    elif condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            alter_aux(p[3], p[5], p[7])


def alterB_aux(id):
    global while_flag, var_queValida_while
    if condition_flag:
        if id in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Bool':
                    if var_name == id:
                        valor_actual = variables_globales[id]
                        if var_value:
                            nuevo_valor = (valor_actual[0], False)
                            variables_globales[id] = nuevo_valor
                            if var_queValida_while == var_name:
                                print(f'Reinicio de while, variable que valida: {var_name}')
                                while_flag = False
                            return False
                        else:
                            nuevo_valor = (valor_actual[0], True)
                            variables_globales[id] = nuevo_valor
                            return True
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'Error en procedure: {proc_en_analisis}, valor dado no corresponde al tipado {id}')
        elif id in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_name == id:
                    if var_type == 'Bool':
                        if var_proc == proc_en_analisis:
                            if var_value:
                                valor_actual = variables_locales[id]
                                nuevo_valor = (valor_actual[0], valor_actual[1], False)
                                variables_locales[id] = nuevo_valor
                                if var_queValida_while == var_name:
                                    while_flag = False
                                return False
                            else:
                                valor_actual = variables_locales[id]
                                nuevo_valor = (valor_actual[0], valor_actual[1], True)
                                variables_locales[id] = nuevo_valor
                                return True
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'Error en procedure: {proc_en_analisis}, variable local no existe en proc')
                    elif index == len(variables_locales) - 1:
                        syntax_errors.append(
                            f'Error en procedure: {proc_en_analisis}, valor dado no corresponde al tipado seleccionado {id}')
        else:
            syntax_errors.append(f'Error en procedure: {proc_en_analisis}, Variable: {id} no existe')


def p_alterB(p):
    '''alterB : ALTERB LPARENT ID RPARENT SEMICOLON'''
    global condition_flag, while_flag, while_list, first_pasada
    var = p[3]
    if first_pasada:
        if while_flag and (lambda: alterB_aux not in while_list):
            while_list.append(lambda: alterB_aux(var))
    elif condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            alterB_aux(var)


def p_comparisson_maq(p):
    '''comparisson_maq : ID MAQ INTEGER'''
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_value > p[3]:
                            print(True)
                            return True
                        else:
                            print(False)
                            return False
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'Error en procedure: {proc_en_analisis}, valor dado no corresponde al tipado seleccionado {p[1]}')
        elif p[1] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_proc == proc_en_analisis:
                            if var_value > p[3]:
                                print(True)
                                return True
                            else:
                                print(False)
                                return False
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'Error en procedure: {proc_en_analisis}, variable local no existe en proc')
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'Error en procedure: {proc_en_analisis}, valor dado no corresponde al tipado seleccionado {p[1]}')
        else:
            syntax_errors.append(f'Error en procedure: {proc_en_analisis}, Variable: {p[1]} no existe')


def p_comparisson_meq(p):
    '''comparisson_meq : ID MEQ INTEGER'''
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_value < p[3]:
                            print(True)
                            return True
                        else:
                            print(False)
                            return False
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[1]}')
        elif p[1] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_proc == proc_en_analisis:
                            if var_value < p[3]:
                                print(True)
                                return True
                            else:
                                print(False)
                                return False
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[1]}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[1]} no existe')


def p_comparisson_equal(p):
    '''comparisson_equal : ID EQUAL INTEGER'''
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_value == p[3]:
                            print(True)
                            return True
                        else:
                            print(False)
                            return False
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[1]}')
        elif p[1] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_proc == proc_en_analisis:
                            if var_value == p[3]:
                                print(True)
                                return True
                            else:
                                print(False)
                                return False
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[1]}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[1]} no existe')


def p_comparisson_dif(p):
    '''comparisson_dif : ID DIFFERENT INTEGER'''
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_value != p[3]:
                            print(True)
                            return True
                        else:
                            print(False)
                            return False
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[1]}')
        elif p[1] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_proc == proc_en_analisis:
                            if var_value != p[3]:
                                print(True)
                                return True
                            else:
                                print(False)
                                return False
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[1]}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[1]} no existe')


def p_comparisson_meqequal(p):
    '''comparisson_meqequal : ID MEQEQUAL INTEGER'''
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_value <= p[3]:
                            print(True)
                            return True
                        else:
                            print(False)
                            return False
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[1]}')
        elif p[1] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_proc == proc_en_analisis:
                            if var_value <= p[3]:
                                print(True)
                                return True
                            else:
                                print(False)
                                return False
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[1]}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[1]} no existe')


def p_comparisson_maqequal(p):
    '''comparisson_maqequal : ID MAQEQUAL INTEGER'''
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_value >= p[3]:
                            print(True)
                            return True
                        else:
                            print(False)
                            return False
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[1]}')
        elif p[1] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_proc == proc_en_analisis:
                            if var_value >= p[3]:
                                print(True)
                                return True
                            else:
                                print(False)
                                return False
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[1]}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[1]} no existe')


def p_isTrue(p):
    '''isTrue : ISTRUE LPARENT ID RPARENT SEMICOLON'''

    global condition_flag, while_flag, first_pasada, var_queValida_while
    if proc_en_analisis in called_procs or processingMaster:
        if p[3] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_name == p[3]:
                    if var_type == 'Bool':
                        if var_value:
                            print("True")
                            if while_flag:
                                first_pasada = True
                                var_queValida_while = var_name
                                print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')
                            return True
                        else:
                            print("False")
                            if while_flag:
                                condition_flag = False
                                first_pasada = False
                                while_flag = False
                            return False
                    elif index == len(variables_globales) - 1:
                        syntax_errors.append(
                            f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado '
                            f'seleccionado {p[3]}')
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


def p_signal(p):
    '''signal : SIGNAL LPARENT INTEGER COMA INTEGER RPARENT SEMICOLON
            | SIGNAL LPARENT ID COMA INTEGER RPARENT SEMICOLON'''
    global condition_flag, while_flag, while_list, first_pasada, proc_en_analisis
    position = p[3]
    estado = p[5]
    if first_pasada:
        if while_flag and (lambda: signal_handler not in while_list):
            while_list.append(lambda: signal_handler(position, estado))

    elif condition_flag:
        if position in variables_globales:
            if isinstance(position, int):
                if 6 >= position >= 1:
                    signal_handler(position, estado)
            else:
                pos = find_global_variable_value(position)
                signal_handler(pos, estado)

        elif position in variables_locales:
            for var_name, (var_proc, var_type, var_value) in variables_locales.items():
                if var_type == 'Num':
                    if var_name == position:
                        if var_proc == proc_en_analisis:
                            if isinstance(position, int):
                                if 6 >= position >= 1:
                                    signal_handler(position, estado)
                            else:
                                pos = find_local_variable_value(position)
                                signal_handler(pos, estado)

    else:
        pass


def signal_handler(position, estado):
    global condition_flag, proc_en_analisis
    if condition_flag:
        if isinstance(position, int):
            pass
        if not isinstance(position, int):
            if position in variables_globales:
                position = find_global_variable_value(position)
            else:
                for var_name, (var_proc, var_type, var_value) in variables_locales.items():
                    if var_type == 'Num':
                        if var_name == position:
                            if var_proc == proc_en_analisis:
                                position = find_local_variable_value(position)

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


def p_while(p):
    '''while : while_handler sentences LPARENT sentences RPARENT SEMICOLON'''

    global while_flag, while_list, first_pasada, condition_flag
    print("llegó a while")
    first_pasada = False
    condition_flag = True
    print(while_list)
    while while_flag:
        for func in while_list:
            func()
            time.sleep(2)

    while_list = []
    condition_flag = True

def p_while_handler(p):
    '''while_handler : WHILE'''

    global while_flag, condition_flag, first_pasada
    while_flag = True
    condition_flag = False
    first_pasada = True


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
    global id_case, condition_flag, else_flag, first_pasada
    id_case = p[1]


def p_condition(p):
    '''condition : WHEN INTEGER THEN
                | WHEN STRING THEN '''

    global id_case, condition_flag, while_flag, while_list, condition_flag
    condition_flag = True
    variable_name = id_case
    condition_value = p[2]
    if while_flag and (lambda: condition_handler not in while_list):
        while_list.append(lambda: condition_handler(variable_name, condition_value))
    elif condition_flag:
        condition_handler(variable_name, condition_value)


def condition_handler(variable_name, condition_value):
    global condition_flag
    if variable_name in variables_globales:
        if find_global_variable_value(variable_name) == condition_value:
            # Set the condition flag to True to execute the following sentences
            print("PASÓ RITEVE")
            condition_flag = True
        else:
            # Set the condition flag to False to skip the following sentences
            print("No coindició CASE")
            condition_flag = False


def p_cut(p):
    '''cut : CUT LPARENT ID COMA STRING RPARENT SEMICOLON
            | CUT LPARENT ID COMA ID RPARENT SEMICOLON'''

    global while_flag, while_list, first_pasada, condition_flag
    if proc_en_analisis in called_procs or processingMaster:
        if p[3] in variables_locales:
            if isinstance(p[5], str) and variables_locales[p[3]][1] == 'Str':
                var_donde_guardar = p[3]
                var_donde_cortar = p[5]
                if first_pasada:
                    if while_flag and (lambda: cut_handler not in while_list):
                        while_list.append(lambda: cut_handler(var_donde_guardar, var_donde_cortar))
                elif condition_flag:
                    cut_handler(var_donde_guardar, var_donde_cortar)
            else:
                syntax_errors.append(
                    f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[3]}')

        elif p[3] in variables_globales:
            if isinstance(p[5], str) and variables_globales[p[3]][0] == 'Str':
                var_donde_guardar = p[3]
                var_donde_cortar = p[5]
                if first_pasada:
                    if while_flag and (lambda: cut_handler not in while_list):
                        while_list.append(lambda: cut_handler(var_donde_guardar, var_donde_cortar))
                elif condition_flag:
                    cut_handler(var_donde_guardar, var_donde_cortar)
            else:
                syntax_errors.append(
                    f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[3]}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def cut_handler(var_donde_guardar, var_donde_cortar):
    if var_donde_cortar in variables_locales:
        string_a_cortar = find_local_variable_value(var_donde_cortar)

    if var_donde_cortar in variables_globales:
        string_a_cortar = find_global_variable_value(var_donde_cortar)

    if var_donde_guardar in variables_locales:
        variables_locales[var_donde_guardar][2] = string_a_cortar[0]
        print(f'Nuevos valores en {var_donde_guardar}: {variables_locales[var_donde_guardar]}')

    if var_donde_guardar in variables_globales:
        variables_globales[var_donde_guardar][1] = string_a_cortar[0]
        print(f'Nuevos valores en {var_donde_guardar}: {variables_globales[var_donde_guardar]}')


def p_recut(p):
    '''recut : RECUT LPARENT ID RPARENT SEMICOLON'''

    global while_flag, while_list
    if proc_en_analisis in called_procs or processingMaster:
        if p[3] in variables_locales:
            if isinstance(p[5], str) and variables_locales[p[3]][1] == 'Str':
                var_donde_editar = p[3]
                if first_pasada:
                    if while_flag and (lambda: recut_handler not in while_list):
                        while_list.append(lambda: recut_handler(var_donde_editar))
                elif condition_flag:
                    recut_handler(var_donde_editar)
            else:
                syntax_errors.append(
                    f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[3]}')

        elif p[3] in variables_globales:
            if isinstance(p[5], str) and variables_globales[p[3]][0] == 'Str':
                var_donde_editar = p[3]
                if first_pasada:
                    if while_flag and (lambda: recut_handler not in while_list):
                        while_list.append(lambda: recut_handler(var_donde_editar))
                elif condition_flag:
                    recut_handler(var_donde_editar)
            else:
                syntax_errors.append(
                    f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[3]}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')


def recut_handler(var):
    if var in variables_locales:
        variables_locales[var][2] = find_local_variable_value(var)[1:]
        print(f'Nuevos valores en {var}: {variables_locales[var]}')

    if var in variables_globales:
        variables_globales[var][1] = find_global_variable_value(var)[1:]
        print(f'Nuevos valores en {var}: {variables_globales[var]}')


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
