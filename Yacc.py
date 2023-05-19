import ply.yacc as yacc
from Lex import tokens

syntax_errors = []
variables = {}
master_found = False
procedure_names = []


# Grammar rules
def p_program(p):
    '''program : variable_definitions procedure_definitions'''
    pass


def p_variable_definitions(p):
    '''variable_definitions : variable_definitions variable_definition
                            | variable_definition'''
    pass


def p_variable_definition(p):
    '''variable_definition : NEW ID SEMICOLON
                           | NEW ID COMMA LPAREN type COMMA value RPAREN SEMICOLON'''
    if len(p[2]) < 3 or len(p[2]) > 13:  # Check variable length
        syntax_errors.append(f"Syntax error: Invalid variable name length for '{p[2]}'")
    else:
        if len(p) == 4:  # Variable without type and value
            variables[p[2]] = None
        else:
            variable_type = p[6]
            variable_value = p[8]
            variables[p[2]] = (variable_type, variable_value)


def p_type(p):
    '''type : ID'''
    p[0] = p[1]


def p_value(p):
    '''value : ID'''
    variable_name = p[1]
    if variable_name in variables:
        p[0] = variables[variable_name][1]  # Return the value of the variable
    else:
        syntax_errors.append(f"Syntax error: Undefined variable '{variable_name}'")


def p_procedure_definitions(p):
    '''procedure_definitions : procedure_definitions procedure_definition
                            | procedure_definition'''
    global master_found
    if p[2][1] == '@Master':
        if master_found:
            syntax_errors.append("Syntax error: Multiple '@Master' procedures found")
        else:
            master_found = True
    pass


def p_procedure_definition(p):
    '''procedure_definition : PROC ID LPAREN statements RPAREN SEMICOLON'''
    procedure_name = p[2]
    if procedure_name in procedure_names:
        syntax_errors.append(f"Syntax error: Duplicate procedure name '{procedure_name}'")
    else:
        procedure_names.append(procedure_name)
    pass


def p_statements(p):
    '''statements : statements statement
                  | statement'''
    pass


def p_statement(p):
    '''statement : ID
                 | call_statement'''
    pass


def p_call_statement(p):
    '''call_statement : CALL LPAREN ID RPAREN SEMICOLON'''
    pass


# Error handling rule
def p_error(p):
    if p:
        syntax_errors.append(f'Syntax error at line {p.lineno}: Unexpected token {p.value}')
    else:
        syntax_errors.append('Syntax error: Unexpected end of input')


# Build the parser
parser = yacc.yacc()
