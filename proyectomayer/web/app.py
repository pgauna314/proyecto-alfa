import streamlit as st
import sys
import os

# --- CORRECCIÓN DE RUTAS PARA STREAMLIT CLOUD ---
# Agregamos la carpeta 'web' al path de Python para que encuentre 'modules'
actual_dir = os.path.dirname(os.path.abspath(__file__))
if actual_dir not in sys.path:
    sys.path.append(actual_dir)

# Ahora sí, importamos las funciones
try:
    from modules.inicio import mostrar_inicio
    from modules.matriz import mostrar_matriz
    from modules.capitulo2 import mostrar_cap2
    from modules.autor import mostrar_autor
    from modules.laboratorio import mostrar_laboratorio
except ModuleNotFoundError as e:
    st.error(f"Error al cargar los módulos: {e}")
    st.stop()

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Proyecto α - Termodinámica", 
    layout="wide", 
    page_icon="α"
)

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("Proyecto α")
    st.markdown("### *Termodinámica de la Conversión de Energía en Argentina*")
    
    st.divider()
    
    # Menú de Navegación (Guardamos la opción en la variable 'menu')
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

# --- ENRUTADOR DE MÓDULOS ---
# Importante: Los nombres aquí DEBEN ser idénticos a los del radio button
if menu == "Inicio (Proyecto α)":
    mostrar_inicio()

elif menu == "Matriz Energética Nacional":
    mostrar_matriz()

elif menu == "Módulo Σ: Simulador de Procesos":
    mostrar_laboratorio()

elif menu == "Módulo λ: Fundamentos de Sistemas":
    mostrar_cap2()

elif menu == "Autor":         
    mostrar_autor()