from pyfirmata import Arduino, SERVO, util
from time import sleep

port = 'COM9'

morado = 11  # 1
verde = 10  # 2
naranja = 9  # 3
blanco = 3  # 4
azul = 5  # 5
amarillo = 6  # 6

estado_motores = {"morado": 0,
                  "verde": 0,
                  "narajna": 0,
                  "blanco": 0,
                  "azul": 0,
                  "amarillo": 0}

'''
board = Arduino(port)

board.digital[morado].mode = SERVO
board.digital[verde].mode = SERVO
board.digital[naranja].mode = SERVO
board.digital[blanco].mode = SERVO
board.digital[azul].mode = SERVO
board.digital[amarillo].mode = SERVO


def rotateservo(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)
'''


def manipulacion_arduino(motor, estado_a_cambiar):
    global estado_motores
    if motor == "morado":
        print(f'Cambio de estado del motor morado a {estado_a_cambiar}')
        if estado_a_cambiar == 1:
            estado_motores["morado"] = 1
            for i in range(0, 18):
                print("movimiento ELIMINAR PRINT después xd")
                #rotateservo(morado, i * 5)
        elif estado_a_cambiar == 0:
            estado_motores["morado"] = 0
            #rotateservo(morado, 5)
        return estado_a_cambiar

    if motor == "verde":
        print(f'Cambio de estado del motor verde a {estado_a_cambiar}')
        if estado_a_cambiar == 1:
            estado_motores["verde"] = 1
            for i in range(0, 18):
                print("movimiento ELIMINAR PRINT después xd")
                #rotateservo(verde, i * 5)
        elif estado_a_cambiar == 0:
            estado_motores["verde"] = 0
            #rotateservo(verde, 5)
        return estado_a_cambiar

    if motor == "naranja":
        print(f'Cambio de estado del motor naranja a {estado_a_cambiar}')
        if estado_a_cambiar == 1:
            estado_motores["naranja"] = 1
            for i in range(0, 18):
                print("movimiento ELIMINAR PRINT después xd")
                #rotateservo(naranja, i * 5)
        elif estado_a_cambiar == 0:
            estado_motores["naranja"] = 0
            #rotateservo(naranja, 5)
        return estado_a_cambiar

    if motor == "blanco":
        print(f'Cambio de estado del motor blanco a {estado_a_cambiar}')
        if estado_a_cambiar == 1:
            estado_motores["blanco"] = 1
            for i in range(0, 18):
                print("movimiento ELIMINAR PRINT después xd")
                #rotateservo(blanco, i * 5)
        elif estado_a_cambiar == 0:
            estado_motores["blanco"] = 0
            #rotateservo(blanco, 5)
        return estado_a_cambiar

    if motor == "azul":
        print(f'Cambio de estado del motor azul a {estado_a_cambiar}')
        if estado_a_cambiar == 1:
            estado_motores["azul"] = 1
            for i in range(0, 18):
                print("movimiento ELIMINAR PRINT después xd")
                #rotateservo(azul, i * 5)
        elif estado_a_cambiar == 0:
            estado_motores["azul"] = 0
            #rotateservo(azul, 5)
        return estado_a_cambiar

    if motor == "amarillo":
        print(f'Cambio de estado del motor amarillo a {estado_a_cambiar}')
        if estado_a_cambiar == 1:
            estado_motores["amarillo"] = 1
            for i in range(0, 18):
                print("movimiento ELIMINAR PRINT después xd")
                #rotateservo(amarillo, i * 5)
        elif estado_a_cambiar == 0:
            estado_motores["amarillo"] = 0
            #rotateservo(amarillo, 5)
        return estado_a_cambiar

def consultar_motor(color):
    global estado_motores
    estado = estado_motores[color]
    return estado
