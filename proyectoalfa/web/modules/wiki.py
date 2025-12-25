# modules/wiki.py
import streamlit as st
import pandas as pd
import os

def main():
    # --- Primero: definir los filtros en el SIDEBAR ---
    st.sidebar.header("🔍 Filtros")
    
    # Cargar datos (fuera del sidebar, pero antes de usarlos)
    ruta_csv = os.path.join(os.path.dirname(__file__), "..", "..", "data", "potencia-instalada.csv")
    if not os.path.exists(ruta_csv):
        st.error("❌ No se encontró `data/potencia-instalada.csv`.")
        return

    df = pd.read_csv(ruta_csv)
    df['fecha_proceso'] = pd.to_datetime(df['fecha_proceso'], errors='coerce')
    df = df.sort_values('fecha_proceso').drop_duplicates(subset=['central'], keep='last')
    df = df.dropna(subset=['region', 'tecnologia', 'fuente_generacion'])

    # Crear listas para filtros
    regiones = ["Todas"] + sorted(df['region'].unique().tolist())
    fuentes = ["Todas"] + sorted(df['fuente_generacion'].unique().tolist())
    tecnologias = ["Todas"] + sorted(df['tecnologia'].unique().tolist())

    # ✅ FILTROS EN SIDEBAR (forma directa)
    region_sel = st.sidebar.selectbox("Región", regiones)
    fuente_sel = st.sidebar.selectbox("Fuente", fuentes)
    tecnologia_sel = st.sidebar.selectbox("Tecnología", tecnologias)

    # --- Ahora: contenido principal ---
    st.title("📚 Wiki Energética")
    st.markdown("Explorá centrales eléctricas reales de Argentina.")

    # Aplicar filtros
    df_filtrado = df.copy()
    if region_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['region'] == region_sel]
    if fuente_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['fuente_generacion'] == fuente_sel]
    if tecnologia_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['tecnologia'] == tecnologia_sel]

    # Mostrar resultados
    if df_filtrado.empty:
        st.warning("No hay centrales con esos filtros.")
    else:
        for _, row in df_filtrado.iterrows():
            with st.container(border=True):
                st.subheader(row['agente_descripcion'])
                st.markdown(f"""
                - **Región**: {row['region']}
                - **Tecnología**: {row['tecnologia']}
                - **Fuente**: {row['fuente_generacion']}
                - **Potencia**: {row['potencia_instalada_mw']:.0f} MW
                """)