import streamlit as st

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Proyecto α - Termodinámica",
    layout="wide",
    page_icon="⚡",  # emoji válido
    initial_sidebar_state="expanded"
)

# SIDEBAR — ÚNICO BLOQUE PERMITIDO
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
    
    # MENÚ PRINCIPAL
    opcion = st.radio(
        "🌐 Navegación Principal:",
        [
            "🏠 Inicio",
            "📊 Matriz Energética Nacional", 
            "⚙️ Calculadora de Propiedades",
            "📚 Balances de Materia y Energía",
            "🔍 Wiki",
            "👤 Autor"
        ]
    )
    
    # FILTROS DINÁMICOS (solo para Wiki)
    if opcion == "🔍 Wiki":
        st.divider()
        st.subheader("🔍 Filtros Wiki")
        # Guardamos en session_state para usar en modules/wiki.py
        st.session_state.region_wiki = st.selectbox(
            "Región",
            ["Todas", "NOA", "NEA", "Centro", "Cuyo", "Patagonia", "Buenos Aires"]
        )
        st.session_state.fuente_wiki = st.selectbox(
            "Fuente",
            ["Todas", "Térmica", "Hidro", "Renovable", "Nuclear"]
        )
        st.session_state.tecnologia_wiki = st.selectbox(
            "Tecnología",
            ["Todas", "Turbina a Gas", "Turbovapor", "Ciclo Combinado", "Hidráulica", "Eólica", "Solar", "Biogás", "Carbón"]
        )
    
    st.divider()
    st.subheader("📦 Recursos")
    st.page_link("https://youtube.com", label="📺 Módulo ϕ (YouTube)", icon="📺")
    st.page_link("https://github.com", label="📘 Módulo λ (PDF)", icon="📘")
    st.divider()
    st.caption("⚡ Soberanía Educativa y Tecnológica")

# ENRUTADOR — contenido principal
if opcion == "🏠 Inicio":
    from modules.inicio import mostrar_inicio
    mostrar_inicio()
    
elif opcion == "📊 Matriz Energética Nacional":
    from modules.matriz import mostrar_matriz
    mostrar_matriz()
    
elif opcion == "⚙️ Calculadora de Propiedades":
    from modules.laboratorio import mostrar_laboratorio
    mostrar_laboratorio()
    
elif opcion == "📚 Balances de Materia y Energía":
    from modules.capitulo2 import mostrar_cap2
    mostrar_cap2()
    
elif opcion == "🔍 Wiki":
    from modules.wiki import main as wiki_main
    wiki_main()
    
elif opcion == "👤 Autor":
    from modules.autor import mostrar_autor
    mostrar_autor()