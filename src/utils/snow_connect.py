from typing import Any, Dict

import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.version import VERSION

# Definición de la clase SnowflakeConnection
class SnowflakeConnection:
    """
    This class is used to establish a connection to Snowflake.

    Attributes
    ----------
    connection_parameters : Dict[str, Any]
        A dictionary containing the connection parameters for Snowflake.
    session : snowflake.snowpark.Session
        A Snowflake session object.

    Methods
    -------
    get_session()
        Establishes and returns the Snowflake connection session.

    """
    # Constructor de la clase
    def __init__(self):
        # Obtiener los parámetros de conexión desde variables de entorno y los almacena en el atributo
        self.connection_parameters = self._get_connection_parameters_from_env()
        # Inicializa el atributo de sesión como None
        self.session = None
        
    # Método estático para obtener los parámetros de conexión desde variables de entorno
    @staticmethod
    def _get_connection_parameters_from_env() -> Dict[str, Any]:
        # Definir un diccionario con los parámetros de conexión extraídos de las variables de entorno
        connection_parameters = {
            "account": st.secrets['snowpark']["SF_ACCOUNT"],
            "user": st.secrets['snowpark']["SF_USER"],
            "password": st.secrets['snowpark']["SF_PASSWORD"],
            "warehouse": st.secrets['snowpark']["SF_WAREHOUSE"],
            "database": st.secrets['snowpark']["SF_DATABASE"],
            "schema": st.secrets['snowpark']["SF_SCHEMA"],
            "role": st.secrets['snowpark']["SF_ROLE"],
        }
        # Devuelve el diccionario con los parámetros
        return connection_parameters

    # Método para establecer y devolver la sesión de conexión con Snowflake
    def get_session(self):
        """
        Establishes and returns the Snowflake connection session.
        Returns:
            session: Snowflake connection session.
        """
        # Si la sesión no ha sido creada aún, la crea utilizando los parámetros de conexión
        if self.session is None:
            self.session = Session.builder.configs(self.connection_parameters).create()
            # Habilitar el simplificador de SQL en la sesión
            self.session.sql_simplifier_enabled = True
        # Devuelve el objeto de sesión
        return self.session
