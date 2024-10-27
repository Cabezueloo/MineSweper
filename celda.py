import const
class Celda:
    def __init__(self,row,col) -> None:
        self.row,self.col = row,col
        self.flagged : bool = False
        self.clicked : bool = False
        self.value = const.D #DESCONOCIDO
        self.aroundCeldas = []
        
    def setAroundCeldas(self,lista):
        self.aroundCeldas = lista
    
    def setFaggled(self): 
        self.flagged = not self.flagged

    
    def desconocidosAlrededor(self):
       
        desconocidas = sum(x.value == const.D for x in self.aroundCeldas)
        return str(desconocidas)

    
    def flaggsAlrededor(self) -> str:
        
        flags = sum(x.flagged for x in self.aroundCeldas)
        return str(flags)

