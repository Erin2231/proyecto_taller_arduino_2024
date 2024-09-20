###############################################################
##              ANÁLISIS DE VUELOS EN BARAJAS                ##
###############################################################
Este proyecto permite obtener y analizar datos en tiempo real de los vuelos que llegan y salen del aeropuerto de Madrid-Barajas (LEMD). Utiliza la API de AviationStack para obtener los datos, genera gráficos con matplotlib, y envía informes personalizados por correo electrónico mediante smtplib.

    REQUISITOS DEL PROYECTO

BIBLIOTECAS Y DEPENDENCIAS:

Este proyecto requiere las siguientes bibliotecas de Python:
    - streamlit: Para crear la interfaz de usuario.
    - requests: Para hacer solicitudes a la API de AviationStack.
    - pandas: Para manipulación de datos y creación de DataFrames.
    - matplotlib: Para generar gráficos de barras.
    - ast: Para la conversión de cadenas a diccionarios.
    - os: Para cargar las variables de entorno.
    - dotenv: Para gestionar variables de entorno.
    - smtplib y ssl: Para enviar correos electrónicos.
    - email.message: Para construir el correo con los archivos adjuntos.
    - mimetypes: Para gestionar tipos MIME.

Puedes instalar todas las dependencias usando el siguiente comando:
        "   
            pip install -r requirements.txt     
                                                "

ARCHIVO ".env":

Crea un archivo .env en el directorio principal para almacenar tus claves de API y credenciales de correo electrónico de forma segura.
        "   
            API_KEY=your_aviationstack_api_key
            PASSWORD=your_email_password        
                                                "

INSTRUCCIONES DE INSTALACION Y CONFIGURACION

    1.  Clonar el Repositorio
        "
            git clone https://github.com/tu-usuario/nombre-del-repositorio.git
            cd nombre-del-repositorio
                                                "
    #khefgkuywgfduwygfuywdgckwgqvwbvkcygywdkukycgwhgcfkjwhgckjgvjgvkjsdgkjhchvgksdvdkjhsdfgvkjrg
    
    2.  Instalar Dependencias
Asegúrate de tener Python 3.8+ instalado. Instala las dependencias del proyecto:
        "
            pip install -r requirements.txt
                                                "

    3.  Configurar el Archivo .env
Añade tus claves API y credenciales de correo en el archivo .env:
    -   API_KEY: Obtén una clave de la API de AviationStack aquí.
    -   PASSWORD: Tu contraseña de aplicación para Gmail (asegúrate de tener activada la autenticación de dos factores en Gmail).

    4.  Ejecutar la Aplicación
Para iniciar la aplicación web, ejecuta el siguiente comando:
        " 
            cd "ruta de acceso a la carpeta del proyecto
            streamlit rut app.py
                                                "

    5.  Usar la Aplicación
· Correo Electrónico: Ingresa tu correo electrónico para recibir el informe con el gráfico.
· Obtener Datos: La aplicación obtendrá los datos de vuelos desde la API de AviationStack.
· Generar Informe: Un gráfico con el número de vuelos por aerolínea será generado.
· Envío del Correo: El gráfico se enviará al correo proporcionado.

ESTRUCTURA DEL PROYECTO
├── app.py                                      # Código principal de la aplicación
├── envio_email.py                              # Código para el envÍo del correo electrónico
├── Hello_World.py                              # Nunca viene mal verificar que el Python es el correcto
├── proyectito_sin_interfaz.py                  # Código SIN la implementación de Streamlit
├── README.md                                   # Documentación del proyecto
├── recopilacion_de_datos.py                    # Dependencias del proyecto
├── requirements.txt                            # Dependencias del proyecto
├── .env                                        # Variables de entorno (no compartido en el repositorio)

USO DE LA API DE AVIATIONSTACK
La API de AviationStack se utiliza para obtener información sobre los vuelos de llegada y salida del aeropuerto de Madrid-Barajas.

Parámetros Principales
    -   arr_icao: El código ICAO del aeropuerto de llegada (LEMD para Barajas).
    -   dep_icao: El código ICAO del aeropuerto de salida (LEMD para Barajas).
    -   limit: Límite de resultados por consulta.

ENVÍO DE CORREOS
La aplicación utiliza las bibliotecas smtplib y ssl para enviar correos electrónicos con archivos adjuntos. Se utiliza Gmail para enviar el correo, por lo que necesitas generar una contraseña de aplicación para autenticación segura.

LICENCIA
Este proyecto está licenciado bajo la MIT License.