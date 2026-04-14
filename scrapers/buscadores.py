import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


def _nova_sessao():
    sessao = requests.Session()
    # Evita herdar proxies quebrados do ambiente.
    sessao.trust_env = False
    return sessao


def _headers_padrao():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }


def _buscar_link_ml_requests(nome_produto):
    termo = quote(nome_produto)
    url = f"https://lista.mercadolivre.com.br/{termo}"
    headers = _headers_padrao()

    session = _nova_sessao()
    res = session.get(url, headers=headers, timeout=15)

    print(f"DEBUG ML STATUS: {res.status_code}")

    if "account-verification" in res.url:
        return None, {
            "status_code": res.status_code,
            "url_final": res.url,
            "bloqueado": True,
            "origem": "requests",
        }

    sopa = BeautifulSoup(res.text, 'html.parser')

    link_tag = sopa.select_one('a.ui-search-item__group__element.ui-search-link') or \
               sopa.select_one('a.ui-search-link') or \
               sopa.select_one('.ui-search-result__content a') or \
               sopa.select_one('a.poly-component__title') or \
               sopa.select_one('a[href*="/MLB-"]')

    if link_tag and 'href' in link_tag.attrs:
        link_produto = _link_produto_mercado_livre(link_tag['href'])
        if link_produto:
            return link_produto, {
                "status_code": res.status_code,
                "url_final": res.url,
                "bloqueado": False,
                "origem": "requests",
            }

    for a in sopa.find_all("a", href=True):
        link_produto = _link_produto_mercado_livre(a['href'])
        if link_produto:
            return link_produto, {
                "status_code": res.status_code,
                "url_final": res.url,
                "bloqueado": False,
                "origem": "requests",
            }

    return None, {
        "status_code": res.status_code,
        "url_final": res.url,
        "bloqueado": False,
        "origem": "requests",
    }


def _buscar_link_ml_playwright(nome_produto):
    termo = quote(nome_produto)
    url = f"https://lista.mercadolivre.com.br/{termo}"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                locale="pt-BR",
                user_agent=_headers_padrao()["User-Agent"],
                viewport={"width": 1366, "height": 900},
            )
            page = context.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(2500)

                if "account-verification" in page.url:
                    return None, {
                        "url_final": page.url,
                        "bloqueado": True,
                        "origem": "playwright",
                        "titulo": page.title(),
                    }

                seletores = [
                    'a.ui-search-item__group__element.ui-search-link',
                    'a.ui-search-link',
                    '.ui-search-result__content a',
                    'a.poly-component__title',
                    'a[href*="/MLB-"]',
                ]

                for seletor in seletores:
                    locator = page.locator(seletor).first
                    if locator.count() > 0:
                        href = locator.get_attribute("href")
                        link_produto = _link_produto_mercado_livre(href)
                        if link_produto:
                            return link_produto, {
                                "url_final": page.url,
                                "bloqueado": False,
                                "origem": "playwright",
                                "titulo": page.title(),
                            }

                for href in page.locator("a").evaluate_all(
                    "(anchors) => anchors.map((a) => a.href).filter(Boolean)"
                ):
                    link_produto = _link_produto_mercado_livre(href)
                    if link_produto:
                        return link_produto, {
                            "url_final": page.url,
                            "bloqueado": False,
                            "origem": "playwright",
                            "titulo": page.title(),
                        }

                return None, {
                    "url_final": page.url,
                    "bloqueado": False,
                    "origem": "playwright",
                    "titulo": page.title(),
                }
            except PlaywrightTimeoutError:
                return None, {
                    "erro": "Timeout ao carregar a busca no navegador automatizado.",
                    "origem": "playwright",
                }
            finally:
                context.close()
                browser.close()
    except Exception as e:
        return None, {
            "erro": f"Falha ao iniciar o navegador automatizado: {e}",
            "origem": "playwright",
        }


def _link_produto_mercado_livre(href):
    if not href:
        return None

    href_limpo = href.split("#")[0]
    dominio = urlparse(href_limpo).netloc.lower()

    if "mercadolivre.com.br" not in dominio:
        return None

    # Ignora páginas de navegação, filtros, login e ajuda.
    trechos_bloqueados = (
        "/navigation/",
        "/noindex/",
        "/ajuda/",
        "/institucional/",
        "/login",
        "_Desde_",
    )
    if any(trecho in href_limpo for trecho in trechos_bloqueados):
        return None

    # O ML usa mais de um formato de URL de produto/anúncio.
    padroes_validos = (
        "/p/",
        "/MLB-",
        "/mlb-",
    )
    if any(padrao in href_limpo for padrao in padroes_validos):
        return href_limpo

    return None

def buscar_link_ml(nome_produto):
    try:
        link_produto, diagnostico = _buscar_link_ml_requests(nome_produto)
        if link_produto:
            return link_produto

        if diagnostico.get("bloqueado"):
            link_produto, _ = _buscar_link_ml_playwright(nome_produto)
            return link_produto

        return None
    except Exception as e:
        print(f"Erro no Scraper ML: {e}")
        return None


def diagnosticar_busca_ml(nome_produto):
    try:
        _, diagnostico_requests = _buscar_link_ml_requests(nome_produto)
        diagnostico = {"requests": diagnostico_requests}

        if diagnostico_requests.get("bloqueado"):
            _, diagnostico_playwright = _buscar_link_ml_playwright(nome_produto)
            diagnostico["playwright"] = diagnostico_playwright

        diagnostico["achou_link"] = bool(buscar_link_ml(nome_produto))
        return diagnostico
    except Exception as e:
        return {
            "erro": str(e)
        }

def buscar_link_amazon(nome_produto):
    from urllib.parse import quote
    termo = quote(nome_produto)
    url = f"https://www.amazon.com.br/s?k={termo}"
    
    # Este é o "Dicionário Gigante" para enganar o firewall da Amazon
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
        # Usar session ajuda a manter a conexão estável
        session = _nova_sessao()
        res = session.get(url, headers=headers, timeout=15)
        
        if res.status_code != 200:
            return None
            
        sopa = BeautifulSoup(res.text, 'html.parser')
        
        # Seletor para o link do primeiro produto da lista
        item = sopa.find("a", class_="a-link-normal s-no-outline")
        
        if item:
            link_final = "https://www.amazon.com.br" + item['href']
            return link_final.split("/ref=")[0] # Limpa o link
        return None
    except:
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
