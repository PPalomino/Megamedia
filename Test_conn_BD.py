# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 04:28:29 2024

@author: Pablo Palomino
"""

# Librería para conectarse a la base de datos
from sqlalchemy import create_engine  

# Función para verificar la conexión a la base de datos
def verificar_conexion(db_uri: str) -> None:
    try:
        # Crear motor de conexión
        engine = create_engine(db_uri)
        # Establecer la conexión
        with engine.connect() as conn:
            result = conn.execute("SELECT * from videos;")
            print("Conexión exitosa. Resultado de la prueba:", result.scalar())
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")

# URI de conexión a la base de datos
db_uri = 'postgresql+psycopg://postgres:Ads1122@localhost:5434/YouTube_Data'

# Verificar conexión
verificar_conexion(db_uri)
