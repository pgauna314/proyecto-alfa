import streamlit as st

# 1. Configuración (Siempre arriba de todo)
st.set_page_config(page_title="Proyecto MAYER", layout="wide")

# 2. Barra Lateral
st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Seleccione una sección:", ["Inicio", "Capítulo II"])

# 3. Panel Principal (Esto es lo que se estaba borrando)
if opcion == "Inicio":
    st.title("🏗️ Proyecto MAYER")
    st.write("Bienvenido al sistema interactivo de ingeniería.")
    st.info("Seleccioná 'Capítulo II' en el menú de la izquierda para ver el contenido.")

elif opcion == "Capítulo II":
    st.title("⚛️ Capítulo II: Sistemas y Balances")
    
    st.markdown("""
    En este capítulo, abordaremos los conceptos fundamentales de **sistema, balance de materia 
    y balance de energía**, aplicándolos al funcionamiento de una central térmica.
    """)
    
    st.subheader("Análisis de Atucha II")
    col1, col2 = st.columns(2)
    with col1:
        caudal = st.number_input("Caudal másico (kg/s)", value=950.4)
    with col2:
        st.write("Cálculo de Balance en tiempo real:")
        st.metric("Potencia Estimada", f"{caudal * 0.8:.1f} MW")
