from PIL import Image, ImageDraw
import numpy as np
from modelo import Tablero
from vista import Vista
from termcolor import colored
from const import termcolors
import pyautogui
import time
import const

class Controlador():
    
    def __init__(self, modelo:Tablero,vista:Vista) -> None:
        self.modelo = modelo
        self.vista = vista
        self.bombasRestantes = 40
        
    
    def updateBoard(self, imageBoard) -> list:
        
        #Convertir la imagen a un array de píxeles para facilitar la inspección
        tablero = self.modelo.board
        
        image_np = np.array(imageBoard)
        

        for row in range(self.modelo.rows):
            for col in range(self.modelo.columns):
                celdaActual = tablero[row][col]
                if not celdaActual.flagged and celdaActual.value != const.SIN_BOMBAS_ALREDEDOR and not celdaActual.clicked:
                    # Calcular el centro de cada celda
                    center_x, center_y = (col * self.vista.SIZEBLOCK + 0.5 * self.vista.SIZEBLOCK, \
                    row * self.vista.SIZEBLOCK + 0.50 * self.vista.SIZEBLOCK)
                    center_x = int(center_x)
                    center_y = int(center_y)

                    # Definir un radio alrededor del centro (opcional, dependiendo de cuántos píxeles quieras inspeccionar)
                    # Puedes ajustar este valor
                    #radio = 10 #50%
                    radio = 20 #65% zoom +-
                    
                    # Obtener los píxeles dentro del radio alrededor del centro
                    region = image_np[max(0, center_y - radio): center_y + radio, max(0, center_x - radio): center_x + radio]

                    
                    # Guardar la subimagen de la región en un archivo
                    # subimage = image_draw.crop((max(0, center_x - radio), max(0, center_y - radio),
                    #                             center_x + radio, center_y + radio))
                    # subimage_path = f"region_row{row}_col{col}.png"
                    # subimage.save(subimage_path)
                    
                    valor : str = self.vista.detectNumber(region)
                    tablero[row][col].value = valor

                    if valor != const.D:
                        tablero[row][col].clicked = True
                        
        ###

        
        #Poner Flaggs dependiendo de las celdas alrededor
        for row in range(self.modelo.rows):
            for col in range(self.modelo.columns):
                #print("Posicion Fila",row, "columna ",col, " tiene ",self.board[row][col].desconocidosAlrededor()," desconocidos alrededor" )
                if not tablero[row][col].flagged and not (tablero[row][col].value == const.D or tablero[row][col].value == const.SIN_BOMBAS_ALREDEDOR):
                   
                    if tablero[row][col].value == tablero[row][col].desconocidosAlrededor():
                        print("Puso flag",row," col",col)
                        lista = self.vista.putFlaggs(row,col,tablero=tablero)
                        self.bombasRestantes= self.bombasRestantes-len(lista)
                        for x in lista:
                            r,f = x[0],x[1]
                            tablero[r][f].flagged = True
                            #tablero[r][f].value = const.FLAGGED #Si pongo esto se rompe todo
                            tablero[r][f].clicked = True

        
        
        #Hacer click para revelar mas tablero
        for row in range(self.modelo.rows):
            for col in range(self.modelo.columns):        
                if not tablero[row][col].flagged or not (tablero[row][col].value == const.D or tablero[row][col].value == const.SIN_BOMBAS_ALREDEDOR) :
                    if tablero[row][col].value == tablero[row][col].flaggsAlrededor():
                       self.vista.revelBlock(row,col,tablero)
                       
        return tablero
        
        
    def printBoard(self):
        print("Tablero actual:")
        for f in range(self.modelo.rows):
            row_str = ""  # Cadena para construir la fila completa antes de imprimir
            for c in range(self.modelo.columns):
                if self.modelo.board[f][c].flagged:
                    cell_display = colored("F", termcolors[const.FLAGGED])
                else:
                    valor = self.modelo.board[f][c].value
                    if valor == -1:
                        valor = 'D'
                    color = termcolors.get(valor, "white")  # Color blanco por defecto
                    cell_display = colored(valor, color)
                
                row_str += f"{cell_display} "  # Agregar la celda a la fila con un espacio
            print(row_str)  # Imprimir la fila completa
            

    def loopMain(self) -> bool:
        
        
        while(True):
            
            time.sleep(0.2)
            im = self.vista.capturaTablero()
            inicio = time.time()
            self.modelo.board = self.updateBoard(im)
        
            self.printBoard()
            print("TIEMPO CICLO-> ", time.time()-inicio) 
            if self.bombasRestantes==0:
                self.vista.primerClick() 
                time.sleep(1)       
                pyautogui.keyDown('f2')                    
                pyautogui.keyUp('f2')                    
                break
            
                    
        
        
        
        