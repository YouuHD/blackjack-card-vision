#Importaciones
import cv2
from ultralytics import YOLO
import torch
import numpy as np
from conteo3 import do_conteo

#Modelo entrenado con el dataset 
model = torch.hub.load('ultralytics/yolov5', 'custom' ,
                       path='best7.pt')
#Evaluación del modelo
model.eval()

#Generar una captura de video
cap = cv2.VideoCapture(1)   #Dispositivo de captura
res= (1280,720)             #Resolución
cap.set(cv2.CAP_PROP_FRAME_WIDTH, res[0])   #Resolución de pantalla x
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, res[1])  #Resolución de pantalla y

#Poner en mayor jerarquia la ventana para que nunca se oculte y siempre esté activa
cv2.namedWindow('Cartas', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Cartas', cv2.WND_PROP_TOPMOST, 1)

while True:
    #Leer los frames de la captura    
    ret,frame = cap.read()
    #Detectar dependiendo del frame y el modelo entrenado
    detect = model(frame)
    #
    height, width = frame.shape[:2]
    #Dividir la pantalla
    vertical_limit = frame.shape[0] // 2

    #Arreglos para guardar las cartas
    player = []     #jugador
    home = []    #casa
    mensaje = ""
    try:
        for det in detect.xyxy[0]:                      #Ciclo for para detectar los atributos de la detección
            bbox = det[:4].cpu().numpy().astype(int)    #Obtener los datos de coordenadas en x1y1x2y2
            class_index = int(det[5])                   #Indice de los atributos
            class_name = detect.names[class_index]      #Nombre de la clase de la detección

            #Buscar mediante la posición de la zona de la casa o del jugador
            if bbox[1] < vertical_limit:        #Si es menor del limite vertical es la zona de la casa
                zone = "Casa"
                if len(class_name) == 3:
                    home.append(class_name[1])      #Guardar las detecciones en el arreglo de casa
                else:
                    home.append(class_name[0])      #Guardar las detecciones en el arreglo de casa
            else:
                zone = "Jugador"                #Si es mayor, es la zona del jugador
                if len(class_name) == 3:
                    player.append(class_name[1])      #Guardar las detecciones en el arreglo de jugador
                else:
                    player.append(class_name[0])      #Guardar las detecciones en el arreglo de jugador
                    
            #Imprimir las clases detectadas 
            print(f"Clase detectada: {class_name}")
            #Mostrar los nombres de las detecciones y remarcarlas en cuadrado
            frame = cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            frame = cv2.putText(frame, f"{class_name}", (bbox[0], bbox[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    
    except:
        mensaje = "Sin cartas detectadas" 

    #Impresión de las cartas detectadas
    print("Home: ",home)
    print("Jugador: ",player)

    #Comienza juego al tener valores de ambos lados
    if len(player) == 0 & len(home) == 0:
        mensaje= "No se han detectado todas las cartas"
    else:
        mensaje = do_conteo(player,home) #Si está lleno, hacer conteo
    
    #Coordenadas del mensaje
    mensaje_x = 10
    mensaje_y = height - 30
    # Agregar el mensaje en la parte inferior izquierda
    frame = cv2.putText(frame, mensaje, (mensaje_x, mensaje_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    
    #Muestra de la ventana
    cv2.imshow("Cartas", frame)
    
    #Si se presiona la letra "esc" se cierra
    if cv2.waitKey(1) == 27:
        break   #Cerrar el ciclo

# Liberar la cámara y cerrar la ventana
cap.release()
cv2.destroyAllWindows()