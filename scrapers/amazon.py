import requests
from bs4 import BeautifulSoup

def coletar_preco_amazon(url_amazon):
    # Cabeçalho robusto para a Amazon não nos bloquear de cara
    cabecalho = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }

    try:
        # Usamos uma sessão para parecer um navegador real
        sessao = requests.Session()
        resposta = sessao.get(url_amazon, headers=cabecalho, timeout=15)
        
        if resposta.status_code != 200:
            print(f"⚠️ Amazon recusou o acesso (Status {resposta.status_code})")
            return None

        sopa = BeautifulSoup(resposta.text, 'html.parser')

        # A Amazon geralmente guarda o preço nestas classes
        elementos_precos = [
            sopa.find("span", class_="a-price-whole"),
            sopa.find("span", id="priceblock_ourprice"),
            sopa.find("span", id="priceblock_dealprice")
        ]

        for elemento in elementos_precos:
            if elemento:
                # Remove pontos e vírgulas para converter em número
                preco_texto = elemento.text.replace('.', '').replace(',', '.').replace('R$', '').strip()
                return float(preco_texto)

        return None

    except Exception as e:
        print(f"❌ Erro na Amazon: {e}")
        return None