#
#  Proyecto Demanda Energética Tenerife


#  Jose Luis Quintero García (c) feb2023

# Corrección de errores: al descargar los archivos de datos, algunos han dado error, generando un CSV vacío
# Volveremos a descargar aquí esos archivos, comprobando si están o no vacíos
# Datos desde https:\\demanda.ree.es

# Librerías
import sys
from os import path, listdir
from pathlib import PurePath
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium.common import exceptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# Inicialización de Variables
url_base = "https://demanda.ree.es/visiona/canarias/tenerife5m/tablas/"
lista_vacios = []
lista_errores = []

# Crea la lista de archivos defectuosos. El archivo tyxt se ha creado a partir de los mensajes de excepción
# que resultan en "listado_paginas.py" cuando se encuentra un archivo vacío: se han copiado todos esos mensajes
# de error a un txt, dejando solo la fecha de la ruta, creándose así el archivo "errores.txt"
with open("errores.txt", "r") as file:
    for fecha in file:
        lista_errores.append(fecha.rstrip('\n'))

# Crea el driver de Selenium para cargar las páginas dinámicas de cada día
options = webdriver.ChromeOptions()
options.add_argument("--headless") # No muestra el navegador que se abre

# Recorre los días desde start_date a start_date + PLAZO
for day in lista_errores:
    url = url_base + day + "/1"
    print(url)

    # Define el nombre del archivo con el que vamos a grabar los datos
    file_name_sinextyension = PurePath(url.split('/')[-2]).name
    file_name = file_name_sinextyension + ".csv"
    file_path = path.join(".","web", file_name)

    # Hay que crear el driver cada vez que carguemos una página
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) 
       
    print(f"[INFO] Descargando archivo '{file_path}'")
    driver.get(url) 

    # Descargamos la tabla de datos del día elegido, metiendo una espera hasta que se haya cargado la tabla
    # Sin la espera, es fácil que aparezca un error al intentar obtener el objeto sin haberse terminado de generar la tabla
    tabla_dia = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'tabla_evolucion')))
    tabla_dia = tabla_dia.find_elements(By.XPATH, 'tbody/tr')
    lista_temporal = []

    # Ahora recogemos los datos de cada columna, registro por registro, hasta acabar la tabla
    # Solo descargo fecha (fecha y hora) y consumo real (el resto no me interesa).
    # El primer elemento son los títulos de la tabla, que debo obviar, así que recorro la lista por índices, 
    # metiendo los datos que queremos en un diccionario
    for num_registro in range(1, len(tabla_dia)):
        registro = tabla_dia[num_registro]

        datos = registro.find_elements(By.TAG_NAME, "td")
        registro_dict = {
            "fecha": datos[0].text,
            "consumo": datos[1].text
            }
        # Añadimos cada registro a una tabla temporal, con las variables ya separadas en el diccionario
        lista_temporal.append(registro_dict)

    # Convertimos la lista en Dataframe para exportar a CSV (1 CSV por día)
    data = pd.DataFrame(lista_temporal)
    data = data.dropna()
    # Comprobamos si sigue estando vacío
    if not data.empty:
        data.to_csv(file_path, index=False)
    else:
        print(f"El archivo {file_name_sinextyension} sigue estando vacío")
        lista_vacios.append(file_name_sinextyension)
    driver.close

print("[INFO] Descargados archivos CSV")
print(lista_vacios)

