import cv2
import numpy as np

# Define el rango de color amarillo que deseas detectar
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Recorta la imagen a la mitad izquierda
    height, width, _ = frame.shape
    left_half = frame[:, :width // 2]

    # Aplica un filtro gaussiano para suavizar la imagen y reducir el ruido
    blurred = cv2.GaussianBlur(left_half, (11, 11), 0)

    # Convierte la imagen a espacio de color HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Crea una máscara para los píxeles dentro del rango de color amarillo
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Aplica una serie de operaciones morfológicas para eliminar pequeñas imperfecciones en la máscara
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Encuentra los contornos de la máscara y dibuja los contornos en la imagen original
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        # Ajusta las coordenadas del contorno para la imagen completa
        c[:, :, 0] += width // 2
        cv2.drawContours(frame, [c], 0, (0, 255, 255), 3)

    # Muestra la imagen original con los contornos detectados
    cv2.imshow('yellow detector', frame)

    # Salir del ciclo si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

