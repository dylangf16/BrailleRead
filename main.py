import tkinter as tk
from Lex import lexer, errores_lexicos
from Yacc import parser, errores_sintacticos

# Configuración de la ventana principal
root = tk.Tk()
root.title("Mi compilador")
root.geometry("1280x720")

# Función para compilar el código
def compilar():
    codigo = codigo_base.get("1.0", "end-1c") # Obtiene el código base

    # Ejecuta el análisis léxico y sintáctico del código
    lexer.input(codigo)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)

    # Ejecuta el análisis léxico y sintáctico del código
    parser.errok()
    resultado_parser = parser.parse(codigo, lexer=lexer)

    # Muestra los errores léxicos y sintácticos en la pantalla de resultados
    resultado.delete("1.0", "end")
    if errores_lexicos:
        resultado.insert("1.0", "Errores léxicos:\n")
        for error in errores_lexicos:
            resultado.insert("end", error + "\n")
    elif errores_sintacticos:
        resultado.insert("1.0", "Errores sintácticos:\n")
        for error in errores_sintacticos:
            resultado.insert("end", error + "\n")
    else:
        resultado.delete("1.0", "end")
        resultado.insert("1.0", resultado_parser)

# Configuración del área de código base
codigo_base = tk.Text(root, height=20, width=80)
codigo_base.pack(side=tk.LEFT)

# Configuración del botón de compilación
boton_compilar = tk.Button(root, text="Compilar", command=compilar)
boton_compilar.pack()

# Configuración del área de resultados
resultado = tk.Text(root, height=20, width=80)
resultado.pack(side=tk.RIGHT)

# Inicia el bucle de eventos
root.mainloop()
