# modules/wiki.py
import streamlit as st
import pandas as pd
import os

def main():
    st.set_page_config(page_title="Wiki Energética", layout="wide")
    
    # --- Cargar datos ---
    ruta_csv = os.path.join(os.path.dirname(__file__), "..", "..", "data", "potencia-instalada.csv")
    if not os.path.exists(ruta_csv):
        st.error("❌ No se encontró `data/potencia-instalada.csv`.")
        return
    
    @st.cache_data
    def cargar_datos():
        df = pd.read_csv(ruta_csv)
        df['fecha_proceso'] = pd.to_datetime(df['fecha_proceso'], errors='coerce')
        df = df.sort_values('fecha_proceso').drop_duplicates(subset=['central'], keep='last')
        df = df.dropna(subset=['region', 'tecnologia', 'fuente_generacion'])
        return df
    
    df = cargar_datos()
    
    # --- Sidebar con filtros ---
    st.sidebar.header("🔍 Filtros")
    
    # Obtener opciones únicas para los filtros
    regiones_opciones = sorted(df['region'].dropna().unique().tolist())
    tecnologias_opciones = sorted(df['tecnologia'].dropna().unique().tolist())
    fuentes_opciones = sorted(df['fuente_generacion'].dropna().unique().tolist())
    
    # Filtro de región (con opción "Todas")
    region_seleccionada = st.sidebar.selectbox(
        "Seleccionar Región",
        options=["Todas"] + regiones_opciones,
        index=0
    )
    
    # Filtro de tecnología (con opción "Todas")
    tecnologia_seleccionada = st.sidebar.selectbox(
        "Seleccionar Tecnología",
        options=["Todas"] + tecnologias_opciones,
        index=0
    )
    
    # Filtro de fuente/tipo (con opción "Todas")
    fuente_seleccionada = st.sidebar.selectbox(
        "Seleccionar Fuente/Tipo",
        options=["Todas"] + fuentes_opciones,
        index=0
    )
    
    # Filtro adicional por potencia (opcional)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filtros Avanzados")
    
    potencia_min = st.sidebar.slider(
        "Potencia Mínima (MW)",
        min_value=0,
        max_value=int(df['potencia_instalada_mw'].max()),
        value=0,
        step=10
    )
    
    # --- Contenido principal ---
    st.title("📚 Wiki Energética")
    st.markdown("Explorá centrales eléctricas reales de Argentina.")
    
    # --- Aplicar filtros ---
    df_filtrado = df.copy()
    
    # Aplicar filtros uno por uno
    if region_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['region'] == region_seleccionada]
    
    if tecnologia_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['tecnologia'] == tecnologia_seleccionada]
    
    if fuente_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['fuente_generacion'] == fuente_seleccionada]
    
    # Aplicar filtro de potencia
    df_filtrado = df_filtrado[df_filtrado['potencia_instalada_mw'] >= potencia_min]
    
    # --- Mostrar estadísticas ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Centrales encontradas", len(df_filtrado))
    with col2:
        st.metric("Potencia total", f"{df_filtrado['potencia_instalada_mw'].sum():.0f} MW")
    with col3:
        st.metric("Potencia promedio", f"{df_filtrado['potencia_instalada_mw'].mean():.0f} MW")
    
    # Mostrar filtros aplicados
    filtros_activos = []
    if region_seleccionada != "Todas":
        filtros_activos.append(f"**Región**: {region_seleccionada}")
    if tecnologia_seleccionada != "Todas":
        filtros_activos.append(f"**Tecnología**: {tecnologia_seleccionada}")
    if fuente_seleccionada != "Todas":
        filtros_activos.append(f"**Fuente**: {fuente_seleccionada}")
    if potencia_min > 0:
        filtros_activos.append(f"**Potencia mínima**: {potencia_min} MW")
    
    if filtros_activos:
        st.info(" | ".join(filtros_activos))
    
    # Botón para limpiar filtros
    if st.button("🧹 Limpiar todos los filtros"):
        st.rerun()
    
    # --- Mostrar resultados ---
    if df_filtrado.empty:
        st.warning("⚠️ No se encontraron centrales con los filtros seleccionados.")
        st.markdown("""
        **Sugerencias:**
        - Intenta seleccionar menos filtros
        - Reduce el valor de potencia mínima
        - Verifica que los filtros no sean contradictorios
        """)
        
        # Mostrar algunas estadísticas para ayudar
        st.subheader("📊 Distribución general de datos")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**Regiones disponibles:**")
            st.write(", ".join(regiones_opciones[:5]) + ("..." if len(regiones_opciones) > 5 else ""))
        with col2:
            st.write("**Tecnologías disponibles:**")
            st.write(", ".join(tecnologias_opciones[:5]) + ("..." if len(tecnologias_opciones) > 5 else ""))
        with col3:
            st.write("**Fuentes disponibles:**")
            st.write(", ".join(fuentes_opciones[:5]) + ("..." if len(fuentes_opciones) > 5 else ""))
    else:
        # Selección de vista
        vista = st.radio(
            "Seleccionar vista:",
            ["Tarjetas", "Tabla", "Resumen"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if vista == "Tarjetas":
            # Mostrar en tarjetas organizadas en columnas
            columnas = st.columns(2)
            for i, (_, fila) in enumerate(df_filtrado.iterrows()):
                with columnas[i % 2]:
                    with st.container(border=True):
                        st.subheader(f"🏭 {fila['agente_descripcion']}")
                        st.markdown(f"""
                        **Región**: {fila['region']}  
                        **Tecnología**: {fila['tecnologia']}  
                        **Fuente**: {fila['fuente_generacion']}  
                        **Potencia instalada**: **{fila['potencia_instalada_mw']:.0f} MW**  
                        **Central**: {fila['central']}
                        """)
                        if st.button("📋 Ver detalles", key=f"det_{i}"):
                            st.json(fila.to_dict())
        
        elif vista == "Tabla":
            # Mostrar tabla con opciones
            columnas_seleccionadas = st.multiselect(
                "Seleccionar columnas para mostrar:",
                options=df_filtrado.columns.tolist(),
                default=['agente_descripcion', 'region', 'tecnologia', 
                        'fuente_generacion', 'potencia_instalada_mw', 'central']
            )
            
            st.dataframe(
                df_filtrado[columnas_seleccionadas],
                use_container_width=True,
                hide_index=True
            )
            
            # Opción para descargar los datos filtrados
            csv = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar datos filtrados (CSV)",
                data=csv,
                file_name=f"centrales_filtradas_{region_seleccionada}_{tecnologia_seleccionada}.csv",
                mime="text/csv"
            )
        
        else:  # Vista Resumen
            st.subheader("📈 Resumen estadístico")
            
            # Mostrar distribución por categorías
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Distribución por Región**")
                region_counts = df_filtrado['region'].value_counts()
                st.dataframe(region_counts)
            
            with col2:
                st.markdown("**Distribución por Tecnología**")
                tech_counts = df_filtrado['tecnologia'].value_counts()
                st.dataframe(tech_counts)
            
            with col3:
                st.markdown("**Distribución por Fuente**")
                fuente_counts = df_filtrado['fuente_generacion'].value_counts()
                st.dataframe(fuente_counts)
            
            # Gráfico de potencias
            st.subheader("📊 Distribución de Potencias")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Potencia máxima", f"{df_filtrado['potencia_instalada_mw'].max():.0f} MW")
                st.metric("Potencia mínima", f"{df_filtrado['potencia_instalada_mw'].min():.0f} MW")
            
            with col2:
                st.metric("Mediana", f"{df_filtrado['potencia_instalada_mw'].median():.0f} MW")
                st.metric("Desvío estándar", f"{df_filtrado['potencia_instalada_mw'].std():.0f} MW")

if __name__ == "__main__":
    main()