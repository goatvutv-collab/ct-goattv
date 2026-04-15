import streamlit as st

def mostrar_sala_defesa():
    st.markdown("## 🛡️ Setor de Defesa: Área de Especialistas")
    st.write("Escolha seu regime de treino defensivo:")

    # Lista de Módulos conforme seu Dossiê
    modulos = {
        "01. Muralha Fixa": "Foco: Desarme e Contato Físico | Sacrifício: Velocidade",
        "02. Perseguidor": "Foco: Agressividade e Velocidade | Sacrifício: Controle de Bola",
        "03. Beque de Saída": "Foco: Passe e Hab. Defensiva | Sacrifício: Finalização",
        "04. Lateral de Apoio": "Foco: Resistência e Cruzamento | Sacrifício: Cabeçada",
        "05. Antena Tática": "Foco: Intercepção e Equilíbrio | Sacrifício: Explosão"
    }

    for nome, desc in modulos.items():
        with st.expander(nome):
            st.write(desc)
            if st.button(f"Iniciar {nome[:2]}", key=nome):
                st.warning(f"O simulador do módulo {nome[:2]} está sendo calibrado.")