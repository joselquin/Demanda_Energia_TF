#
#  Proyecto Demanda Energética Tenerife


#  Jose Luis Quintero García (c) feb2023

# Creación del dataset con histórico de demanda de energía cada 5m en Tenerife
# Datos desde https:\\demanda.ree.es

# Librerías
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
start_date = datetime(2023, 2, 16)
PLAZO = 15 # Finalización desde fecha de inicio en años
end_date = start_date + relativedelta(days=PLAZO) # Uso de relativedelta en vez de timedelta, pues timedelta no admite years

# Diferencia entre fecha de inicio y fecha de fin en días 
dif_fechas = (end_date - start_date).days

# Crea el driver de Selenium para cargar las páginas dinámicas de cada día
options = webdriver.ChromeOptions()
options.add_argument("--headless") # No muestra el navegador que se abre

# Recorre los días desde start_date a start_date + PLAZO
for day in range(dif_fechas):
    date = start_date + timedelta(days=day)
    url = url_base + date.strftime('%Y-%m-%d') + "/1"
    print(url)

    # Define el nombre del archivo con el que vamos a grabar los datos
    file_name = PurePath(url.split('/')[-2]).name + ".csv"
    file_path = path.join(".","web", file_name)

    # Si el archivo no existe, lo descarga
    if not path.exists(file_path):
    
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
        data.to_csv(file_path, index=False)
        driver.close
    else:
        print(f"[INFO] Archivo '{file_path}' ya existe")
    
print("[INFO] Descargados archivos CSV")

# Borra los ejemplos con alguna columna vacía
# Lo suyo es hacer esto en el momento de descargar los CSV al principio, pero no lo hice entonces 
# y no los voy a descargar de nuevo ;)
ruta = path.abspath(path.join(".","web"))
list_csv = [path.join(ruta, file) for file in listdir(ruta) if '.csv' in file]
for file in list_csv:
    try:
        df = pd.read_csv(file, delimiter=",", keep_default_na=False)
        df = df.dropna()
        df.to_csv(file, index=False)
    except Exception as e:
        print(f"Excepción en {file}: {e}")





