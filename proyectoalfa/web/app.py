import streamlit as st
from src.utils import load_power_data

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
    mostrar_autor()
    
# Título
st.title("📊 Análisis de la Matriz Energética Argentina")

# Cargar datos
df = load_power_data()

# Sidebar: filtros
region = st.sidebar.selectbox("Región", options=["Todas"] + sorted(df["region"].dropna().unique().tolist()))
tecnologia = st.sidebar.selectbox("Tecnología", options=["Todas"] + sorted(df["tecnologia"].dropna().unique().tolist()))

# Aplicar filtros
if region != "Todas":
    df = df[df["region"] == region]
if tecnologia != "Todas":
    df = df[df["tecnologia"] == tecnologia]

# Mostrar resumen
st.subheader(f"Potencia instalada total: {df['potencia_instalada_mw'].sum():,.0f} MW")
st.dataframe(df[['central', 'region', 'tecnologia', 'potencia_instalada_mw', 'anio']].head(10))

# Gráfico opcional
st.bar_chart(df.groupby('fuente_generacion')['potencia_instalada_mw'].sum())