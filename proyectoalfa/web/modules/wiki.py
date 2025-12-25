# modules/wiki.py
import streamlit as st
import pandas as pd
import os

def main():
    # --- Configuración de página ---
    st.set_page_config(page_title="Wiki Energética", layout="wide")
    
    # --- Cargar datos ---
    ruta_csv = os.path.join(os.path.dirname(__file__), "..", "..", "data", "potencia-instalada.csv")
    if not os.path.exists(ruta_csv):
        st.error("❌ No se encontró `data/potencia-instalada.csv`.")
        return
    
    df = pd.read_csv(ruta_csv)
    df['fecha_proceso'] = pd.to_datetime(df['fecha_proceso'], errors='coerce')
    df = df.sort_values('fecha_proceso').drop_duplicates(subset=['central'], keep='last')
    df = df.dropna(subset=['region', 'tecnologia', 'fuente_generacion'])
    
    # --- Sidebar con filtros avanzados ---
    st.sidebar.header("🔍 Filtros Avanzados")
    
    # Opción 1: Filtros independientes con multiselect
    st.sidebar.subheader("Filtrar por:")
    
    # Multiselect con opción "Todas" automática
    regiones = ["Todas"] + sorted(df['region'].unique().tolist())
    tecnologias = ["Todas"] + sorted(df['tecnologia'].unique().tolist())
    fuentes = ["Todas"] + sorted(df['fuente_generacion'].unique().tolist())
    
    # Filtros con selección múltiple
    region_sel = st.sidebar.multiselect(
        "Región",
        options=sorted(df['region'].unique().tolist()),
        default=None,
        help="Selecciona una o más regiones"
    )
    
    tecnologia_sel = st.sidebar.multiselect(
        "Tecnología",
        options=sorted(df['tecnologia'].unique().tolist()),
        default=None,
        help="Selecciona una o más tecnologías"
    )
    
    fuente_sel = st.sidebar.multiselect(
        "Fuente de Generación",
        options=sorted(df['fuente_generacion'].unique().tolist()),
        default=None,
        help="Selecciona uno o más tipos de fuente"
    )
    
    # Filtro adicional por potencia (opcional)
    st.sidebar.subheader("Filtro por Potencia")
    potencia_min = st.sidebar.number_input(
        "Potencia Mínima (MW)",
        min_value=0.0,
        max_value=float(df['potencia_instalada_mw'].max()),
        value=0.0,
        step=10.0
    )
    
    potencia_max = st.sidebar.number_input(
        "Potencia Máxima (MW)",
        min_value=0.0,
        max_value=float(df['potencia_instalada_mw'].max()),
        value=float(df['potencia_instalada_mw'].max()),
        step=10.0
    )
    
    # --- Contenido principal ---
    st.title("📚 Wiki Energética")
    st.markdown("Explorá centrales eléctricas reales de Argentina.")
    
    # --- Aplicar filtros ---
    df_filtrado = df.copy()
    
    # Aplicar filtros de selección múltiple
    if region_sel:
        df_filtrado = df_filtrado[df_filtrado['region'].isin(region_sel)]
    
    if tecnologia_sel:
        df_filtrado = df_filtrado[df_filtrado['tecnologia'].isin(tecnologia_sel)]
    
    if fuente_sel:
        df_filtrado = df_filtrado[df_filtrado['fuente_generacion'].isin(fuente_sel)]
    
    # Aplicar filtro de potencia
    df_filtrado = df_filtrado[
        (df_filtrado['potencia_instalada_mw'] >= potencia_min) &
        (df_filtrado['potencia_instalada_mw'] <= potencia_max)
    ]
    
    # --- Mostrar resultados ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Centrales", len(df_filtrado))
    with col2:
        st.metric("Potencia Total", f"{df_filtrado['potencia_instalada_mw'].sum():.0f} MW")
    with col3:
        st.metric("Regiones", df_filtrado['region'].nunique())
    
    # Botón para resetear filtros
    if st.button("🔄 Limpiar Filtros"):
        st.rerun()
    
    # Mostrar centrales
    if df_filtrado.empty:
        st.warning("No hay centrales con los filtros aplicados.")
    else:
        # Opción para ver como tarjetas o tabla
        vista = st.radio(
            "Vista:",
            ["Tarjetas", "Tabla"],
            horizontal=True
        )
        
        if vista == "Tarjetas":
            # Dividir en columnas para mejor visualización
            cols = st.columns(2)
            for idx, (_, row) in enumerate(df_filtrado.iterrows()):
                with cols[idx % 2]:
                    with st.container(border=True):
                        st.subheader(f"🏭 {row['agente_descripcion']}")
                        st.markdown(f"""
                        **Ubicación**: {row['region']}
                        **Tecnología**: {row['tecnologia']}
                        **Fuente**: {row['fuente_generacion']}
                        **Potencia Instalada**: {row['potencia_instalada_mw']:.0f} MW
                        **Central**: {row['central']}
                        """)
        else:
            # Vista de tabla
            columnas_mostrar = [
                'agente_descripcion', 'region', 'tecnologia', 
                'fuente_generacion', 'potencia_instalada_mw', 'central'
            ]
            st.dataframe(
                df_filtrado[columnas_mostrar].rename(columns={
                    'agente_descripcion': 'Agente',
                    'region': 'Región',
                    'tecnologia': 'Tecnología',
                    'fuente_generacion': 'Fuente',
                    'potencia_instalada_mw': 'Potencia (MW)',
                    'central': 'Central'
                }),
                use_container_width=True
            )

if __name__ == "__main__":
    main()