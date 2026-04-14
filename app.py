import streamlit as st
import time  # Import necessário para o sleep
from scrapers.buscadores import buscar_link_magalu, buscar_link_amazon
from scrapers.magalu import coletar_preco_magalu
from scrapers.amazon import coletar_preco_amazon

st.title("🔍 Comparador de Preços Pro")

produto_usuario = st.text_input("Digite o nome do produto (seja específico):")

if st.button("Comparar Agora"):
    if produto_usuario:
        col1, col2 = st.columns(2)
        
        # --- BUSCA NA MAGALU ---
        with col1:
            st.subheader("Magalu")
            link_magalu = buscar_link_magalu(produto_usuario)

            if link_magalu:
                preco_magalu = coletar_preco_magalu(link_magalu)
                if preco_magalu:
                    st.metric("Preço Magalu", f"R$ {preco_magalu:,.2f}")
                    st.link_button("Ver na Magalu", link_magalu)
                else:
                    st.warning("Não conseguimos ler o preço.")
                    st.write(f"[Link direto para conferir]({link_magalu})")
            else:
                st.error("Nenhum produto encontrado na Magalu.")

        # --- PAUSA ESTRATÉGICA ---
        # Aguarda 2 segundos antes de consultar a Amazon
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
