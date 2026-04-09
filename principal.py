from conexao_banco import supabase
# Importando scraper
from scrapers.ml import coletar_preco_ml
from scrapers.magalu import coletar_preco_magalu
from scrapers.amazon import coletar_preco_amazon 

def executar_comparador():
    print("\n--- 🔍 Iniciando Comparador de Preços Pro ---")
    
    # 1. Busca todos os produtos cadastrados na sua tabela de monitoramento
    try:
        resposta = supabase.table("links_monitoramento").select("*").execute()
        produtos = resposta.data
    except Exception as e:
        print(f"❌ Erro ao conectar ao Supabase: {e}")
        return

    if not produtos:
        print("ℹ️ Nenhuma linha encontrada na tabela 'links_monitoramento'.")
        return

    for produto in produtos:
        nome = produto.get('nome_produto', 'Produto sem nome')
        print(f"\n# Verificando: {nome}")
        
        precos_encontrados = []

        # --- VERIFICAÇÃO AMAZON ---
        if produto.get('url_amazon'):
            print(f"🔎 Consultando Amazon...")
            valor_amazon = coletar_preco_amazon(produto['url_amazon'])
            if valor_amazon:
                print(f"✅ Amazon: R$ {valor_amazon}")
                precos_encontrados.append(valor_amazon)
            else:
                print("❌ Amazon: Preço não encontrado ou acesso bloqueado.")

        # --- VERIFICAÇÃO MERCADO LIVRE 
        if produto.get('url_mercadolivre'):
            print(f"🔎 Consultando Mercado Livre...")
            valor_ml = coletar_preco_ml(produto['url_mercadolivre'])
            if valor_ml:
                print(f"✅ Mercado Livre: R$ {valor_ml}")
                precos_encontrados.append(valor_ml)
            else:
                print("❌ Mercado Livre: Preço não encontrado.")

        # --- VERIFICAÇÃO MAGALU ---
        if produto.get('url_magalu'):
            print(f"🔎 Consultando Magalu...")
            valor_magalu = coletar_preco_magalu(produto['url_magalu'])
            if valor_magalu:
                print(f"✅ Magalu: R$ {valor_magalu}")
                precos_encontrados.append(valor_magalu)
            else:
                print("❌ Magalu: Preço não encontrado.")

        # --- LÓGICA DO MENOR PREÇO ---
        if precos_encontrados:
            menor_preco = min(precos_encontrados)
            print(f"🏆 VENCEDOR: {nome} por R$ {menor_preco}")
            
            # 2. Salva o histórico da melhor oferta na tabela 'produtos'
            dados_historico = {
                "nome": nome,
                "preco_alvo": menor_preco
            }
            
            try:
                supabase.table("produtos").insert(dados_historico).execute()
                print("✨ Resultado salvo no histórico do Supabase!")
            except Exception as e:
                print(f"⚠️ Erro ao salvar no histórico: {e}")
        else:
            print(f"⚠️ Nenhum preço capturado para '{nome}' em nenhuma das lojas.")

if __name__ == "__main__":
    executar_comparador()