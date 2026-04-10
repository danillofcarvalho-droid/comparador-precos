import streamlit as st
import time  # Import necessário para o sleep
from scrapers.buscadores import buscar_link_ml, buscar_link_amazon
from scrapers.ml import coletar_preco_ml
from scrapers.amazon import coletar_preco_amazon

st.title("🔍 Comparador de Preços Pro")

produto_usuario = st.text_input("Digite o nome do produto (seja específico):")

if st.button("Comparar Agora"):
    if produto_usuario:
        col1, col2 = st.columns(2)
        
        # --- BUSCA NO MERCADO LIVRE ---
        with col1:
            st.subheader("Mercado Livre")
            link_ml = buscar_link_ml(produto_usuario)
            if link_ml:
                preco_ml = coletar_preco_ml(link_ml)
                if preco_ml:
                    st.metric("Preço ML", f"R$ {preco_ml:,.2f}")
                    st.link_button("Ver no Mercado Livre", link_ml)
                else:
                    st.warning("Não conseguimos ler o preço.")
                    st.write(f"[Link direto para conferir]({link_ml})")
            else:
                st.error("Nenhum produto encontrado no ML.")

        # --- PAUSA ESTRATÉGICA ---
        # Aguarda 2 segundos antes de "atacar" a Amazon para diminuir chances de block
        time.sleep(2)

        # --- BUSCA NA AMAZON ---
        with col2:
            st.subheader("Amazon")
            link_amz = buscar_link_amazon(produto_usuario)
            if link_amz:
                preco_amz = coletar_preco_amazon(link_amz)
                if preco_amz:
                    st.metric("Preço Amazon", f"R$ {preco_amz:,.2f}")
                    st.link_button("Ver na Amazon", link_amz)
                else:
                    st.warning("Não conseguimos ler o preço.")
                    st.write(f"[Link direto para conferir]({link_amz})")
            else:
                st.error("Nenhum produto encontrado na Amazon.")
    else:
        st.error("Digite algo para pesquisar!")