from flask import Flask, jsonify
import requests
from flask_cors import CORS  # Para permitir requisições de diferentes origens
from flask_caching import Cache  # <-- IMPORT DO CACHE

app = Flask(__name__)
CORS(app)

# 🔧 Configuração do cache simples (em memória)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # cache dura 300 segundos (5 min)
cache = Cache(app)

API_KEY = "6feb01d74563498abf67a00a4c1068d5"

def buscar_noticias_trabalho():
    url = f"https://newsapi.org/v2/everything?q=trabalho OR trabalhador OR emprego OR direitos+trabalhistas OR sindicato&language=pt&apiKey={API_KEY}"
    resposta = requests.get(url)
    dados = resposta.json()

    noticias = []
    
    if dados["status"] == "ok":
        for artigo in dados["articles"]:
            noticias.append({
                "titulo": artigo["title"],
                "link": artigo["url"],
                "fonte": artigo["source"]["name"],
                "publicado_em": artigo["publishedAt"]
            })

    return noticias

# 🚀 Rota com cache ativado
@app.route("/noticias", methods=["GET"])
@cache.cached(timeout=300)  # <-- cache por 5 minutos
def obter_noticias():
    return jsonify(buscar_noticias_trabalho())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
