import requests
from bs4 import BeautifulSoup
import re  # Novo import necessário

def coletar_preco_magalu(url_magalu):
    cabecalho = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    try:
        resposta = requests.get(url_magalu, headers=cabecalho, timeout=15)
        sopa = BeautifulSoup(resposta.text, 'html.parser')

        # Tentativa de encontrar o elemento
        elemento_preco = sopa.find("p", {"data-testid": "price-value"}) or \
                         sopa.find("span", {"class": "price-value"})

        if elemento_preco:
            texto = elemento_preco.text
            
            # REGEX MÁGICO: Procura por padrões como 4.999,00 ou 4999.00
            # Ele ignora palavras como "Preço", "R$", etc.
            padrao_preco = r"(\d{1,3}(\.\d{3})*|(\d+))(\,\d{2})?"
            match = re.search(padrao_preco, texto)
            
            if match:
                valor_sujo = match.group()
                # Limpeza final para o Python entender como número
                valor_limpo = valor_sujo.replace('.', '').replace(',', '.')
                return float(valor_limpo)
        
        return None

    except Exception as e:
        print(f"❌ Erro na Magalu: {e}")
        return None