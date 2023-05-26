from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options 
import json
# from modulos.email import Email
from datetime import datetime
from urllib.parse import unquote
from core import config
import time
from utils.anuncios import get_data

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
  "download.default_directory": "/path/to/download/dir",
  "download.prompt_for_download": False,
})
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= chrome_options)
url = config.URL

# obtenemos los articulos de las x cantidad de paginas
anuncios = []
for i in range(1, config.CANTIDAD_PAGINAS + 1):

    driver.get(url.format(i)   )
    time.sleep(config.TIEMPO_ESPERA)

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    articulos = soup.find_all('div', class_='gallery-item-container')
    
    for articulo in articulos:
        id = articulo.attrs['id']
        anuncios.append(f"{config.URL_BASE}/{id}")
# print(anuncios)

# obtenemos los datos de cada articulo
datos = []
for index, anuncio in enumerate(anuncios):
    driver.get(anuncio)
    time.sleep(config.TIEMPO_ESPERA)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    print(index)
    get_data(soup, driver.current_url)


driver.close()
driver.quit()


