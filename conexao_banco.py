import os
from supabase import create_client, Client

# --- CONFIGURAÇÕES DO SEU PROJETO ---
# Pegue esses dados no seu painel do Supabase: Settings > API
URL_PROJETO = 'https://lzaktbpmaanlgcwuhbkj.supabase.co'
CHAVE_API = "sb_publishable_EMfgvW0eejC7yR2WA0tLOg_yhyovFFq"

# Inicializa o cliente do Supabase
supabase: Client = create_client(URL_PROJETO, CHAVE_API)

def testar_conexao():
    try:
        # Tenta buscar os produtos da tabela que criamos no SQL
        resposta = supabase.table("produtos").select("*").execute()
        print("✅ Conexão com Supabase estabelecida com sucesso!")
        print(f"Produtos encontrados: {resposta.data}")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")

if __name__ == "__main__":
    testar_conexao()