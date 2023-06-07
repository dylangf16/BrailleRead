import ply.yacc as yacc
import ply.lex as lex
from collections import deque


#Lex ---------------------
lexical_errors = []

# List of token names
tokens = ['MASTER','ID', 'SEMICOLON', 'INTEGER', 'BOOL', 'MAQ', 'MEQ', 'EQUAL', 'DIFFERENT', 'MEQEQUAL', 'MAQEQUAL', 'ARROBA',
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
            | master_vars master procedures master_vars
            | master_vars master procedures'''
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
                       | sentence14
                       | sentence15
                       | empty'''
    p[0] = p[1]  # Assign the value of the matched alternative to p[0]

def p_master_vars(p):
    '''master_vars : master_var
                    | master_vars master_var'''
def p_master_var(p):
    '''master_var : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON
                    | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON'''
    print("Paso variable global")
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


# Recursividad para agarrar todas las sentencias
def p_sentences(p):
    '''sentences : sentence
                 | sentences sentence'''


# Aquí se van agregando todas las sentencias, así como vamos
# TODO toda sentence que se agregue aquí, se tiene que agregar a master_sentence
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
                | sentence14
                | sentence15 '''
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

# Estructura en el diccionario de variables = ID [nombreProc, tipo, valor]
def p_local_variable(p):
    '''local_variable : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON
                | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON'''
    if proc_en_analisis in called_procs:
        print("Paso variable local")
        if len(p[2]) > 2 and len(p[2]) < 12:
            if p[5] == 'Num' and isinstance(p[7], int):
                variables_locales[p[2]] = [proc_en_analisis,p[5], p[7]]
            elif p[5] == 'Bool' and isinstance(p[7], bool):
                variables_locales[p[2]] = [proc_en_analisis,p[5], p[7]]
            else:
                syntax_errors.append(
                    f'Error en línea {p.lineno}, posición {p.lexpos}, valor dado no corresponde al tipado seleccionado')
        else:
            syntax_errors.append(
                f'Error en línea {p.lineno}, posición {p.lexpos}, tamaño de nombre de variable no cumple con el estándar')

def p_values(p):
    '''values : VALUES LPARENT ID COMA INTEGER RPARENT SEMICOLON
                 | VALUES LPARENT ID COMA BOOL RPARENT SEMICOLON
                 | VALUES LPARENT ID COMA return_statement RPARENT SEMICOLON'''
    if proc_en_analisis in called_procs or processingMaster:
        if p[3] in variables_locales:
            if isinstance(p[5], int) and variables_locales[p[3]][1] == 'Num':
                variables_locales[p[3]][2] = p[5]
            elif isinstance(p[5], bool) and variables_locales[p[3]][1] == 'Bool':
                variables_locales[p[3]][2] = p[5]
            else:
                syntax_errors.append(
                    f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado {p[3]}')
                return
            return variables_locales[p[3]][2]
        elif p[3] in variables_globales:
            if isinstance(p[5], int) and variables_globales[p[3]][0] == 'Num':
                variables_globales[p[3]][1] = p[5]
            elif isinstance(p[5], bool) and variables_globales[p[3]][0] == 'Bool':
                variables_globales[p[3]][1] = p[5]
            else:
                syntax_errors.append(
                    f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado {p[3]}')
                return
            return variables_globales[p[3]][1]
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

def p_call(p):
    '''call : CALL LPARENT ID RPARENT SEMICOLON'''
    if proc_en_analisis in called_procs or processingMaster:
        called_procs.append(p[3])

def find_local_variable_value(variable_name):
    for var_name, (var_proc,var_type, var_value) in variables_locales.items():
        if var_name == variable_name:
            return var_value
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

def p_printable_sentence_var(p):
    '''printable_sentence_var : ID '''
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_locales:
            print(find_local_variable_value(p[1]))
        elif p[1] in variables_globales:
            print(variables_globales[p[1]][1])
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[1]} no existe')

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
    if proc_en_analisis in called_procs or processingMaster:
        if p[5] == "ADD":
            if p[3] in variables_globales:
                if variables_globales[p[3]][0] == 'Num':
                    valor_actual = variables_globales[p[3]]
                    nuevo_valor = (valor_actual[0], valor_actual[1] + p[7])
                    variables_globales[p[3]] = nuevo_valor
                    return variables_globales[p[3]][1]
                else:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado {p[3]}')
            elif p[3] in variables_locales:
                for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                    if var_type == 'Num':
                        if var_name == p[3]:
                            if var_proc == proc_en_analisis:
                                valor_actual = variables_locales[p[3]]
                                nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] + p[7])
                                variables_locales[p[3]] = nuevo_valor
                                return variables_locales[p[3]][2]
                            elif index == len(variables_locales) - 1:
                                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                    elif index == len(variables_locales) - 1:
                        syntax_errors.append(
                            f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado {p[3]}')
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')
        elif p[5] == "SUB":
            if p[3] in variables_globales:
                if variables_globales[p[3]][0] == 'Num':
                    valor_actual = variables_globales[p[3]]
                    nuevo_valor = (valor_actual[0], valor_actual[1] - p[7])
                    variables_globales[p[3]] = nuevo_valor
                    return variables_globales[p[3]][1]
                else:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado {p[3]}')
            elif p[3] in variables_locales:
                for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                    if var_type == 'Num':
                        if var_name == p[3]:
                            if var_proc == proc_en_analisis:
                                valor_actual = variables_locales[p[3]]
                                nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] - p[7])
                                variables_locales[p[3]] = nuevo_valor
                                return variables_locales[p[3]][2]
                            elif index == len(variables_locales) - 1:
                                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                    elif index == len(variables_locales) - 1:
                        syntax_errors.append(
                            f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado {p[3]}')
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')
        elif p[5] == 'MUL':
            if p[3] in variables_globales:
                if variables_globales[p[3]][0] == 'Num':
                    valor_actual = variables_globales[p[3]]
                    nuevo_valor = (valor_actual[0], valor_actual[1] * p[7])
                    variables_globales[p[3]] = nuevo_valor
                    return variables_globales[p[3]][1]
                else:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado {p[3]}')
            elif p[3] in variables_locales:
                for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                    if var_type == 'Num':
                        if var_name == p[3]:
                            if var_proc == proc_en_analisis:
                                valor_actual = variables_locales[p[3]]
                                nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] * p[7])
                                variables_locales[p[3]] = nuevo_valor
                                return variables_locales[p[3]][2]
                            elif index == len(variables_locales) - 1:
                                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                    elif index == len(variables_locales) - 1:
                        syntax_errors.append(
                            f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado {p[3]}')
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')
        elif p[5] == 'DIV':
            if p[3] in variables_globales:
                if variables_globales[p[3]][0] == 'Num':
                    valor_actual = variables_globales[p[3]]
                    nuevo_valor = (valor_actual[0], valor_actual[1] / p[7])
                    variables_globales[p[3]] = nuevo_valor
                    return variables_globales[p[3]][1]
                else:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado {p[3]}')
            elif p[3] in variables_locales:
                for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                    if var_type == 'Num':
                        if var_name == p[3]:
                            if var_proc == proc_en_analisis:
                                valor_actual = variables_locales[p[3]]
                                nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] / p[7])
                                variables_locales[p[3]] = nuevo_valor
                                return variables_locales[p[3]][2]
                            elif index == len(variables_locales) - 1:
                                syntax_errors.append(
                                    f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                    elif index == len(variables_locales) - 1:
                        syntax_errors.append(
                            f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado {p[3]}')
            else:
                syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')
def p_alterB(p):
    '''alterB : ALTERB LPARENT ID RPARENT SEMICOLON'''
    if proc_en_analisis in called_procs or processingMaster:
        if p[3] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Bool':
                    if var_name == p[3]:
                        valor_actual = variables_globales[p[3]]
                        if var_value == True:
                            nuevo_valor = (valor_actual[0], False)
                            variables_globales[p[3]] = nuevo_valor
                            return False
                        else:
                            nuevo_valor = (valor_actual[0], True)
                            variables_globales[p[3]] = nuevo_valor
                            return True
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado {p[3]}')
        elif p[3] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_name == p[3]:
                    if var_type == 'Bool':
                        if var_proc == proc_en_analisis:
                            if var_value == True:
                                valor_actual = variables_locales[p[2]]
                                nuevo_valor = (valor_actual[0], valor_actual[1], False)
                                variables_locales[p[3]] = nuevo_valor
                                return False
                            else:
                                valor_actual = variables_locales[p[2]]
                                nuevo_valor = (valor_actual[0], valor_actual[1], True)
                                variables_locales[p[3]] = nuevo_valor
                                return True
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                    elif index == len(variables_locales) - 1:
                        syntax_errors.append(
                            f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[3]}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

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
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[1]}')
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
                            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: variable local no existe en proc {proc_en_analisis}')
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[1]}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[1]} no existe')

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
    if proc_en_analisis in called_procs or processingMaster:
        if p[3] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_name == p[3]:
                    if var_type == 'Bool':
                        if var_value:
                            print("True")
                            return True
                        else:
                            print("False")
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
    
