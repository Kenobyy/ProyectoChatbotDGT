# Importar las bibliotecas necesarias
import streamlit as st # Importa Streamlit para la creación de aplicaciones web

from langchain.embeddings.openai import OpenAIEmbeddings # Importa "embeddings" de OpenAI para procesamiento de lenguaje
import os # Importa "os" para interactuar con el sistema operativo
import constants as constants # Importa "constants" definidas en otro archivo
import utils.utils as utils # Importa "utils" definidas en otro módulo
from dotenv import load_dotenv, find_dotenv # Importa funciones para cargar variables de entorno

from utils.snow_connect import SnowflakeConnection  # Importa una clase para conexión con Snowflake
from openai import OpenAI # Importa "la API de OpenAI" para interactuar con modelos de lenguaje
import re # Importa "re" para expresiones regulares

# Inicializa el cliente de OpenAI
client = OpenAI()

# Carga las variables de entorno del archivo .env
load_dotenv(find_dotenv(), override=True)

# Configuración de título y descripción en la aplicación Streamlit
st.title("🧐 Vehicles & Insurances - Conversational Chatbot")
st.caption("Desarrollado por alumnos de EIP 👩‍💻 con IA 🤖")

# Creo sidebar con información sobre el bot
with open("ui/sidebar.md", "r", encoding='utf-8') as sidebar_file: # Lee el contenido del archivo de la barra lateral
   sidebar_content = sidebar_file.read() # Muestra el contenido de la barra lateral

# Toggle para mostrar o no consultas SQL
st.sidebar.markdown(sidebar_content)

show_sql = st.sidebar.toggle('Mostrar SQL', value=False)
    
# Menú en el sidebar para elegir la tabla sobre la que realizar la consulta
selected_table = st.sidebar.selectbox(
    label="Selecciona una tabla:",
    options=constants.tables,
    format_func=lambda x: constants.tables_options.get(x)
)

# Formatea y muestra la tabla seleccionada
format_selected_table = constants.tables_options.get(selected_table)

st.sidebar.markdown(f"### Información de la tabla {format_selected_table}")
st.sidebar.markdown(f"{constants.dgt_info}")


# Inicialización de las credenciales de Snowflake y Pinecone
SF_USER = st.secrets["snowpark"]["SF_USER"]
SF_PASSWORD = st.secrets["snowpark"]["SF_PASSWORD"]
SF_ACCOUNT = st.secrets["snowpark"]["SF_ACCOUNT"]
SF_DATABASE = st.secrets["snowpark"]["SF_DATABASE"]
SF_SCHEMA = st.secrets["snowpark"]["SF_SCHEMA"]
SF_WAREHOUSE = st.secrets["snowpark"]["SF_WAREHOUSE"]
SF_ROLE = st.secrets["snowpark"]["SF_ROLE"]

# Inicializar messages para chat
INITIAL_MESSAGE = [
    {
        "role": "assistant",
        "content": "¡Hola!, soy tu asistente de conocimiento sobre los datos de matriculaciones. Pregúntame lo que quieras y estaré encantado de buscar entre los datos lo que necesites.",
    },
]
# Verifica si 'messages' no está en el estado de la sesión y lo inicializa
if "messages" not in st.session_state.keys():
    st.session_state["messages"] = INITIAL_MESSAGE
# Verifica si 'history' no está en el estado de la sesión y lo inicializa
if "history" not in st.session_state:
    st.session_state["history"] = []

# Formato de URL de conexión a Snowflake
snowflake_url = f"snowflake://{SF_USER}:{SF_PASSWORD}@{SF_ACCOUNT}/{SF_DATABASE}/{SF_SCHEMA}?warehouse={SF_WAREHOUSE}&role={SF_ROLE}"

# Nota en el sidebar sobre la limitación de la memoria del chatbot
st.sidebar.markdown(
    "**Nota:** <span style='color:red'>El chatbot no cuenta con memoria en la conversación ya que esto supondría un aumento de coste debido al número de tokens.</span>",
    unsafe_allow_html=True,
)

# Función para verificar la seguridad de una consulta SQL
def sql_query_check(query):
    # Expresión regular para buscar palabras clave peligrosas
    palabras_clave_peligrosas = re.compile(r'\b(?:DROP|ALTER|TRUNCATE|DELETE|INSERT|UPDATE)\b', re.IGNORECASE)
    
    # Comprobación de la presencia de palabras clave peligrosas
    if palabras_clave_peligrosas.search(query):
        return False # Devuelve False si se encuentran palabras peligrosas
    
    # Comprobación de que la consulta comienza con "SELECT"
    resultado = query.strip().upper().startswith("SELECT")
    
    # Comprobación de si la query comienza con SELECT
    return resultado

# Función para manejar el historial de chat
def append_chat_history(question, answer):
    st.session_state["history"].append((question, answer))

# Función para añadir mensajes al historial de chat
def append_message(content, role="assistant", display=False):
    message = {"role": role, "content": content} # Crea un nuevo mensaje
    st.session_state.messages.append(message) # Añade el mensaje al estado de la sesión
    # Si el mensaje no es un dato, lo añade al historial de chat
    if role != "data":
        append_chat_history(st.session_state.messages[-2]["content"], content)

# Función para ejecutar consultas SQL utilizando una conexión existente
def execute_sql(query, conn):
    return conn.sql(query).collect() # Ejecuta la consulta SQL y recoge los resultados

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]): # Crea un contenedor de mensaje de chat
        st.markdown(message["content"]) # Muestra el contenido del mensaje

# Aceptar entrada de usuario
if prompt := st.chat_input("¿Qué quieres saber?"):
    # Añade el mensaje del usuario al historial de chat
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Muestra el mensaje del usuario en un contenedor de mensaje de chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara para mostrar la respuesta del asistente en un contenedor de mensaje de chat
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # Lugar para mostrar mensajes dinámicos
        full_response = "" # Inicia la respuesta completa como una cadena vacía
        
        # Copia los ejemplos de aprendizaje y añade el mensaje actual del usuario
        temp_context = constants.few_shot_learning_examples.copy()
        temp_context.append({"role": "user", "content": prompt})
        
        # Obtener respuesta del modelo de OpenAI
        response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                stream=False,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in temp_context
                ],
            )
            
        chat_response = response.choices[0].message.content # Almacena la respuesta

        print(f"Respuesta del primer LLM: {chat_response}")
                
        # Si lo devuelto por el primer LLM es una query SQL
        if sql_query_check(chat_response):

            try:
                conn = SnowflakeConnection().get_session() # Obtiener la sesión de Snowflake
                df = execute_sql(chat_response, conn) # Ejecutar la consulta SQL
                
                # Agregar los resultados de la consulta al contexto para interpretación
                temp_context.append({"role": "user", "content": f"Estos son los resultados de la query: {df}\n¿Qué interpretación podrías dar?"})
                
                # Obtiener la interpretación de los resultados por parte del modelo de OpenAI
                for response in client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    stream=True,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in temp_context
                    ]
                ):
                    full_response += (response.choices[0].delta.content or "")
                    message_placeholder.markdown(full_response + "▌") # Muestra la respuesta con un indicador de continuación
                
                # Si se debe mostrar el SQL, añade la consulta SQL a la respuesta
                if show_sql:
                    full_response = f"""Código SQL:\n\n ```sql\n\n {chat_response} \n``` \n\n --- \n\n {full_response}"""

                message_placeholder.markdown(full_response) # Muestra la respuesta completa

            except Exception as e:
                print(f"EXCEPTION: {e}")
                full_response = "No puedo responderte a eso" # Manejo de excepciones

        # Si lo devuelto por el primer LLM no es una query SQL
        else:
            full_response = "No puedo responderte a eso."
            message_placeholder.markdown(full_response)

        # Añade la respuesta del asistente al historial de chat
        st.session_state.messages.append({"role": "assistant", "content": full_response})