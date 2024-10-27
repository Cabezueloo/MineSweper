import pyautogui
from pynput.mouse import Listener
from Partida import Partida
import pyscreenshot as ImageGrab
import keyboard

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
rows = 8
columns = 8

# Tamaño de cada bloque/celda
sizeBlock_width = (right - left) / columns
sizeBlock_height = (bottom - top) / rows
SIZEBLOCK = min(sizeBlock_height,sizeBlock_width)

print("Left -> ", left, " Top -> ", top)
print("Right -> ", right, " Bottom -> ", bottom)
print(f"Tamaño de cada celda: Ancho -> {sizeBlock_width}px, Alto -> {sizeBlock_height}px")


partida = Partida(left,top,right,bottom,rows,columns,SIZEBLOCK)
while True:
    
    im = ImageGrab.grab(bbox=(left,top,right,bottom))
    #im.show()
    
    partida.updateBoard(im)
    if keyboard.is_pressed('q'):
        pyautogui.FAILSAFE
        break

    partida.printBoard()
    print()
    
    
    
    
    
    