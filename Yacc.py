import ply.yacc as yacc
from Lex import tokens

syntax_errors = []

# Start symbol
start = 'program'

# Grammar rules
def p_statement(p):
    '''statement : ID'''
    if len(p[1]) < 2 or len(p[1]) > 12:
        syntax_errors.append(f"Syntax error: Invalid ID length for '{p[1]}'")
    else:
        # Valid ID, do something with it...
        pass

def p_program(p):
    '''program : procedure_definitions'''
    pass


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


def p_error(p):
    if p:
        syntax_errors.append(f'Syntax error at line {p.lineno}: Unexpected token {p.value}')
    else:
        syntax_errors.append('Syntax error: Unexpected end of input')
        # Additional check for unmatched opening parenthesis
        if '(' in p.lexer.lexdata:
            syntax_errors.append('Syntax error: Unmatched opening parenthesis')


# Build the parser
parser = yacc.yacc()

# Test input code

input_code = '''
// Sample code to test lexical analysis and parsing

// Procedure definitions
(
    (Num, 5);
    ,
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
