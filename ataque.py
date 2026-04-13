import streamlit as st

def mostrar_sala_ataque():
    st.markdown("## 🎯 Setor de Ataque: Finalizadores e Pontas")
    st.write("Aperfeiçoe o instinto matador:")

    # O Módulo 11 é o seu Slalom em U
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 11. Slalom em U (Drible)")
        st.write("**Foco:** Drible, Controle e Equilíbrio")
    with col2:
        if st.button("TREINAR AGORA", key="mod11"):
            st.session_state.executando_treino = "DRIBLE"

    st.write("---")
    
    # Outros módulos do setor
    outros = ["12. Pivô de Ferro", "13. Homem-Gol", "14. Segundo Atacante", "15. Tanque de Explosão"]
    for item in outros:
        with st.expander(item):
            st.write("Módulo em fase de codificação técnica.")
            st.button("Bloqueado", disabled=True, key=item)
