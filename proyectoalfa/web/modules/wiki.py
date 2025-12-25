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
    
    # --- Encabezado principal ---
    st.title("📚 Wiki Energética")
    st.markdown("Explorá centrales eléctricas reales de Argentina.")
    
    # --- FILTROS EN LA PÁGINA PRINCIPAL ---
    st.markdown("---")
    st.subheader("🔍 Filtros de Búsqueda")
    
    # Crear 3 columnas para los filtros principales
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        # Filtro de región (con opción "Todas")
        regiones_opciones = ["Todas"] + sorted(df['region'].dropna().unique().tolist())
        region_seleccionada = st.selectbox(
            "Región",
            options=regiones_opciones,
            index=0,
            help="Selecciona una región específica o 'Todas'"
        )
    
    with col2:
        # Filtro de tecnología (con opción "Todas")
        tecnologias_opciones = ["Todas"] + sorted(df['tecnologia'].dropna().unique().tolist())
        tecnologia_seleccionada = st.selectbox(
            "Tecnología",
            options=tecnologias_opciones,
            index=0,
            help="Selecciona un tipo de tecnología o 'Todas'"
        )
    
    with col3:
        # Filtro de fuente/tipo (con opción "Todas")
        fuentes_opciones = ["Todas"] + sorted(df['fuente_generacion'].dropna().unique().tolist())
        fuente_seleccionada = st.selectbox(
            "Fuente/Tipo",
            options=fuentes_opciones,
            index=0,
            help="Selecciona una fuente de generación o 'Todas'"
        )
    
    with col4:
        # Botón para limpiar filtros
        st.markdown(" ")  # Espacio vertical
        st.markdown(" ")  # Espacio vertical
        if st.button("🧹 Limpiar", use_container_width=True):
            st.rerun()
    
    # --- Filtros avanzados en un expander ---
    with st.expander("⚙️ **Filtros Avanzados**", expanded=False):
        col_adv1, col_adv2, col_adv3 = st.columns(3)
        
        with col_adv1:
            # Filtro por potencia mínima
            potencia_min = st.slider(
                "Potencia Mínima (MW)",
                min_value=0,
                max_value=int(df['potencia_instalada_mw'].max()),
                value=0,
                step=10
            )
        
        with col_adv2:
            # Filtro por agente/empresa (opcional)
            agentes_opciones = ["Todos"] + sorted(df['agente_descripcion'].dropna().unique().tolist())
            agente_seleccionado = st.selectbox(
                "Agente/Empresa",
                options=agentes_opciones,
                index=0
            )
        
        with col_adv3:
            # Búsqueda por nombre de central
            busqueda_texto = st.text_input(
                "Buscar central (nombre)",
                placeholder="Ej: Hidroeléctrica..."
            )
    
    # --- Aplicar filtros ---
    df_filtrado = df.copy()
    
    # Aplicar filtros principales
    filtros_activos = []
    
    if region_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['region'] == region_seleccionada]
        filtros_activos.append(f"**Región**: {region_seleccionada}")
    
    if tecnologia_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['tecnologia'] == tecnologia_seleccionada]
        filtros_activos.append(f"**Tecnología**: {tecnologia_seleccionada}")
    
    if fuente_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['fuente_generacion'] == fuente_seleccionada]
        filtros_activos.append(f"**Fuente**: {fuente_seleccionada}")
    
    # Aplicar filtros avanzados
    if potencia_min > 0:
        df_filtrado = df_filtrado[df_filtrado['potencia_instalada_mw'] >= potencia_min]
        filtros_activos.append(f"**Potencia mínima**: {potencia_min} MW")
    
    if agente_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['agente_descripcion'] == agente_seleccionado]
        filtros_activos.append(f"**Agente**: {agente_seleccionado}")
    
    if busqueda_texto:
        df_filtrado = df_filtrado[df_filtrado['central'].str.contains(busqueda_texto, case=False, na=False) |
                                   df_filtrado['agente_descripcion'].str.contains(busqueda_texto, case=False, na=False)]
        filtros_activos.append(f"**Búsqueda**: '{busqueda_texto}'")
    
    # --- Mostrar resultados y estadísticas ---
    st.markdown("---")
    
    # Mostrar filtros aplicados
    if filtros_activos:
        st.info("🗂️ **Filtros activos:** " + " | ".join(filtros_activos))
    
    # Estadísticas principales
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric(
            "🏭 Centrales",
            f"{len(df_filtrado):,}",
            f"{len(df_filtrado) - len(df):,}" if len(df_filtrado) != len(df) else "0"
        )
    
    with col_stat2:
        st.metric(
            "⚡ Potencia Total",
            f"{df_filtrado['potencia_instalada_mw'].sum():.0f} MW",
            f"{df_filtrado['potencia_instalada_mw'].sum() - df['potencia_instalada_mw'].sum():.0f} MW" 
            if len(df_filtrado) != len(df) else "0 MW"
        )
    
    with col_stat3:
        potencia_promedio = df_filtrado['potencia_instalada_mw'].mean() if not df_filtrado.empty else 0
        st.metric("📊 Potencia Promedio", f"{potencia_promedio:.0f} MW")
    
    with col_stat4:
        st.metric("🌍 Regiones", df_filtrado['region'].nunique())
    
    # --- Mensaje si no hay resultados ---
    if df_filtrado.empty:
        st.warning("""
        ⚠️ **No se encontraron centrales con los filtros seleccionados.**
        
        **Sugerencias:**
        1. Intenta con filtros menos específicos
        2. Reduce la potencia mínima requerida
        3. Verifica que los filtros no sean contradictorios
        """)
        
        # Mostrar vista previa de datos disponibles
        with st.expander("📋 Ver datos disponibles para filtros"):
            col_prev1, col_prev2, col_prev3 = st.columns(3)
            
            with col_prev1:
                st.write("**Regiones disponibles:**")
                for region in sorted(df['region'].unique().tolist())[:10]:
                    st.write(f"- {region}")
                if len(df['region'].unique()) > 10:
                    st.write(f"... y {len(df['region'].unique()) - 10} más")
            
            with col_prev2:
                st.write("**Tecnologías disponibles:**")
                for tech in sorted(df['tecnologia'].unique().tolist())[:10]:
                    st.write(f"- {tech}")
                if len(df['tecnologia'].unique()) > 10:
                    st.write(f"... y {len(df['tecnologia'].unique()) - 10} más")
            
            with col_prev3:
                st.write("**Fuentes disponibles:**")
                for fuente in sorted(df['fuente_generacion'].unique().tolist())[:10]:
                    st.write(f"- {fuente}")
                if len(df['fuente_generacion'].unique()) > 10:
                    st.write(f"... y {len(df['fuente_generacion'].unique()) - 10} más")
        
        return  # Terminar la ejecución aquí
    
    # --- Selector de vista ---
    st.markdown("---")
    vista_col1, vista_col2 = st.columns([1, 3])
    
    with vista_col1:
        vista = st.radio(
            "**Seleccionar vista:**",
            ["Tarjetas", "Tabla", "Resumen"],
            horizontal=True
        )
    
    with vista_col2:
        # Opción para ordenar resultados
        opciones_orden = [
            "Potencia (Mayor a Menor)",
            "Potencia (Menor a Mayor)",
            "Nombre A-Z",
            "Nombre Z-A",
            "Región A-Z"
        ]
        orden_seleccionado = st.selectbox("Ordenar por:", opciones_orden)
        
        # Aplicar orden - CORRECCIÓN AQUÍ
        if orden_seleccionado == "Potencia (Mayor a Menor)":
            df_filtrado = df_filtrado.sort_values('potencia_instalada_mw', ascending=False)
        elif orden_seleccionado == "Potencia (Menor a Mayor)":
            df_filtrado = df_filtrado.sort_values('potencia_instalada_mw', ascending=True)
        elif orden_seleccionado == "Nombre A-Z":  # CORREGIDO: era 'orden_select'
            df_filtrado = df_filtrado.sort_values('agente_descripcion', ascending=True)
        elif orden_seleccionado == "Nombre Z-A":
            df_filtrado = df_filtrado.sort_values('agente_descripcion', ascending=False)
        elif orden_seleccionado == "Región A-Z":
            df_filtrado = df_filtrado.sort_values('region', ascending=True)
    
    # --- VISTA: TARJETAS ---
    if vista == "Tarjetas":
        st.markdown(f"### 🏭 Centrales encontradas: {len(df_filtrado)}")
        
        # Calcular número de columnas según cantidad de datos
        num_columnas = 3 if len(df_filtrado) > 5 else 2
        
        # Crear columnas dinámicas
        columnas = st.columns(num_columnas)
        
        for i, (_, fila) in enumerate(df_filtrado.iterrows()):
            with columnas[i % num_columnas]:
                with st.container(border=True, height=220):
                    # Encabezado con icono según tecnología
                    icono = "⚡"
                    if "HIDRO" in str(fila['tecnologia']).upper():
                        icono = "💧"
                    elif "TERMO" in str(fila['tecnologia']).upper():
                        icono = "🔥"
                    elif "SOLAR" in str(fila['tecnologia']).upper():
                        icono = "☀️"
                    elif "EOLICA" in str(fila['tecnologia']).upper():
                        icono = "💨"
                    
                    st.markdown(f"#### {icono} {fila['agente_descripcion'][:30]}{'...' if len(fila['agente_descripcion']) > 30 else ''}")
                    
                    st.markdown(f"""
                    **Región**: {fila['region']}  
                    **Tecnología**: {fila['tecnologia']}  
                    **Fuente**: {fila['fuente_generacion']}  
                    **Potencia**: **{fila['potencia_instalada_mw']:.0f} MW**  
                    """)
                    
                    # Botón para ver más detalles
                    with st.expander("📋 Ver detalles"):
                        st.write(f"**Central**: {fila['central']}")
                        st.write(f"**Agente**: {fila['agente_descripcion']}")
                        st.write(f"**Potencia exacta**: {fila['potencia_instalada_mw']:.2f} MW")
                        if 'fecha_proceso' in df.columns:
                            st.write(f"**Fecha actualización**: {fila['fecha_proceso'].strftime('%d/%m/%Y')}")
    
    # --- VISTA: TABLA ---
    elif vista == "Tabla":
        # Selector de columnas a mostrar
        columnas_disponibles = [
            'agente_descripcion', 'region', 'tecnologia', 
            'fuente_generacion', 'potencia_instalada_mw', 'central'
        ]
        
        columnas_seleccionadas = st.multiselect(
            "Seleccionar columnas para mostrar:",
            options=columnas_disponibles,
            default=columnas_disponibles
        )
        
        if columnas_seleccionadas:
            # Renombrar columnas para mejor visualización
            nombres_bonitos = {
                'agente_descripcion': 'Agente/Empresa',
                'region': 'Región',
                'tecnologia': 'Tecnología',
                'fuente_generacion': 'Fuente',
                'potencia_instalada_mw': 'Potencia (MW)',
                'central': 'Nombre Central'
            }
            
            df_mostrar = df_filtrado[columnas_seleccionadas].rename(columns=nombres_bonitos)
            
            # Formatear la columna de potencia si existe
            if 'Potencia (MW)' in df_mostrar.columns:
                df_mostrar['Potencia (MW)'] = df_mostrar['Potencia (MW)'].apply(lambda x: f"{x:,.0f} MW")
            
            st.dataframe(
                df_mostrar,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Opciones de descarga
            st.download_button(
                label="📥 Descargar datos filtrados (CSV)",
                data=df_filtrado[columnas_seleccionadas].to_csv(index=False).encode('utf-8'),
                file_name=f"centrales_filtradas_{len(df_filtrado)}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # --- VISTA: RESUMEN ---
    else:
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.subheader("📊 Distribución por Región")
            region_dist = df_filtrado['region'].value_counts().head(10)
            st.bar_chart(region_dist)
            
            st.subheader("🏗️ Distribución por Tecnología")
            tech_dist = df_filtrado['tecnologia'].value_counts()
            st.dataframe(tech_dist, use_container_width=True)
        
        with col_res2:
            st.subheader("⚡ Estadísticas de Potencia")
            
            col_met1, col_met2 = st.columns(2)
            with col_met1:
                st.metric("Máxima", f"{df_filtrado['potencia_instalada_mw'].max():.0f} MW")
                st.metric("Mínima", f"{df_filtrado['potencia_instalada_mw'].min():.0f} MW")
            
            with col_met2:
                st.metric("Promedio", f"{df_filtrado['potencia_instalada_mw'].mean():.0f} MW")
                st.metric("Mediana", f"{df_filtrado['potencia_instalada_mw'].median():.0f} MW")
            
            st.subheader("📈 Top 10 Centrales por Potencia")
            top_10 = df_filtrado.nlargest(10, 'potencia_instalada_mw')[['agente_descripcion', 'region', 'potencia_instalada_mw']]
            top_10.index = range(1, 11)
            st.dataframe(top_10, use_container_width=True)

if __name__ == "__main__":
    main()