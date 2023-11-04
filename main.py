import tkinter as tk
from PIL import Image, ImageTk
import cv2
import imutils
import os
from datetime import datetime
from ultralytics import YOLO

from DB.controlDB import guardar_deteccion

# umbral de confianza personalizado
umbral_confianza = 0.65  # Ajusta este valor

# ruta de la carpeta para guardar las fotos
carpeta_fotos = "RetroModelo"

# verifica si la carpeta de fotos existe, si no, créala
if not os.path.exists(carpeta_fotos):
    os.makedirs(carpeta_fotos)

# funcion para guardar una foto en la carpeta de fotos
def guardar_foto(frame, class_name):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_foto = f"{class_name}_{timestamp}.jpg"
    ruta_foto = os.path.join(carpeta_fotos, nombre_foto)
    cv2.imwrite(ruta_foto, frame)
    print(f"Foto guardada: {ruta_foto}")

# Funcion de escaneo
def Scanner():
    if cap is not None:
        ret, frame = cap.read()
        frame_show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret:
            results = model(frame)

            for result in results:
                if len(result.boxes.cls) > 0:
                    for i in range(len(result.boxes.cls)):
                        class_id = int(result.boxes.cls[i])
                        confianza = float(result.boxes.conf[i])
                        if confianza >= umbral_confianza:
                            class_name = model.names[class_id]
                            guardar_deteccion(class_name)  # Guarda el nombre de la clase detectada
                            guardar_foto(frame, class_name)  # Guarda la foto

            # dibuja las detecciones de personas en el frame
            annotated_frame = results[0].plot()

            # mostrar frame con detecciones
            frame_show = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

            # resize
            frame_show = imutils.resize(frame_show, width=1280, height=720)

            im = Image.fromarray(frame_show)
            img = ImageTk.PhotoImage(image=im)

            # mostrar
            labelVideo.configure(image=img)
            labelVideo.image = img
            labelVideo.after(10, Scanner)
        else:
            cap.release()

def main_window():
    global model, labelVideo, cap

    pantalla = tk.Tk()
    pantalla.title("Sistema de detección de objetos")
    pantalla.geometry("1280x720")

    # Fondo de pantalla (reemplaza "" con la ruta de tu imagen)
    imagenfondo = tk.PhotoImage(file="")
    background = tk.Label(image=imagenfondo)
    background.place(x=0, y=0, relwidth=1, relheight=1)

    # Modelo de IA para la detección de objetos
    model = YOLO("modelo/best.pt")

    # Label de video
    labelVideo = tk.Label(pantalla)
    labelVideo.place(x=1, y=1)

    # Cámara
    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)  # Ancho
    cap.set(4, 1080)  # Alto

    # Escáner
    Scanner()

    pantalla.mainloop()

if __name__ == "__main__":
    main_window()
