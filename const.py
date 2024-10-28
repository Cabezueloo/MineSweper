import numpy as np

D = -1 #DESCONOCIDO
FLAGGED = -2 #VALOR HAY BOMBA
SIN_BOMBAS_ALREDEDOR = 0
datos = {
    
    1: [0, 0, 255],
    2: [0, 123, 0],
    3: [234, 50, 35],
    4: [5, 0, 123],
    5: [123, 1, 0],
    D: [255,255,255]
}

termcolors = {
    
    SIN_BOMBAS_ALREDEDOR: 'black',
    1: 'cyan',
    2: 'green',
    3: 'red',
    4: 'blue',
    5: 'magenta',
    FLAGGED: 'yellow',
    D: 'white'
    
}