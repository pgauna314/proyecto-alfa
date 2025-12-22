import streamlit as st
# Importamos las funciones desde nuestra carpeta de módulos
from modules.inicio import mostrar_inicio
from modules.matriz import mostrar_matriz
from modules.capitulo2 import mostrar_cap2
from modules.autor import mostrar_autor
# Módulo Σ: El simulador/laboratorio
from modules.laboratorio import mostrar_laboratorio

# Configuración de página con la identidad del Proyecto α
st.set_page_config(
    page_title="Proyecto α - Termodinámica", 
    layout="wide", 
    page_icon="α"
)

# --- Barra Lateral (Sidebar) ---
with st.sidebar:
    st.title("Proyecto α (Alfa)")
    st.markdown("### *Termodinámica de la Conversión de Energía en Argentina*")
    
    st.divider()
    
    # Menú de Navegación actualizado y más ambicioso
    menu = st.radio("Entorno de Trabajo:", [
        "Inicio (Proyecto α)", 
        "Matriz Energética Nacional", 
        "Módulo Σ: Simulador de Procesos", 
        "Módulo λ: Fundamentos de Sistemas",
        "Autor"
    ])
    
    st.divider()
    
    # Acceso a los otros Sostenes del Entorno (Links externos)
    st.subheader("Sostenes del Entorno")
    st.link_button("Módulo ϕ (YouTube)", "https://youtube.com")
    st.link_button("Módulo λ (Libro PDF)", "https://github.com")
    
    st.divider()
    # El lema como cierre del menú lateral
    st.caption("Soberanía Educativa y Tecnológica")

# --- Enrutador de Módulos (Routing) ---
# Nota: Los strings deben coincidir exactamente con las opciones del radio menu anterior
if menu == "Inicio (Proyecto α)":
    mostrar_inicio()

elif menu == "Matriz Energética Nacional":
    mostrar_matriz()

elif menu == "Módulo Σ: Simulador de Procesos":
    # El corazón del cálculo del proyecto
    mostrar_laboratorio()

elif menu == "Módulo λ: Fundamentos de Sistemas":
    # Teoría y formalismo matemático del libro
    mostrar_cap2()

elif menu == "Sobre el autor":         
    mostrar_autor()