import numpy as np
import celda
from const import datos,termcolors,FLAGGED,D
from PIL import Image, ImageDraw
from termcolor import colored
import pyautogui 
import time


class Partida:
    def __init__(self, left, top, right, bottom, rows, columns, SIZEBLOCK) -> None:
        
        self.left, self.top = left, top
        self.right, self.bottom = right, bottom
        self.rows, self.columns = rows, columns
        self.SIZEBLOCK = SIZEBLOCK
        self.board = self.createBoard()
    
    def createBoard(self) -> list:
        board = []
        for row in range(self.rows):
            rowInfo = []
            for col in range(self.columns):
                rowInfo.append(celda.Celda(row,col))
            
            board.append(rowInfo)
            
        return board

    def updateBoard(self, imageBoard):
        # Convertir la imagen a un array de píxeles para facilitar la inspección
        image_np = np.array(imageBoard)
        
        # Si quieres dibujar las regiones inspeccionadas en la imagen
        image_draw = Image.fromarray(image_np)  # Convertir de nuevo a Image para poder dibujar
        draw = ImageDraw.Draw(image_draw)

        for row in range(self.rows):
            for col in range(self.columns):
                celdaActual = self.board[row][col]
                if not celdaActual.flagged and celdaActual.value != '0' and not celdaActual.clicked:
                    # Calcular el centro de cada celda
                    center_x, center_y = (col * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK, \
                    row * self.SIZEBLOCK + 0.50 * self.SIZEBLOCK)
                    center_x = int(center_x)
                    center_y = int(center_y)

                    # Definir un radio alrededor del centro (opcional, dependiendo de cuántos píxeles quieras inspeccionar)
                    radio = 20  # Puedes ajustar este valor
                    
                    # Obtener los píxeles dentro del radio alrededor del centro
                    region = image_np[max(0, center_y - radio): center_y + radio, max(0, center_x - radio): center_x + radio]

                    
                
                    
                    valor : str = self.detectNumber(region)
                    self.board[row][col].value = valor

                   

                        
                    if valor != 'D':
                        self.board[row][col].clicked = True
                        

        
        
        #Una vez se ha generado todo el tablero
        for row in range(self.rows):
            for col in range(self.columns):
                if not self.board[row][col].value == D and not self.board[row][col].value == '0':
                    celdasAlrededorLista : list = self.setCeldasAlrededor(row,col)
                    self.board[row][col].setAroundCeldas(celdasAlrededorLista)

        #Poner Flaggs dependiendo de las celdas alrededor
        print()
        for row in range(self.rows):
            for col in range(self.columns):
                #print("Posicion Fila",row, "columna ",col, " tiene ",self.board[row][col].desconocidosAlrededor()," desconocidos alrededor" )
                if not self.board[row][col].flagged and not (self.board[row][col].value == D or self.board[row][col].value == '0'):
                   
                    if self.board[row][col].value == self.board[row][col].desconocidosAlrededor():
                        print("Puso flag")
                        self.putFlaggs(row,col)

        
        #Hacer click para revelar mas tablero
        for row in range(self.rows):
            for col in range(self.columns):        
                if not self.board[row][col].flagged or not (self.board[row][col].value == D or self.board[row][col].value == '0') :
                    if self.board[row][col].value == self.board[row][col].flaggsAlrededor():
                       self.revelBlock(row,col) 

            
    def revelBlock(self,row,col):
        neightbors = self.board[row][col].aroundCeldas
        for x in neightbors:
            if x.value == D and not x.flagged:
                center_x = int(self.left + x.col * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK)
                center_y = int(self.top + x.row * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK)
                pyautogui.click(x=center_x,y=center_y,button="left")
                          
    #Arreglar
    def putFlaggs(self,row,col):
        
        neightbors = self.board[row][col].aroundCeldas
        
        for x in neightbors:
            if x.value == D and not x.flagged:
                center_x = int(self.left + x.col * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK)
                center_y = int(self.top + x.row * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK)
                print("FILA",x.row," Coluna ",x.col)
                pyautogui.click(x=center_x,y=center_y,button="right")
                self.board[x.row][x.col].flagged = True
                #self.board[x.row][x.col].value = FLAGGED #Si pongo esto se rompe todo
                self.board[x.row][x.col].clicked = True



    def setCeldasAlrededor(self,row,col) -> list:
        celdasAlrededor = []
        for x in range(-1,2):
            for y in range(-1,2):
                if (x == 0 and y == 0):
                    continue  # Saltar la posición central
                nueva_fila = row + x
                nueva_columna = col + y

                # Para que no de error por salir index bound of bonds, debe de ser mayor que 0 y menor que el tamagno de campo
                if (0 <= nueva_fila < self.rows) and (0 <= nueva_columna < self.columns):
                    celdasAlrededor.append(self.board[nueva_fila][nueva_columna])
        
        return celdasAlrededor


    
    # Método auxiliar para verificar si hay algun color existe en la region.
    def detectNumber(self, region):
        # Recorrer cada número y su color de referencia
        for num, color_ref in datos.items():
            # Comprobar si algún píxel en la región coincide con `color_ref` con una tolerancia
            
            if np.any(np.all(np.isclose(region, color_ref, atol=50), axis=-1)):
                return num
        return '0'  # Devolver '0' o un valor predeterminado si no se encuentra ningún color coincidente(Significa que no hay bomba)
         
   

    def printBoard(self):
        print("Tablero actual:")
        for f in range(self.rows):
            row_str = ""  # Cadena para construir la fila completa antes de imprimir
            for c in range(self.columns):
                if self.board[f][c].flagged:
                    cell_display = colored("F", termcolors['F'])
                else:
                    valor = str(self.board[f][c].value)
                    color = termcolors.get(valor, "white")  # Color blanco por defecto
                    cell_display = colored(valor, color)
                
                row_str += f"{cell_display} "  # Agregar la celda a la fila con un espacio
            print(row_str)  # Imprimir la fila completa
