# modules/wiki.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from modules.palettes import ENERGY_THEME

def obtener_color_por_tecnologia(tecnologia):
    tec = str(tecnologia).upper()
    if "HIDRO" in tec:
        return ENERGY_THEME["Hidraulica"]
    if "NUCLEAR" in tec:
        return ENERGY_THEME["Nuclear"]
    if "TERMO" in tec:
        return ENERGY_THEME["Termica"]
    if any(x in tec for x in ["SOLAR", "EOLICA", "RENOVABLE", "BIOMASA"]):
        return ENERGY_THEME["Renovables"]
    return "#000000"

def main():
    st.set_page_config(page_title="Wiki Energética", layout="wide")
    
    # --- Cargar datos ---
    ruta_csv = os.path.join(os.path.dirname(__file__), "..", "..", "data", "potencia-instalada.csv")
    if not os.path.exists(ruta_csv):
        st.error(f"❌ No se encontró `{ruta_csv}`.")
        return
    
    @st.cache_data
    def cargar_datos():
        df = pd.read_csv(ruta_csv)
        df['fecha_proceso'] = pd.to_datetime(df['fecha_proceso'], errors='coerce')
        df = df.sort_values('fecha_proceso').drop_duplicates(subset=['central'], keep='last')
        df = df.dropna(subset=['region', 'tecnologia', 'fuente_generacion'])
        return df
    
    df = cargar_datos()
    
    st.title("📚 Wiki Energética")
    st.markdown("Explorá centrales eléctricas reales de Argentina con identidad visual accesible.")
    
    # --- FILTROS ---
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        regiones_opciones = ["Todas"] + sorted(df['region'].unique().tolist())
        region_seleccionada = st.selectbox("Región", options=regiones_opciones)
    
    with col2:
        tecnologias_opciones = ["Todas"] + sorted(df['tecnologia'].unique().tolist())
        tecnologia_seleccionada = st.selectbox("Tecnología", options=tecnologias_opciones)
    
    with col3:
        fuentes_opciones = ["Todas"] + sorted(df['fuente_generacion'].unique().tolist())
        fuente_seleccionada = st.selectbox("Fuente/Tipo", options=fuentes_opciones)
    
    with col4:
        st.markdown(" ")
        st.markdown(" ")
        if st.button("🧹 Limpiar", use_container_width=True):
            st.rerun()
    
    with st.expander("⚙️ **Filtros Avanzados**"):
        col_adv1, col_adv2, col_adv3 = st.columns(3)
        with col_adv1:
            potencia_min = st.slider("Potencia Mínima (MW)", 0, int(df['potencia_instalada_mw'].max()), 0, 10)
        with col_adv2:
            agentes_opciones = ["Todos"] + sorted(df['agente_descripcion'].dropna().unique().tolist())
            agente_seleccionado = st.selectbox("Agente/Empresa", options=agentes_opciones)
        with col_adv3:
            busqueda_texto = st.text_input("Buscar central (nombre)", placeholder="Ej: Atucha...")

    # --- Aplicar filtros ---
    df_filtrado = df.copy()
    if region_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['region'] == region_seleccionada]
    if tecnologia_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['tecnologia'] == tecnologia_seleccionada]
    if fuente_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['fuente_generacion'] == fuente_seleccionada]
    if potencia_min > 0:
        df_filtrado = df_filtrado[df_filtrado['potencia_instalada_mw'] >= potencia_min]
    if agente_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['agente_descripcion'] == agente_seleccionado]
    if busqueda_texto:
        df_filtrado = df_filtrado[df_filtrado['central'].str.contains(busqueda_texto, case=False, na=False)]

    # --- Métricas ---
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🏭 Centrales", f"{len(df_filtrado):,}")
    m2.metric("⚡ Potencia Total", f"{df_filtrado['potencia_instalada_mw'].sum():.0f} MW")
    m3.metric("📊 Promedio", f"{df_filtrado['potencia_instalada_mw'].mean():.0f} MW" if not df_filtrado.empty else "0")
    m4.metric("🌍 Regiones", df_filtrado['region'].nunique())

    if df_filtrado.empty:
        st.warning("⚠️ No se encontraron resultados.")
        return

    # --- Vistas ---
    vista = st.radio("**Vista:**", ["Tarjetas", "Tabla", "Resumen"], horizontal=True)
    
    # Ordenamiento
    opciones_orden = ["Potencia (Desc)", "Potencia (Asc)", "Nombre A-Z"]
    orden = st.selectbox("Ordenar por:", opciones_orden)
    if "Desc" in orden:
        df_filtrado = df_filtrado.sort_values('potencia_instalada_mw', ascending=False)
    elif "Asc" in orden:
        df_filtrado = df_filtrado.sort_values('potencia_instalada_mw', ascending=True)
    else:
        df_filtrado = df_filtrado.sort_values('agente_descripcion', ascending=True)

    if vista == "Tarjetas":
        columnas = st.columns(3)
        for i, (_, fila) in enumerate(df_filtrado.iterrows()):
            color_tec = obtener_color_por_tecnologia(fila['tecnologia'])
            with columnas[i % 3]:
                with st.container(border=True, height=240):
                    st.markdown(f"""
                        <div style="border-left: 5px solid {color_tec}; padding-left: 10px;">
                            <h4 style="margin:0;">{fila['agente_descripcion'][:25]}...</h4>
                            <p style="color:{color_tec}; font-weight:bold; margin:0;">{fila['tecnologia']}</p>
                            <p style="margin:0;">Región: {fila['region']}</p>
                            <h3 style="margin:5px 0;">{fila['potencia_instalada_mw']:.0f} MW</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    with st.expander("Detalles"):
                        st.write(f"Central: {fila['central']}")

    elif vista == "Tabla":
        st.dataframe(df_filtrado[['agente_descripcion', 'region', 'tecnologia', 'potencia_instalada_mw']], use_container_width=True)

    else: # Resumen
        c_res1, c_res2 = st.columns(2)
        with c_res1:
            st.subheader("Distribución Tecnológica (MW)")
            tech_mw = df_filtrado.groupby('tecnologia')['potencia_instalada_mw'].sum()
            fig = px.bar(tech_mw, color=tech_mw.index, 
                         color_discrete_map={t: obtener_color_por_tecnologia(t) for t in tech_mw.index})
            st.plotly_chart(fig, use_container_width=True)
        with c_res2:
            st.subheader("Top 10 Centrales")
            st.table(df_filtrado.nlargest(10, 'potencia_instalada_mw')[['central', 'potencia_instalada_mw']])

if __name__ == "__main__":
    main()