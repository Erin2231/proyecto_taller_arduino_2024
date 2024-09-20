import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
import mimetypes

load_dotenv() # Cargar las variables de entorno desde el archivo .env (seguridad)

email_envio = "asitentedevuelo@gmail.com"
password = os.getenv("PASSWORD")
email_recepcion = "fgranados1976@gmail.com"

subject = "Análisis de Vuelos y Gráficos Adjuntos"
body = """
Estimado/a pasajero/a,

Control de tráfico aéreo informa que el "reporte adjunto" está listo para despegar. La pista está despejada y la visibilidad es excelente. No hemos encontrado turbulencias en los datos, así que el vuelo hacia el análisis será suave y sin contratiempos.

Le recordamos que mantenga los cinturones de seguridad abrochados mientras navega por la información adjunta. Si encuentra alguna duda o necesita soporte durante el vuelo, nuestro equipo de tierra está a su disposición para asistirle.

Agradecemos su preferencia por nuestros servicios de análisis a bordo y le deseamos cielos despejados en su ruta de datos. Nos vemos en el próximo aviso de control.

Permiso para aterrizar concedido,
Barry Allen.
"""

mensaje = EmailMessage()
mensaje["From"] = email_envio
mensaje["To"] = email_recepcion
mensaje["Subject"] = subject
mensaje.set_content(body)

lista_imagenes = [
    "C:\\Users\\User\\OneDrive\\Escritorio\\proyecto_taller_arduino_2024\\numero_vuelos_por_aerolinea_colores.png",
    #"C:\\Users\\User\\OneDrive\\Escritorio\\proyecto_taller_arduino_2024\\numero_vuelos_porciudad_colores.png"
]

for archivo in lista_imagenes:
    if os.path.exists(archivo):
        tipo_mime, _ = mimetypes.guess_type(archivo)
        if tipo_mime is None:
            tipo_mime = "application/octet-stream"
        tipo_principal, subtipo = tipo_mime.split("/")
        with open(archivo, "rb") as f:
            mensaje.add_attachment(f.read(), maintype=tipo_principal, subtype=subtipo, filename=os.path.basename(archivo))
    else:
        print(f"No se encontró el archivo {archivo}")

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
    smtp.login(email_envio, password)
    smtp.sendmail(email_envio, email_recepcion, mensaje.as_string())