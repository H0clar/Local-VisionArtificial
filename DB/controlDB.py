import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Inicializa la aplicación de Firebase
cred = credentials.Certificate("proyecto-vision-c1e93-firebase-adminsdk-9vt9l-841f55bda8.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://proyecto-vision-c1e93-default-rtdb.firebaseio.com/'
})
print("Firebase inicializado correctamente")


# Función para guardar detecciones en Firebase
def guardar_deteccion(class_name):
    # Obtiene la fecha actual
    fecha_actual = datetime.datetime.now()
    fecha_str = fecha_actual.strftime("%d-%m-%Y")  # Formato de fecha

    # Crea una referencia a la carpeta de detecciones con la fecha actual
    ref = db.reference(f'/detecciones/{fecha_str}')

    # Crea una nueva detección bajo la carpeta de la fecha actual
    nueva_deteccion = ref.push()

    # Guarda los datos de la detección
    nueva_deteccion.set({
        'clase': class_name,  # Guarda el nombre de la clase
        'fecha': fecha_actual.strftime("%d/%m/%Y %H:%M")
    })

    print(f'Detección de {class_name} guardada en Realtime Database en la carpeta {fecha_str}')
