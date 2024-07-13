import crawler_functions
import requests
from bs4 import BeautifulSoup
import re
import logging
import os

# Configurando log
log = logging.getLogger()

# URL inicial
base_url = "https://dadosabertos.tse.jus.br/organization/tse-agel?groups=candidatos&page=1"
bucket_name = "ped2_dados"
all_links = []
zip_links = []
page_number = 1

# Coletando links de todas as páginas de datasets
while base_url:
    print(f"Processando página: {page_number}")
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Falha na requisição HTTP. Status code: {response.status_code}")
        break
    
    soup = BeautifulSoup(response.content, 'html.parser')
    links = crawler_functions.extract_links_from_page(base_url)
    all_links.extend(links)
    
    base_url = crawler_functions.find_next_page(soup)
    page_number += 1

# Coletando links dos arquivos zip de cada página de dataset
for link in all_links:
    log.info(f"Accessing dataset: {link}")
    year_match = re.search(r'(\d{4})', link)
    if year_match:
        year = year_match.group(1)
        zip_link = crawler_functions.extract_zip_link(link, year)
        if zip_link:
            print(zip_link)
            print(f"Encontrado arquivo zip: {zip_link}")
            zip_links.append(zip_link)
        else:
            log.info(f"Nenhum arquivo zip encontrado para o ano {year} em {link}")
    else:
        log.info(f"Não foi possível encontrar o ano no link: {link}")


# Fazendo download, descompactando e salvando arquivos no GCS
for zip_link in zip_links:
    log.info(f"Downloading and decompressing: {zip_link}")
    crawler_functions.download_and_extract_zip(zip_link, bucket_name)
    # ## delete the zip file and the extracted files
    # os.remove(zip_link)
    
log.info("Download completed.")
