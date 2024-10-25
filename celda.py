from const import N_BOMBAS
class Celda:
    def __init__(self) -> None:
        self.flagged : bool = False
        self.bombsAround = N_BOMBAS.D
        self.clicked : bool = False
        self.value = N_BOMBAS.D

    def setFaggled(self): 
        self.flagged = not self.flagged
        