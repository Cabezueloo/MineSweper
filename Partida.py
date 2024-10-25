import numpy as np
import celda
from const import datos,termcolors,FLAGGED
from PIL import Image, ImageDraw
from termcolor import colored

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
                rowInfo.append(celda.Celda())
            
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

                # Calcular el centro de cada celda
                center_x, center_y = (col * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK, \
                row * self.SIZEBLOCK + 0.50 * self.SIZEBLOCK)
                center_x = int(center_x)
                center_y = int(center_y)

                # Definir un radio alrededor del centro (opcional, dependiendo de cuántos píxeles quieras inspeccionar)
                radio = 20  # Puedes ajustar este valor
                
                # Obtener los píxeles dentro del radio alrededor del centro
                region = image_np[max(0, center_y - radio): center_y + radio, max(0, center_x - radio): center_x + radio]

                # Guardar la subimagen de la región en un archivo
                subimage = image_draw.crop((max(0, center_x - radio), max(0, center_y - radio),
                                            center_x + radio, center_y + radio))
                subimage_path = f"region_row{row}_col{col}.png"
                subimage.save(subimage_path)
                #subimage.show()


                
                if not celdaActual.flagged and celdaActual.value != '0':
                    valor : str = self.detectNumber(region)

                    if self.isFlagged(row,col):
                        valor = FLAGGED
                        
                
                    self.board[row][col].clicked = True
                        
                    self.board[row][col].value = valor

    
    
    # Método auxiliar para verificar si hay algun color existe en la region.
    def detectNumber(self, region):
        # Recorrer cada número y su color de referencia
        for num, color_ref in datos.items():
            # Comprobar si algún píxel en la región coincide con `color_ref` con una tolerancia
            
            if np.any(np.all(np.isclose(region, color_ref, atol=50), axis=-1)):
                return num
        return '0'  # Devolver '0' o un valor predeterminado si no se encuentra ningún color coincidente(Significa que no hay bomba)
         
         
    def isFlagged(self,row,col) -> bool:
        return self.board[row][col].flagged
        
   

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
