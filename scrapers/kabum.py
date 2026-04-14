import json

import requests
from bs4 import BeautifulSoup


def _nova_sessao():
    sessao = requests.Session()
    sessao.trust_env = False
    return sessao


def _extrair_produtos_json_ld(sopa):
    for script in sopa.find_all("script", type="application/ld+json"):
        conteudo = script.string or script.get_text()
        if not conteudo:
            continue

        try:
            dados = json.loads(conteudo)
        except json.JSONDecodeError:
            continue

        if isinstance(dados, list):
            produtos = [item for item in dados if item.get("@type") == "Product"]
            if produtos:
                return produtos

        if isinstance(dados, dict) and dados.get("@type") == "Product":
            return [dados]

    return []


def buscar_link_kabum(nome_produto):
    termo = nome_produto.replace(" ", "-").lower()
    url = f"https://www.kabum.com.br/busca/{termo}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    try:
        session = _nova_sessao()
        res = session.get(url, headers=headers, timeout=15)
        if res.status_code != 200:
            return None

        sopa = BeautifulSoup(res.text, "html.parser")
        produtos = _extrair_produtos_json_ld(sopa)
        if not produtos:
            return None

        offers = produtos[0].get("offers", {})
        return offers.get("url")
    except Exception as e:
        print(f"Erro no buscador KaBuM: {e}")
        return None


def coletar_preco_kabum(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    try:
        session = _nova_sessao()
        res = session.get(url, headers=headers, timeout=15)
        if res.status_code != 200:
            return None

        sopa = BeautifulSoup(res.text, "html.parser")
        produtos = _extrair_produtos_json_ld(sopa)
        if not produtos:
            return None

        offers = produtos[0].get("offers", {})
        preco = offers.get("price")
        if preco is None:
            return None

        return float(preco)
    except Exception as e:
        print(f"Erro no scraper KaBuM: {e}")
        return None
