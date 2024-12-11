# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 20:30:58 2024

@author: Pablo Palomino
"""

import requests

# Configuración de la API para autenticar las solicitudes de YouTube
API_KEY = 'AIzaSyCdrebworNo2iTcXg3WYAwwFKRzsqDgPok'

# ID del canal de Meganoticias en Vivo, desde donde se extraerán los datos
CHANNEL_ID = 'UCkccyEbqhhM3uKOI6Shm-4Q'

url = f'https://www.googleapis.com/youtube/v3/channels?key={API_KEY}&id={CHANNEL_ID}&part=snippet'

response = requests.get(url)
print(response.status_code)
print(response.json())
