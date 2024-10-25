import numpy as np
colorsBombs = np.asarray([
    [189, 189, 189], # 0
    [0, 33, 245], # 1
    [53, 120, 32], # 2
    [234, 50, 35], # 3
    [5, 0, 123], # 4
    [123, 1, 0], # 5
    [255, 255, 255] # white, for the left region of unclicked piece
])
    
class N_BOMBAS:
    B = -1  #HAY BOMBA
    D = -2 #Desconocido
    VACIO = 0
    UNO = 1
    DOS = 2
    TRES = 3
    CUATRO = 4
    CINCO = 5
    SEIS = 6

datos = {
    '0': [189, 189, 189],
    '1': [0, 33, 245],
    '2': [53, 120, 32],
    '3': [234, 50, 35],
    '4': [5, 0, 123],
    '5': [123, 1, 0]
}

termcolors = {
    
    '0': 'white',
    '1': 'blue',
    '2': 'green',
    '3': 'red',
    'F': 'yellow'
    
}