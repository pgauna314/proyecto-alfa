import streamlit as st
import sys
import os

# --- CORRECCIÓN DE RUTAS ---
actual_dir = os.path.dirname(os.path.abspath(__file__))
if actual_dir not in sys.path:
    sys.path.append(actual_dir)

from modules.inicio import mostrar_inicio
from modules.matriz import mostrar_matriz
from modules.capitulo2 import mostrar_cap2
from modules.autor import mostrar_autor
from modules.laboratorio import mostrar_laboratorio

st.set_page_config(page_title="Proyecto α - Termodinámica", layout="wide", page_icon="α")

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("Proyecto α")
    
    # SUBTÍTULO JUSTIFICADO
    st.markdown(
        """
        <div style="text-align: justify; font-style: italic; font-size: 1.1em; color: #808495; line-height: 1.3;">
            Termodinámica de la Conversión de Energía en Argentina
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.divider()
    
    menu = st.radio("Entorno de Trabajo:", [
        "Inicio (Proyecto α)", 
        "Matriz Energética Nacional", 
        "Módulo Σ: Simulador de Procesos", 
        "Módulo λ: Fundamentos de Sistemas",
        "Autor"
    ])
    
    st.divider()
    st.subheader("Sostenes del Entorno")
    st.link_button("Módulo ϕ (YouTube)", "https://youtube.com")
    st.link_button("Módulo λ (Libro PDF)", "https://github.com")
    
    st.divider()
    st.caption("Soberanía Educativa y Tecnológica")

# --- ENRUTADOR ---
if menu == "Inicio (Proyecto α)":
    mostrar_inicio()
elif menu == "Matriz Energética Nacional":
    mostrar_matriz()
elif menu == "Módulo Σ: Simulador de Procesos":
    mostrar_laboratorio()
elif menu == "Módulo λ: Fundamentos de Sistemas":
    mostrar_cap2()
elif menu == "Sobre el autor":         
    mostrar_autor()