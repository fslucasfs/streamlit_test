import streamlit as st

# Inicializando o estado dos inputs
if "input_opcao1" not in st.session_state:
    st.session_state.input_opcao1 = ""
if "input_opcao2" not in st.session_state:
    st.session_state.input_opcao2 = 0

# Funções para atualizar os valores no estado
def update_opcao1(value):
    st.session_state.input_opcao1 = value

def update_opcao2(value):
    st.session_state.input_opcao2 = value

# Input principal
input_principal = st.selectbox("Selecione uma opção:", ["Selecione", "Opção 1", "Opção 2"])

# Mostrar inputs baseados no valor selecionado
if input_principal == "Opção 1":
    st.text_input(
        "Insira algo para Opção 1:",
        value=st.session_state.input_opcao1,
        on_change=update_opcao1,
        key="input_opcao1"
    )
elif input_principal == "Opção 2":
    st.number_input(
        "Insira um número para Opção 2:",
        value=st.session_state.input_opcao2,
        on_change=update_opcao2,
        key="input_opcao2"
    )
else:
    st.write("Escolha uma opção para liberar um novo campo.")
