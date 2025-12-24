# modules/wiki.py
import streamlit as st
import pandas as pd
import os

def main():
    st.title("📚 Wiki Energética")
    st.markdown("Explorá centrales eléctricas reales de Argentina con datos oficiales.")

    # --- Cargar datos ---
   ruta_csv = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "potencia-instalada.csv")
    
    if not os.path.exists(ruta_csv):
        st.error("❌ No se encontró el archivo de datos en `data/potencia-instalada.csv`.")
        return

    df = pd.read_csv(ruta_csv)

    # --- Obtener última potencia por central ---
    df['fecha_proceso'] = pd.to_datetime(df['fecha_proceso'], errors='coerce')
    df = df.sort_values('fecha_proceso')
    df = df.drop_duplicates(subset=['central'], keep='last')

    # --- Filtros ---
    st.sidebar.header("_filtros_")
    regiones = ["Todas"] + sorted(df['region'].dropna().unique().tolist())
    region_sel = st.sidebar.selectbox("Región", regiones)
    
    if region_sel != "Todas":
        df = df[df['region'] == region_sel]

    # --- Selector de central ---
    centrales = sorted(df['agente_descripcion'].dropna().unique())
    central_seleccionada = st.selectbox("Seleccioná una central", centrales)

    if central_seleccionada:
        datos = df[df['agente_descripcion'] == central_seleccionada].iloc[0]

        # --- Ficha técnica ---
        st.subheader(f"⚡ {datos['agente_descripcion']}")
        st.markdown(f"""
        - **Ubicación**: {datos['region']}
        - **Tecnología**: {datos['tecnologia']}
        - **Fuente**: {datos['fuente_generacion']}
        - **Potencia instalada**: {datos['potencia_instalada_mw']:.1f} MW
        - **Código de central**: `{datos['central']}`
        """)

        # --- Contexto termodinámico (básico) ---
        fuente = str(datos['fuente_generacion']).lower()
        if 'térmica' in fuente or 'gas' in fuente or 'carbón' in fuente:
            st.info("🔹 Esta central opera con un **ciclo térmico** (Rankine, Brayton o combinado), estudiado en el **Capítulo 2** del libro.")
        elif 'hidro' in fuente:
            st.info("🔹 Esta central aprovecha la energía potencial del agua (energía mecánica), analizada en el contexto de **sistemas abiertos en estado estacionario**.")
        elif 'nuclear' in fuente:
            st.info("🔹 La fuente de calor es una reacción nuclear, pero el ciclo de potencia sigue siendo **Rankine** (vapor de agua).")
        else:
            st.info("🔹 Central de fuente renovable. Ver enfoque en el **Capítulo 1** sobre diversificación energética.")

        # --- Enlace al libro ---
        st.page_link("https://github.com/pgauna314/proyecto-alfa/blob/main/proyectoalfa/web/main.pdf", label="📘 Ver en el libro", icon="📘")