import requests
from bs4 import BeautifulSoup
import json

def scrape_panini(urls, modelo_de_classes): 
    todos_universos = {}
    
    for universo, url_universoglobal in urls.items():
        dados_universo = []
        total_paginas = 2 # inicia como 2, mas é alterado durante o looping para buscar na mesma requisição e poupar tempo

        for num_pag in range(1, total_paginas):
            url = url_universoglobal.format(num_pag=num_pag)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            hqs = soup.find_all('li', class_='item product product-item')

            if num_pag == 1:
                numero_paginas = soup.find('a', class_="page last")
                
                if numero_paginas:
                    total_paginas = int(numero_paginas.text.split()[-1])
        
            for hq in hqs:
                hq_info = {}

                # Pegando preço antigo
                preco_antigo_tag = hq.find('span', class_=modelo_de_classes['preco_antigo'])
                if preco_antigo_tag:
                    hq_info['preco_antigo'] = preco_antigo_tag.text.strip()
                else:
                    continue


                # Pegando nome
                name_tag = hq.find('a', class_=modelo_de_classes['nome_produto'])
                if name_tag:
                    hq_info['nome_produto'] = name_tag.text
                if dados_universo:
                    if dados_universo[0]['nome_produto'] == hq_info['nome_produto']:
                            todos_universos[universo] = dados_universo
                            break

                # Pré-venda
                esta_pre_venda = hq.find('span', class_='infobase-label-presale')
                if esta_pre_venda:
                  hq_info['esta_pre_venda'] = esta_pre_venda.text

                # Pegando link
                link_tag = hq.find('a', class_=modelo_de_classes['link_produto'])
                if link_tag:
                    hq_info['link_produto'] = link_tag['href']

                # Pegando imagem
                img_tag = hq.find('img', class_=modelo_de_classes['imagem_produto'])
                if img_tag and 'data-srcset' in img_tag.attrs:
                    # Tratando o dataset de links
                    image_urls = img_tag['data-srcset'].split(',')
                    if image_urls:
                        hq_info['imagem_produto'] = image_urls[-1].strip().split(' ')[0] # Pega o último link do dataset


                # Pegando preço atual
                preco_atual_tag = hq.find('span', class_=modelo_de_classes['preco_atual'])
                if preco_atual_tag:
                    hq_info['preco_atual'] = preco_atual_tag.text.strip()

                if hq_info and hq_info['preco_antigo']:
                    dados_universo.append(hq_info)
           

        todos_universos[universo] = dados_universo
    
    return todos_universos