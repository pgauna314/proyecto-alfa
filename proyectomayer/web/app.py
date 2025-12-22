import streamlit as st
# Importamos las funciones desde nuestra carpeta de módulos
from modules.inicio import mostrar_inicio
from modules.matriz import mostrar_matriz
from modules.capitulo2 import mostrar_cap2
from modules.autor import mostrar_autor

st.set_page_config(page_title="Proyecto MAYER", layout="wide", page_icon="⚛️")

# Barra Lateral
with st.sidebar:
    st.title("🏗️ Proyecto MAYER")
    # AGREGUÉ "Sobre el Autor" AQUÍ ABAJO:
    menu = st.radio("Navegación:", [
        "Inicio", 
        "Matriz Energética", 
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
elif menu == "Capítulo II: Sistemas":
    mostrar_cap2()
elif menu == "Sobre el Autor":         
    mostrar_autor()



