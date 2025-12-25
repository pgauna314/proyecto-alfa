# modules/wiki.py
import streamlit as st
import pandas as pd
import os
import re

def normalizar_texto(texto):
    """Normaliza texto: quita acentos, convierte a mayúsculas, etc."""
    if pd.isna(texto):
        return ""
    
    texto = str(texto).strip()
    
    # Reemplazar acentos y caracteres especiales
    reemplazos = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'á': 'A', 'é': 'E', 'í': 'I', 'ó': 'O', 'ú': 'U',
        'Ñ': 'N', 'ñ': 'N'
    }
    for orig, repl in reemplazos.items():
        texto = texto.replace(orig, repl)
    
    # Convertir a mayúsculas y quitar espacios extra
    texto = texto.upper()
    texto = re.sub(r'\s+', ' ', texto)  # Múltiples espacios a uno solo
    
    return texto

def encontrar_columna_similar(df, nombres_posibles):
    """Busca columnas similares a las esperadas"""
    columnas_df = [col.lower().strip() for col in df.columns]
    
    for nombre_buscado in nombres_posibles:
        nombre_buscado = nombre_buscado.lower().strip()
        
        # Búsqueda exacta
        if nombre_buscado in columnas_df:
            idx = columnas_df.index(nombre_buscado)
            return df.columns[idx]
        
        # Búsqueda parcial
        for col in df.columns:
            col_lower = col.lower()
            if (nombre_buscado in col_lower or 
                col_lower in nombre_buscado or
                nombre_buscado.replace('_', '') in col_lower.replace('_', '')):
                return col
    
    return None

def main():
    st.set_page_config(page_title="Wiki Energética", layout="wide")
    
    # --- Cargar datos con detección inteligente ---
    ruta_csv = os.path.join(os.path.dirname(__file__), "..", "..", "data", "potencia-instalada.csv")
    if not os.path.exists(ruta_csv):
        st.error("❌ No se encontró `data/potencia-instalada.csv`.")
        return
    
    @st.cache_data
    def cargar_y_normalizar_datos():
        try:
            # Intentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'ISO-8859-1', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(ruta_csv, encoding=encoding)
                    st.success(f"✅ CSV cargado con encoding: {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                st.error("❌ No se pudo leer el CSV con ningún encoding común")
                return pd.DataFrame()
            
            # Panel de diagnóstico
            with st.expander("🔧 Panel de Diagnóstico", expanded=False):
                tab1, tab2, tab3, tab4 = st.tabs(["Columnas", "Muestra", "Estadísticas", "Problemas"])
                
                with tab1:
                    st.write("**Columnas encontradas:**")
                    for i, col in enumerate(df.columns, 1):
                        st.write(f"{i}. `{col}` (tipo: {df[col].dtype}, nulos: {df[col].isna().sum()})")
                
                with tab2:
                    st.write("**Primeras 5 filas:**")
                    st.dataframe(df.head())
                
                with tab3:
                    st.write("**Resumen estadístico:**")
                    st.write(df.describe(include='all'))
                
                with tab4:
                    # Buscar problemas comunes
                    problemas = []
                    for col in df.columns:
                        nulos = df[col].isna().sum()
                        if nulos > 0:
                            problemas.append(f"Columna '{col}': {nulos} valores nulos ({nulos/len(df)*100:.1f}%)")
                    
                    if problemas:
                        st.warning("Problemas encontrados:")
                        for p in problemas:
                            st.write(f"- {p}")
                    else:
                        st.success("✅ No se encontraron problemas graves")
            
            # Mapeo inteligente de columnas
            mapeo_columnas = {
                'REGION': ['region', 'región', 'provincia', 'zona', 'area', 'location'],
                'TECNOLOGIA': ['tecnologia', 'tipo', 'tech', 'generacion', 'generación'],
                'FUENTE': ['fuente', 'fuente_generacion', 'origen', 'tipo_fuente', 'combustible'],
                'POTENCIA': ['potencia', 'potencia_mw', 'mw', 'capacidad', 'potencia_instalada'],
                'CENTRAL': ['central', 'nombre', 'planta', 'estacion', 'unidad'],
                'AGENTE': ['agente', 'empresa', 'operador', 'propietario', 'dueno']
            }
            
            # Crear nuevo DataFrame normalizado
            df_norm = pd.DataFrame()
            columna_mapeada = {}
            
            for col_std, posibles in mapeo_columnas.items():
                col_encontrada = encontrar_columna_similar(df, posibles)
                if col_encontrada:
                    df_norm[col_std] = df[col_encontrada]
                    columna_mapeada[col_std] = col_encontrada
                else:
                    st.warning(f"⚠️ No se encontró columna para: {col_std}")
            
            # Mostrar mapeo realizado
            if columna_mapeada:
                st.info("**Mapeo de columnas detectado:**")
                for std, original in columna_mapeada.items():
                    st.write(f"  {std} ← {original}")
            
            # Validar que tenemos las columnas mínimas
            columnas_minimas = ['REGION', 'TECNOLOGIA', 'FUENTE', 'POTENCIA']
            faltan = [col for col in columnas_minimas if col not in df_norm.columns]
            
            if faltan:
                st.error(f"❌ Faltan columnas esenciales: {faltan}")
                st.stop()
            
            # Normalizar valores de texto
            for col in ['REGION', 'TECNOLOGIA', 'FUENTE', 'CENTRAL', 'AGENTE']:
                if col in df_norm.columns:
                    df_norm[col] = df_norm[col].apply(normalizar_texto)
            
            # Normalizar potencia (convertir a numérico)
            if 'POTENCIA' in df_norm.columns:
                # Intentar extraer números del texto
                def extraer_potencia(valor):
                    if pd.isna(valor):
                        return 0
                    
                    valor_str = str(valor)
                    # Buscar números con decimales
                    numeros = re.findall(r'\d+\.?\d*', valor_str)
                    if numeros:
                        return float(numeros[0])
                    return 0
                
                df_norm['POTENCIA'] = df_norm['POTENCIA'].apply(extraer_potencia)
                df_norm = df_norm[df_norm['POTENCIA'] > 0]  # Filtrar potencias válidas
            
            # Agrupar valores similares
            if 'TECNOLOGIA' in df_norm.columns:
                grupos_tecnologia = {
                    'HIDRO': ['HIDRO', 'HIDRAULICA', 'HIDROELECTRICA'],
                    'TERMICA': ['TERMICA', 'TERMO', 'CARBON', 'GAS', 'COMBUSTIBLE'],
                    'EOLICA': ['EOLICA', 'VIENTO', 'WIND'],
                    'SOLAR': ['SOLAR', 'FOTOVOLTAICA', 'PV'],
                    'NUCLEAR': ['NUCLEAR', 'ATOMICA'],
                    'BIOMASA': ['BIOMASA', 'BIOGAS', 'BIOCOMBUSTIBLE']
                }
                
                def clasificar_tecnologia(texto):
                    texto = texto.upper()
                    for grupo, palabras in grupos_tecnologia.items():
                        for palabra in palabras:
                            if palabra in texto:
                                return grupo
                    return texto
                
                df_norm['TECNOLOGIA_GRUPO'] = df_norm['TECNOLOGIA'].apply(clasificar_tecnologia)
            
            return df_norm
            
        except Exception as e:
            st.error(f"❌ Error crítico: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return pd.DataFrame()
    
    # Cargar datos
    df = cargar_y_normalizar_datos()
    
    if df.empty:
        st.error("No se pudieron cargar los datos. Verifica el archivo CSV.")
        return
    
    # --- Interfaz de usuario mejorada ---
    st.title("🏭 Centrales Eléctricas de Argentina")
    
    # Mostrar estadísticas rápidas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Centrales", len(df))
    with col2:
        st.metric("Potencia Total", f"{df['POTENCIA'].sum():.0f} MW")
    with col3:
        st.metric("Regiones Únicas", df['REGION'].nunique())
    with col4:
        st.metric("Tecnologías", df['TECNOLOGIA'].nunique())
    
    # --- FILTROS EN LA PÁGINA ---
    st.markdown("---")
    st.subheader("🔍 Filtros de Búsqueda")
    
    # Crear filtros basados en los datos normalizados
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        regiones = ["TODAS"] + sorted(df['REGION'].dropna().unique().tolist())
        region_sel = st.selectbox("Región", regiones, help="Filtrar por región geográfica")
    
    with col_f2:
        tecnologias = ["TODAS"] + sorted(df['TECNOLOGIA'].dropna().unique().tolist())
        tech_sel = st.selectbox("Tecnología", tecnologias, help="Filtrar por tipo de tecnología")
    
    with col_f3:
        fuentes = ["TODAS"] + sorted(df['FUENTE'].dropna().unique().tolist())
        fuente_sel = st.selectbox("Fuente", fuentes, help="Filtrar por fuente de generación")
    
    # Filtro de potencia con slider
    st.markdown("---")
    potencia_min, potencia_max = st.slider(
        "Rango de Potencia (MW)",
        min_value=0,
        max_value=int(df['POTENCIA'].max()),
        value=(0, int(df['POTENCIA'].max())),
        step=10
    )
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if region_sel != "TODAS":
        df_filtrado = df_filtrado[df_filtrado['REGION'] == region_sel]
    
    if tech_sel != "TODAS":
        df_filtrado = df_filtrado[df_filtrado['TECNOLOGIA'] == tech_sel]
    
    if fuente_sel != "TODAS":
        df_filtrado = df_filtrado[df_filtrado['FUENTE'] == fuente_sel]
    
    df_filtrado = df_filtrado[
        (df_filtrado['POTENCIA'] >= potencia_min) & 
        (df_filtrado['POTENCIA'] <= potencia_max)
    ]
    
    # Mostrar resultados
    st.markdown("---")
    st.subheader(f"📊 Resultados: {len(df_filtrado)} centrales encontradas")
    
    if len(df_filtrado) == 0:
        st.warning("No hay centrales que coincidan con los filtros seleccionados.")
    else:
        # Selector de vista
        vista = st.radio("Vista:", ["Tarjetas", "Tabla", "Resumen"], horizontal=True)
        
        if vista == "Tarjetas":
            # Mostrar tarjetas organizadas
            cols = st.columns(2)
            for i, (_, fila) in enumerate(df_filtrado.iterrows()):
                with cols[i % 2]:
                    with st.container(border=True):
                        # Icono según tecnología
                        iconos = {
                            'HIDRO': '💧',
                            'TERMICA': '🔥',
                            'EOLICA': '💨',
                            'SOLAR': '☀️',
                            'NUCLEAR': '☢️',
                            'BIOMASA': '🌿'
                        }
                        icono = iconos.get(fila.get('TECNOLOGIA_GRUPO', 'HIDRO'), '⚡')
                        
                        nombre = fila.get('CENTRAL', fila.get('AGENTE', 'Sin nombre'))
                        st.markdown(f"### {icono} {nombre[:40]}")
                        
                        info = f"""
                        **Región**: {fila.get('REGION', 'N/A')}  
                        **Tecnología**: {fila.get('TECNOLOGIA', 'N/A')}  
                        **Fuente**: {fila.get('FUENTE', 'N/A')}  
                        **Potencia**: **{fila.get('POTENCIA', 0):.0f} MW**
                        """
                        
                        if 'AGENTE' in fila and fila['AGENTE']:
                            info += f"\n**Agente**: {fila['AGENTE']}"
                        
                        st.markdown(info)
        
        elif vista == "Tabla":
            st.dataframe(
                df_filtrado,
                column_config={
                    "REGION": "Región",
                    "TECNOLOGIA": "Tecnología",
                    "FUENTE": "Fuente",
                    "POTENCIA": st.column_config.NumberColumn(
                        "Potencia (MW)",
                        format="%.0f MW"
                    ),
                    "CENTRAL": "Central",
                    "AGENTE": "Agente"
                },
                hide_index=True,
                use_container_width=True
            )
        
        else:  # Resumen
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.subheader("Distribución por Región")
                region_counts = df_filtrado['REGION'].value_counts()
                st.bar_chart(region_counts.head(10))
            
            with col_r2:
                st.subheader("Distribución por Tecnología")
                tech_counts = df_filtrado['TECNOLOGIA'].value_counts()
                st.dataframe(tech_counts)

if __name__ == "__main__":
    main()