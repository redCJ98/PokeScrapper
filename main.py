from pandas import DataFrame
import argparse
import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from funciones_auxiliares import obtener_general_pokemon, obtener_datos_pokemon, obtener_caracteristicas_pokemon, obtener_info_pokemon, siguiente_pokemon


# En caso de que haya argumentos, los pasamos a variables
def positive_int(value):
    """
    Convierte una cadena en un entero positivo.

    Argumentos:
        value (str): La cadena que se intentará convertir a un entero positivo.

    Salida:
        int: El valor entero positivo.

    Raises:
        argparse.ArgumentTypeError: Si `value` no se puede convertir a un
        entero positivo o si es menor o igual a cero.
    """
    try:
        ivalue = int(value)
    except:
        raise argparse.ArgumentTypeError(f'{value} no es un número entero positivo')
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f'{value} no es un número entero positivo')
    return ivalue

def greater_than_1_float(value):
    """
    Convierte una cadena en un entero positivo.

    Argumentos:
        value (str): La cadena que se intentará convertir a decimal.

    Salida:
        int: El valor entero positivo.

    Raises:
        argparse.ArgumentTypeError: Si `value` no se puede convertir a un
        float o si es menor que 1.
    """
    try:
        ivalue = float(value)
    except:
        raise argparse.ArgumentTypeError(f'{value} no es un float')
    if ivalue <= 1:
        raise argparse.ArgumentTypeError(f'{value} no es mayor que 1')
    return ivalue


parser = argparse.ArgumentParser(
                        prog="WebScrapper_LauraYCarlos_UniBot1.0",
                        description="WebScrapper empleando Selenium que recorre la página www.wikidex.net recabando información sobre Pokemon",
                        epilog="La licencia de los dataset obtenidos es de CC-BY-SA 4.0 y debe referenciarse su origen (wikidex.net)")
# Si "name" está vacío, empezamos por Bulbasaur (Pokemon Nº 1)
parser.add_argument('inicio', metavar='--name', nargs='?', type=str, default='Bulbasaur', help='Nombre del pokemon de inicio (Bulbasaur by default)')
parser.add_argument('num_max', metavar='--num', nargs='?', default=-1, type=positive_int, help='Máximos pokemons procesados (todos by default)')
parser.add_argument('time_sleep', metavar='--time', nargs='?', default=1,
                    type=greater_than_1_float, help='Tiempo de espera en secs (1 by default y como min)')
parser.add_argument('--name', type=str, dest='inicio_name', help=argparse.SUPPRESS)
parser.add_argument('--num', type=positive_int, dest='num_max_num', help=argparse.SUPPRESS)
parser.add_argument('--time', type=greater_than_1_float, dest='time_sleep_time', help=argparse.SUPPRESS)
parser.add_argument('--headless', type=str, default="Y", dest='headless', help='Opcion headless del webdriver (Yes by default)')
args = parser.parse_args()
inicio = args.inicio_name or args.inicio
num_max = args.num_max_num or args.num_max
time_sleep = args.time_sleep_time or args.time_sleep
headless = args.headless

# Creamos el driver, cambiando el user agent
opts = Options()
opts.add_argument("user-agent=Chrome/123.0.0.0 (Windows NT 10.0; Win64; x64) (Laura_y_Carlos_UniBot/1.0; Python/3.12; Ejercicio_master)")
# Si la primera letra de la variable headless es Y o S, lo activamos
if headless[0].lower() in {'y', 's'}:
    opts.add_argument('--headless')
    headless = True
else:
    headless = False

driver = webdriver.Chrome(options=opts)
print(driver.execute_script("return navigator.userAgent"))
driver.get("https://www.wikidex.net/wiki/" + inicio)


# Definimos las columnas de interes
nombres_columnas = ['NumNacional', 'Nombre', 'NombreJapo',
                'Evoluciona', 'Generación',
                'Categoría', 'Tipos', 'Habilidad',
                'Hab.Oculta', 'Peso', 'Altura',
                'GrupoHuevo', 'Sexo', 'Color',
                'PS_Max', 'At_Max', 'Def_Max',
                'AtEsp_Max', 'DefEsp_Max', 'Vel_Max',
                'PE_PS', 'PE_At', 'PE_Def',
                'PE_AtEsp,', 'PE_DefEsp', 'PE_Vel']

# Create a DataFrame
df = DataFrame(columns=nombres_columnas)

# Si era -1, nunca será 0 hasta que en siguiente_pokemon salte el error
while num_max != 0:
    num_max -= 1
    info_poke = obtener_info_pokemon(driver)
    # Añadimos la fila al dataframe
    df.loc[len(df)] = info_poke
    time.sleep(time_sleep)
    try:
        siguiente_pokemon(driver, headless)
    except:
        num_max = 0

# Guardamos el datadrame
current_date = datetime.now()
date_number = "{:02d}{:02d}{:02d}".format(current_date.year % 100,
                                current_date.month, current_date.day)
num_max = args.num_max_num or args.num_max
num_final = str(num_max) if num_max != -1 else "tot"
df.to_csv('pokemon_stats_' + date_number + "_" + inicio + "_" + num_final + '.csv',
          index=False, mode='w')

print('pokemon_stats_' + date_number + "_" + inicio + "_" + num_final + '.csv creado con éxito')
# Cerrar el navegador web
driver.quit()