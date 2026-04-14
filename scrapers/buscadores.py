import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


def _nova_sessao():
    sessao = requests.Session()
    sessao.trust_env = False
    return sessao


def buscar_link_amazon(nome_produto):
    termo = quote(nome_produto)
    url = f"https://www.amazon.com.br/s?k={termo}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    try:
        session = _nova_sessao()
        res = session.get(url, headers=headers, timeout=15)

        if res.status_code != 200:
            return None

        sopa = BeautifulSoup(res.text, "html.parser")
        item = sopa.find("a", class_="a-link-normal s-no-outline")

        if item:
            link_final = "https://www.amazon.com.br" + item["href"]
            return link_final.split("/ref=")[0]
        return None
    except Exception:
        return None


def buscar_link_magalu(nome_produto):
    termo = quote(nome_produto.replace(" ", "-"))
    url = f"https://www.magazineluiza.com.br/busca/{termo}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
    }

    try:
        session = _nova_sessao()
        res = session.get(url, headers=headers, timeout=15)

        if res.status_code != 200:
            return None

        sopa = BeautifulSoup(res.text, "html.parser")
        seletores = [
            'a[data-testid="product-card-container"]',
            'a[href*="/p/"]',
            'a[href*="/produto/"]',
        ]

        for seletor in seletores:
            item = sopa.select_one(seletor)
            if item and item.get("href"):
                href = item["href"]
                if href.startswith("/"):
                    return "https://www.magazineluiza.com.br" + href
                if "magazineluiza.com.br" in href:
                    return href

        return None
    except Exception as e:
        print(f"Erro no buscador Magalu: {e}")
        return None
