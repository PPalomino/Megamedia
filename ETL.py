# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 22:30:25 2024

@author: Pablo Palomino

"""

# Librería para realizar solicitudes HTTP
import requests
# Librería para manipulación y análisis de datos
import pandas as pd
# Librería para conectarse a la base de datos
from sqlalchemy import create_engine  
# Biblioteca para trabajar con fechas y horas
from datetime import datetime
# Librería para especificar tipos de datos en las funciones
from typing import List, Tuple
# Librería adicional para ejecutar comandos de administración 
from sqlalchemy import text

# Configuración de la API para autenticar las solicitudes de YouTube
API_KEY = 'AIzaSyCdrebworNo2iTcXg3WYAwwFKRzsqDgPok'

# ID del canal de Meganoticias en Vivo, desde donde se extraerán los datos
CHANNEL_ID = 'UCkccyEbqhhM3uKOI6Shm-4Q'

# Función para obtener IDs de los videos
def obtener_ids_videos(api_key: str, channel_id: str) -> List[str]:
    
    url: str = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=id&order=date&maxResults=20'
   
    # Hacemos la solicitud a la API de YouTube
    response = requests.get(url)
    
    # Imprimir el estado de la solicitud y la URL para depuración
    print(f"Estado de la solicitud: {response.status_code}")
    print(f"URL de la solicitud: {url}")
    
    # Parseamos la respuesta JSON
    data = response.json()
    
    # Imprimir la respuesta completa para verificar su contenido
    print(f"Respuesta completa: {data}")
    
    # Verificar si la clave 'items' está presente en la respuesta
    if 'items' not in data:
        raise ValueError("La respuesta de la API no contiene la clave 'items'. Verifica tu clave de API y el ID del canal.")
    
    # Lista para almacenar los IDs de los videos
    video_ids: List[str] = []
    for item in data['items']:
        if item['id']['kind'] == 'youtube#video':
            # Extraemos el ID del video.
            video_id: str = item['id']['videoId']
            video_ids.append(video_id)
    return video_ids

# Función para obtener detalles de videos por IDs
def obtener_datos_videos(api_key: str, video_ids: List[str]) -> List[Tuple[str, str, str, str, int]]:

    # Lista para almacenar los detalles de los videos.
    video_data: List[Tuple[str, str, str, str, int]] = []
    
    for video_id in video_ids:
        url: str = f'https://www.googleapis.com/youtube/v3/videos?key={api_key}&id={video_id}&part=snippet,contentDetails,statistics'
        
        # Hacemos la solicitud GET para cada video ID.
        response = requests.get(url)
        
        # Convertir la respuesta JSON a una variable de Python
        data = response.json()
        
        # Verificar si 'items' está presente en la respuesta
        if 'items' not in data:
            raise ValueError("La respuesta de la API no contiene la clave 'items'. Verifica tu clave de API y el ID del video.")
        
        # Extraemos los datos
        for item in data['items']:
            title: str = item['snippet']['title']
            published_at: str = item['snippet']['publishedAt']
            duration: str = item['contentDetails']['duration']
            views: int = int(item['statistics']['viewCount'])
            
            # Se agregan los detalles del video a la lista
            video_data.append((video_id, title, published_at, duration, views))
    
    return video_data

# Función para transformar los datos
def transformar_datos(video_data: List[Tuple[str, str, str, str, int]]) -> pd.DataFrame:
    
    # Crear un DataFrame de pandas a partir de los datos de los videos
    df: pd.DataFrame = pd.DataFrame(video_data, columns=['video_id', 'titulo', 'fecha_publicacion', 'duracion', 'reproducciones'])
    # Convertir la columna fecha_publicacion a un objeto de fecha y hora
    df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'])
    # se agrega la fecha de extracción
    df['fecha_extraccion'] = datetime.now() 
    
    return df  # Retornar el DataFrame transformado

# Función para cargar los datos en PostgreSQL con TimescaleDB
def cargar_datos(df: pd.DataFrame, db_uri: str) -> None:

    # Creamos una conexión a la base de datos utilizando SQLAlchemy
    engine = create_engine(db_uri)
    
    # Convertir a una hypertable si no lo es 
    with engine.connect() as conn: 
        # Asegurar que TimescaleDB esté habilitado y convertir la tabla en una Hypertable.
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;"))
        conn.execute(text("SELECT create_hypertable('videos', 'fecha_publicacion', if_not_exists => TRUE);"))
    
    # Cargamos los datos del DataFrame en la tabla 'videos' de la base de datos
    df.to_sql('videos', engine, if_exists='append', index=False)


# Pipeline ETL
try:
    video_ids = obtener_ids_videos(API_KEY, CHANNEL_ID)
    video_data = obtener_datos_videos(API_KEY, video_ids)
    transformed_data = transformar_datos(video_data)
    cargar_datos(transformed_data, 'postgresql+psycopg://postgres:Ads1122@localhost:5434/YouTube_Data')
except Exception as e:
    print(f"Error durante el proceso ETL: {e}")
