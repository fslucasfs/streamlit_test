import streamlit as st

# Inicializando o estado dos inputs
if "input_opcao1" not in st.session_state:
    st.session_state.input_opcao1 = ""
if "input_opcao2" not in st.session_state:
    st.session_state.input_opcao2 = 0

# Input principal
input_principal = st.selectbox("Selecione uma opção:", ["Selecione", "Opção 1", "Opção 2"])

# Mostrar inputs baseados no valor selecionado
if input_principal == "Opção 1":
    st.text_input(
        "Insira algo para Opção 1:",
        key="input_opcao1"  # Associado diretamente ao estado
    )
elif input_principal == "Opção 2":
    st.number_input(
        "Insira um número para Opção 2:",
        key="input_opcao2"  # Associado diretamente ao estado
    )
else:
    st.write("Escolha uma opção para liberar um novo campo.")

# Exibir valores armazenados no estado (para depuração ou verificação)
st.write("Valor armazenado para Opção 1:", st.session_state.input_opcao1)
st.write("Valor armazenado para Opção 2:", st.session_state.input_opcao2)
