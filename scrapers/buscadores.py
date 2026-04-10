import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def buscar_link_ml(nome_produto):
    termo_busca = quote(nome_produto)
    url_busca = f"https://lista.mercadolivre.com.br/{termo_busca}"
    
    # Headers mais completos para parecer um navegador real
    cabecalho = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        resposta = requests.get(url_busca, headers=cabecalho, timeout=10)
        
        # Se o ML bloquear, ele retorna código 403 ou 429
        if resposta.status_code != 200:
            print(f"Erro de acesso: Status {resposta.status_code}")
            return None

        sopa = BeautifulSoup(resposta.text, 'html.parser')
        # Se isso imprimir um texto curto ou com "Access Denied", você foi bloqueado temporariamente
        print(sopa.title.text)

        # Tentativa de pegar todos os links que pareçam de produtos
        itens = sopa.find_all("a", href=True)
        
        for item in itens:
            link = item['href']
            # Filtro reforçado: links de produtos reais do ML
            if ("articulo.mercadolivre.com.br" in link or "/p/MLB" in link) and "/navigation/" not in link:
                return link
                
        return None
    except Exception as e:
        print(f"Erro: {e}")
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