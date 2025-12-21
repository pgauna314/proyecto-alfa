import streamlit as st

st.set_page_config(page_title="Proyecto MAYER - Cap II", layout="wide")

# Barra lateral
with st.sidebar:
    st.title("Proyecto MAYER")
    st.markdown("### Capítulo II\n**Sistemas y Balances**")
    st.divider()
    st.info("Analizando la generación de electricidad para formalizar la termodinámica.")

# Cuerpo principal
st.title("Capítulo II: De la Central a la Teoría")

st.markdown("""
### 1. La Central Térmica como Sistema
Antes de ir a las definiciones abstractas, observemos nuestra unidad de estudio: **Atucha II**. 
En ingeniería, definimos un **Sistema** como una porción del universo que aislamos para su análisis.
""")

# Simulación de Balance de Masa y Energía
st.subheader("2. Análisis de Balance en el Generador de Vapor")

col1, col2 = st.columns([1, 1])

with col1:
    st.write("**Entradas y Salidas (Volumen de Control)**")
    # Datos reales para que el alumno juegue con el balance
    m_punto = st.number_input("Caudal másico (kg/s)", value=950.4)
    h_entrada = st.number_input("Entalpía de entrada (kJ/kg)", value=950.0)
    h_salida = st.number_input("Entalpía de salida (kJ/kg)", value=2770.0)

with col2:
    # Ecuación de Balance de Energía Simplificada
    # Q = m * (h_salida - h_entrada)
    potencia_termica = m_punto * (h_salida - h_entrada) / 1000 # Resultado en MW
    
    st.metric("Transferencia de Calor (Q)", f"{potencia_termica:.2f} MWt")
    st.caption("Este cálculo representa el calor entregado por el reactor al ciclo secundario.")

st.divider()

st.markdown("""
### 3. Hacia la Formalización
A partir del ejemplo anterior, podemos definir:
* **Masa ($\dot{m}$):** Se conserva (Balance de materia).
* **Energía ($Q, W$):** Se transforma (Balance de energía).
* **Sistema Abierto:** Atucha II intercambia materia y energía con su entorno.
""")

# Botón para descargar el texto que me pasaste
st.download_button("Descargar Borrador Texto Cap. II", 
                   "En este capítulo, abordaremos los conceptos fundamentales...", 
                   "Capitulo_II_Intro.txt")
