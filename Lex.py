import ply.lex as lex

lexical_errors = []

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
]

# Regular expression rules for tokens
t_PROC = r'PROC'
t_NEW = r'NEW'
t_CALL = r'CALL'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','
t_NUM = r'Num'
t_BOOL = r'Bool'

# Ignored characters
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    lexical_errors.append(f"Invalid token: {t.value[0]}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test input code
input_code = '''
// Sample code to test lexical analysis and parsing

// Procedure definitions
Proc @Procedure1
(
    @variable1,
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
    (Num, 30)
);

// Invalid token
Proc @Procedure5
{
    @variable5,
    (Num, 35);
};

'''

# Run the lexer
lexer.input(input_code)

# Print the tokens
for token in lexer:
    print(token)

# Print the lexical errors
if lexical_errors:
    print("\nLexical errors:")
    for error in lexical_errors:
        print(error)
