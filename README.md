# ChatbotDGT 
## Vehicles & Insurances - Conversational Chatbot
![image](https://github.com/MRocioRR/ChatbotDGT/assets/52194835/57756900-8e60-4542-b75b-38fa376137dd)

📝Nota informativa: Proyecto elaborado en colaboración de compañeros de máster para el proyecto final. El proyecto necesita algunas mejoras para su buen uso.

ChatbotDGT es una aplicación intuitiva y fácil de usar diseñada para interactuar con datos de matriculaciones realizadas por la Dirección General de Tráfico (DGT), a través de consultas en lenguaje natural. Este sistema innovador marca un hito en la manera en que los usuarios pueden acceder y analizar información relevante, prescindiendo de la necesidad de dominar técnicas de consulta SQL o tener conocimientos avanzados en gestión de bases de datos.

Mediante la incorporación de tecnologías de procesamiento de lenguaje natural (PLN) junto con la robusta infraestructura de almacenamiento y análisis de datos de Snowflake, ChatbotDGT simplifica la ejecución de consultas complejas y la extracción de información valiosa de forma directa. Los usuarios solo tienen que formular sus preguntas o requerimientos en un lenguaje que les resulte natural, y la aplicación se encarga de transformar estas interacciones en consultas SQL específicas que se ejecutan sobre los datos almacenados en Snowflake, particularmente aquellos relacionados con las matriculaciones de la DGT.

Esta estrategia no solo optimiza el proceso de análisis de datos, sino que también lo hace accesible para una amplia gama de perfiles dentro de una organización, abarcando desde analistas de negocio y gestores de proyectos hasta integrantes del equipo técnico. Al democratizar el acceso a los datos y facilitar su análisis, ChatbotDGT promueve la toma de decisiones informadas y contribuye a fomentar una cultura de datos más inclusiva y colaborativa.

## Obtención de datos
Uso de la base de datos de matriculaciones de vehículos nuevos que provee la DGT. Es importante mencionar que esta base de datos se actualiza de manera diaria y se puede consultar a través de su página web en el siguiente enlace:
https://www.dgt.es/nuestros-servicios/tu-vehiculo/tus-vehiculos/consulta-los-datos-de-tus-vehiculos/

- Adjuntos:
  - Archivo análisis.ipynb que engloba todo el análisis de la base de datos original con más de 3 millores de registros de los años compredidos entre 2021 y 2023.
  - Archivo tablafinal.sql con los scripst para la obtención de la data. 
  - Archivo archivo llamado "data.txt" donde puede se visulizar los datos con lo que el chatbot trabaja.


## Descripción técnica
Este chatbot está construido con Streamlit y Langchain. La versión actual utiliza el modelo de chat OpenAI ("gpt-3") para generar respuestas, siendo sencillo cambiar esta opción si precisas de otro modelo.

## Requisitos previos: 
- Python entre las versiones  3.10 - 3.12
- Tener un entorno de trabajo en Snowflake y subida la base de datos

## Ejecución de la aplicación
Una vez que el entorno esté configurado y los secretos (ver el archivo secrects-example) estén establecidos, incluida la conexión a un entorno de Snowflake con la vista relevante, la aplicación se puede ejecutar mediante:

### 1. Instalar virtualenv:
```sh
python3 -m pip install virtualenv
```
### 2. Crear un entorno virtual (permitiendo separar y manejar de forma independiente las bibliotecas y paquetes para proyectos específicos.):
```sh
virtualenv env
```
### 3. Configurar la política de ejecución (solo para Windows):
```sh
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass 
```
### 4. Activar el entorno virtual (es importante activar el entorno antes de instalar los "requirements" para asegurarse de que se instalen en el entorno virtual y no en el sistema globalmente.):
```sh
.\.venv\Scripts\activate
```
### 5. Instalar dependencias:
```sh
.\.venv\Scripts\pip install -r requirements.txt  
```
### 6. Ejecutar la aplicación (Mención: Streamlit facilita la creación de aplicaciones web para proyectos de ciencia de datos y machine learning de forma rápida y sencilla.):
```sh
streamlit run src/main.py
```

**📝Nota informativa:** Es importante seguir estos pasos en el orden dado para asegurar que el entorno esté correctamente configurado y las dependencias estén instaladas en el entorno virtual, evitando conflictos con otras instalaciones de Python que puedas tener en tu sistema.


## Visión General (foto o video de la app)


## Un ejemplo práctico de como crea un chatbot con streamlit simple y rápido
El tutorial completo se encuentra aquí:
https://quickstarts.snowflake.com/guide/frosty_llm_chatbot_on_streamlit_snowflake/#0
