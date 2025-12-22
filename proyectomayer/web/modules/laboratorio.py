import streamlit as st
from CoolProp.CoolProp import PropsSI
import plotly.graph_objects as go
import numpy as np

def mostrar_laboratorio():
    st.title("🧪 Laboratorio de Diagnóstico Termodinámico")
    
    # --- PANEL DE CONTROL ---
    with st.sidebar:
        st.header("Configuración")
        tipo_grafico = st.selectbox("Eje del gráfico:", ["T-s (Temperatura-Entropía)", "P-v (Presión-Volumen)"])
        ejecutar = st.button("🚀 Ejecutar Diagnóstico", use_container_width=True)

    # 1. Selección de Sustancias
    sustancias_map = {"Agua": "Water", "Amoníaco": "Ammonia", "Aire": "Air", "R134a": "R134a"}
    nombre_user = st.selectbox("Seleccioná la sustancia:", list(sustancias_map.keys()))
    sustancia = sustancias_map[nombre_user]

    # 2. Selección de Par de Variables
    par = st.selectbox("Par de variables de entrada:", ["P y h", "P y T", "P y x", "T y x"])

    col1, col2 = st.columns(2)
    with col1:
        if "P" in par:
            v1 = st.number_input("Presión (bar)", value=1.0, format="%.4f")
            p_pa = v1 * 100000
        else:
            v1 = st.number_input("Temperatura (°C)", value=100.0)
            t_k = v1 + 273.15

    with col2:
        if "x" in par:
            v2 = st.slider("Título de vapor (x)", 0.0, 1.0, 0.5)
            x_in = v2
        elif "h" in par:
            v2 = st.number_input("Entalpía (kJ/kg)", value=2000.0)
            h_j = v2 * 1000
        elif "T" in par:
            v2 = st.number_input("Temperatura (°C)", value=20.0)
            t_k = v2 + 273.15

    st.divider()

    # --- LÓGICA DE EJECUCIÓN ---
    if ejecutar:
        try:
            st.subheader("📖 El cuento de cómo llegamos aquí:")
            
            # Variables para el gráfico
            t_plot, s_plot, p_plot, v_plot = 0, 0, 0, 0
            
            if par == "P y h":
                # Buscamos saturación para explicar el proceso
                hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
                hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
                h_in = v2
                
                st.write(f"1. Primero, fuimos a las tablas de **{nombre_user}** con la presión de **{v1} bar**.")
                st.write(f"2. Encontramos que el líquido saturado tiene $h_f = {hf:.2f}$ kJ/kg y el vapor saturado $h_g = {hg:.2f}$ kJ/kg.")
                
                if h_in < hf:
                    estado = "Líquido Comprimido"
                    st.info(f"**Diagnóstico:** Como tu entalpía ({h_in}) es menor a $h_f$ ({hf:.2f}), la sustancia es **{estado}**.")
                elif h_in > hg:
                    estado = "Vapor Sobrecalentado"
                    st.warning(f"**Diagnóstico:** Como tu entalpía ({h_in}) es mayor a $h_g$ ({hg:.2f}), la sustancia es **{estado}**.")
                else:
                    x = (h_in - hf) / (hg - hf)
                    st.success(f"**Diagnóstico:** Como tu entalpía está entre $h_f$ y $h_g$, estamos en zona de **Mezcla** con un título de {x:.4f}.")
                
                t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15
                s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000
                p_plot = v1
                v_plot = 1 / PropsSI('D', 'P', p_pa, 'H', h_in*1000, sustancia)

            # --- GENERAR GRÁFICO SELECCIONADO ---
            t_crit = PropsSI('Tcrit', sustancia)
            t_min = PropsSI('Tmin', sustancia)
            t_vec = np.linspace(t_min, t_crit - 0.1, 100)
            
            fig = go.Figure()
            
            if "T-s" in tipo_grafico:
                sf = [PropsSI('S', 'T', t, 'Q', 0, sustancia)/1000 for t in t_vec]
                sg = [PropsSI('S', 'T', t, 'Q', 1, sustancia)/1000 for t in t_vec]
                fig.add_trace(go.Scatter(x=sf+sg[::-1], y=[t-273.15 for t in t_vec]+[t-273.15 for t in t_vec][::-1], 
                                         fill='toself', name='Campana', line=dict(color='blue')))
                fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers', marker=dict(color='red', size=15), name='Estado'))
                fig.update_layout(xaxis_title="Entropía (s) [kJ/kgK]", yaxis_title="Temperatura (T) [°C]")
            else:
                vf = [1/PropsSI('D', 'T', t, 'Q', 0, sustancia) for t in t_vec]
                vg = [1/PropsSI('D', 'T', t, 'Q', 1, sustancia) for t in t_vec]
                fig.add_trace(go.Scatter(x=vf+vg[::-1], y=[PropsSI('P', 'T', t, 'Q', 0, sustancia)/100000 for t in t_vec]*2, 
                                         fill='toself', name='Campana', line=dict(color='green')))
                fig.add_trace(go.Scatter(x=[v_plot], y=[p_plot], mode='markers', marker=dict(color='red', size=15), name='Estado'))
                fig.update_layout(xaxis_type="log", xaxis_title="Volumen (v) [m³/kg]", yaxis_title="Presión (P) [bar]")

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"❌ **¡Error de ingreso!** El valor de {v2} no es posible para la sustancia {nombre_user} a esa presión.")
            st.write("Detalle técnico:", e)
    else:
        st.info("Configurá los datos y presioná 'Ejecutar Diagnóstico' en el panel lateral.")