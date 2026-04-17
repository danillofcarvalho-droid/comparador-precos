# Comparador de Precos Pro

Aplicacao em Python para comparar precos de produtos em diferentes marketplaces brasileiros.

Atualmente o projeto consulta:
- Amazon
- Magalu
- KaBuM!

A interface principal foi construida com Streamlit e o projeto tambem possui integracao com Supabase para monitoramento e registro de historico de precos.

## Visao Geral

O usuario digita o nome de um produto e a aplicacao:
- busca o item em cada loja suportada
- tenta capturar o preco da pagina do produto
- exibe os resultados lado a lado
- disponibiliza o link direto quando a loja responde corretamente

O projeto tambem possui um script auxiliar para consultar links salvos no Supabase e registrar o menor preco encontrado.

## Funcionalidades

- Comparacao de precos em 3 lojas
- Interface web simples com Streamlit
- Scrapers separados por marketplace
- Integracao com Supabase
- Estrutura modular para adicionar novas lojas no futuro

## Tecnologias Utilizadas

- Python 3
- Streamlit
- Requests
- BeautifulSoup4
- Supabase

## Estrutura do Projeto

```text
conexao_banco/
|-- app.py
|-- principal.py
|-- conexao_banco.py
|-- requirements.txt
|-- README.md
`-- scrapers/
    |-- amazon.py
    |-- buscadores.py
    |-- kabum.py
    `-- magalu.py
```

## Como Executar o Projeto

### 1. Clonar o repositorio

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd conexao_banco
```

### 2. Criar e ativar um ambiente virtual

No Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependencias

```bash
pip install -r requirements.txt
```

### 4. Executar a aplicacao Streamlit

```bash
streamlit run app.py
```

## Como Usar

1. Abra a aplicacao no navegador.
2. Digite o nome do produto.
3. Clique em `Comparar Agora`.
4. Veja os precos encontrados em cada loja.

## Integracao com Supabase

O projeto pode usar variaveis de ambiente ou `st.secrets` para acessar o Supabase.

### Variaveis esperadas

```env
SUPABASE_URL=seu_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase
```

### Onde essas configuracoes sao usadas

- [`conexao_banco.py`](./conexao_banco.py): cria a conexao com o Supabase
- [`principal.py`](./principal.py): consulta produtos salvos e registra o menor preco

## Script de Monitoramento

Para executar o monitoramento via terminal:

```bash
python principal.py
```

Esse script:
- busca registros na tabela `links_monitoramento`
- consulta Amazon, Magalu e KaBuM!
- identifica o menor preco
- salva o resultado na tabela `produtos`

## Observacoes Importantes

- Alguns marketplaces podem bloquear requisicoes automatizadas em determinados momentos.
- Dependendo da loja, um produto pode ser encontrado, mas o link ou o preco nao ficarem disponiveis temporariamente.
- O comportamento pode variar conforme regras anti-bot, disponibilidade da pagina e mudancas no HTML das lojas.

## Melhorias Futuras

- Adicionar novos marketplaces
- Melhorar o tratamento de bloqueios e links indisponiveis
- Criar historico visual de precos
- Adicionar testes automatizados
- Melhorar ranking e relevancia dos resultados encontrados

## Autor

Danillo Carvalho. Projeto desenvolvido para estudo e pratica de scraping, comparacao de precos e integracao com banco de dados.
