# ... Imports ...

# --- DENTRO DA ÁREA LOGADA ---
tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

with tabs[3]: # O PILAR DE EDIÇÃO
    st.subheader("⚙️ Central de Personalização")
    with st.form("edit_perfil_total"):
        col1, col2 = st.columns(2)
        new_n = col1.text_input("Nome de Guerra:", value=p["nome"])
        new_pos = col2.selectbox("Posição Principal:", ["ATA", "MEI", "DEF", "GOL"], index=["ATA", "MEI", "DEF", "GOL"].index(p["posicao"]))
        
        new_alt = col1.number_input("Altura (m):", value=p["altura"])
        new_peso = col2.number_input("Peso (kg):", value=p["peso"])
        
        nova_ft = st.file_uploader("Trocar Foto Oficial:")
        
        if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
            db = carregar_db()
            id_atleta = st.session_state.id_logado
            
            if nova_ft:
                path = f"fotos_atletas/{id_atleta}.png"
                Image.open(nova_ft).save(path)
                db[id_atleta]["foto"] = path
            
            db[id_atleta].update({"nome": new_n, "posicao": new_pos, "altura": new_alt, "peso": new_peso})
            salvar_db(db)
            st.session_state.perfil = db[id_atleta]
            st.rerun()
