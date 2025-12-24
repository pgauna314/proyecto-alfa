import streamlit as st
import os
import sys

# Configurar path para importar módulos
sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="Proyecto α - Termodinámica",
    layout="wide",
    page_icon="α"
)

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
    
    menu = st.radio("Entorno de Trabajo:", [
        "Inicio (Proyecto α)",
        "Matriz Energética Nacional",
        "Módulo Σ: Simulador de Procesos",
        "Módulo λ: Fundamentos de Sistemas",
        "Wiki",
        "Autor"
    ], index=0)  # index=0 selecciona "Inicio" por defecto
    
    st.divider()
    st.subheader("Sostenes del Entorno")
    st.link_button("Módulo ϕ (YouTube)", "https://youtube.com")
    st.link_button("Módulo λ (Libro PDF)", "https://github.com")
    st.divider()
    st.caption("Soberanía Educativa y Tecnológica")

# PANEL DE DIAGNÓSTICO (oculto por defecto)
with st.sidebar.expander("🔧 Estado del Sistema", expanded=False):
    st.write(f"Directorio: `{os.path.dirname(__file__)}`")
    st.write("Módulos encontrados:")
    
    modulos_a_verificar = ["inicio", "matriz", "laboratorio", "capitulo2", "autor", "wiki"]
    for modulo in modulos_a_verificar:
        ruta = os.path.join("modules", f"{modulo}.py")
        existe = os.path.exists(ruta)
        st.write(f"• {modulo}: {'✅' if existe else '❌'}")

# IMPORTAR SOLO EL MÓDULO SELECCIONADO (CON MANEJO DE ERRORES)
try:
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
        from modules.wiki import main as wiki_main
        wiki_main()
    elif menu == "Autor":
        from modules.autor import mostrar_autor
        mostrar_autor()
except Exception as e:
    st.error(f"❌ Error al cargar el módulo: `{menu}`")
    st.code(str(e))
    st.info("Revisa la terminal para más detalles.")