from modelo import Tablero
from PIL import Image, ImageDraw
import numpy as np
from const import datos
import pyautogui 
import pyscreenshot as ImageGrab
import const

class Vista:
    
    def __init__(self, left, top, right, bottom, rows, columns, SIZEBLOCK,modelo:Tablero) -> None:
        self.left, self.top = left, top
        self.right, self.bottom = right, bottom
        self.rows, self.columns = rows, columns
        self.SIZEBLOCK = SIZEBLOCK
        self.modelo = modelo
        
             
    # Método auxiliar para verificar si hay algun color existe en la region.
    def detectNumber(self, region) -> int:
        # Recorrer cada número y su color de referencia
        for num, color_ref in datos.items():
            # Comprobar si algún píxel en la región coincide con `color_ref` con una tolerancia
            
            if np.any(np.all(np.isclose(region, color_ref, atol=50), axis=-1)):
                return num
        return const.SIN_BOMBAS_ALREDEDOR  # Devolver 0 o un valor predeterminado si no se encuentra ningún color coincidente(Significa que no hay bomba)
    
    
    
    def putFlaggs(self,row,col,tablero) -> list:
        lista = []
        neightbors = tablero[row][col].aroundCeldas
        
        for x in neightbors:
            if x.value == const.D and not x.flagged:
                center_x = int(self.left + x.col * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK)
                center_y = int(self.top + x.row * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK)
                print("FILA",x.row," Coluna ",x.col)
                pyautogui.click(x=center_x,y=center_y,button="right")
                lista.append((x.row,x.col))
        
        return lista
    
    
    def revelBlock(self,row,col,tablero):
        
        neightbors = tablero[row][col].aroundCeldas
        
        for x in neightbors:
            if x.value == const.D and not x.flagged:
                center_x = int(self.left + x.col * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK)
                center_y = int(self.top + x.row * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK)
                pyautogui.click(x=center_x,y=center_y,button="left")
                
    def capturaTablero(self):
        return ImageGrab.grab(bbox=(self.left,self.top,self.right,self.bottom))
    
    def primerClick(self):
        center_x = int(self.left + (self.rows/2) * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK)
        center_y = int(self.top + (self.columns/2) * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK)

        pyautogui.click(x=center_x,y=center_y,button="left")
        