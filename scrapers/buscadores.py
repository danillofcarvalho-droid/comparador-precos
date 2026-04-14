import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def buscar_link_ml(nome_produto):
    termo = quote(nome_produto)
    url = f"https://lista.mercadolivre.com.br/{termo}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        res = requests.get(url, headers=headers, timeout=15)
        
        # DEBUG para ver nos logs do Streamlit Cloud
        print(f"DEBUG ML STATUS: {res.status_code}")
        
        sopa = BeautifulSoup(res.text, 'html.parser')

        # Estratégia 1: Busca por seletores CSS comuns (mais estáveis)
        link_tag = sopa.select_one('a.ui-search-item__group__element.ui-search-link') or \
                   sopa.select_one('a.ui-search-link') or \
                   sopa.select_one('.ui-search-result__content a')

        if link_tag and 'href' in link_tag.attrs:
            return link_tag['href'].split('#')[0]

        # Estratégia 2: Backup - procura qualquer link que pareça um produto
        for a in sopa.find_all("a", href=True):
            href = a['href']
            if "articulo.mercadolivre.com.br" in href and "/p/" in href:
                return href.split('#')[0]

        return None
    except Exception as e:
        print(f"Erro no Scraper ML: {e}")
        return None

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
        session = requests.Session()
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