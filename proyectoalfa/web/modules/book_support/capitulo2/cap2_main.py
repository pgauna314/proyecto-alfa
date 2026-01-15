import streamlit as st
from .cap2_content import mostrar_resumen
from .cap2_examples import examples_render
from .cap2_viz import render_graficos
from .cap2_eval import render_examen_completo # Importamos el nuevo módulo

def render():
    # --- ESTILO ---
    st.markdown("""
        <style>
            .block-container { padding-top: 1.5rem; }
            h1 { margin-bottom: 0rem; }
        </style>
    """, unsafe_allow_html=True)

    st.title("Balances de Masa y Energía")
    st.caption("Sistemas abiertos y estado estacionario")

    # --- ESTADO DE COMPETENCIAS ---
    if 'competencias_cap2' not in st.session_state:
        st.session_state.competencias_cap2 = {
            "Teórica": False, 
            "Cálculo": False, 
            "Análisis": False
        }

    with st.expander("🎯 Tu progreso en esta unidad", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.success("✅ Dominio Teórico") if st.session_state.competencias_cap2["Teórica"] else st.warning("⏳ Dominio Teórico")
        with c2:
            st.success("✅ Capacidad de Cálculo") if st.session_state.competencias_cap2["Cálculo"] else st.warning("⏳ Capacidad de Cálculo")
        with c3:
            st.success("✅ Análisis Gráfico") if st.session_state.competencias_cap2["Análisis"] else st.warning("⏳ Análisis Gráfico")

    st.write("") 

    # --- PESTAÑAS PRINCIPALES ---
    tabs = st.tabs(["📖 Resumen", "🧮 Ejemplos", "📊 Visualización", "📝 Autoevaluación"])
    
    with tabs[0]:
        mostrar_resumen()
    with tabs[1]:
        examples_render()
    with tabs[2]:
        render_graficos()
    with tabs[3]:
        # Delegamos toda la evaluación al nuevo archivo
        render_examen_completo()