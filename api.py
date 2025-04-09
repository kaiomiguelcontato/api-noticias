from flask import Flask, jsonify
import requests
from flask_cors import CORS  # Para permitir requisições de diferentes origens
from flask_caching import Cache  # <-- IMPORT DO CACHE
import os  # Importe o módulo os para acessar variáveis de ambiente

app = Flask(__name__)
CORS(app)

# 🔧 Configuração do cache simples (em memória)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # cache dura 300 segundos (5 min)
cache = Cache(app)

# Tente obter a API_KEY de uma variável de ambiente, se não estiver definida, use a chave diretamente
API_KEY = os.environ.get("NEWSAPI_KEY")
if not API_KEY:
    API_KEY = "6feb01d74563498abf67a00a4c1068d5"  # Use sua chave aqui como fallback em desenvolvimento
    print("Aviso: Usando a API_KEY diretamente no código. Recomenda-se usar variáveis de ambiente em produção.")

def buscar_noticias_trabalho():
    url = f"https://newsapi.org/v2/everything?q=trabalho OR trabalhador OR emprego OR direitos+trabalhistas OR sindicato&language=pt&apiKey={API_KEY}"
    print(f"Fazendo requisição para: {url}")  # Adicionado para log
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # Lança uma exceção para códigos de status ruins (4xx ou 5xx)
        dados = resposta.json()
        print(f"Resposta da NewsAPI: {dados}")  # Adicionado para log

        noticias = []

        if dados["status"] == "ok":
            for artigo in dados["articles"]:
                noticias.append({
                    "titulo": artigo["title"],
                    "link": artigo["url"],
                    "fonte": artigo["source"]["name"],
                    "publicado_em": artigo["publishedAt"]
                })
        else:
            print(f"Erro na resposta da NewsAPI: Status: {dados.get('status')}, Mensagem: {dados.get('message')}")  # Adicionado para log
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição para a NewsAPI: {e}")
        return []
    except ValueError:
        print("Erro ao decodificar a resposta JSON da NewsAPI.")
        return []

    return noticias

# 🚀 Rota com cache ativado
@app.route("/noticias", methods=["GET"])
@cache.cached(timeout=300)  # <-- cache por 5 minutos
def obter_noticias():
    noticias = buscar_noticias_trabalho()
    return jsonify(noticias)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
