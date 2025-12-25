# modules/wiki.py
import streamlit as st
import pandas as pd
import os

def main():
    st.sidebar.header("🔍 Filtros Combinados")
    
    # Cargar datos
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
    tecnologias = ["Todas"] + sorted(df['tecnologia'].unique().tolist())
    fuentes = ["Todas"] + sorted(df['fuente_generacion'].unique().tolist())
    
    # Filtros individuales
    region_sel = st.sidebar.selectbox("Región", regiones)
    tecnologia_sel = st.sidebar.selectbox("Tecnología", tecnologias)
    fuente_sel = st.sidebar.selectbox("Tipo/Fuente", fuentes)
    
    # --- Contenido principal ---
    st.title("📚 Wiki Energética")
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    filtros_aplicados = []
    if region_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['region'] == region_sel]
        filtros_aplicados.append(f"Región: {region_sel}")
    
    if tecnologia_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['tecnologia'] == tecnologia_sel]
        filtros_aplicados.append(f"Tecnología: {tecnologia_sel}")
    
    if fuente_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['fuente_generacion'] == fuente_sel]
        filtros_aplicados.append(f"Fuente: {fuente_sel}")
    
    # Mostrar filtros aplicados
    if filtros_aplicados:
        st.write("**Filtros aplicados:**", " | ".join(filtros_aplicados))
    
    # Mostrar resultados
    if df_filtrado.empty:
        st.warning("No hay centrales con los filtros seleccionados.")
        st.info("💡 Prueba con combinaciones diferentes de filtros")
    else:
        st.success(f"✅ Se encontraron {len(df_filtrado)} centrales")
        
        # Agrupar por alguna categoría si hay muchos resultados
        if len(df_filtrado) > 10:
            grupo = st.selectbox(
                "Agrupar por:",
                ["Ninguno", "Región", "Tecnología", "Fuente"]
            )
            
            if grupo != "Ninguno":
                for valor, grupo_df in df_filtrado.groupby(grupo.lower()):
                    st.subheader(f"{grupo}: {valor}")
                    for _, row in grupo_df.iterrows():
                        with st.container(border=True):
                            cols = st.columns([3, 1])
                            with cols[0]:
                                st.write(f"**{row['agente_descripcion']}**")
                                st.write(f"{row['central']}")
                            with cols[1]:
                                st.metric("Potencia", f"{row['potencia_instalada_mw']:.0f} MW")
            else:
                mostrar_centrales(df_filtrado)
        else:
            mostrar_centrales(df_filtrado)

def mostrar_centrales(df):
    """Función auxiliar para mostrar las centrales"""
    for _, row in df.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(row['agente_descripcion'])
                st.markdown(f"""
                **Región**: {row['region']}  
                **Tecnología**: {row['tecnologia']}  
                **Fuente**: {row['fuente_generacion']}  
                **Central**: {row['central']}
                """)
            with col2:
                st.metric("Potencia Instalada", f"{row['potencia_instalada_mw']:.0f} MW")

if __name__ == "__main__":
    main()