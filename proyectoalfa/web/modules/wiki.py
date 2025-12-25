# modules/wiki.py
import streamlit as st
import pandas as pd
import os

def main():
    st.title("📚 Wiki Energética")
    st.markdown("Explorá centrales eléctricas reales de Argentina mediante filtros.")

    # --- Cargar datos ---
    ruta_csv = os.path.join(os.path.dirname(__file__), "..", "..", "data", "potencia-instalada.csv")
    if not os.path.exists(ruta_csv):
        st.error("❌ No se encontró `data/potencia-instalada.csv`.")
        return

    df = pd.read_csv(ruta_csv)

    # Tomar el registro más reciente por central
    df['fecha_proceso'] = pd.to_datetime(df['fecha_proceso'], errors='coerce')
    df = df.sort_values('fecha_proceso').drop_duplicates(subset=['central'], keep='last')

    # --- LIMPIEZA DE CATEGORÍAS ---
    # Normalizar regiones y tecnologías para evitar duplicados
    df = df.dropna(subset=['region', 'tecnologia', 'fuente_generacion'])

    # --- FILTROS EN SIDEBAR ---
    st.sidebar.header("🔍 Filtros")
    
    regiones = ["Todas"] + sorted(df['region'].unique().tolist())
    region_sel = st.sidebar.selectbox("Región", regiones)

    fuentes = ["Todas"] + sorted(df['fuente_generacion'].unique().tolist())
    fuente_sel = st.sidebar.selectbox("Fuente", fuentes)

    tecnologias = ["Todas"] + sorted(df['tecnologia'].unique().tolist())
    tecnologia_sel = st.sidebar.selectbox("Tecnología", tecnologias)

    # --- APLICAR FILTROS ---
    df_filtrado = df.copy()
    if region_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['region'] == region_sel]
    if fuente_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['fuente_generacion'] == fuente_sel]
    if tecnologia_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['tecnologia'] == tecnologia_sel]

    # --- MOSTRAR RESULTADOS ---
    if df_filtrado.empty:
        st.warning("No hay centrales que coincidan con los filtros seleccionados.")
    else:
        st.subheader(f"⚡ {len(df_filtrado)} centrales encontradas")
        
        for _, row in df_filtrado.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(row['agente_descripcion'])
                    st.markdown(f"""
                    - **Región**: {row['region']}
                    - **Tecnología**: {row['tecnologia']}
                    - **Fuente**: {row['fuente_generacion']}
                    """)
                with col2:
                    st.metric("Potencia", f"{row['potencia_instalada_mw']:.0f} MW")
                
                # Contexto termodinámico básico (opcional)
                if "Gas" in str(row['tecnologia']):
                    st.info("🔹 Usa ciclo Brayton (turbina a gas).")
                elif "Vapor" in str(row['tecnologia']):
                    st.info("🔹 Usa ciclo Rankine (turbovapor).")
                elif "Hidro" in str(row['fuente_generacion']):
                    st.info("🔹 Energía potencial → mecánica.")