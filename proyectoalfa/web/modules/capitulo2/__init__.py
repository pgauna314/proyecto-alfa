import streamlit as st
from .cap2_content import mostrar_resumen
from .cap2_examples import examples_render
from .cap2_viz import render_graficos

def render():
    st.title("Capítulo 2: Balances de Masa y Energía")
    
    tab1, tab2, tab3 = st.tabs(["📖 Resumen", "🧮 Ejemplos", "📊 Visualización"])
    
    with tab1:
        mostrar_resumen()
    
    with tab2:
        examples_render()
    
    with tab3:
        render_graficos()
