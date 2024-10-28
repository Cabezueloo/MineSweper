import const

class Tablero:
    def __init__(self,rows,columns) -> None:
        self.rows, self.columns = rows,columns
       
        self.board = self.createBoard()
        
    def createBoard(self) -> list:
        board = []
        for row in range(self.rows):
            rowInfo = []
            for col in range(self.columns):
                rowInfo.append(Celda(row,col))
            
            board.append(rowInfo)
            
        
        #Una vez se ha generado todo el tablero, agregamos vecinos
        for row in range(self.rows):
            for col in range(self.columns):
                    celdasAlrededorLista : list = self.knowCeldasAlrededor(row,col,b=board)
                    board[row][col].setAroundCeldas(celdasAlrededorLista)
            
        
        return board
        
    
    def knowCeldasAlrededor(self,row,col,b) -> list:
        celdasAlrededor = []
        for x in range(-1,2):
            for y in range(-1,2):
                if (x == 0 and y == 0):
                    continue  # Saltar la posición central
                nueva_fila = row + x
                nueva_columna = col + y

                # Para que no de error por salir index bound of bonds, debe de ser mayor que 0 y menor que el tamagno de campo
                if (0 <= nueva_fila < self.rows) and (0 <= nueva_columna < self.columns):
                    celdasAlrededor.append(b[nueva_fila][nueva_columna])
        
        return celdasAlrededor


class Celda:
    def __init__(self,row,col) -> None:
        self.row,self.col = row,col
        self.flagged : bool = False
        self.clicked : bool = False
        self.value = const.D
        self.aroundCeldas = []
        
    def setAroundCeldas(self,lista):
        self.aroundCeldas = lista
    
    def desconocidosAlrededor(self) -> int:
       
        desconocidas = sum(x.value == const.D for x in self.aroundCeldas)
        return desconocidas
    
    def flaggsAlrededor(self) -> int:
        
        flags = sum(x.flagged for x in self.aroundCeldas)
        return flags