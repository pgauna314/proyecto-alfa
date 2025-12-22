import streamlit as st
# Importamos las funciones desde nuestra carpeta de módulos
from modules.inicio import mostrar_inicio
from modules.matriz import mostrar_matriz
from modules.capitulo2 import mostrar_cap2
from modules.autor import mostrar_autor
# Laboratorio de Propiedades (Módulo Σ)
from modules.laboratorio import mostrar_laboratorio

# Configuración de página con la identidad del Proyecto α
st.set_page_config(
    page_title="Proyecto α - Termodinámica", 
    layout="wide", 
    page_icon="α"
)

# --- Barra Lateral (Sidebar) ---
with st.sidebar:
    st.title("Proyecto α")
    st.markdown("### *Termodinámica de la Conversión de Energía en Argentina*")
    
    st.divider()
    
   # Menú de Navegación actualizado y más ambicioso
    menu = st.radio("Entorno de Trabajo:", [
    "Inicio (Proyecto α)", 
    "Matriz Energética Nacional", 
    "Módulo Σ: Simulador de Procesos", # <-- Más que un laboratorio, es un simulador
    "Módulo λ: Fundamentos de Sistemas",
    "Autor"])
    
    st.divider()
    
    # Acceso a los otros Sostenes del Entorno
    st.subheader("Sostenes del Entorno")
    st.link_button("Módulo ϕ (YouTube)", "https://youtube.com")
    st.link_button("Módulo λ (Libro PDF)", "https://github.com")
    
    st.divider()
    # El lema como cierre del menú lateral
    st.caption("Soberanía Educativa y Tecnológica")

# --- Enrutador de Módulos ---
if menu == "Inicio (Proyecto α)":
    # Aquí es donde el usuario ve la descripción general del entorno
    mostrar_inicio()

elif menu == "Matriz Energética Nacional":
    mostrar_matriz()

elif menu == "Σ - Laboratorio de Propiedades":
    # El corazón del cálculo del proyecto
    mostrar_laboratorio()

elif menu == "λ - Capítulo II: Sistemas":
    # Teoría y formalismo matemático
    mostrar_cap2()

elif menu == "Autor":         
    mostrar_autor()