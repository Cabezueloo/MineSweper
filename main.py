from pynput.mouse import Listener
from modelo import Tablero
import pyscreenshot as ImageGrab
from vista import Vista
from controlador import Controlador
import time
coord = []

def click(x, y, button, pressed):
    if pressed:
        x = (x)
        y = (y)
        coord.append((x, y))

        if len(coord) == 2:
            print("Coordenadas guardadas:", coord)
            return False  # Detiene el listener después de 2 clics

# Escuchar los clics del mouse
with Listener(on_click=click) as listener:
    listener.join()


# Coordenadas de la esquina superior izquierda y la esquina inferior derecha
left, top = coord[0]
right, bottom = coord[1]

# Número de filas y columnas (esto depende del tamaño de tu tablero)
rows = 16
columns = 16


# Tamaño de cada bloque/celda
sizeBlock_width = (right - left) / columns
sizeBlock_height = (bottom - top) / rows
SIZEBLOCK = min(sizeBlock_height,sizeBlock_width)


while(True):
    modelo = Tablero(rows=rows,columns=columns)

    vista = Vista(left,top,right,bottom,rows,columns,SIZEBLOCK,modelo)

    controlador = Controlador(modelo,vista)

    controlador.vista.primerClick()
    controlador.loopMain()

