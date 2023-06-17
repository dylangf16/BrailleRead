import ply.yacc as yacc

import arduino
from Lex import tokens, lexer, lexical_errors
from arduino import manipulacion_arduino, consultar_motor
import time

# Dictionary of names
processingMaster = True
called_procs = []
procs = []
variables_locales = {}
variables_globales = {}
syntax_errors = []
print_resultados = []
master = 0
proc_en_analisis = ''

#Flags
while_flag = False
while_list = []
first_pasada = False
var_queValida_while = None

id_case = None
condition_flag = True
else_flag = False

repeat_flag = False
repeat_list = []

until_flag = False
until_list = []
var_queValida_until = None

values_flag = False
values_valor = None

comparisson_en_uso = None
valor_comparison = None

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
)

#Token inicial
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
    for call in called_procs:
        syntax_errors.append(
            f'Error: procedure no encontrado: {call}')

#Estado con token terminal para definir procedure actual
def p_declare_procedure(p):
    '''declare_procedure : PROC ID'''
    global procs, proc_en_analisis
    if p[2] not in procs:
        procs.append(p[2])
        print(str(p[2]) + " agregado a la lista de procs")
        proc_en_analisis = p[2]
    else:
        syntax_errors.append(f'- Proc con el nombre {p[2]} ya existe')
        raise SyntaxError()

#Recursividad para tener varios procedures
def p_procedures(p):
    '''procedures : procedure
                    | procedures procedure'''

#Formato declaracion de procedures con tokens no terminales
def p_procedure(p):
    '''procedure : declare_procedure LPARENT sentences RPARENT SEMICOLON'''
    # Acción semántica: Realizar las acciones correspondientes al análisis sintáctico
    # de un procedimiento
    if proc_en_analisis in called_procs:
        called_procs.remove(proc_en_analisis)
    p[0] = ('procedure', p[2], p[4])

#Formato para la funcion master
def p_master(p):
    '''master : MASTER LPARENT master_sentences RPARENT SEMICOLON'''
    # Acción semántica: Realizar las aciones correspondientes al análisis sintáctico de @Master

    global proc_en_analisis
    proc_en_analisis = '@Master'
    print("pasó master")
    global master, processingMaster
    master += 1
    if master != 1:
        syntax_errors.append(f'- Debe existir solamente un @Master')
        raise SyntaxError()
    processingMaster = False


# Recursividad para las sentencias dentro del master
def p_master_sentences(p):
    '''master_sentences : master_sentence
                        | master_sentences master_sentence'''
    if len(p) == 2:
        p[0] = [p[1]]  # Create a list with a single item
    else:
        p[0] = p[1] + [p[2]]  # Append the new item to the existing list


#Formato para todos los posibles procedures dentro de la funcion master
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
                       | sleep
                       | case
                       | while
                       | repeat
                       | until
                       | break
                       | empty'''
    p[0] = p[1]  # Assign the value of the matched alternative to p[0]

#Recursividad para la creacion de variables globales
def p_master_vars(p):
    '''master_vars : master_var
                    | master_vars master_var'''


#Formato de variables globales y su administracion
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
                f'- Variable Global: {p[2]} // valor dado no corresponde al tipado seleccionado')
            raise SyntaxError()

    else:
        syntax_errors.append(
            f'- Variable Global: {p[2]} // Nombre de variable tiene que ser entre 2 y 12 caracteres')
        raise SyntaxError()

# Recursividad para todas las sentencias
def p_sentences(p):
    '''sentences : sentence
                 | sentences sentence'''

#Todas las posibles sentencias que pueden haber dentro de un procedure
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
                | sleep
                | case
                | while
                | until
                | repeat
                | break
                | empty'''
    p[0] = p[1]

#Sentencias que retornan un valor, para asi poder utilizarlas dentro de otras
#sentencias de forma recursiva
def p_return_statement(p):
    '''return_statement : isTrue
                        | comparisson_maqequal
                        | comparisson_meqequal
                        | comparisson_dif
                        | comparisson_equal
                        | comparisson_meq
                        | comparisson_maq
                        | alterB
                        | alter
                        | viewsignal'''

#Funcion auxiliar del la p_function para variables locales
#Crea y almacena las variables locales en una lista en tuplas con le formato:
# [nombre variable]: {Procedure en el que esta, tipo de variable, valor}
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
                    f'- Error en procedure: {proc_en_analisis} // Variable Local: {id} // valor dado no corresponde al tipado seleccionado')
                raise SyntaxError()
        else:
            syntax_errors.append(
                f'- Error en procedure: {proc_en_analisis} // Variable local: {id}  // Nombre de variable tiene que ser entre 2 y 12 caracteres')
            raise SyntaxError()
    else:
        syntax_errors.append(
            f'- Error en procedure: {proc_en_analisis}, definicion multiple de variable local: {id}')
        raise SyntaxError()


# Estructura en el diccionario de variables locales
# contiene todos los flags necesarios para lidiar con ellas en while, until, case y repeat
def p_local_variable(p):
    '''local_variable : NEW ID COMA LPARENT TYPE COMA INTEGER RPARENT SEMICOLON
                | NEW ID COMA LPARENT TYPE COMA BOOL RPARENT SEMICOLON
                | NEW ID COMA LPARENT TYPE COMA STRING RPARENT SEMICOLON'''
    global condition_flag, while_flag, while_list, first_pasada, repeat_flag, repeat_list, until_flag, until_list
    id = p[2]
    type = p[5]
    value = p[7]

    if first_pasada:
        if while_flag and (lambda: local_variable_aux not in while_list):
            while_list.append(lambda: local_variable_aux(id, type, value))
        if repeat_flag and (lambda: local_variable_aux not in repeat_list):
            repeat_list.append(lambda: local_variable_aux(id, type, value))
        if until_flag and (lambda: local_variable_aux not in until_list):
            until_list.append(lambda: local_variable_aux(id, type, value))
            local_variable_aux(id, type, value)

    elif condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            local_variable_aux(id, type, value)

# Funcion auxiliar de la p_function de values
# Hace la verificacion necesaria para cambiar el valor de una variable
# Y en caso de cumplir condiciones cambia el valor de la variable
# Altera los flags de las condicionales para que funcionen acorde al values
def values_aux(id, value):
    global condition_flag, values_flag, values_valor, comparisson_en_uso, valor_comparison, while_flag, until_flag
    if condition_flag:
        print(f'Valor en Values: {values_valor}')
        print(f'Estado flag values: {values_flag}')
        if isinstance(values_valor, int) or isinstance(values_valor, bool):
            value = values_valor
        print(f'Valor de: {id} anterior a cambio: {value}')
        print(type(value))
        if condition_flag:
            if id in variables_locales:
                if isinstance(value, int) and variables_locales[id][1] == 'Num':
                    variables_locales[id][2] = value
                    values_valor = None
                    values_flag = False
                    print(f'Valor de: {id} después del cambio: {variables_locales[id][2]}')
                    if comparisson_en_uso == "MAQ":
                        if variables_locales[id][2] <= valor_comparison:
                            while_flag = False
                            until_flag = False
                    if comparisson_en_uso == "MEQ":
                        if variables_locales[id][2] >= valor_comparison:
                            while_flag = False
                            until_flag = False
                    if comparisson_en_uso == "EQUAL":
                        if variables_locales[id][2] != valor_comparison:
                            while_flag = False
                            until_flag = False
                    if comparisson_en_uso == "DIFF":
                        if variables_locales[id][2] == valor_comparison:
                            while_flag = False
                            until_flag = False
                    if comparisson_en_uso == "MAQEQUAL":
                        if variables_locales[id][2] < valor_comparison:
                            while_flag = False
                            until_flag = False
                    if comparisson_en_uso == "MEQEQUAL":
                        if variables_locales[id][2] > valor_comparison:
                            while_flag = False
                            until_flag = False
                elif isinstance(value, bool) and variables_locales[id][1] == 'Bool':
                    variables_locales[id][2] = value
                    values_valor = None
                    values_flag = False
                    print(f'Valor de: {id} después del cambio: {variables_locales[id][2]}')
                elif isinstance(value, str) and variables_locales[id][1] == 'Str':
                    variables_locales[id][2] = value
                    values_valor = None
                    values_flag = False
                    print(f'Valor de: {id} después del cambio: {variables_locales[id][2]}')
                else:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Values // variable local: {id} // valor dado no corresponde al tipado')
                    raise SyntaxError()
                return variables_locales[id][2]

            elif id in variables_globales:
                if isinstance(value, int) and variables_globales[id][0] == 'Num':
                    variables_globales[id][1] = value
                    values_valor = None
                    values_flag = False
                    print(f'Valor de: {id} después del cambio: {variables_globales[id][1]}')
                    if comparisson_en_uso == "MAQ":
                        if variables_globales[id][1] <= valor_comparison:
                            while_flag = False
                            until_flag = False
                    if comparisson_en_uso == "MEQ":
                        if variables_globales[id][1] >= valor_comparison:
                            while_flag = False
                            until_flag = False
                    if comparisson_en_uso == "EQUAL":
                        if variables_globales[id][1] != valor_comparison:
                            while_flag = False
                            until_flag = False
                    if comparisson_en_uso == "DIFF":
                        if variables_globales[id][1] == valor_comparison:
                            while_flag = False
                            until_flag = False
                    if comparisson_en_uso == "MAQEQUAL":
                        if variables_globales[id][1] < valor_comparison:
                            while_flag = False
                            until_flag = False
                    if comparisson_en_uso == "MEQEQUAL":
                        if variables_globales[id][1] > valor_comparison:
                            while_flag = False
                            until_flag = False
                elif isinstance(value, bool) and variables_globales[id][0] == 'Bool':
                    variables_globales[id][1] = value
                    values_valor = None
                    values_flag = False
                    print(f'Valor de: {id} después del cambio: {variables_globales[id][1]}')
                elif isinstance(value, str) and variables_globales[id][0] == 'Str':
                    variables_globales[id][1] = value
                    values_valor = None
                    values_flag = False
                    print(f'Valor de: {id} después del cambio: {variables_globales[id][1]}')
                else:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Values // variable global: {id} // valor dado no corresponde al tipado')
                    raise SyntaxError()
                return variables_globales[id][1]
            else:
                syntax_errors.append(
                    f'- Error en procedure: {proc_en_analisis} // Sentencia Values // Variable: {id} no existe')
                raise SyntaxError()

# Estructura de de Values, ya sea con valores terminales o con la otras funciones dentro
# Contiene todos los flags necesarios para lidiar con values en while, until, case y repeat
def p_values(p):
    '''values : value LPARENT ID COMA INTEGER RPARENT SEMICOLON
                 | value LPARENT ID COMA BOOL RPARENT SEMICOLON
                 | value LPARENT ID COMA return_statement RPARENT SEMICOLON'''
    global condition_flag, while_flag, while_list, first_pasada, repeat_flag, repeat_list, until_flag, until_list
    id = p[3]
    new_value = p[5]
    if first_pasada:
        if while_flag and (lambda: values_aux not in while_list):
            while_list.append(lambda: values_aux(id, new_value))

        if repeat_flag and (lambda: values_aux not in repeat_list):
            repeat_list.append(lambda: values_aux(id, repeat_list))

        if until_flag and (lambda: values_aux not in until_list):
            until_list.append(lambda: values_aux(id, until_list))
            values_aux(id, until_list)

    elif condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            values_aux(id, new_value)

#Se usa para permitir que hayan funciones dentro de un values
def p_values_handler(p):
    '''value : VALUES'''
    global values_flag
    values_flag = True

#Agrega el procedure llamado a una lista de procedures
#A la hora de alcanzar el procedure solo se recorre si se encuentra dentro de esta lista
def p_call(p):
    '''call : CALL LPARENT ID RPARENT SEMICOLON'''
    if proc_en_analisis in called_procs or processingMaster:
        called_procs.append(p[3])

#Fucion para encontrar el valor de una variable local
#Recibe el nombre de la variable y la busca dentro de la lista del variables locales
def find_local_variable_value(variable_name):
    for var_name, (var_proc, var_type, var_value) in variables_locales.items():
        if var_name == variable_name:
            return var_value
    return None  # Variable not found

#Fucion para encontrar el valor de una variable global
#Recibe el nombre de la variable y la busca dentro de la lista del variables globales
def find_global_variable_value(variable_name):
    for var_name, var_value in variables_globales.items():
        if var_name == variable_name:
            # print(f'Variable GLOBAL buscada: {var_name} // Valor: {var_value}')
            return var_value[1]
    return None  # Variable not found

#Estructura del printValues
def p_print_values(p):
    '''print_values : PRINTVALUES LPARENT printable_sentences RPARENT SEMICOLON'''


#Todas las posibles combinaciones de un printValues y su recursividad
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

#Funcion auxiliar del p_function printValues para variables
#Busca la variable en globales y locales para imprimir su valor
def printable_sentence_var_aux(id):
    global condition_flag
    if condition_flag:
        if id in variables_locales:
            print(find_local_variable_value(id))
            print_resultados.append(str(find_local_variable_value(id)))
        elif id in variables_globales:
            print(find_global_variable_value(id))
            print_resultados.append(str(find_global_variable_value(id)))
        else:
            syntax_errors.append(
                f'- Error en procedure: {proc_en_analisis} // Sentencia PrintValues // variable: {id} no existe')
            raise SyntaxError()

# Estructura con token terminal para el printValues de una variable
# Contiene todos los flags necesarios para lidiar con ellas en while, until, case y repeat
def p_printable_sentence_var(p):
    '''printable_sentence_var : ID '''
    global condition_flag, while_flag, while_list, first_pasada, repeat_flag, repeat_list, until_flag, until_list
    id = p[1]
    if first_pasada:
        if while_flag and (lambda: printable_sentence_var_aux not in while_list):
            while_list.append(lambda: printable_sentence_var_aux(id))

        if repeat_flag and (lambda: printable_sentence_var_aux not in repeat_list):
            repeat_list.append(lambda: printable_sentence_var_aux(id))

        if until_flag and (lambda: printable_sentence_var_aux not in until_list):
            until_list.append(lambda: printable_sentence_var_aux(id))
            printable_sentence_var_aux(id)

    elif condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            printable_sentence_var_aux(p[1])

# Funcion auxiliar del p_function printValues para strings
# Imprime el valor del string
def printable_sentence_string_aux(id):
    global condition_flag
    if condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            print(id)
            print_resultados.append(str(id))

# Estructura con token terminal para el printValues de un string
# Contiene todos los flags necesarios para lidiar con ellas en while, until, case y repeat
def p_printable_sentence_string(p):
    '''printable_sentence_string : STRING '''
    global condition_flag, while_flag, while_list, first_pasada, repeat_flag, repeat_list, until_flag, until_list, var_queValida_while, var_queValida_until
    string = p[1]
    if first_pasada:
        if while_flag and (lambda: printable_sentence_string_aux not in while_list):
            while_list.append(lambda: printable_sentence_string_aux(string))
        if repeat_flag and (lambda: printable_sentence_string_aux not in repeat_list):
            repeat_list.append(lambda: printable_sentence_string_aux(string))
        if until_flag and (lambda: printable_sentence_string_aux not in until_list):
            until_list.append(lambda: printable_sentence_string_aux(string))
            printable_sentence_string_aux(string)
    elif condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            printable_sentence_string_aux(p[1])

# Fucion auxiliar para la p_function de alter
# Hace todas las verificaciones necesarias y cambia el valor de la variable dependiendo
# de la accion recibida
def alter_aux(id, action, integer):
    global condition_flag, values_flag, values_valor
    if condition_flag:
        if action == "ADD":
            if id in variables_globales:
                if variables_globales[id][0] == 'Num':
                    valor_actual = variables_globales[id]
                    nuevo_valor = (valor_actual[0], valor_actual[1] + integer)
                    variables_globales[id] = nuevo_valor
                    if values_flag:
                        values_valor = variables_globales[id][1]
                    return variables_globales[id][1]
                else:
                    syntax_errors.append(
                        f'- Error en procedure {proc_en_analisis} // Sentencia Alter // valor dado no corresponde al tipado {id}')
            elif id in variables_locales:
                for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                    if var_type == 'Num':
                        if var_name == id:
                            if var_proc == proc_en_analisis:
                                valor_actual = variables_locales[id]
                                nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] + integer)
                                variables_locales[id] = nuevo_valor
                                if values_flag:
                                    values_valor = variables_locales[id][2]
                                return variables_locales[id][2]
                            elif index == len(variables_locales) - 1:
                                syntax_errors.append(
                                    f'- Error en procedure: {proc_en_analisis} // Sentencia Alter // variable local: {id} no existe')
                                raise SyntaxError()
                    elif index == len(variables_locales) - 1:
                        syntax_errors.append(
                            f'- Error en procedure {proc_en_analisis} // Sentencia Alter // valor dado no corresponde al tipado {id}')
                        raise SyntaxError()
            else:
                syntax_errors.append(
                    f'- Error en procedure {proc_en_analisis} // Sentencia Alter // variable: {id} no existe')
                raise SyntaxError()

        elif action == "SUB":
            if id in variables_globales:
                if variables_globales[id][0] == 'Num':
                    valor_actual = variables_globales[id]
                    nuevo_valor = (valor_actual[0], valor_actual[1] - integer)
                    variables_globales[id] = nuevo_valor
                    if values_flag:
                        values_valor = variables_globales[id][1]
                    return variables_globales[id][1]
                else:
                    syntax_errors.append(
                        f'- Error en procedure {proc_en_analisis} // Sentencia Alter // valor dado no corresponde al tipado {id}')
                    raise SyntaxError()
            elif id in variables_locales:
                for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                    if var_type == 'Num':
                        if var_name == id:
                            if var_proc == proc_en_analisis:
                                valor_actual = variables_locales[id]
                                nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] - integer)
                                variables_locales[id] = nuevo_valor
                                if values_flag:
                                    values_valor = variables_locales[id][2]
                                return variables_locales[id][2]
                            elif index == len(variables_locales) - 1:
                                syntax_errors.append(
                                    f'- Error en procedure: {proc_en_analisis} // Sentencia Alter // variable local: {id} no existe')
                                raise SyntaxError()
                    elif index == len(variables_locales) - 1:
                        syntax_errors.append(
                            f'- Error en procedure {proc_en_analisis} // Sentencia Alter // valor dado no corresponde al tipado {id}')
                        raise SyntaxError()
            else:
                syntax_errors.append(
                    f'- Error en procedure {proc_en_analisis} // Sentencia Alter // variable: {id} no existe')
                raise SyntaxError()

        elif action == 'MUL':
            if id in variables_globales:
                if variables_globales[id][0] == 'Num':
                    valor_actual = variables_globales[id]
                    nuevo_valor = (valor_actual[0], valor_actual[1] * integer)
                    variables_globales[id] = nuevo_valor
                    if values_flag:
                        values_valor = variables_globales[id][1]
                    return variables_globales[id][1]
                else:
                    syntax_errors.append(
                        f'- Error en procedure {proc_en_analisis} // Sentencia Alter // valor dado no corresponde al tipado {id}')
                    raise SyntaxError()
            elif id in variables_locales:
                for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                    if var_type == 'Num':
                        if var_name == id:
                            if var_proc == proc_en_analisis:
                                valor_actual = variables_locales[id]
                                nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] * integer)
                                variables_locales[id] = nuevo_valor
                                if values_flag:
                                    values_valor = variables_locales[id][2]
                                return variables_locales[id][2]
                            elif index == len(variables_locales) - 1:
                                syntax_errors.append(
                                    f'- Error en procedure: {proc_en_analisis} // Sentencia Alter // variable local: {id} no existe')
                                raise SyntaxError()
                    elif index == len(variables_locales) - 1:
                        syntax_errors.append(
                            f'- Error en procedure {proc_en_analisis} // Sentencia Alter // valor dado no corresponde al tipado {id}')
                        raise SyntaxError()
            else:
                syntax_errors.append(
                    f'- Error en procedure {proc_en_analisis} // Sentencia Alter // variable: {id} no existe')
                raise SyntaxError()

        elif action == 'DIV':
            if id in variables_globales:
                if variables_globales[id][0] == 'Num':
                    valor_actual = variables_globales[id]
                    nuevo_valor = (valor_actual[0], valor_actual[1] / integer)
                    variables_globales[id] = nuevo_valor
                    if values_flag:
                        values_valor = variables_globales[id][1]
                    return variables_globales[id][1]
                else:
                    syntax_errors.append(
                        f'- Error en procedure {proc_en_analisis} // Sentencia Alter // valor dado no corresponde al tipado {id}')
                    raise SyntaxError()
            elif id in variables_locales:
                for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                    if var_type == 'Num':
                        if var_name == id:
                            if var_proc == proc_en_analisis:
                                valor_actual = variables_locales[id]
                                nuevo_valor = (valor_actual[0], valor_actual[1], valor_actual[2] / integer)
                                variables_locales[id] = nuevo_valor
                                if values_flag:
                                    values_valor = variables_locales[id][2]
                                return variables_locales[id][2]
                            elif index == len(variables_locales) - 1:
                                syntax_errors.append(
                                    f'- Error en procedure: {proc_en_analisis} // Sentencia Alter // variable local: {id} no existe')
                                raise SyntaxError()
                    elif index == len(variables_locales) - 1:
                        syntax_errors.append(
                            f'- Error en procedure {proc_en_analisis} // Sentencia Alter // valor dado no corresponde al tipado {id}')
                        raise SyntaxError()
            else:
                syntax_errors.append(
                    f'- Error en procedure {proc_en_analisis} // Sentencia Alter // variable: {id} no existe')
                raise SyntaxError()


# Estructura en el diccionario para el Alter
# Contiene todos los flags necesarios para lidiar con ellas en while, until, case y repeat
def p_alter(p):
    '''alter : ALTER LPARENT ID COMA ADD COMA INTEGER RPARENT SEMICOLON
                | ALTER LPARENT ID COMA SUB COMA INTEGER RPARENT SEMICOLON
                | ALTER LPARENT ID COMA MUL COMA INTEGER RPARENT SEMICOLON
                | ALTER LPARENT ID COMA DIV COMA INTEGER RPARENT SEMICOLON'''
    global condition_flag, while_flag, while_list, first_pasada, repeat_flag, repeat_list, until_flag, until_list
    id = p[3]
    action = p[5]
    integer = p[7]
    if first_pasada:
        if while_flag and (lambda: alter_aux not in while_list):
            while_list.append(lambda: alter_aux(id, action, integer))

        if repeat_flag and (lambda: alter_aux not in repeat_list):
            repeat_list.append(lambda: alter_aux(id, action, integer))

        if until_flag and (lambda: alter_aux not in until_list):
            until_list.append(lambda: alter_aux(id, action, integer))
            alter_aux(id, action, integer)

    elif condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            alter_aux(id, action, integer)

# Funcion auxiliar para la p_function alterB
# Hace la validacion necesaria y cambia el valor de un bool por opuesto
def alterB_aux(id):
    global while_flag, var_queValida_while, until_flag, var_queValida_until, values_flag, values_valor
    if condition_flag:
        if id in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Bool':
                    if var_name == id:
                        valor_actual = variables_globales[id]
                        if var_value:
                            nuevo_valor = (valor_actual[0], False)
                            variables_globales[id] = nuevo_valor
                            if values_flag:
                                values_valor = False
                            if var_queValida_while == var_name:
                                print(f'Reinicio de while, variable que valida: {var_name}')
                                while_flag = False
                            elif var_queValida_until == var_name:
                                print(f'Reinicio de until, variable que valida: {var_name}')
                                until_flag = False
                            return False
                        else:
                            nuevo_valor = (valor_actual[0], True)
                            if values_flag:
                                values_valor = True
                            variables_globales[id] = nuevo_valor
                            return True
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia AlterB // valor dado no corresponde al tipado {id}')
                    raise SyntaxError()

        elif id in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_name == id:
                    if var_type == 'Bool':
                        if var_proc == proc_en_analisis:
                            if var_value:
                                valor_actual = variables_locales[id]
                                nuevo_valor = (valor_actual[0], valor_actual[1], False)
                                variables_locales[id] = nuevo_valor
                                if values_flag:
                                    values_valor = False
                                if var_queValida_while == var_name:
                                    while_flag = False
                                elif var_queValida_until == var_name:
                                    print(f'Reinicio de until, variable que valida: {var_name}')
                                    until_flag = False
                                return False
                            else:
                                valor_actual = variables_locales[id]
                                nuevo_valor = (valor_actual[0], valor_actual[1], True)
                                variables_locales[id] = nuevo_valor
                                if values_flag:
                                    values_valor = True
                                return True
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'- Error en procedure: {proc_en_analisis} // Sentencia AlterB // variable local no existe en proc')
                            raise SyntaxError()
                    elif index == len(variables_locales) - 1:
                        syntax_errors.append(
                            f'- Error en procedure: {proc_en_analisis} // Sentencia AlterB // valor dado no corresponde al tipado seleccionado {id}')
                        raise SyntaxError()
        else:
            syntax_errors.append(
                f'- Error en procedure: {proc_en_analisis} // Sentencia AlterB // Variable: {id} no existe')
            raise SyntaxError()

# Estructura del alterB
# Contiene todos los flags necesarios para lidiar con el bool en while, until, case y repeat
def p_alterB(p):
    '''alterB : ALTERB LPARENT ID RPARENT SEMICOLON'''
    global condition_flag, while_flag, while_list, first_pasada, repeat_flag, repeat_list, until_flag, until_list
    var = p[3]
    if first_pasada:
        if while_flag and (lambda: alterB_aux not in while_list):
            while_list.append(lambda: alterB_aux(var))

        if repeat_flag and (lambda: alterB_aux not in repeat_list):
            repeat_list.append(lambda: alterB_aux(var))

        if until_flag and (lambda: alterB_aux not in until_list):
            until_list.append(lambda: alterB_aux(var))
            alterB_aux(var)

    elif condition_flag:
        if proc_en_analisis in called_procs or processingMaster:
            alterB_aux(var)

# Estructura de comparacion del mayor que
# retorna True si se cumple que el ID es mayor que el numero y False de lo contrario
def p_comparisson_maq(p):
    '''comparisson_maq : ID MAQ INTEGER'''
    global condition_flag, while_flag, first_pasada, var_queValida_while, until_flag, var_queValida_until, values_flag, values_valor, comparisson_en_uso, valor_comparison
    comparisson_en_uso = "MAQ"
    valor_comparison = p[3]
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_value > p[3]:
                            print(True)
                            if values_flag:
                                values_valor = True

                            if while_flag:
                                first_pasada = True
                                var_queValida_while = var_name
                                print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')

                            if until_flag:
                                first_pasada = True
                                var_queValida_until = var_name
                                print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                            return True
                        else:
                            print(False)
                            if values_flag:
                                values_valor = False

                            if while_flag:
                                condition_flag = False
                                first_pasada = False
                                while_flag = False

                            if until_flag:
                                condition_flag = False
                                first_pasada = False
                                until_flag = False
                            return False
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MAQ // valor dado no corresponde al tipado seleccionado {p[1]}')
                    raise SyntaxError()
        elif p[1] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_proc == proc_en_analisis:
                            if var_value > p[3]:
                                print(True)
                                if values_flag:
                                    values_valor = True

                                if while_flag:
                                    first_pasada = True
                                    var_queValida_while = var_name
                                    print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')

                                if until_flag:
                                    first_pasada = True
                                    var_queValida_until = var_name
                                    print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                                return True
                            else:
                                print(False)
                                if values_flag:
                                    values_valor = False

                                if while_flag:
                                    condition_flag = False
                                    first_pasada = False
                                    while_flag = False

                                if until_flag:
                                    condition_flag = False
                                    first_pasada = False
                                    until_flag = False
                                return False
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MAQ // variable local no existe en proc')
                            raise SyntaxError()
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MAQ // valor dado no corresponde al tipado seleccionado {p[1]}')
                    raise SyntaxError()
        else:
            syntax_errors.append(
                f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MAQ // Variable: {p[1]} no existe')
            raise SyntaxError()

# Estructura de comparacion del menor que
# retorna True si se cumple que el ID es menor que el numero y False de lo contrario
def p_comparisson_meq(p):
    '''comparisson_meq : ID MEQ INTEGER'''

    global condition_flag, while_flag, first_pasada, var_queValida_while, until_flag, var_queValida_until, values_flag, values_valor, comparisson_en_uso, valor_comparison
    comparisson_en_uso = "MEQ"
    valor_comparison = p[3]
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_value < p[3]:
                            print(True)
                            if values_flag:
                                values_valor = True
                            if while_flag:
                                first_pasada = True
                                var_queValida_while = var_name
                                print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')

                            if until_flag:
                                first_pasada = True
                                var_queValida_until = var_name
                                print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                            return True
                        else:
                            print(False)
                            if values_flag:
                                values_valor = False
                            if while_flag:
                                condition_flag = False
                                first_pasada = False
                                while_flag = False

                            if until_flag:
                                condition_flag = False
                                first_pasada = False
                                until_flag = False
                            return False
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MEQ // valor dado no corresponde al tipado seleccionado {p[1]}')
                    raise SyntaxError()
        elif p[1] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_proc == proc_en_analisis:
                            if var_value < p[3]:
                                print(True)
                                if values_flag:
                                    values_valor = True
                                if while_flag:
                                    first_pasada = True
                                    var_queValida_while = var_name
                                    print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')

                                if until_flag:
                                    first_pasada = True
                                    var_queValida_until = var_name
                                    print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                                return True
                            else:
                                print(False)
                                if values_flag:
                                    values_valor = False
                                if while_flag:
                                    condition_flag = False
                                    first_pasada = False
                                    while_flag = False

                                if until_flag:
                                    condition_flag = False
                                    first_pasada = False
                                    until_flag = False
                                return False
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MEQ // variable local no existe')
                            raise SyntaxError()
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MEQ // valor dado no corresponde al tipado seleccionado')
                    raise SyntaxError()
        else:
            syntax_errors.append(
                f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MEQ // Variable: {p[1]} no existe')
            raise SyntaxError()

# Estructura de comparacion del igual que
# retorna True si se cumple que el ID es igual que el numero y False de lo contrario
def p_comparisson_equal(p):
    '''comparisson_equal : ID EQUAL INTEGER'''

    global condition_flag, while_flag, first_pasada, var_queValida_while, until_flag, var_queValida_until, values_flag, values_valor, comparisson_en_uso, valor_comparison

    comparisson_en_uso = "EQUAL"
    valor_comparison = p[3]
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_value == p[3]:
                            print(True)
                            if values_flag:
                                values_valor = True
                            if while_flag:
                                first_pasada = True
                                var_queValida_while = var_name
                                print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')

                            if until_flag:
                                first_pasada = True
                                var_queValida_until = var_name
                                print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                            return True
                        else:
                            print(False)
                            if values_flag:
                                values_valor = False

                            if while_flag:
                                condition_flag = False
                                first_pasada = False
                                while_flag = False

                            if until_flag:
                                condition_flag = False
                                first_pasada = False
                                until_flag = False
                            return False
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson EQUAL // valor dado no corresponde al tipado seleccionado {p[1]}')
                    raise SyntaxError()
        elif p[1] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_proc == proc_en_analisis:
                            if var_value == p[3]:
                                print(True)
                                if values_flag:
                                    values_valor = True
                                if while_flag:
                                    first_pasada = True
                                    var_queValida_while = var_name
                                    print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')

                                if until_flag:
                                    first_pasada = True
                                    var_queValida_until = var_name
                                    print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                                return True
                            else:
                                print(False)
                                if values_flag:
                                    values_valor = False
                                if while_flag:
                                    condition_flag = False
                                    first_pasada = False
                                    while_flag = False

                                if until_flag:
                                    condition_flag = False
                                    first_pasada = False
                                    until_flag = False
                                return False
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson EQUAL // variable local no existe')
                            raise SyntaxError()
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson EQUAL // valor dado no corresponde al tipado seleccionado {p[1]}')
                    raise SyntaxError()
        else:
            syntax_errors.append(
                f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson EQUAL // Variable: {p[1]} no existe')
            raise SyntaxError()

# Estructura de comparacion del diferente que
# retorna True si se cumple que el ID es diferente que el numero y False de lo contrario
def p_comparisson_dif(p):
    '''comparisson_dif : ID DIFFERENT INTEGER'''

    global condition_flag, while_flag, first_pasada, var_queValida_while, until_flag, var_queValida_until, values_flag, values_valor, comparisson_en_uso, valor_comparison

    comparisson_en_uso = "DIFF"
    valor_comparison = p[3]
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_value != p[3]:
                            print(True)
                            if values_flag:
                                values_valor = True
                            if while_flag:
                                first_pasada = True
                                var_queValida_while = var_name
                                print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')

                            if until_flag:
                                first_pasada = True
                                var_queValida_until = var_name
                                print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                            return True
                        else:
                            print(False)
                            if values_flag:
                                values_valor = False
                            if while_flag:
                                condition_flag = False
                                first_pasada = False
                                while_flag = False

                            if until_flag:
                                condition_flag = False
                                first_pasada = False
                                until_flag = False
                            return False
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson DIF // valor dado no corresponde al tipado seleccionado {p[1]}')
                    raise SyntaxError()
        elif p[1] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_proc == proc_en_analisis:
                            if var_value != p[3]:
                                print(True)
                                if values_flag:
                                    values_valor = True
                                if while_flag:
                                    first_pasada = True
                                    var_queValida_while = var_name
                                    print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')

                                if until_flag:
                                    first_pasada = True
                                    var_queValida_until = var_name
                                    print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                                return True
                            else:
                                print(False)
                                if values_flag:
                                    values_valor = False
                                if while_flag:
                                    condition_flag = False
                                    first_pasada = False
                                    while_flag = False

                                if until_flag:
                                    condition_flag = False
                                    first_pasada = False
                                    until_flag = False
                                return False
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson DIF // variable local no existe')
                            raise SyntaxError()
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson DIF // valor dado no corresponde al tipado seleccionado {p[1]}')
                    raise SyntaxError()
        else:
            syntax_errors.append(
                f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson DIF // Variable: {p[1]} no existe')
            raise SyntaxError()

# Estructura de comparacion del menor o igual que
# retorna True si se cumple que el ID es menor o igual que el numero y False de lo contrario
def p_comparisson_meqequal(p):
    '''comparisson_meqequal : ID MEQEQUAL INTEGER'''

    global condition_flag, while_flag, first_pasada, var_queValida_while, until_flag, var_queValida_until, values_flag, values_valor, comparisson_en_uso, valor_comparison

    comparisson_en_uso = "MEQEQUAL"
    valor_comparison = p[3]
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_value <= p[3]:
                            print(True)
                            if values_flag:
                                values_valor = True
                            if while_flag:
                                first_pasada = True
                                var_queValida_while = var_name
                                print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')

                            if until_flag:
                                first_pasada = True
                                var_queValida_until = var_name
                                print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                            return True
                        else:
                            print(False)
                            if values_flag:
                                values_valor = False
                            if while_flag:
                                condition_flag = False
                                first_pasada = False
                                while_flag = False

                            if until_flag:
                                condition_flag = False
                                first_pasada = False
                                until_flag = False
                            return False
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MEQEQUAL // valor dado no corresponde al tipado seleccionado {p[1]}')
                    raise SyntaxError()
        elif p[1] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_proc == proc_en_analisis:
                            if var_value <= p[3]:
                                print(True)
                                if values_flag:
                                    values_valor = True
                                if while_flag:
                                    first_pasada = True
                                    var_queValida_while = var_name
                                    print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')

                                if until_flag:
                                    first_pasada = True
                                    var_queValida_until = var_name
                                    print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                                return True
                            else:
                                print(False)
                                if values_flag:
                                    values_valor = False
                                if while_flag:
                                    condition_flag = False
                                    first_pasada = False
                                    while_flag = False

                                if until_flag:
                                    condition_flag = False
                                    first_pasada = False
                                    until_flag = False
                                return False
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MEQEQUAL // variable local no existe')
                            raise SyntaxError()
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MEQEQUAL // valor dado no corresponde al tipado seleccionado {p[1]}')
                    raise SyntaxError()
        else:
            syntax_errors.append(
                f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MEQEQUAL //: Variable: {p[1]} no existe')
            raise SyntaxError()

# Estructura de comparacion del mayor o igual que
# retorna True si se cumple que el ID es mayor o igual que el numero y False de lo contrario
def p_comparisson_maqequal(p):
    '''comparisson_maqequal : ID MAQEQUAL INTEGER'''
    global condition_flag, while_flag, first_pasada, var_queValida_while, until_flag, var_queValida_until, values_flag, values_valor, comparisson_en_uso, valor_comparison
    comparisson_en_uso = "MAQEQUAL"
    valor_comparison = p[3]
    if proc_en_analisis in called_procs or processingMaster:
        if p[1] in variables_globales:
            for index, (var_name, (var_type, var_value)) in enumerate(variables_globales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_value >= p[3]:
                            print(True)
                            if values_flag:
                                values_valor = True
                            if while_flag:
                                first_pasada = True
                                var_queValida_while = var_name
                                print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')

                            if until_flag:
                                first_pasada = True
                                var_queValida_until = var_name
                                print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                            return True
                        else:
                            print(False)
                            if values_flag:
                                values_valor = False
                            if while_flag:
                                condition_flag = False
                                first_pasada = False
                                while_flag = False

                            if until_flag:
                                condition_flag = False
                                first_pasada = False
                                until_flag = False
                            return False
                elif index == len(variables_globales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MAQEQUAL // valor dado no corresponde al tipado seleccionado {p[1]}')
                    raise SyntaxError()
        elif p[1] in variables_locales:
            for index, (var_name, (var_proc, var_type, var_value)) in enumerate(variables_locales.items()):
                if var_type == 'Num':
                    if var_name == p[1]:
                        if var_proc == proc_en_analisis:
                            if var_value >= p[3]:
                                print(True)
                                if values_flag:
                                    values_valor = True
                                if while_flag:
                                    first_pasada = True
                                    var_queValida_while = var_name
                                    print(f'Inicio primera pasada // Var que valida while: {var_queValida_while}')

                                if until_flag:
                                    first_pasada = True
                                    var_queValida_until = var_name
                                    print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                                return True
                            else:
                                print(False)
                                if values_flag:
                                    values_valor = False
                                if while_flag:
                                    condition_flag = False
                                    first_pasada = False
                                    while_flag = False

                                if until_flag:
                                    condition_flag = False
                                    first_pasada = False
                                    until_flag = False
                                return False
                        elif index == len(variables_locales) - 1:
                            syntax_errors.append(
                                f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MAQEQUAL // variable local no existe')
                            raise SyntaxError()
                elif index == len(variables_locales) - 1:
                    syntax_errors.append(
                        f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MAQEQUAL // valor dado no corresponde al tipado seleccionado {p[1]}')
                    raise SyntaxError()
        else:
            syntax_errors.append(
                f'- Error en procedure: {proc_en_analisis} // Sentencia Comparisson MAQEQUAL // Variable: {p[1]} no existe')
            raise SyntaxError()

# Estructura del isTrue
# Hace las verificaciones necesarias
# Busca la variable en globales y locales
# Retorna true si la variable es True y False de lo contrario
def p_isTrue(p):
    '''isTrue : ISTRUE LPARENT ID RPARENT SEMICOLON'''

    global condition_flag, while_flag, first_pasada, var_queValida_while, until_flag, var_queValida_until
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

                            if until_flag:
                                first_pasada = True
                                var_queValida_until = var_name
                                print(f'Inicio primera pasada // Var que valida Until: {var_queValida_until}')
                            return True
                        else:
                            print("False")
                            if while_flag:
                                condition_flag = False
                                first_pasada = False
                                while_flag = False

                            if until_flag:
                                condition_flag = False
                                first_pasada = False
                                until_flag = False
                            return False
                    elif index == len(variables_globales) - 1:
                        syntax_errors.append(
                            f'- Error en procedure: {proc_en_analisis} // Sentencia IsTrue // valor dado no corresponde al tipado seleccionado {p[3]}')
                        raise SyntaxError()
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
                            f'- Error en procedure: {proc_en_analisis} // Sentencia IsTrue // variable local no existe en proc {proc_en_analisis}')
                        raise SyntaxError()
        else:
            syntax_errors.append(
                f'- Error en procedure: {proc_en_analisis} // Sentencia IsTrue // Variable: {p[3]} no existe')
            raise SyntaxError()

# Estructura de la p_function SIGNAL
# Contiene todos los flags necesarios para lidiar con ellas en while, until, case y repeat
# Llama la funcion de signal_handler en caso de cumplir con las condiciones
def p_signal(p):
    '''signal : SIGNAL LPARENT INTEGER COMA INTEGER RPARENT SEMICOLON
            | SIGNAL LPARENT ID COMA INTEGER RPARENT SEMICOLON'''
    global condition_flag, while_flag, while_list, first_pasada, proc_en_analisis, repeat_list, repeat_flag, until_flag, until_list, proc_en_analisis, called_procs, processingMaster
    position = p[3]
    estado = p[5]
    if proc_en_analisis in called_procs or processingMaster:
        if first_pasada:
            if while_flag and (lambda: signal_handler not in while_list):
                while_list.append(lambda: signal_handler(position, estado))

            if repeat_flag and (lambda: signal_handler not in repeat_list):
                repeat_list.append(lambda: signal_handler(position, estado))

            if until_flag and (lambda: signal_handler not in until_list):
                until_list.append(lambda: signal_handler(position, estado))
                signal_handler(position, estado)

        elif condition_flag:
            if isinstance(position, int):
                if 6 >= position >= 1:
                    signal_handler(position, estado)
                else:
                    syntax_errors.append(f'Error en procedure: {proc_en_analisis} // Sentencia Signal // ')

            if position in variables_globales:
                if isinstance(position, int):
                    if 6 >= position >= 1:
                        signal_handler(position, estado)
                    else:
                        syntax_errors.append(f'Error en procedure: {proc_en_analisis} // Sentencia Signal // ')
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
                syntax_errors.append(
                    f'Error en procedure: {proc_en_analisis} // Sentencia Signal // Variable no existe')

# Funcion que maneja las senales de los motores
# Activa el motor en la posicion dada
def signal_handler(position, estado):
    global condition_flag, proc_en_analisis
    if condition_flag:
        if isinstance(position, int):
            pass
        if not isinstance(position, int):
            if position in variables_globales:
                position = find_global_variable_value(position)
            elif position in variables_locales:
                for var_name, (var_proc, var_type, var_value) in variables_locales.items():
                    if var_type == 'Num':
                        if var_name == position:
                            if var_proc == proc_en_analisis:
                                position = find_local_variable_value(position)
            else:
                syntax_errors.append(
                    f'Error en procedure: {proc_en_analisis} // Sentencia Signal // Variable: {position} no existe')

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

# Estructura del viewSignal
# Contiene todos los flags necesarios para lidiar con ellas en while, until, case y repeat
# Llama la funcion auxiliar en caso de cumplir condiciones
def p_viewsignal(p):
    '''viewsignal : VIEWSIGNAL LPARENT INTEGER RPARENT SEMICOLON
                    | VIEWSIGNAL LPARENT ID RPARENT SEMICOLON'''
    global condition_flag, while_flag, while_list, first_pasada, proc_en_analisis, repeat_list, repeat_flag, until_flag, until_list, proc_en_analisis, called_procs, processingMaster
    position = p[3]
    if proc_en_analisis in called_procs or processingMaster:
        if first_pasada:
            if while_flag and (lambda: signal_handler not in while_list):
                while_list.append(lambda: viewsignal_handler(position))

            if repeat_flag and (lambda: signal_handler not in repeat_list):
                repeat_list.append(lambda: viewsignal_handler(position))

            if until_flag and (lambda: signal_handler not in until_list):
                until_list.append(lambda: viewsignal_handler(position))
                return viewsignal_handler(position)

        elif condition_flag:
            if isinstance(position, int):
                if 6 >= position >= 1:
                    return viewsignal_handler(position)
                else:
                    syntax_errors.append(f'Error en procedure: {proc_en_analisis} // Sentencia Signal // ')

            if position in variables_globales:
                if isinstance(position, int):
                    if 6 >= position >= 1:
                        return viewsignal_handler(position)
                    else:
                        syntax_errors.append(f'Error en procedure: {proc_en_analisis} // Sentencia Signal // ')
                else:
                    pos = find_global_variable_value(position)
                    return viewsignal_handler(pos)

            elif position in variables_locales:
                for var_name, (var_proc, var_type, var_value) in variables_locales.items():
                    if var_type == 'Num':
                        if var_name == position:
                            if var_proc == proc_en_analisis:
                                if isinstance(position, int):
                                    if 6 >= position >= 1:
                                        return viewsignal_handler(position)
                                else:
                                    pos = find_local_variable_value(position)
                                    return viewsignal_handler(pos)
            else:
                syntax_errors.append(
                    f'Error en procedure: {proc_en_analisis} // Sentencia Signal // Variable no existe')

# Retorna el estado de un motor (1 o 0)
def viewsignal_handler(motor):
    global condition_flag, values_flag, values_valor
    if condition_flag:
        estado = consultar_motor(motor)
        if values_flag:
            values_valor = estado
        return estado

# Estructura del while
# Crea el loop del while para que se recorra mientras se cumpla la condicion
def p_while(p):
    '''while : while_handler sentence LPARENT sentences RPARENT SEMICOLON'''
    global while_flag, while_list, first_pasada, condition_flag, proc_en_analisis, processingMaster, called_procs
    print("llegó a while")
    first_pasada = False
    condition_flag = True
    print(while_list)
    if proc_en_analisis in called_procs or processingMaster:
        while while_flag:
            for func in while_list:
                func()
    while_list = []
    condition_flag = True
    while_flag = False

# p_function con token termianl para administrar los flags del while
def p_while_handler(p):
    '''while_handler : WHILE'''
    global while_flag, condition_flag, first_pasada
    while_flag = True
    condition_flag = False
    first_pasada = True

# Estructura del until
# Crea el loop del until para que se recorra mientras se cumpla la condicion
def p_until(p):
    '''until : until_handler LPARENT sentences RPARENT sentence SEMICOLON'''
    global until_flag, until_list, first_pasada, condition_flag
    print("llegó a UNTIL")
    first_pasada = False
    condition_flag = True
    print(until_list)
    if proc_en_analisis in called_procs or processingMaster:
        while until_flag:
            for func in until_list:
                func()
                #time.sleep(0.1)

    until_list = []
    condition_flag = True
    until_flag = False

# p_function con token termianl para administrar los flags del until
def p_until_handler(p):
    '''until_handler : UNTIL'''
    global until_flag, condition_flag, first_pasada
    until_flag = True
    condition_flag = False
    first_pasada = True

# Estructura del repeat
# Crea el loop del repeat para que se recorra mientras se cumpla la condicion
def p_repeat(p):
    '''repeat : repeat_handler LPARENT sentences RPARENT SEMICOLON'''
    global repeat_flag, repeat_list, first_pasada, condition_flag, proc_en_analisis, called_procs, processingMaster
    print("llegó a repeat")
    first_pasada = False
    condition_flag = True
    print(repeat_list)
    if proc_en_analisis in called_procs or processingMaster:
        while repeat_flag:
            for func in repeat_list:
                func()

    repeat_list = []
    condition_flag = True
    repeat_flag = False

# p_function con token termianl para administrar los flags del repeat
def p_repeat_handler(p):
    '''repeat_handler : REPEAT'''
    global repeat_flag, condition_flag, first_pasada
    repeat_flag = True
    condition_flag = False
    first_pasada = True

# Estructura del break
# Llama el repeat_func en caso de cumplir condiciones
def p_break(p):
    '''break : BREAK SEMICOLON'''
    global repeat_flag, first_pasada, repeat_list, condition_flag
    if first_pasada:
        if repeat_flag and (lambda: repeat_func not in repeat_list):
            repeat_list.append(lambda: repeat_func())
    elif condition_flag:
        repeat_func()

# Torna el flag de repeat False en caso de cumplirse la condicion
def repeat_func():
    global repeat_flag, condition_flag
    if condition_flag:
        repeat_flag = False

# Estructura del case
# Torna el flag de condicion True
def p_case(p):
    '''case : CASE expression recursive_conditions SEMICOLON'''
    global condition_flag
    condition_flag = True
    pass

# Estructura del else
# Si no se cumple la condition Flag torna el else Flag True
def p_else_condition(p):
    '''else_condition : LPARENT sentences RPARENT'''
    global condition_flag, else_flag
    if not condition_flag:
        else_flag = True

    pass

# Recursividad para las funciones recursivas
def p_recursive_conditions(p):
    '''recursive_conditions : recursive_condition
                            | recursive_conditions recursive_condition'''
    pass

# Estructura para las condiciones recursivas
def p_recursive_condition(p):
    '''recursive_condition :  condition LPARENT sentences RPARENT'''
    pass

# Token terminal para lidiar con el id de una expresion
def p_expression(p):
    'expression : ID'
    global id_case, condition_flag, else_flag, first_pasada
    id_case = p[1]

# Estructura del When - Then
# Contiene todos los flags necesarios para lidiar con ellas en while, until, case y repeat
# Llama el condition handler
def p_condition(p):
    '''condition : WHEN INTEGER THEN
                | WHEN STRING THEN '''
    global id_case, condition_flag, while_flag, while_list, condition_flag, repeat_flag, repeat_list, until_flag, until_list, proc_en_analisis, called_procs, processingMaster
    condition_flag = True
    variable_name = id_case
    condition_value = p[2]
    if proc_en_analisis in called_procs or processingMaster:
        if first_pasada:
            if while_flag and (lambda: condition_handler not in while_list):
                while_list.append(lambda: condition_handler(variable_name, condition_value))
            if repeat_flag and (lambda: condition_handler not in repeat_list):
                repeat_list.append(lambda: condition_handler(variable_name, condition_value))
            if until_flag and (lambda: condition_handler not in until_list):
                until_list.append(lambda: condition_handler(variable_name, condition_value))
                condition_handler(variable_name, condition_value)
        elif condition_flag:
            condition_handler(variable_name, condition_value)

# Verifica si se cumple el case de cada WHEN
def condition_handler(variable_name, condition_value):
    global condition_flag, proc_en_analisis
    if variable_name in variables_globales:
        if find_global_variable_value(variable_name) == condition_value:
            # Set the condition flag to True to execute the following sentences
            print("PASÓ RITEVE")
            condition_flag = True
        else:
            # Set the condition flag to False to skip the following sentences
            print("No coindició CASE")
            condition_flag = False

    elif variable_name in variables_locales:
        for var_name, (var_proc, var_type, var_value) in variables_locales.items():
            if var_type == 'Num':
                if var_name == variable_name:
                    if var_proc == proc_en_analisis:
                        if find_global_variable_value(variable_name) == condition_value:
                            # Set the condition flag to True to execute the following sentences
                            print("PASÓ RITEVE")
                            condition_flag = True
                        else:
                            # Set the condition flag to False to skip the following sentences
                            print("No coindició CASE")
                            condition_flag = False
    else:
        syntax_errors.append(
            f'Error en procedure: {proc_en_analisis} // Sentencia Case // Variable {variable_name} no existe')

# Estrucutra del cut
# Realiza las validaciones necesarias
# Contiene todos los flags necesarios para lidiar con ellas en while, until, case y repeat
# Llama el cut handler
def p_cut(p):
    '''cut : CUT LPARENT ID COMA STRING RPARENT SEMICOLON
            | CUT LPARENT ID COMA ID RPARENT SEMICOLON'''
    global while_flag, while_list, first_pasada, condition_flag, repeat_flag, repeat_list, until_flag, until_list
    if proc_en_analisis in called_procs or processingMaster:
        if p[3] in variables_locales:
            for var_name, (var_proc, var_type, var_value) in variables_locales.items():
                if var_type == 'Str':
                    if var_name == p[3]:
                        if var_proc == proc_en_analisis:
                            if isinstance(p[5], str) and variables_locales[p[3]][1] == 'Str':
                                var_donde_guardar = p[3]
                                var_donde_cortar = p[5]
                                if first_pasada:
                                    if while_flag and (lambda: cut_handler not in while_list):
                                        while_list.append(lambda: cut_handler(var_donde_guardar, var_donde_cortar))

                                    if repeat_flag and (lambda: cut_handler not in repeat_list):
                                        repeat_list.append(lambda: cut_handler(var_donde_guardar, var_donde_cortar))

                                    if until_flag and (lambda: cut_handler not in until_list):
                                        until_list.append(lambda: cut_handler(var_donde_guardar, var_donde_cortar))
                                        cut_handler(var_donde_guardar, var_donde_cortar)

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

                    if repeat_flag and (lambda: cut_handler not in repeat_list):
                        repeat_list.append(lambda: cut_handler(var_donde_guardar, var_donde_cortar))

                    if until_flag and (lambda: cut_handler not in until_list):
                        until_list.append(lambda: cut_handler(var_donde_guardar, var_donde_cortar))
                        cut_handler(var_donde_guardar, var_donde_cortar)

                elif condition_flag:
                    cut_handler(var_donde_guardar, var_donde_cortar)
            else:
                syntax_errors.append(
                    f'Error en línea {p.lineno}, posición {p.lexpos}: valor dado no corresponde al tipado seleccionado {p[3]}')
        else:
            syntax_errors.append(f'Error en línea {p.lineno}, posición {p.lexpos}: Variable: {p[3]} no existe')

# Remueve el primer caracter de la segunda variabley lo almacena en la primera
def cut_handler(var_donde_guardar, var_donde_cortar):
    if var_donde_cortar in variables_locales:
        string_a_cortar = find_local_variable_value(var_donde_cortar)

    if var_donde_cortar in variables_globales:
        string_a_cortar = find_global_variable_value(var_donde_cortar)

    if var_donde_guardar in variables_locales:
        if len(string_a_cortar) > 0:
            variables_locales[var_donde_guardar][2] = string_a_cortar[0]
            print(f'Nuevos valores en {var_donde_guardar}: {variables_locales[var_donde_guardar]}')
        else:
            syntax_errors.append(
                f'Error en {proc_en_analisis} string de cut no puede ser nulo')

    if var_donde_guardar in variables_globales:
        if len(string_a_cortar) > 0:
            variables_globales[var_donde_guardar][1] = string_a_cortar[0]
            print(f'Nuevos valores en {var_donde_guardar}: {variables_globales[var_donde_guardar]}')
        else:
            syntax_errors.append(
                f'Error en {proc_en_analisis} string de cut no puede ser nulo')

# Estrucutra del recut
# Realiza las validaciones necesarias
# Contiene todos los flags necesarios para lidiar con ellas en while, until, case y repeat
# Llama el recut handler
def p_recut(p):
    '''recut : RECUT LPARENT ID RPARENT SEMICOLON'''
    global while_flag, while_list, repeat_flag, repeat_list, until_flag, until_list
    if proc_en_analisis in called_procs or processingMaster:
        if p[3] in variables_locales:
            if isinstance(p[5], str) and variables_locales[p[3]][1] == 'Str':
                var_donde_editar = p[3]
                if first_pasada:
                    if while_flag and (lambda: recut_handler not in while_list):
                        while_list.append(lambda: recut_handler(var_donde_editar))

                    if repeat_flag and (lambda: recut_handler not in repeat_list):
                        repeat_list.append(lambda: recut_handler(var_donde_editar))

                    if until_flag and (lambda: recut_handler not in until_list):
                        until_list.append(lambda: recut_handler(var_donde_editar))
                        recut_handler(var_donde_editar)

                elif condition_flag:
                    recut_handler(var_donde_editar)
            else:
                syntax_errors.append(
                    f'Error en procedure: {proc_en_analisis}: valor dado no corresponde al tipado seleccionado {p[3]}')

        elif p[3] in variables_globales:
            if isinstance(p[5], str) and variables_globales[p[3]][0] == 'Str':
                var_donde_editar = p[3]
                if first_pasada:
                    if while_flag and (lambda: recut_handler not in while_list):
                        while_list.append(lambda: recut_handler(var_donde_editar))

                    if repeat_flag and (lambda: recut_handler not in repeat_list):
                        repeat_list.append(lambda: recut_handler(var_donde_editar))

                    if until_flag and (lambda: recut_handler not in until_list):
                        until_list.append(lambda: recut_handler(var_donde_editar))
                        recut_handler(var_donde_editar)

                elif condition_flag:
                    recut_handler(var_donde_editar)
            else:
                syntax_errors.append(
                    f'Error en procedure: {proc_en_analisis} valor dado no corresponde al tipado seleccionado {p[3]}')
        else:
            syntax_errors.append(f'Error en procedure: {proc_en_analisis}, Variable: {p[3]} no existe')

# Funcion de recut
# Remueve el primer caracter de la variable
def recut_handler(var):
    if len(var) > 0:
        if var in variables_locales:
            variables_locales[var][2] = find_local_variable_value(var)[1:]
            print(f'Nuevos valores en {var}: {variables_locales[var]}')
        if var in variables_globales:
            variables_globales[var][1] = find_global_variable_value(var)[1:]
            print(f'Nuevos valores en {var}: {variables_globales[var]}')
    else:
        syntax_errors.append(
            f'Error en {proc_en_analisis} string de recut no puede ser nulo')

# Estrucutra del sleep
# Realiza las validaciones necesarias
# Contiene todos los flags necesarios para lidiar con ellas en while, until, case y repeat
# Llama el sleep handler
def p_sleep(p):
    '''sleep : SLEEP LPARENT INTEGER RPARENT SEMICOLON'''
    global first_pasada, condition_flag, until_flag, while_flag, repeat_flag, proc_en_analisis, processingMaster, called_procs
    tiempo_deseado = p[3]
    if proc_en_analisis in called_procs or processingMaster:
        if first_pasada:
            if while_flag and (lambda: sleep_handler not in while_list):
                while_list.append(lambda: sleep_handler(tiempo_deseado))

            if repeat_flag and (lambda: sleep_handler not in repeat_list):
                repeat_list.append(lambda: sleep_handler(tiempo_deseado))

            if until_flag and (lambda: sleep_handler not in until_list):
                until_list.append(lambda: sleep_handler(tiempo_deseado))
                sleep_handler(tiempo_deseado)

        elif condition_flag:
            sleep_handler(tiempo_deseado)

# Funcion handler de sleep
# Si se cumple la condicion hace un sleep del tiempo
def sleep_handler(tiempo_deseado):
    global condition_flag
    if condition_flag:
        time.sleep(tiempo_deseado)
        print(f'Ingreso a SLEEP // Tiempo dormido = {tiempo_deseado}')

# p funcion de empty
def p_empty(p):
    '''empty :'''
    p[0] = None


# Regla para manejar los errores no dertectado en el resto de codigo
def p_error(p):
    global proc_en_analisis
    if p:
        syntax_errors.append(
            f"- Token inesperado '{p.value}' // en Proc: {proc_en_analisis}")

# Build the parser
parser = yacc.yacc()

'''
with open('codigo_arduino.txt', 'r', encoding='utf-8') as file:
    input_text = file.read()

print("Ejecutando análisis")
lexer.input(input_text)
for token in lexer:
    print(token)
# Print the lexical errors
if lexical_errors:
    print("\nLexical errors:")
    for error in lexical_errors:
        print(error)

result = parser.parse(input_text)

# Print the syntax errors
if syntax_errors:
    print("Syntax errors:")
    for error in syntax_errors:
        print(error)
else:
    print(result)

'''

