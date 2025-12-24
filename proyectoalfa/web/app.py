<<<<<<< HEAD
import streamlit as st
import os
import sys

# Agregar el directorio actual al path para poder importar módulos
sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(page_title="Proyecto α - Termodinámica", layout="wide", page_icon="α")

with st.sidebar:
    st.title("Proyecto α")
    st.markdown(
        """
        <div style="text-align: justify; font-style: italic; font-weight: bold; font-size: 1.1em; color: #808495; line-height: 1.3;">
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
        "Wiki",
        "Autor"
    ])
    st.divider()
    st.subheader("Sostenes del Entorno")
    st.link_button("Módulo ϕ (YouTube)", "https://youtube.com")
    st.link_button("Módulo λ (Libro PDF)", "https://github.com")
    st.divider()
    st.caption("Soberanía Educativa y Tecnológica")

# Importar y ejecutar el módulo correspondiente
if menu == "Inicio (Proyecto α)":
    from modules.inicio import mostrar_inicio
    mostrar_inicio()
elif menu == "Matriz Energética Nacional":
    from modules.matriz import mostrar_matriz
    mostrar_matriz()
elif menu == "Módulo Σ: Simulador de Procesos":
    from modules.laboratorio import mostrar_laboratorio
    mostrar_laboratorio()
elif menu == "Módulo λ: Fundamentos de Sistemas":
    from modules.capitulo2 import mostrar_cap2
    mostrar_cap2()
elif menu == "Wiki":
    #from modules.wiki import main as wiki_main
    #wiki_main()
elif menu == "Autor":
    from modules.autor import mostrar_autor
=======
import streamlit as st

# CONFIGURACIÓN DE PÁGINA (DEBE SER LO PRIMERO)
st.set_page_config(
    page_title="Proyecto α - Termodinámica",
    layout="wide",
    page_icon="α",
    initial_sidebar_state="expanded"
)

# SIDEBAR - MENÚ
with st.sidebar:
    st.title("Proyecto α")
    st.markdown(
        """
        <div style="text-align: justify; font-style: italic; font-weight: bold; 
                    font-size: 1.1em; color: #808495; line-height: 1.3;">
            Termodinámica de la Conversión de Energía en Argentina
        </div>
        """,
        unsafe_allow_html=True
    )
    st.divider()
    
    # MENU PRINCIPAL
    opcion = st.radio(
        "🌐 Navegación Principal:",
        [
            "🏠 Inicio",
            "📊 Matriz Energética", 
            "⚙️ Simulador de Procesos",
            "📚 Fundamentos de Sistemas",
            "🔍 Wiki",
            "👤 Autor"
        ]
    )
    
    st.divider()
    st.subheader("📦 Recursos")
    st.page_link("https://youtube.com", label="📺 Módulo ϕ (YouTube)", icon="📺")
    st.page_link("https://github.com", label="📘 Módulo λ (PDF)", icon="📘")
    st.divider()
    st.caption("⚡ Soberanía Educativa y Tecnológica")

# CONTENIDO PRINCIPAL BASADO EN LA OPCIÓN
if opcion == "🏠 Inicio":
    from modules.inicio import mostrar_inicio
    mostrar_inicio()
    
elif opcion == "📊 Matriz Energética":
    from modules.matriz import mostrar_matriz
    mostrar_matriz()
    
elif opcion == "⚙️ Simulador de Procesos":
    from modules.laboratorio import mostrar_laboratorio
    mostrar_laboratorio()
    
elif opcion == "📚 Fundamentos de Sistemas":
    from modules.capitulo2 import mostrar_cap2
    mostrar_cap2()
    
elif opcion == "🔍 Wiki":
    from modules.wiki import main as wiki_main
    wiki_main()
    
elif opcion == "👤 Autor":
    from modules.autor import mostrar_autor
>>>>>>> 1a24feb0dbd31b1b70938b2c48315a35e76f7756
    mostrar_autor()