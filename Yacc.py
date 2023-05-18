import ply.yacc as yacc
import Lex

syntax_errors = []
variables = {}

# List of token names
tokens = [
    'PROC',
    'NEW',
    'CALL',
    'ID',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'COMMA',
    'NUM',
    'BOOL',
    'COMPARISON_OP',
    'OPERATOR',
]

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
    pass

def p_procedure_definition(p):
    '''procedure_definition : PROC ID LPAREN statements RPAREN SEMICOLON'''
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

# Test input code

input_code = '''
// Sample code to test lexical analysis and parsing

// Procedure definitions
New @ale;
Proc @Procedure1
(
    New @variable1, (Num, 5);
    (Num, 5);
    @variable2,
    (Bool, True);
);

Proc @Procedure2
(
    CALL(@Procedure1);
);

Proc @Master
(
    CALL(@Procedure1);
    CALL(@Procedure2);
);

// Variable definition outside of any procedure
New @variable3,
(Num, 10);

// Invalid procedure definition
Proc @Procedure1
(
    @variable3,
    (Num, 15);
);

// Invalid variable definition
New @variable4,
(Num, 20);

// Invalid syntax
Proc Procedure3
(
    CALL(@Procedure1);
    CALL(@Procedure2);
);

// Invalid token
@var5 = 25;

// Missing semicolon
Proc @Procedure4
(
    @variable4,
    (Num, 30);
);

// Invalid token
Proc @Procedure5
{
    @variable5,
    (Num, 35);
};

'''

# Run the parser
result = parser.parse(input_code)

# Print the syntax errors
if syntax_errors:
    print("Syntax errors:")
    for error in syntax_errors:
        print(error)
else:
    print(result)
