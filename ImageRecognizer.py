import cv2
import pytesseract
from matplotlib import pyplot as plt
import easyocr

# Cargar la imagen proporcionada por el usuario
image_path = '/mnt/data/image.png'
imagen_test = cv2.imread(image_path)

# Inicializamos el OCR con EasyOCR
class ImageRecognizer:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def extraer_texto(self, imagen):
        # Convertir la imagen a escala de grises
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)


        # Mostrar la imagen en escala de grises
        plt.imshow(imagen_gris, cmap='gray')
        plt.title('Imagen en Escala de Grises')
        plt.axis('off')  # No mostrar los ejes
        plt.show()
        # Aplicar un umbral para mejorar la detección de caracteres
        _, imagen_umbral = cv2.threshold(imagen_gris, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Usar EasyOCR para extraer texto (solo números permitidos)
        result = self.reader.readtext(imagen_umbral, allowlist='0123456789')
        return result

    def reconocer(self, imagen):
        numero_detectado = self.extraer_texto(imagen)
        return numero_detectado if numero_detectado else "No se detectó ningún número"

# Crear la instancia y ejecutar el reconocimiento
recognizer = ImageRecognizer()
img= cv2.imread("image.png")
resultado = recognizer.reconocer(img)
print(resultado)
