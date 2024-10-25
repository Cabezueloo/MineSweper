import const
class Celda:
    def __init__(self) -> None:
        self.flagged : bool = False
        self.clicked : bool = False
        self.value = const.D #DESCONOCIDO

    def setFaggled(self): 
        self.flagged = not self.flagged
        