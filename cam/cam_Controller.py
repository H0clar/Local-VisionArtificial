from flask import Flask, Response
import cv2

app = Flask(__name__)

# URL de la cámara IP de tu teléfono
camara_ip_url = "http://192.168.18.150:8080/video"

# Función para transmitir el video desde la cámara IP
def generar_frames():
    cap = cv2.VideoCapture(camara_ip_url)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            if not ret:
                continue
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

@app.route("/video")
def video():
    return Response(generar_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
