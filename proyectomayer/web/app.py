import streamlit as st
# Importamos las funciones desde nuestra carpeta de módulos
from modules.inicio import mostrar_inicio
from modules.matriz import mostrar_matriz
from modules.capitulo2 import mostrar_cap2
from modules.autor import mostrar_autor
from modules.laboratorio import mostrar_laboratorio

# Configuración de página con la nueva identidad
st.set_page_config(
    page_title="Proyecto α - Termodinámica", 
    layout="wide", 
    page_icon="α"
)

# Barra Lateral (Sidebar)
with st.sidebar:
    st.title("Proyecto α (Alfa)")
    st.markdown("### *Conversión de Energía en Argentina*")
    
    st.divider()
    
    # Menú de Navegación actualizado
    menu = st.radio("Entorno de Trabajo:", [
        "Inicio (Proyecto α)", 
        "Matriz Energética Nacional", 
        "Σ - Laboratorio de Propiedades", 
        "λ - Capítulo II: Sistemas",
        "Autor"
    ])
    
    st.divider()
    
    # Sostenes del Entorno (Acceso a los otros módulos)
    st.subheader("Sostenes del Entorno")
    st.link_button("Módulo ϕ (YouTube)", "https://youtube.com")
    st.link_button("Módulo λ (Libro PDF)", "https://github.com")
    
    st.divider()
    st.caption("Soberanía Educativa y Tecnológica")

# Enrutador inteligente (Routing)
if menu == "Inicio (Proyecto α)":
    mostrar_inicio()
elif menu == "Matriz Energética Nacional":
    mostrar_matriz()
elif menu == "Σ - Laboratorio de Propiedades":
    mostrar_laboratorio()
elif menu == "λ - Capítulo II: Sistemas":
    mostrar_cap2()
elif menu == "Autor":         
    mostrar_autor()