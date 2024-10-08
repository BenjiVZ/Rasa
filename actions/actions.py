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
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction

class ValidateFilterProductForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_filter_product_form"

    def validate_precio_min(
        self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        try:
            precio_min = float(value)
            if precio_min < 0:
                dispatcher.utter_message(text="El precio mínimo no puede ser negativo.")
                return {"precio_min": None}
            return {"precio_min": precio_min}
        except ValueError:
            dispatcher.utter_message(text="El valor ingresado para el precio mínimo no es válido.")
            return {"precio_min": None}

    def validate_precio_max(
        self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        try:
            precio_max = float(value)
            if precio_max < 0:
                dispatcher.utter_message(text="El precio máximo no puede ser negativo.")
                return {"precio_max": None}
            return {"precio_max": precio_max}
        except ValueError:
            dispatcher.utter_message(text="El valor ingresado para el precio máximo no es válido.")
            return {"precio_max": None}

class ActionConsultarProductos(Action):

    def name(self) -> Text:
        return "action_consultar_productos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Ejecutando la consulta de productos...")

        # Obtener la ruta completa del archivo de base de datos en la carpeta "database"
        db_path = r'C:\Users\Benjamin\Desktop\djangoapp-main\db.sqlite3'

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
        db_path = r'C:\Users\Benjamin\Desktop\djangoapp-main\db.sqlite3'

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

class ActionFiltrarProductos(Action):

    def name(self) -> Text:
        return "action_filtrar_productos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Ejecutando el filtro de productos...")

        # Obtener la ruta completa del archivo de base de datos
        db_path = r'C:\Users\Benjamin\Desktop\djangoapp-main\db.sqlite3'

        # Comprobar si el archivo de base de datos existe
        if not os.path.exists(db_path):
            dispatcher.utter_message(text=f"Error: No se encontró la base de datos en la ruta: {db_path}")
            return []

        try:
            # Conectar a la base de datos SQLite
            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()

            # Obtener los filtros del tracker
            marca_filtro = tracker.get_slot('marca')  # Entidad: marca
            nombre_filtro = tracker.get_slot('nombre')  # Entidad: nombre
            descripcion_filtro = tracker.get_slot('descripcion')  # Entidad: descripcion
            precio_min = tracker.get_slot('precio_min')  # Entidad: precio_min
            precio_max = tracker.get_slot('precio_max')  # Entidad: precio_max

            # Construir la consulta con los filtros
            query = '''
            SELECT p.nombre, p.precio, p.descripcion, m.nombre
            FROM myapp_producto p
            JOIN myapp_marca m ON p.marca_id = m.id
            WHERE 1=1
            '''
            parametros = []

            # Agregar condiciones a la consulta según los filtros
            if marca_filtro:
                query += " AND m.nombre LIKE ?"
                parametros.append(f"%{marca_filtro}%")
            
            if nombre_filtro:
                query += " AND p.nombre LIKE ?"
                parametros.append(f"%{nombre_filtro}%")

            if descripcion_filtro:
                query += " AND p.descripcion LIKE ?"
                parametros.append(f"%{descripcion_filtro}%")

            if precio_min:
                query += " AND p.precio >= ?"
                parametros.append(precio_min)

            if precio_max:
                query += " AND p.precio <= ?"
                parametros.append(precio_max)

            # Ejecutar la consulta con los parámetros
            cursor.execute(query, parametros)

            # Obtener los resultados de la consulta
            resultados = cursor.fetchall()

            # Crear un mensaje con los resultados
            if resultados:
                mensaje = "Aquí están los productos filtrados según los criterios:\n"
                for nombre, precio, descripcion, marca in resultados:
                    mensaje += f"- {nombre}: ${precio} (Marca: {marca}, Descripción: {descripcion})\n"
            else:
                mensaje = "No encontré productos que coincidan con los filtros."

            # Enviar el mensaje de vuelta al usuario
            dispatcher.utter_message(text=mensaje)

        except sqlite3.Error as e:
            dispatcher.utter_message(text=f"Error al acceder a la base de datos: {e}")
        finally:
            # Cerrar la conexión
            if 'conexion' in locals():
                conexion.close()

        return []