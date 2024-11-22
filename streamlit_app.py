import streamlit as st

# Input principal
input_principal = st.selectbox("Selecione uma opção:", ["Selecione", "Opção 1", "Opção 2"])

# Mostrar outro input dependendo do valor selecionado
if input_principal == "Opção 1":
    st.text_input("Insira algo para Opção 1:")
elif input_principal == "Opção 2":
    st.number_input("Insira um número para Opção 2:")
else:
    st.write("Escolha uma opção para liberar um novo campo.")
