from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from starlette.responses import JSONResponse
from services import scrape_panini

num_pag = 1 # Página padrão para iniciar
urls_dc = {
    "batman": f"https://panini.com.br/dc-comics/universo-batman?p={num_pag}&price=14-105&product_list_order=high_to_low",
    "superman": f"https://panini.com.br/dc-comics/universo-superman?p={num_pag}&price=14-105&product_list_order=high_to_low",
    "mulher-maravilha": f"https://panini.com.br/dc-comics/universo-mulher-maravilha?p={num_pag}&price=14-105&product_list_order=high_to_low",
    "liga-da-justica": f"https://panini.com.br/dc-comics/universo-liga-da-jusica?p={num_pag}&price=14-105&product_list_order=high_to_low",
    "flash": f"https://panini.com.br/dc-comics/universo-flash?p={num_pag}&price=14-105&product_list_order=high_to_low"
}

urls_marvel = {
    "quarteto-fantastico": f"https://panini.com.br/marvel/universo-quarteto-fantastico?p={num_pag}&price=13-199&product_list_order=high_to_low",
    "homem-aranha": f"https://panini.com.br/marvel/universo-homem-aranha?p={num_pag}&price=13-174&product_list_order=high_to_low"
}

modelo_saida_classes = {
    "pre_venda": "infobase-label-presale", # span .text
    "link_produto": "product photo product-item-photo", # a ["href"]
    "nome_produto": "product-item-link", # a .text
    "imagem_produto": "product-image-photo", # Filtrar img ["data-srcset"]
    "preco_antigo": "old-price", # span .text
    "preco_atual": "price" # span .text
}

app = FastAPI()

origins = [
    "http://localhost:19000",  # Expo em desenvolvimento (web)
    "exp://127.0.0.1:19000",   # Expo Go no dispositivo
    "exp://10.124.14.33:8081",
    "*"                        # Ou '*' para permitir todas as origens (menos seguro)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return "Bem-vindo ao PROMO HQ"

@app.get("/dc-tudo")
def buscar_tudo_dc():
    dc_data = scrape_panini(urls_dc, modelo_saida_classes)
    json.dumps(dc_data, indent=4, ensure_ascii=False)
    return dc_data

@app.get("/marvel-tudo")
def buscar_tudo_marvel():
    marvel_data = scrape_panini(urls_marvel, modelo_saida_classes)
    json.dumps(marvel_data, indent=4, ensure_ascii=False)
    return marvel_data