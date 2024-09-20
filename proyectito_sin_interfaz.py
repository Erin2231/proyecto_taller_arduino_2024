import requests
import pandas as pd
import matplotlib.pyplot as plt
import ast
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
import mimetypes

##########################################################################################
#  RECOGIDA DE DATOS DE VUELOS DE LLEGADAS Y SALIDAS EN EL AEROPUERTO DE MADRID-BARAJAS  #
##########################################################################################

print("Hacer solicitud a la API o no: (s/n)")
respuesta = input()
excel_doc = 'vuelos_barajas.xlsx'

if respuesta == "s":

    # Configuración de la API de AviationStack
    base_url = "http://api.aviationstack.com/v1/flights"
    api_key = os.getenv("API_KEY")  # Reemplaza con tu clave API

    # Parámetros para obtener vuelos de llegadas y salidas en Barajas (LEMD)
    params_llegadas = { 'access_key': api_key,
        'arr_icao': 'LEMD',  # Código ICAO para el aeropuerto de Madrid-Barajas
        'limit': 50,        # Límite de resultados por solicitud
    }

    params_salidas = {
        'access_key': api_key, 
        'dep_icao': 'LEMD', 
        'limit': 50, 
    }

    # Solicitar datos de llegadas
    respuesta_llegadas = requests.get(base_url, params=params_llegadas)
    datos_llegadas = respuesta_llegadas.json()['data']

    # Solicitar datos de salidas
    respuesta_salidas = requests.get(base_url, params=params_salidas) #recoje datos de la API
    datos_salidas = respuesta_salidas.json()['data'] #pasar de json a data(la estructura estandar de ordenar datos en las APIs)

    # Convertir los datos de llegadas y salidas en DataFrames de pandas (estructura de tabla tabulada para que lo entienda Excel)
    llegadas_df = pd.DataFrame(datos_llegadas) #se puede pasar muy simple porq comparten una estructura similara a un diccionario los dos
    salidas_df = pd.DataFrame(datos_salidas)

    # Unir ambos DataFrames para obteneros en un solo DataFrame y que su analisis sea mas sencillo
    vuelos_df = pd.concat([llegadas_df, salidas_df])

    # Guardar los datos en un archivo Excel
    with pd.ExcelWriter(excel_doc) as writer:
        llegadas_df.to_excel(writer, sheet_name='Llegadas', index=False)
        salidas_df.to_excel(writer, sheet_name='Salidas', index=False)
        
    print(f"Datos guardados en el archivo Excel: {excel_doc}")
    
elif respuesta == "n":
    print("No se ha hecho la solicitud a la API")

else:
    print("Respuesta no válida")

llegadas_df=pd.read_excel("vuelos_barajas.xlsx",sheet_name="Llegadas")
salidas_df=pd.read_excel("vuelos_barajas.xlsx",sheet_name="Salidas")
vuelos_df = pd.concat([llegadas_df, salidas_df])

##########################################################################################
#               ANALISIS DE DATOS CON PANDAS Y CREACION DE GRAFICOS                      #
##########################################################################################

plt.style.use("classic")

# Convertir las entradas de la columna 'airline' de strings a diccionarios
def convertir_a_diccionario(string):
    try:
        return ast.literal_eval(string)  # Convertir string a diccionario
    except (ValueError, SyntaxError):
        return {}  # Retornar un diccionario vacío en caso de error

#GRAFICO 1: Número de Vuelos por Aerolínea en Barajas (grafico de barras)

# Aplicar la conversión a la columna 'airline'
vuelos_df['airline'] = vuelos_df['airline'].apply(convertir_a_diccionario)

# Extraer solo el nombre de la aerolínea
vuelos_df['airline_name'] = vuelos_df['airline'].apply(lambda x: x.get('name', 'Desconocido'))

# Contar el número de vuelos por aerolínea
vuelos_por_aerolinea = vuelos_df['airline_name'].value_counts()

# Crear una lista de colores distintos para cada aerolínea
colors = plt.cm.tab20.colors[:len(vuelos_por_aerolinea)]  # Colores diferentes

# Mostrar el gráfico de Número de Vuelos por Aerolínea
plt.figure(figsize=(10, 6))
vuelos_por_aerolinea.plot(kind='bar', color=colors)

# Añadir título y etiquetas
plt.title('Número de Vuelos por Aerolínea en Barajas')
plt.xlabel('Aerolínea')
plt.ylabel('Número de Vuelos')

# Asegurar que los nombres de las aerolíneas aparezcan debajo de cada barra
plt.xticks(rotation=60, ha="right")

# Ajustar los márgenes para evitar que los nombres se corten
plt.tight_layout()

# Guardar el gráfico
plt.savefig('numero_vuelos_por_aerolinea_colores.png')

#GRAFICO 2: Vuelos con retraso por franja de retraso (grafico de pastel)
#lo dejaremos papra cuando me apetezca :)

##########################################################################################
#                                   ENVIO DE MAIL                                        #
##########################################################################################

load_dotenv() # Cargar las variables de entorno desde el archivo .env (seguridad)

email_envio = "asitentedevuelo@gmail.com"
password = os.getenv("PASSWORD")
email_recepcion = "martina.ricart@gmail.com"

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

print("Correo enviado con éxito")