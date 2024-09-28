# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import sqlite3
import os
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

class ActionConsultarProductos(Action):

    def name(self) -> Text:
        return "action_consultar_productos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Ejecutando la consulta de productos...")

        # Obtener la ruta completa del archivo de base de datos en la carpeta "database"
        db_path = r'C:\Users\Benjamin\anaconda3\envs\jojoto\database\db.sqlite3'

        # Comprobar si el archivo de base de datos existe
        if not os.path.exists(db_path):
            dispatcher.utter_message(text=f"Error: No se encontró la base de datos en la ruta: {db_path}")
            return []

        try:
            # Conectar a la base de datos SQLite
            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()

            # Consulta para obtener productos y marcas
            query = '''
            SELECT p.nombre, p.precio, m.nombre
            FROM myapp_producto p
            JOIN myapp_marca m ON p.marca_id = m.id
            '''
            cursor.execute(query)

            # Obtener los resultados de la consulta
            resultados = cursor.fetchall()

            # Crear un mensaje con los resultados
            if resultados:
                mensaje = "Aquí están los productos disponibles:\n"
                for producto, precio, marca in resultados:
                    mensaje += f"- {producto}: ${precio} (Marca: {marca})\n"
            else:
                mensaje = "No encontré productos en la base de datos."

            # Enviar el mensaje de vuelta al usuario
            dispatcher.utter_message(text=mensaje)

        except sqlite3.Error as e:
            dispatcher.utter_message(text=f"Error al acceder a la base de datos: {e}")
        finally:
            # Cerrar la conexión
            if 'conexion' in locals():
                conexion.close()

        return []

class ActionConsultarMarcas(Action):

    def name(self) -> Text:
        return "action_consultar_marcas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Ejecutando la consulta de marcas...")

        # Obtener la ruta completa del archivo de base de datos en la carpeta "database"
        db_path = r'C:\Users\Benjamin\anaconda3\envs\jojoto\database\db.sqlite3'

        # Comprobar si el archivo de base de datos existe
        if not os.path.exists(db_path):
            dispatcher.utter_message(text=f"Error: No se encontró la base de datos en la ruta: {db_path}")
            return []

        try:
            # Conectar a la base de datos SQLite
            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()

            # Consulta para obtener las marcas
            query = "SELECT nombre FROM myapp_marca"
            cursor.execute(query)

            # Obtener los resultados de la consulta
            resultados = cursor.fetchall()

            # Crear un mensaje con los resultados
            if resultados:
                mensaje = "Aquí están las marcas disponibles:\n"
                for (marca,) in resultados:
                    mensaje += f"- {marca}\n"
            else:
                mensaje = "No encontré marcas en la base de datos."

            # Enviar el mensaje de vuelta al usuario
            dispatcher.utter_message(text=mensaje)

        except sqlite3.Error as e:
            dispatcher.utter_message(text=f"Error al acceder a la base de datos: {e}")
        finally:
            # Cerrar la conexión
            if 'conexion' in locals():
                conexion.close()

        return []
