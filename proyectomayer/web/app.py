import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Proyecto MAYER", layout="wide", page_icon="🏗️")

# 2. Barra Lateral (Navegación y Botones)
with st.sidebar:
    st.title("🏗️ Hola AYU")
    st.divider()
    
    # Menú de Secciones
    menu = st.radio("Secciones del Libro:", 
                    ["Inicio", "Capítulo II: Sistemas", "Observatorio de Datos"])
    
    st.divider()
    st.write("### Recursos Externos")
    
    # Botones de acceso rápido
    st.link_button("📺 Canal de YouTube", "https://youtube.com/@TuCanal")
    st.link_button("📚 Libro Completo (PDF)", "https://github.com/TuUsuario/Proyecto-Mayer/libro/main.pdf")
    
    st.divider()
    st.info("Autor: Dr. Pablo Gauna")

# 3. Panel Principal
if menu == "Inicio":
    st.title("Bienvenidos al Proyecto MAYER")
    st.markdown("""
    Este sitio es el soporte dinámico para el estudio de la termodinámica aplicada.
    Aquí transformamos las ecuaciones del libro en herramientas de cálculo reales.
    """)
    st.image("https://www.na-sa.com.ar/assets/images/centrales/atucha2_header.jpg", caption="Central Nuclear Atucha II")

elif menu == "Capítulo II: Sistemas":
    st.title("⚛️ Definición de Límites y Balances")
    
    st.markdown("""
    ### El Generador de Vapor (GV) como Volumen de Control
    Para formalizar la Primera Ley, primero debemos definir los **límites del sistema**.
    En Atucha II, el GV es un intercambiador de calor de tubos en U.
    """)

    # --- ESQUEMA DE CAÑERÍAS (SIMULADO) ---
    st.markdown("""
    <div style="background-color: #1e1e1e; color: #00ff00; padding: 20px; border-radius: 10px; font-family: 'Courier New', monospace;">
        <p> [CIRCUITO PRIMARIO: D2O] ---->( Calor Q )----> [CIRCUITO SECUNDARIO: H2O] </p>
        <p> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ^ </p>
        <p> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | </p>
        <p> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ( LÍMITE DEL SISTEMA ) </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Límites del Sistema")
        st.write("""
        Si definimos el límite **solo** en el fluido secundario:
        * Es un **sistema abierto**.
        * **No es adiabático**: Recibe energía del primario.
        * El balance es: $\dot{Q} = \dot{m} (h_{sal} - h_{ent})$
        """)
        
    with col2:
        st.subheader("2. Parámetros Reales")
        m = 950.4
        h_ent = 950   # Agua de alimentación
        h_sal = 2770  # Vapor Saturado
        st.latex(r"h_{entrada} = 950 \frac{kJ}{kg}")
        st.latex(r"h_{salida} = 2770 \frac{kJ}{kg}")

    st.divider()

    # Gráfico de Balance de Energía (Sankey o Barras)
    st.subheader("Flujo de Energía en el Generador")
    st.info("Aquí visualizamos cómo la entalpía 'crece' gracias al aporte de calor del reactor.")
    
    df_bal = pd.DataFrame({
        'Punto': ['Entrada', 'Aporte Calor (Q)', 'Salida'],
        'Energía (MW)': [m*h_ent/1000, m*(h_sal-h_ent)/1000, m*h_sal/1000]
    })
    st.bar_chart(df_bal, x='Punto', y='Energía (MW)')

    st.markdown("""
    > **Pregunta para el alumno:** Si consideráramos el sistema como el conjunto de Primario + Secundario, 
    > y aislamos el exterior del Generador de Vapor, ¿el sistema sería adiabático? 
    > **Respuesta:** Sí, y el balance sería $\sum \dot{m}h_{ent} = \sum \dot{m}h_{sal}$.
    """)

elif menu == "Observatorio de Datos":
    st.title("🔭 Observatorio de Datos")
    st.write("Visualización de parámetros históricos de Atucha II.")
    # Aquí podrías poner un gráfico más adelante
    st.bar_chart([745, 740, 745, 730, 745])




