import streamlit as st

def render_examen_completo():
    st.subheader("Certificación de Competencias")
    st.write("Completá ambas dimensiones para certificar tu dominio del Capítulo 2.")

    subtab1, subtab2 = st.tabs(["📝 Test Teórico (60%)", "🧮 Desafío Numérico"])

    # --- SUB-PESTAÑA 1: TEORÍA ---
    with subtab1:
        if st.session_state.competencias_cap2["Teórica"]:
            st.success("✅ Competencia Teórica Validada.")
            if st.button("Reiniciar Test Teórico"):
                st.session_state.competencias_cap2["Teórica"] = False
                st.rerun()
        else:
            preguntas = [
                {"id": 1, "pregunta": "¿Qué define a un sistema abierto?", "opciones": ["Masa constante", "Flujo de masa a través de fronteras", "Sin intercambio de calor"], "correcta": "Flujo de masa a través de fronteras"},
                {"id": 2, "pregunta": "En estado estacionario, la acumulación de masa es:", "opciones": ["Máxima", "Cero", "Variable"], "correcta": "Cero"},
                {"id": 3, "pregunta": r"La entalpía ($h$) se define matemáticamente como:", "opciones": [r"$u + Pv$", r"$u - Pv$", r"$Q + W$"], "correcta": r"$u + Pv$"},
                {"id": 4, "pregunta": "Si la frontera envuelve solo al vapor en un condensador, el calor cedido:", "opciones": ["Es energía interna", "Cruza la frontera", "Es trabajo de flujo"], "correcta": "Cruza la frontera"},
                {"id": 5, "pregunta": "La primera ley para sistemas abiertos relaciona:", "opciones": ["Solo calor y trabajo", "Solo flujos másicos", "Calor, trabajo y flujos de energía"], "correcta": "Calor, trabajo y flujos de energía"}
            ]

            with st.form("form_teoria"):
                respuestas = {}
                for p in preguntas:
                    st.markdown(f"**{p['id']}. {p['pregunta']}**")
                    respuestas[p['id']] = st.radio("Respuesta:", p['opciones'], index=None, key=f"eval_t_{p['id']}", label_visibility="collapsed")
                    st.write("")
                
                if st.form_submit_button("Validar Teoría"):
                    if None in respuestas.values():
                        st.warning("⚠️ Respondé todas las preguntas.")
                    else:
                        aciertos = sum(1 for p in preguntas if respuestas[p['id']] == p['correcta'])
                        if (aciertos / 5) >= 0.6:
                            st.session_state.competencias_cap2["Teórica"] = True
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(f"Puntaje: {aciertos}/5. Necesitás al menos 3 correctas.")

    # --- SUB-PESTAÑA 2: CÁLCULO ---
    with subtab2:
        if st.session_state.competencias_cap2["Cálculo"]:
            st.success("✅ Competencia de Cálculo Validada.")
            if st.button("Reiniciar Desafío Numérico"):
                st.session_state.competencias_cap2["Cálculo"] = False
                st.rerun()
        else:
            st.markdown("### Problema: Balance en Condensador")
            st.write(r"Calculá el flujo de agua de enfriamiento ($\dot{m}_{agua}$) con estos datos:")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown(r"""
                - $\dot{m}_{vapor} = 100 \ kg/s$
                - $h_{in} = 2500 \ kJ/kg$
                - $h_{out} = 200 \ kJ/kg$
                """)
            with col_d2:
                st.markdown(r"""
                - $\Delta T_{agua} = 10 \ K$
                - $C_{p, agua} = 4.18 \ kJ/kg\cdot K$
                """)

            valor_usuario = st.number_input("Resultado [kg/s]:", min_value=0.0, format="%.2f", key="input_num_eval")
            
            if st.button("Validar Resultado"):
                target = 5502.39
                if abs(valor_usuario - target) <= 5.0:
                    st.session_state.competencias_cap2["Cálculo"] = True
                    st.balloons()
                    st.success("🎯 ¡Excelente! Balance de energía correcto.")
                    st.rerun()
                else:
                    st.error(r"El valor no es correcto. Revisá el balance: $\dot{Q}_{vapor} = \dot{Q}_{agua}$")