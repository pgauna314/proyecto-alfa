import streamlit as st
# Importamos las funciones desde nuestra carpeta de módulos
from modules.inicio import mostrar_inicio
from modules.matriz import mostrar_matriz
from modules.capitulo2 import mostrar_cap2
from modules.autor import mostrar_autor
# NUEVO: Importamos el laboratorio
from modules.laboratorio import mostrar_laboratorio

st.set_page_config(page_title="Proyecto TERMO", layout="wide", page_icon="⚛️")

# Barra Lateral
with st.sidebar:
    st.title("🏗️ Proyecto MAYER")
    # AGREGAMOS "Laboratorio de Propiedades" al menú:
    menu = st.radio("Navegación:", [
        "Inicio", 
        "Matriz Energética", 
        "Laboratorio de Propiedades", # <-- NUEVA OPCIÓN
        "Capítulo II: Sistemas",
        "Sobre el Autor"
    ])
    st.divider()
    st.link_button("📺 YouTube", "https://youtube.com")
    st.link_button("📚 Libro PDF", "https://github.com")

# Enrutador inteligente
if menu == "Inicio":
    mostrar_inicio()
elif menu == "Matriz Energética":
    mostrar_matriz()
elif menu == "Laboratorio de Propiedades": # <-- NUEVA RUTA
    mostrar_laboratorio()
elif menu == "Capítulo II: Sistemas":
    mostrar_cap2()
elif menu == "Sobre el Autor":         
    mostrar_autor()

