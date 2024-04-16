from pandas import DataFrame
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def obtener_general_pokemon(driver):
    """
    Extrae el número y nombre del pokémon cargado en la página

    Argumentos:
        driver -- WebDriver de Selenium

    Salida:
        general_pokemon -- lista con el número y nombre del pokémon
    """
    # Aquí número y nombre
    general_pokemon = []
    general_pokemon.append(driver.find_element(By.XPATH,
                                               '//*[@id="numeronacional"]').text)
    general_pokemon.append(driver.find_element(By.XPATH,
                                               '//*[@id="nombrepokemon"]').text)
    general_pokemon.append(driver.find_element(By.XPATH,
                                               '//*[@class="nombrejapones"]').text)
    if general_pokemon[1] + " no evoluciona" in driver.page_source:
        general_pokemon.append(0)
    else:
        general_pokemon.append(1)
    print("Estoy en "+ general_pokemon[1] + " Nº "+ general_pokemon[0])
    return general_pokemon


def obtener_datos_pokemon(driver):
    """
    Obtiene los datos generales del Pokémon, como su generación, categoría,
    tipo, habilidades, etc.

    Argumentos:
        driver -- WebDriver de Selenium.

    Salida:
        datos_pokemon: Un diccionario que contiene los datos generales del
        Pokémon.
    """
    # Buscamos el elemento buscando su clase CSS
    datos = driver.find_element(By.CSS_SELECTOR, '.datos.resalto')
    datos_html = datos.get_attribute('outerHTML')
    datos_soup = BeautifulSoup(datos_html, 'html.parser')
    # Inicializamos las variables
    datos_pokemon = {
        'Generación': None,
        'Categoría': None,
        'Tipo': None,
        'Tipos': None,
        'Habilidad': None,
        'Habilidades': None,
        'Hab. oculta': None,
        'Peso': None,
        'Altura': None,
        'Grupo de huevo': None,
        'Grupos de huevo': None,
        'Sexo': None,
        'Color': None
    }
    
    # Buscamos y separamos la información (con "|")
    br_tags = datos_soup.find_all('br')
    for br_tag in br_tags:
        br_tag.replace_with('|')
    
    for row in datos_soup.find_all('tr'):
        th = row.find('th')
        td = row.find('td')
        if th and td:
            key = th.get_text(strip=True)
            value = ' '.join(td.get_text(strip=True).split())
            # Tipos, al no tener texto, tiene un tratamiento especial:
            if key =="Tipo" or key=="Tipos":
                img_tags = td.find_all('img')
                alt_values = [img.get('alt').replace('Tipo ', '').replace('.gif', '')
                    for img in img_tags]
                value = '|'.join(alt_values)
            if key in datos_pokemon:
                datos_pokemon[key] = value
    # Limpiamos altura y peso
    datos_pokemon['Peso'] = datos_pokemon['Peso'].replace(' kg', '')
    datos_pokemon['Altura'] = datos_pokemon['Altura'].replace(' m', '')
    
    # Como Grupo de huevo/Grupos de huevo, Habilidad/Habilidades y Tipo/Tipos
    # son lo mismo, los unimos
    datos_pokemon['Tipo'] = datos_pokemon['Tipo'] or datos_pokemon['Tipos']
    datos_pokemon['Habilidad'] = datos_pokemon['Habilidad'] or datos_pokemon['Habilidades']
    datos_pokemon['Grupo de huevo'] = datos_pokemon['Grupo de huevo'] or datos_pokemon['Grupos de huevo']
    del datos_pokemon['Tipos']
    del datos_pokemon['Habilidades']
    del datos_pokemon['Grupos de huevo']
    return datos_pokemon

def obtener_caracteristicas_pokemon(driver):
    """
    Obtiene las características de combate del Pokémon.

    Argumentos:
        driver: WebDriver de Selenium.

    Salida:
        caracteristicas_pokemon: Una lista que contiene las características de
        combate del Pokémon.
    """
    # Encontramos el elemento con id "Características de combate", ya que hay varias tablas
    caracteristicas=driver.find_element(By.ID, "Características_de_combate")
    # De ahí encontramos la tabla
    tabla_caracteristicas = caracteristicas.find_element(By.XPATH,
          "./following::table[@class='tabpokemon'][1]").get_attribute("outerHTML")
    # Extraemos las filas
    rows= BeautifulSoup(tabla_caracteristicas, 'html.parser').find_all('tr')
    # Fuardamos la información
    data = []
    # Sacamos los datos de ese formato
    for row in rows:
        cols = row.find_all('td')
        if not cols:
            # Saltamos las columnas vacías
            continue
        # Extraemos el texto de cada celda
        cols_text = [ele.text.strip() for ele in cols]
        data.append(cols_text)
    # Sabemos que la info de nv100 maxla tenemos en la "penultima columna" ([-])
    # Y de los puntos de esfueszo en la última (-1)
    # (menos de la última, que es texto) y que cada elemento son listas 
    caracteristicas_pokemon=[sublista[-2] for sublista in data[:-1]] 
    caracteristicas_pokemon+=[sublista[-1] for sublista in data[:-1]]
    return caracteristicas_pokemon


def obtener_info_pokemon(driver):
    """
    Obtiene toda la información disponible del Pokémon actualmente cargado en
    la página.

    Argumentos:
        driver: WebDriver de Selenium.

    Salida:
        info_poke: Una lista que contiene toda la información del Pokémon,
        incluyendo datos generales y características de combate.
    """
    general_pokemon = obtener_general_pokemon(driver)
    datos_pokemon = obtener_datos_pokemon(driver)
    caracteristicas_pokemon = obtener_caracteristicas_pokemon(driver)
    # Creamos una fila con la info
    info_poke = general_pokemon + list(datos_pokemon.values()) + caracteristicas_pokemon
    return info_poke


def siguiente_pokemon(driver, headless):
    """
    Navega a la página del siguiente Pokémon en la lista.

    Argumentos:
        driver: WebDriver de Selenium.
    """
    numero_nacional = driver.find_element(By.XPATH, '//*[@id="numeronacional"]')
    enlace_siguiente = numero_nacional.find_element(By.XPATH,
                                                    "./following-sibling::a")
    # Si está headless, empleamos JavaScript para simular el "click"
    if headless:
        driver.execute_script("arguments[0].click();", enlace_siguiente)
    else:
        enlace_siguiente.click()
