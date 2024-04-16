# Wikidex Web Scraper

## Autores
  * Laura María Lidón Tárraga
  * Carlos Juan Blanco - [carlosjuan98@gmail.com](carlosjuan98@gmail.com)

## Sitio web elegido
[https://www.wikidex.net/wiki/WikiDex](https://www.wikidex.net/wiki/WikiDex)

## Enlace DOI Zenodo
El conjunto de datos extraído reúne datos tanto numéricos como categóricos de distintos Pokémon presentes en los juegos principales. Utilizando como criterio de ordenación el número de la Pokédex Nacional (hace la función de ID) se muestran desde el número 1 al número máximo de Pokémon que existan en ese momento (a día 14-04-2024 hay registrados 1025). Este dataset ha sido publicado en Zenodo con DOI [10.5281/zenodo.10971521](https://doi.org/10.5281/zenodo.10971521).

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10971521.svg)](https://doi.org/10.5281/zenodo.10971521)

## Descripción del repositorio
Descripción aquí

  * `/source/scraper.py`: Archivo principal.
  * `/source/scraper_aux.py`: Descripción archivo.
  * (...)
  * `/source/requirements.txt`: Lista de paquetes utilizados (Python 3.10).
  * `/dataset/collected_data_1.csv`: Descripción archivo.
  * `/dataset/collected_data_2.csv`: Descripción archivo.
  * (...)

## Configuración
Para ejecutar el script en la consola de comandos, primero han de instalarse las librerías necesarias. Para facilitar el proceso se utilizará el archivo `requirements.txt` para instalar las librerías necesarias de la siguiente forma:

```
pip install -r requirements.txt
```

A continuación, como hemos provisto al script de una opción para mostrar la ayuda, vamos a mostrarla y así entender cómo funcionan los argumentos posicionales. Para ello, introducimos en la cmd `python main.py -h` y este es el resultado obtenido:

```
usage: WebScrapper_LauraYCarlos_UniBot1.0 [-h] [--headless HEADLESS] [--name] [--num] [--time]

WebScrapper empleando Selenium que recorre la página www.wikidex.net recabando información sobre Pokemon

positional arguments:
  --name               Nombre del pokemon de inicio
  --num                Máximos pokemons procesados
  --time               Tiempo de espera en secs (min 1)

options:
  -h, --help           show this help message and exit
  --headless HEADLESS  Opcion headless del webdriver

La licencia de los dataset obtenidos es de CC-BY-SA 4.0 y debe referenciarse su origen (wikidex.net)
```

Esto nos señala que tenemos 3 argumentos posicionales para el nombre del pokémon, el número de pokémon que vamos a recorrer y el tiempo de espera entre pokémon y pokémon para no saturar la página web. Para ilustrarlo, utilizaré dos ejemplos:

El primero consiste en el comando que se utilizó para obtener el dataset facilitado en el repositorio en la carpeta `/dataset`. Este código es `python main.py --time 5` para que el tiempo de espera sea de 5 segundos para actuar de acuerdo a las buenas prácticas durante el Web Scraping. De esta manera se obtendrá el csv con las 1025 especies distintas de pokémon existentes a fecha del 14 de abril de 2024.

Para el segundo ejemplo, obtendremos los 9 pokémon iniciales de la 4ª generación con un tiempo de espera de 2s. Esto lo haremos a partir del previo conocimiento sobre el primer pokémon de esta generación, que es Turtwig y así el comando resultaría `python main.py Turtwig 9 2`. También podría escribirse los argumentos de la siguiente forma: `python main.py --name Turtwig --num 9 --time 2` y para ambos casos el resultado sería:

```
DevTools listening on ws://127.0.0.1:59825/devtools/browser/d46f67d1-5ce5-4dd6-b512-5208fd67833f
Chrome/123.0.0.0 (Windows NT 10.0; Win64; x64) (Laura_y_Carlos_UniBot/1.0; Python/3.12; Ejercicio_master)

Estoy en Turtwig Nº 0387
Estoy en Grotle Nº 0388
Estoy en Torterra Nº 0389
Estoy en Chimchar Nº 0390
Estoy en Monferno Nº 0391
Estoy en Infernape Nº 0392
Estoy en Piplup Nº 0393
Estoy en Prinplup Nº 0394
Estoy en Empoleon Nº 0395
pokemon_stats_240415_Turtwig_9.csv creado con éxito
```

Así, durante la ejecución se muestra por qué pokémon va esta ejecución y cuando ha finalizado, señala el nombre del csv creado, que en este caso es `pokemon_stats_240415_Turtwig_9.csv`
