from fastapi import FastAPI
from services import scrape_panini
import json

num_pag = 1 # Página padrão para iniciar
urls_dc = {
    "batman": f"https://panini.com.br/dc-comics/universo-batman?p={num_pag}&product_list_order=high_to_low",
    "flash": f"https://panini.com.br/dc-comics/universo-flash?p={num_pag}&product_list_order=high_to_low",
    "lanterna-verde": f"https://panini.com.br/dc-comics/universo-lanterna-verde?p={num_pag}&product_list_order=high_to_low",
    "liga-da-justica": f"https://panini.com.br/dc-comics/universo-liga-da-jusica?p={num_pag}&product_list_order=high_to_low",
    "mulher-maravilha": f"https://panini.com.br/dc-comics/universo-mulher-maravilha?p={num_pag}&product_list_order=high_to_low",
    "sandman": f"https://panini.com.br/dc-comics/universo-sandman?p={num_pag}&product_list_order=high_to_low",
    "superman": f"https://panini.com.br/dc-comics/universo-superman?p={num_pag}&product_list_order=high_to_low",
    "outros": f"https://panini.com.br/dc-comics/outros?p={num_pag}&product_list_order=high_to_low"
}

urls_marvel = {
    "capitao-america": f"https://panini.com.br/marvel/universo-capitao-america?p={num_pag}&product_list_order=high_to_low",
    "demolidor": f"https://panini.com.br/marvel/universo-demolidor?p={num_pag}&product_list_order=high_to_low",
    "homem-aranha": f"https://panini.com.br/marvel/universo-homem-aranha?p={num_pag}&product_list_order=high_to_low",
    "quarteto-fantastico": f"https://panini.com.br/marvel/universo-quarteto-fantastico?p={num_pag}&product_list_order=high_to_low",
    "vingadores": f"https://panini.com.br/marvel/universo-vingadores?p={num_pag}&product_list_order=high_to_low",
    "x-men": f"https://panini.com.br/marvel/universo-x-men?p={num_pag}&product_list_order=high_to_low",
    "outros": f"https://panini.com.br/marvel/outros?p={num_pag}&product_list_order=high_to_low"
}

urls_manga = {
    "berserk": f"https://panini.com.br/planet-manga/berserk?p={num_pag}&product_list_order=high_to_low",
    "chainsaw-man": f"https://panini.com.br/planet-manga/chainsaw-man?p={num_pag}&product_list_order=high_to_low",
    "demon-slayer": f"https://panini.com.br/planet-manga/demon-slayer?p={num_pag}&product_list_order=high_to_low",
    "dragon-ball": f"https://panini.com.br/planet-manga/dragon-ball?p={num_pag}&product_list_order=high_to_low",
    "jujutsu-kaisen": f"https://panini.com.br/planet-manga/jujutsu-kaisen?p={num_pag}&product_list_order=high_to_low",
    "naruto": f"https://panini.com.br/planet-manga/naruto?p={num_pag}&product_list_order=high_to_low",
    "one-piece": f"https://panini.com.br/planet-manga/one-piece?p={num_pag}&product_list_order=high_to_low",
    "pokemon": f"https://panini.com.br/planet-manga/pokemon?p={num_pag}&product_list_order=high_to_low",
    "outros": f"https://panini.com.br/planet-manga/outros?p={num_pag}&product_list_order=high_to_low"
}

modelo_saida_classes = {
    "numero_paginas": "page last", # a
    "pre_venda": "infobase-label-presale", # span .text
    "link_produto": "product photo product-item-photo", # a ["href"]
    "nome_produto": "product-item-link", # a .text
    "imagem_produto": "product-image-photo", # Filtrar img ["data-srcset"]
    "preco_antigo": "old-price", # span .text
    "preco_atual": "price" # span .text
}

app = FastAPI()

@app.get("/status")
def get_status():
    return {"status": "ok"}

# Para Uptime Robot
@app.head("/status")
def status_head():
    return {"status": "ok"}

@app.get("/")
def home():
    return "Bem-vindo ao PROMO HQ"

@app.get("/dc-tudo")
def buscar_tudo_dc(filtro_universos = None):
    dc_data = scrape_panini(urls_dc, modelo_saida_classes, filtro_universos)
    json.dumps(dc_data, indent=4, ensure_ascii=False)
    return dc_data

@app.get("/marvel-tudo")
def buscar_tudo_marvel(filtro_universos = None):
    marvel_data = scrape_panini(urls_marvel, modelo_saida_classes, filtro_universos)
    json.dumps(marvel_data, indent=4, ensure_ascii=False)
    return marvel_data

@app.get("/planet-manga-tudo")
def buscar_tudo_marvel(filtro_universos = None):
    manga_data = scrape_panini(urls_manga, modelo_saida_classes, filtro_universos)
    json.dumps(manga_data, indent=4, ensure_ascii=False)
    return manga_data