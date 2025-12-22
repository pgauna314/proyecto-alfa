import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Proyecto MAYER", layout="wide", page_icon="⚛️")

# 2. Barra Lateral
with st.sidebar:
    st.title("🏗️ Proyecto MAYER")
    menu = st.radio("Navegación:", ["Inicio", "Capítulo II: Sistemas"])
    st.divider()
    st.link_button("📺 YouTube", "https://youtube.com")
    st.link_button("📚 Libro PDF", "https://github.com")

# 3. Contenido Principal
if menu == "Inicio":
    st.title("Estudio de Sistemas Térmicos")
    st.write("Bienvenido a la plataforma interactiva del Proyecto MAYER.")

elif menu == "Capítulo II: Sistemas":
    st.title("⚛️ Capítulo II: Análisis de Sistemas y Balances")
    
    st.markdown("""
    En esta sección analizamos el **Generador de Vapor (GV)** de Atucha II. 
    Para aplicar la Primera Ley, es crucial definir si nuestro sistema es el fluido, 
    el equipo, o el conjunto de circuitos.
    """)

    # --- DEFINICIÓN VISUAL DEL SISTEMA ---
    st.subheader("Configuración del Volumen de Control")
    
    # Creamos un esquema más limpio con columnas y bordes
    c1, c2, c3 = st.columns([1, 1.5, 1])
    
    with c1:
        st.markdown("### 🔵 Primario\n**Agua Pesada ($D_2O$)**")
        st.caption("Proviene del Reactor")
        st.latex(r"T \approx 312 °C")
        st.write("---")
        st.write("⬅️ Retorno al Reactor")

    with c2:
        # Representación estética del intercambiador
        st.markdown(
            """
            <div style="border: 2px solid #555; background-color: #f0f2f6; padding: 20px; border-radius: 15px; text-align: center;">
                <b style="color: #ff4b4b;">LÍMITE DEL SISTEMA (VC)</b><br>
                <small>Interfase de los tubos en U</small>
                <div style="margin: 20px; border: 2px dashed #ff4b4b; padding: 10px;">
                    <h3 style="margin:0;">GENERADOR DE VAPOR</h3>
                    <p style="font-size: 20px;">$\dot{Q}$</p>
                </div>
                <p>Transferencia de calor por conducción y convección</p>
            </div>
            """, unsafe_allow_html=True
        )

    with c3:
        st.markdown("### ⚪ Secundario\n**Agua Leve ($H_2O$)**")
        st.caption("Hacia la Turbina")
        st.latex(r"P = 56.1 \text{ bar}")
        st.write("---")
        st.write("⬅️ Agua de Alimentación")

    st.divider()

    # --- BALANCE DE ENERGÍA ---
    st.subheader("Balance de Energía en Estado Estacionario")
    
    # Datos técnicos
    m = 950.4    # kg/s
    h_ent = 950   # kJ/kg
    h_sal = 2770  # kJ/kg
    Q_mw = m * (h_sal - h_ent) / 1000

    st.write("Considerando el **fluido secundario** como nuestro sistema:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.latex(r"\dot{Q} = \dot{m} \cdot (h_{salida} - h_{entrada})")
        st.write(f"Sustituyendo con valores de diseño de Atucha II:")
        st.success(f"$\dot{{Q}} = {m} \, kg/s \cdot ({h_sal} - {h_ent}) \, kJ/kg = {Q_mw:.1f} \, MW_t$")
    
    with col_b:
        st.info("""
        **Nota Pedagógica:** El sistema NO es adiabático porque el límite corta 
        la interfase de los tubos, permitiendo el flujo de calor $\dot{Q}$ desde 
        el circuito primario.
        """)

    # Tabla de Balance de Materia
    st.subheader("Balance de Masa")
    df_masa = pd.DataFrame({
        "Flujo": ["Entrada (Alimentación)", "Salida (Vapor)"],
        "Caudal Másico [kg/s]": [m, m],
        "Estado": ["Líquido Subenfriado", "Vapor Saturado"]
    })
    st.table(df_masa)




