import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Proyecto TERMODDINAMICA", layout="wide")

# Título Principal
st.title("🏗️ Proyecto TERMO")
st.subheader("Sistema Integral de Aprendizaje de Termodinámica")

# Barra lateral para navegar
st.sidebar.header("Navegación")
seccion = st.sidebar.radio("Ir a:", ["Estado del Proyecto", "Capítulo 2: Atucha II", "Observatorio"])

if seccion == "Estado del Proyecto":
    st.info("Bienvenido, Pablo. Este es el entorno de pre-lanzamiento para el Sistema Mayer.")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Avance Editorial")
        st.progress(15) # Esto lo vas subiendo vos
    with col2:
        st.write("### Avance del Simulador")
        st.progress(5)

elif seccion == "Capítulo 2: Atucha II":
    st.header("Capítulo 2: Conceptos Fundamentales")
    st.write("En este capítulo usamos **Atucha II** como sistema para entender balances de masa y energía.")
    
    st.markdown("---")
    st.write("#### 🛠️ Herramientas del Capítulo")
    if st.button("Ver Borrador PDF (LaTeX)"):
        st.write("Aquí se abrirá el link al PDF que subas a la carpeta /libro")
    
    # Un pequeño prototipo del calculador
    st.write("#### 🧮 Simulador de Balance (Prototipo)")
    caudal = st.number_input("Introduzca Caudal Másico (kg/s)", value=950)
    st.write(f"En estado estacionario, el balance de materia para Atucha II indica que salen {caudal} kg/s.")

elif seccion == "Observatorio":
    st.header("🔎 Observatorio Energético")
    st.write("Fichas técnicas de activos reales.")
    st.success("Ficha A.1: Central Nuclear Atucha II - DISPONIBLE")
    st.table({
        "Parámetro": ["Tipo de Reactor", "Potencia Neta", "Presión de Vapor"],
        "Valor": ["PHWR", "745 MW", "56 bar"]
    })