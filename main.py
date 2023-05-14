from Lex import lexer
from Yacc import parser

while True:
    try:
        s = input('calc> ')
    except EOFError:
        break
    if not s:
        continue
    try:
        result = parser.parse(s, lexer=lexer)
        print(result)
    except Exception as e:
        print("Error al analizar la entrada:", e)
