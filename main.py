import tkinter as tk
from Lex import lexer
from Yacc import parser

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

    output = parser.parse(codigo, lexer=lexer)

    # Guarda el output en una variable llamada output

    # Muestra el output en la pantalla de resultados
    resultado.delete("1.0", "end")
    resultado.insert("1.0", output)

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
