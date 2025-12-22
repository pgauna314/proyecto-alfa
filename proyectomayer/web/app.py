import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(page_title="Proyecto MAYER", layout="wide", page_icon="⚛️")

# 2. Barra Lateral
with st.sidebar:
    st.title("🏗️ Proyecto MAYER")
    menu = st.radio("Navegación:", [
        "Inicio", 
        "Monitor de Generación (SADI)",
        "Capítulo II: Sistemas"
    ])
    st.divider()
    st.link_button("📺 YouTube", "https://youtube.com")
    st.link_button("📚 Libro PDF", "https://github.com")

# 3. Contenido Principal

if menu == "Inicio":
    st.title("Estudio de Sistemas Térmicos")
    st.write("Bienvenido a la plataforma interactiva del Proyecto MAYER.")

# --- NUEVA SECCIÓN: MONITOR DE GENERACIÓN ---
elif menu == "Monitor de Generación (SADI)":
    st.title("⚡ Generación de Potencia en Tiempo Real")
    st.markdown("""
    Análisis de la matriz energética argentina según datos de **CAMMESA**. 
    Este gráfico utiliza una paleta optimizada para daltonismo para garantizar la legibilidad.
    """)

    # Datos representativos de la matriz argentina (en MW)
    # Paleta para daltónicos (Okabe-Ito): 
    # Naranja: #E69F00, AzulCielo: #56B4E9, VerdeAzulado: #009E73, Amarillo: #F0E442, Azul: #0072B2, Vermillion: #D55E00
    data = {
        'Fuente': ['Térmica (Gas/Fuel)', 'Hidráulica', 'Nuclear', 'Eólica', 'Solar', 'Otras'],
        'Potencia [MW]': [11800, 4500, 1650, 3200, 950, 400],
        'Color': ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00']
    }
    df = pd.DataFrame(data)

    col1, col2 = st.columns([1.5, 1])

    with col1:
        # Gráfico de Torta con Plotly
        fig = px.pie(
            df, 
            values='Potencia [MW]', 
            names='Fuente',
            color='Fuente',
            color_discrete_map={
                'Térmica (Gas/Fuel)': '#E69F00',
                'Hidráulica': '#56B4E9',
                'Nuclear': '#009E73',
                'Eólica': '#F0E442',
                'Solar': '#0072B2',
                'Otras': '#D55E00'
            },
            hole=0.4
        )
        # Ajustes de diseño del gráfico
        fig.update_traces(textinfo='percent+label', hovertemplate='%{label}<br>%{value} MW')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Resumen de Capacidad")
        total = df['Potencia [MW]'].sum()
        st.metric("Demanda Total Estimada", f"{total} MW")
        
        # Mostrar tabla limpia con los datos
        st.dataframe(
            df[['Fuente', 'Potencia [MW]']], 
            hide_index=True, 
            use_container_width=True
        )
        
        st.warning("⚠️ Nota: Los datos mostrados son valores medios de referencia para la temporada actual.")

# --- SECCIÓN: CAPÍTULO II (Se mantiene igual) ---
elif menu == "Capítulo II: Sistemas":
    st.title("⚛️ Capítulo II: Análisis de Sistemas")
    st.info("Aquí continuaremos con el análisis del Generador de Vapor y Atucha II.")
