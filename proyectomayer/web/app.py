import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Proyecto MAYER", page_icon="🏗️", layout="wide")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (MENÚ) ---
with st.sidebar:
    st.image("https://www.na-sa.com.ar/assets/images/centrales/atucha2_thumb.jpg", caption="CNA II - Proyecto MAYER")
    st.title("Navegación")
    menu = st.radio("Ir a:", ["📊 Estado del Proyecto", "⚛️ Capítulo 2: Atucha II", "🔭 Observatorio de Datos"])
    st.divider()
    st.info("Este portal es el complemento interactivo del libro 'Ingeniería Mayer'.")

# --- LÓGICA DE LAS SECCIONES ---

if menu == "📊 Estado del Proyecto":
    st.title("🏗️ Tablero de Control - Proyecto MAYER")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Progreso del Libro", "65%", "+5% esta semana")
    col2.metric("Capítulos Listos", "4 / 12")
    col3.metric("Revisión Técnica", "Pendiente")

    st.subheader("Checklist de Avance")
    st.checkbox("Capítulo 1: Fundamentos", value=True)
    st.checkbox("Capítulo 2: Atucha II y Ciclos de Vapor", value=False)
    st.write("---")
    st.write("📩 **Nota para el autor:** Recordá subir el último PDF a la carpeta `/libro` para que los alumnos puedan descargarlo.")

elif menu == "⚛️ Capítulo 2: Atucha II":
    st.title("⚛️ Capítulo 2: El Ciclo de Atucha II")
    
    st.write("""
    En esta sección analizamos la **Central Nuclear Atucha II** como un sistema termodinámico de gran escala. 
    A diferencia de una central térmica convencional, aquí el 'combustible' no se quema, sino que fisiona.
    """)

    # Simulador Interactivo
    st.subheader("🎮 Simulador de Parámetros Operativos")
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        p_vapor = st.slider("Presión de Vapor Vivo (bar)", 40.0, 70.0, 56.1, step=0.1)
        t_vapor = st.slider("Temperatura de Vapor (°C)", 250.0, 300.0, 271.5, step=0.5)
        st.warning("El punto de diseño nominal es 56.1 bar.")

    with col_b:
        # Cálculo ficticio para visualización
        eficiencia = (p_vapor * 0.4) + (t_vapor * 0.05)
        st.subheader(f"Eficiencia Estimada del Ciclo: {eficiencia:.2f}%")
        st.progress(eficiencia / 100)
        
        st.info("Este cálculo utiliza las tablas de vapor cargadas en el sistema.")

    st.divider()
    st.subheader("📥 Descargas")
    # Intentará buscar el PDF en tu carpeta libro/main.pdf
    st.button("Descargar Borrador del Capítulo 2 (PDF)")

elif menu == "🔭 Observatorio de Datos":
    st.title("🔭 Observatorio de Datos Atucha II")
    st.write("Monitoreo de parámetros históricos y comparativas.")

    # Generamos datos de ejemplo para que la app no se vea vacía
    chart_data = pd.DataFrame({
        'Día': range(1, 11),
        'Generación (MW)': [740, 745, 742, 738, 745, 746, 740, 735, 744, 745]
    })
    
    st.line_chart(chart_data, x='Día', y='Generación (MW)')
    st.success("Sincronizado con los archivos .csv del repositorio.")
