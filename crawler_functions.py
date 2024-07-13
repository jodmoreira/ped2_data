import requests
from bs4 import BeautifulSoup
import re
import zipfile
import io
import logging

# Configurando log
log = logging.getLogger()

# Função para extrair links de uma página
def extract_links_from_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Falha na requisição HTTP. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    dataset_items = soup.find_all('li', class_='dataset-item')
    links = [f"https://dadosabertos.tse.jus.br{item.find('h2', class_='dataset-heading').find('a')['href']}" for item in dataset_items]
    return links

# Função para encontrar a próxima página
def find_next_page(soup):
    pagination = soup.find('ul', class_='pagination')
    if not pagination:
        return None
    next_page = pagination.find('li', class_='active').find_next_sibling('li')
    if next_page and next_page.find('a'):
        return f"https://dadosabertos.tse.jus.br{next_page.find('a')['href']}"
    return None

# Função para extrair link do arquivo zip da página do dataset
def extract_zip_link(dataset_url, year):
    response = requests.get(dataset_url)
    if response.status_code != 200:
        print(f"Falha na requisição HTTP ao acessar {dataset_url}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    zip_link = soup.find('a', href=re.compile(f'consulta_cand_{year}.zip'))
    if zip_link:
        return f"{zip_link['href']}"
    return None

# Função para fazer download e descompactar arquivo zip
def download_and_extract_zip(zip_url):
    response = requests.get(zip_url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
            for zipinfo in thezip.infolist():
                with thezip.open(zipinfo) as thefile:
                    local_filename = zipinfo.filename
                    with open(local_filename, 'wb') as f:
                        f.write(thefile.read())
    else:
        log.info(f"Falha ao fazer download do arquivo zip. Status code: {response.status_code}")



