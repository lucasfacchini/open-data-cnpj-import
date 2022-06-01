import requests
import os
import time
from lxml import html
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def getZipFileUrls():
    baseUrl='http://200.152.38.155/CNPJ/'
    text_file = open("cnpjfiles.txt", "w")
    try:
        with requests.get(baseUrl, stream=True) as r:
            tree = html.fromstring(r.content)
            #pega todos os links da pagina
            lista = tree.xpath('//a/@href')    
            for link in lista:
                if link.find('.zip')>-1:
                    print(link)
                    text_file.write(baseUrl+link+'\n')
    finally:
        text_file.close()
def downloadZipFiles():
    os.system('mkdir data/download')
    os.system("aria2c -s 16 -x 16 -j 10 --auto-file-renaming=false --allow-overwrite=false --check-integrity=true --input-file cnpjfiles.txt --save-session cnpjfiles-errors.txt -d data/download ")
    
getZipFileUrls()
downloadZipFiles()