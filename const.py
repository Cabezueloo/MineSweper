import numpy as np

D = 'D' #DESCONOCIDO
FLAGGED = 'F' #VALOR HAY BOMBA

datos = {
    
    '1': [0, 0, 255],
    '2': [0, 123, 0],
    '3': [234, 50, 35],
    '4': [5, 0, 123],
    '5': [123, 1, 0],
    'D': [255,255,255]
}

termcolors = {
    
    '0': 'black',
    '1': 'cyan',
    '2': 'green',
    '3': 'red',
    '4': 'blue',
    '5': 'magenta',
    'F': 'yellow',
    'D': 'white'
    
}