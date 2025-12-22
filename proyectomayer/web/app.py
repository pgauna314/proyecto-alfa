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
    st.title("⚛️ Análisis de Sistemas: El Generador de Vapor")
    
    # Tu texto pedagógico
    st.markdown(f"""
    > **Enfoque del Capítulo:** {st.session_state.get('intro_text', 'Analizaremos cómo los principios de balance se aplican en la generación de electricidad, para finalmente formalizar los conceptos clave.')}
    """)

    st.markdown("""
    ### 1. El Concepto de Volumen de Control
    Para entender el balance, aislamos el **Generador de Vapor** de Atucha II. 
    Lo representamos como una 'Caja Negra' donde solo nos importan los flujos que cruzan la frontera.
    """)

    # --- REPRESENTACIÓN DE LA CAJA NEGRA ---
    st.subheader("Visualización del Balance de Energía")
    
    m = 950.4    # kg/s (Caudal)
    h_in = 950   # kJ/kg (Entalpía agua)
    h_out = 2770 # kJ/kg (Entalpía vapor)
    Q = m * (h_out - h_in) / 1000 # Potencia en MW

    col1, col_box, col2 = st.columns([1, 2, 1])
    
    with col1:
        st.write("### 📥 Entra")
        st.latex(r"\dot{m} \cdot h_{ent}")
        st.metric("Energía de Entrada", f"{m*h_in/1000:.0f} MW")
        st.caption("Agua de alimentación de los precalentadores.")

    with col_box:
        # Dibujo de la Caja Negra con HTML/CSS
        st.markdown(
            f"""
            <div style="border: 3px dashed #ff4b4b; padding: 30px; text-align: center; border-radius: 15px; background-color: #fff5f5;">
                <h3 style="color: #333;">SISTEMA: GENERADOR DE VAPOR</h3>
                <hr style="border: 1px solid #ff4b4b;">
                <h2 style="color: #ff4b4b; margin: 20px 0;">Q = {Q:.1f} MWt</h2>
                <p style="font-weight: bold;">Calor transferido desde el circuito primario</p>
            </div>
            """, unsafe_allow_html=True
        )

    with col2:
        st.write("### 📤 Sale")
        st.latex(r"\dot{m} \cdot h_{sal}")
        st.metric("Energía de Salida", f"{m*h_out/1000:.0f} MW")
        st.caption("Vapor saturado hacia la turbina.")

    st.divider()
    st.markdown("""
    ### 2. Formalización Matemática
    Como se observa arriba, la energía no desaparece. Para un sistema abierto en estado estacionario:
    """)
    st.latex(r"\dot{Q} - \dot{W} = \dot{m} \cdot (h_{sal} - h_{ent})")
    st.write("En este equipo no hay trabajo ($W=0$), por lo que todo el cambio de entalpía se debe al calor ($Q$) aportado por el reactor.")

elif menu == "Observatorio de Datos":
    st.title("🔭 Observatorio de Datos")
    st.write("Visualización de parámetros históricos de Atucha II.")
    # Aquí podrías poner un gráfico más adelante
    st.bar_chart([745, 740, 745, 730, 745])



