import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlsplit, urlunsplit


def _nova_sessao():
    sessao = requests.Session()
    sessao.trust_env = False
    return sessao


def _normalizar_link_magalu(href):
    if not href:
        return None

    if href.startswith("/"):
        href = "https://www.magazineluiza.com.br" + href

    partes = urlsplit(href)
    dominio = partes.netloc.lower()
    caminho = partes.path.rstrip("/")

    if "magazineluiza.com.br" not in dominio:
        return None

    if "/p/" not in caminho:
        return None

    # Remove query string e fragmentos de campanha/tracking.
    return urlunsplit((partes.scheme or "https", partes.netloc, caminho + "/", "", ""))


def link_magalu_disponivel(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    try:
        session = _nova_sessao()
        res = session.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return False

        texto = res.text.lower()
        if "forbidden" in texto or "azion - default error page" in texto:
            return False

        return True
    except Exception:
        return False


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
                link_normalizado = _normalizar_link_magalu(item["href"])
                if link_normalizado:
                    return link_normalizado

        return None
    except Exception as e:
        print(f"Erro no buscador Magalu: {e}")
        return None
