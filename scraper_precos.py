import requests
from bs4 import BeautifulSoup

def coletar_preco_teste(url_produto):
    cabecalho = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        resposta = requests.get(url_produto, headers=cabecalho)
        sopa = BeautifulSoup(resposta.text, 'html.parser')

        # No site de teste, o preço está em um span com itemprop="price"
        elemento_preco = sopa.find("span", attrs={"itemprop": "price"})

        if elemento_preco:
            # O texto vem como "$899.99", precisamos tirar o "$"
            texto_limpo = elemento_preco.text.replace('$', '').strip()
            return float(texto_limpo)
        
        print("❌ Não encontrei o preço no HTML informado.")
        return None

    except Exception as e:
        print(f"❌ Erro na coleta: {e}")
        return None

if __name__ == "__main__":
    # Use o link que você me enviou
    url = "https://webscraper.io/test-sites/e-commerce/allinone/phones"
    valor = coletar_preco_teste(url)
    if valor:
        print(f"✅ Sucesso! Preço capturado no site de teste: R$ {valor}")