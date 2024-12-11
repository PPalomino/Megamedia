# YouTube Data ETL Project

Este proyecto implementa un pipeline de ETL (Extracción, Transformación y Carga) para recuperar datos de la API de YouTube, almacenarlos en una base de datos de series temporales PostgreSQL con TimescaleDB y generar informes de análisis en un notebook de Jupyter.

## Requisitos

- Python 3.7+
- PostgreSQL 13+
- GIT 2.4+
- TimescaleDB 16+
- Las siguientes bibliotecas de Python (listadas en `requirements.txt`):
  - pandas
  - matplotlib
  - sqlalchemy
  - jupyter
  - requests
  - psycopg2-binary

## Instalación

1. **Clonar el Repositorio**:
   	sh: git clone https://github.com/PPalomino/Megamedia.git

2. Navegar al Directorio del Proyecto:
	cd Megamedia

3. Instalar las Dependencias:
	pip install -r requirements.txt	

4. Configuración de la Base de Datos:
	Instalar PostgreSQL y TimescaleDB (en caso de que no estén instaladas): Sigue las instrucciones oficiales para instalar PostgreSQL y TimescaleDB.
	Configurar la Base de Datos: Crea una base de datos llamada YouTube_Data.
	Asegúrate de que TimescaleDB esté habilitado en tu base de datos.

5. Ejecución del Script ETL
	Configurar el API Key de YouTube:
	Asegúrate de tener un API Key válido de YouTube Data API.
	Importante:Reemplaza Tu_API_KEY en el script ETL.py con tu API Key.

6. Ejecutar el Script ETL: python ETL.py

7. Uso del Notebook de Análisis:
	Abrir Jupyter Notebook: 
		sh:jupyter notebook
	Abrir el Archivo: Informe_ETL.ipynb (Sigue las celdas del notebook para realizar el análisis y generar gráficos)

8. Pruebas
	Prueba de Extracción de Datos: python test_API.py
	Prueba de conexión a PostgreSQL: python Test_conn_BD.py

9. Finalmente se adjunta archivo denominado Resolución Caso Megamedia.docx, el cual contiene el detalle de las actividades realizadas y evidencias de las mismas.
