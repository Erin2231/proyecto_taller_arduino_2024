import requests
import pandas as pd
import matplotlib.pyplot as plt
import ast
import os
from dotenv import load_dotenv

load_dotenv()

##########################################################################################
#   RECOGIDA DE DATOS DE VUELOS DE LLEGADAS Y SALIDAS EN EL AEROPUERTO DE MADRID-BARAJAS #
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
