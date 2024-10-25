import numpy as np
import celda
from const import datos,termcolors
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
                # Calcular el centro de cada celda
                center_x, center_y = (col * self.SIZEBLOCK + 0.5 * self.SIZEBLOCK, \
                row * self.SIZEBLOCK + 0.50 * self.SIZEBLOCK)
                center_x = int(center_x)
                center_y = int(center_y)

                # Definir un radio alrededor del centro (opcional, dependiendo de cuántos píxeles quieras inspeccionar)
                radio = 5  # Puedes ajustar este valor
                
                # Obtener los píxeles dentro del radio alrededor del centro
                region = image_np[max(0, center_y - radio): center_y + radio, max(0, center_x - radio): center_x + radio]

                # Imprimir los colores (valores RGB) de los píxeles de la región
                #print(f"Celda ({row}, {col}) - Centro: ({center_x}, {center_y})")
               # print("Píxeles de la región: ")
               # print(region)  # Imprime los valores de los píxeles (puede ser muy largo, ajusta si es necesario)
                
                # Guardar la subimagen de la región en un archivo
                subimage = image_draw.crop((max(0, center_x - radio), max(0, center_y - radio),
                                            center_x + radio, center_y + radio))
                subimage_path = f"region_row{row}_col{col}.png"
                subimage.save(subimage_path)
                print(f"Guardada subimagen de la celda ({row}, {col}) en {subimage_path}")

                # Aquí puedes hacer un análisis del color promedio de los píxeles dentro de esta región
                avg_color = np.mean(region, axis=(0, 1))  # Calcula el color promedio de la región
                
                #print(f"Color promedio: {avg_color}\n")

                valor : str = 'D'
                
                if self.isFlagged(row,col):
                    valor = 'F'
                    self.board[row][col].clicked = True
                else:
                    valor = self.detectNumber(avg_color)
                    self.board[row][col].clicked = True
                    
                self.board[row][col].value = valor

         
    def isFlagged(self,row,col) -> bool:
        return self.board[row][col].flagged
        
    # Método auxiliar para verificar si el color detectado corresponde a un número
    def detectNumber(self, avg_color) -> str:
        for x in datos:
            color_ref = datos[x]
            # Debug: imprimir los colores comparados
            print(f"Comparando {avg_color} con referencia {color_ref}")
            
            if np.allclose(avg_color, color_ref, atol=30):  # Tolerancia ajustable
                print(f"Detectado número {x} para el color {avg_color}")
                return x
        print(f"No se detectó ningún número para el color {avg_color}")
        return None  # Si no se detecta ningún color

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
