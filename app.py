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
import streamlit as st

load_dotenv() # Cargar las variables de entorno desde el archivo .env (seguridad)

##########################################################################################
#  RECOGIDA DE DATOS DE VUELOS DE LLEGADAS Y SALIDAS EN EL AEROPUERTO DE MADRID-BARAJAS  #
##########################################################################################

def obtener_datos_vuelos(api_key, excel_doc, limit = 50):
    base_url = "http://api.aviationstack.com/v1/flights"
    
    params_llegadas = { 
        'access_key' : api_key,
        'arr_icao' : 'LEMD',
        'limit' : limit,
    }
    params_salidas = {
        'access_key' : api_key,
        'dep_icao' : 'LEMD',
        'limit' : limit,
    }

    # Solicitar datos de llegadas
    respuesta_llegadas = requests.get(base_url, params=params_llegadas)
    datos_llegadas = respuesta_llegadas.json()['data']

    # Solicitar datos de salidas
    respuesta_salidas = requests.get(base_url, params=params_salidas)
    datos_salidas = respuesta_salidas.json()['data']

    # Convertir los datos de llegadas y salidas en DataFrames de pandas (estructura de tabla tabulada para que lo entienda Excel)
    llegadas_df = pd.DataFrame(datos_llegadas) #se puede pasar muy simple porq comparten una estructura similara a un diccionario los dos
    salidas_df = pd.DataFrame(datos_salidas)

    # Unir ambos DataFrames para obteneros en un solo DataFrame y que su analisis sea mas sencillo
    vuelos_df = pd.concat([llegadas_df, salidas_df])

    # Guardar los datos en un archivo Excel
    with pd.ExcelWriter(excel_doc) as writer:
        llegadas_df.to_excel(writer, sheet_name='Llegadas', index=False)
        salidas_df.to_excel(writer, sheet_name='Salidas', index=False)
 
    return vuelos_df

def generar_grafico_vuelos_por_aerolinea(vuelos_df):
    plt.style.use("classic")
    
    # Convertir las entradas de la columna 'airline' de strings a diccionarios
    vuelos_df['airline'] = vuelos_df['airline'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # Extraer solo el nombre de la aerolínea
    vuelos_df['airline_name'] = vuelos_df['airline'].apply(lambda x: x.get('name', 'Desconocido') if isinstance(x,dict) else 'Desconocido')

    #Contar el número de vuelos por aerolínea
    vuelos_por_aerolinea = vuelos_df['airline_name'].value_counts()

    # Colores diferentes para cada aerolínea
    colors = plt.cm.tab20.colors[:len(vuelos_por_aerolinea)]

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    vuelos_por_aerolinea.plot(kind='bar', color=colors)
    plt.title('Número de Vuelos por Aerolínea en Barajas')
    plt.xlabel('Aerolínea')
    plt.ylabel('Número de Vuelos')
    plt.xticks(rotation=60, ha="right")
    plt.tight_layout()

    # Guardar el gráfico
    grafico_path = 'numero_vuelos_por_aerolinea.png'
    plt.savefig(grafico_path)

    return grafico_path

def enviar_correo(email_recepcion, grafico_path):
    email_envio = "asitentedevuelo@gmail.com"
    password = os.getenv("PASSWORD")

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


    if os.path.exists(grafico_path):
        tipo_mime, _ = mimetypes.guess_type(grafico_path)
        if tipo_mime is None:
            tipo_mime = "application/octet-stream"
        tipo_principal, subtipo = tipo_mime.split("/")
        with open(grafico_path, "rb") as f:
            mensaje.add_attachment(f.read(), maintype=tipo_principal, subtype=subtipo, filename=os.path.basename(grafico_path))
    else:
        return "No se ha encontrado el archivo del gráfico."
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_envio, password)
        smtp.sendmail(email_envio, email_recepcion, mensaje.as_string())
    
    return "Correo enviado con éxito"

##########################################################################################
#                           INTERFAZ DE USUARIO EN STREAMLIT                             #
##########################################################################################

st.title("Analisis de Vuelos en BARAJAS")

email_recepcion = st.text_input('Introduce tu correo electrónico para recibir el informe:')

if st.button('Obtener Datos y genera Informe'):
    if not email_recepcion:
        st.error("Por favor, introduce un correo electrónico válido.")
    else:
        st.info("Obteniendo datos de vuelos...")

        api_key = os.getenv("API_KEY")
        excel_doc = 'vuelos_barajas.xlsx'

        if not api_key:
            st.error("Falta la clave de API. Por favor, revisa el archivo .env.")
        else:
            try:
                vuelos_df = obtener_datos_vuelos(api_key, excel_doc)
                st.success("Datos de vuelos obtenidos con éxito.")

                st.info("Enviando correo electronico...")
                resultado_envio = enviar_correo(email_recepcion, generar_grafico_vuelos_por_aerolinea(vuelos_df))
                st.success(resultado_envio)
            
            except Exception as e:
                st.error(f"Error al obtener los datos de vuelos: {e}")
