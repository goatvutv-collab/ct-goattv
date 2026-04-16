import streamlit as st

def mostrar_sala_meio():
    st.markdown("## ⚙️ Setor de Meio-Campo: O Cérebro do Time")
    st.write("Refine sua visão de jogo e cadência:")

    modulos = {
        "06. Maestro Cadenciado": "Foco: Passes e Controle | Sacrifício: Explosão",
        "07. Meia-Infiltrador": "Foco: Finalização e Ofensividade | Sacrifício: Defesa",
        "08. Motor de Arranque": "Foco: Drible e Equilíbrio | Sacrifício: Força de Chute",
        "09. Organizador Recuado": "Foco: Passe Rasteiro e Defesa | Sacrifício: Efeito",
        "10. Especialista em Curvas": "Foco: Chute Colocado e Efeito | Sacrifício: Contato Físico"
    }

    for nome, desc in modulos.items():
        with st.expander(nome):
            st.write(desc)
            if st.button(f"Iniciar {nome[:2]}", key=nome):
                st.warning("Aguardando liberação do Comitê Técnico.")