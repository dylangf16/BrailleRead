import tkinter as tk
from Lex import *
from Yacc import *

# Configuración de la ventana principal
root = tk.Tk()
root.title("Mi compilador")
root.geometry("1280x720")

# Configuración del tema oscuro
root.configure(bg="#1E1E1E")
root.option_add('*foreground', 'white')
root.option_add('*background', '#1E1E1E')
root.option_add('*activeBackground', '#333333')
root.option_add('*activeForeground', 'white')


# Función de ejecución
# TODO hacer una función aparte de solo compilación // "compilar()" es de "ejecución"
# Función de ejecución
def compilar():
    codigo = codigo_base.get("1.0", "end-1c") # Obtiene el código base

    # Ejecuta el análisis léxico
    lexer.input(codigo)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)

    update_line_numbers()


    # Ejecuta el análisis sintáctico del código
    parser.errok()
    resultado_parser = parser.parse(codigo, lexer=lexer)

    # Muestra los errores léxicos y sintácticos en la pantalla de resultados
    resultado.delete("1.0", "end")
    if lexical_errors:
        resultado.insert("1.0", "Errores léxicos:\n")
        for error in lexical_errors:
            resultado.insert("end", error + "\n")
    if syntax_errors:
        resultado.insert("end", "Errores sintácticos:\n")
        for error in syntax_errors:
            resultado.insert("end", error + "\n")
    elif not lexical_errors and not syntax_errors:
        resultado.delete("1.0", "end")
        resultado.insert("1.0", resultado_parser)


def update_line_numbers():
    content = codigo_base.get("1.0", "end")
    lines = content.split("\n")
    line_numbers = "\n".join(str(i) for i in range(1, len(lines) + 1))
    line_number_widget.config(state="normal")
    line_number_widget.delete("1.0", "end")
    line_number_widget.insert("1.0", line_numbers)
    line_number_widget.config(state="disabled")

def actualizar_linea(event):
    update_line_numbers()


# Configuración del área de código base
codigo_frame = tk.Frame(root, bg="#333333")
codigo_label = tk.Label(codigo_frame, text="Código", bg="#333333", fg="white", font=("Arial", 12, "bold"))
codigo_label.pack(side=tk.TOP, pady=10)
codigo_base = tk.Text(codigo_frame, height=20, width=80, bg="#1E1E1E", fg="white", insertbackground="white", font=("Consolas", 12))
codigo_base.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

line_number_widget = tk.Text(codigo_frame, width=4, bg="#333333", fg="white", insertbackground="white", font=("Consolas", 12))
line_number_widget.pack(side=tk.LEFT, fill=tk.Y)

# Configuración del botón de compilación
boton_compilar = tk.Button(root, text="Compilar", command=compilar, bg="#333333", fg="white", font=("Arial", 12, "bold"))
boton_compilar.pack(pady=10)

# Configuración del área de resultados
resultado_frame = tk.Frame(root, bg="#333333")
resultado_label = tk.Label(resultado_frame, text="Resultados", bg="#333333", fg="white", font=("Arial", 12, "bold"))
resultado_label.pack(side=tk.TOP, pady=10)
resultado = tk.Text(resultado_frame, height=20, width=80, bg="#1E1E1E", fg="white", insertbackground="white", font=("Consolas", 12))
resultado.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

codigo_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
boton_compilar.pack(pady=10)
resultado_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

codigo_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
boton_compilar.pack(pady=10)
resultado_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

root.bind("<Key>", actualizar_linea)
root.mainloop()