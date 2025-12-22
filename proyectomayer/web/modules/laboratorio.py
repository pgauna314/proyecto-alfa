import streamlit as st
from CoolProp.CoolProp import PropsSI
import plotly.graph_objects as go
import numpy as np

def mostrar_laboratorio():
    st.title("🧪 Laboratorio y Diagnóstico Termodinámico")
    
    # --- CONFIGURACIÓN DE ENTRADA ---
    sustancias_map = {"Agua": "Water", "R134a": "R134a", "D2O (Agua Pesada)": "HeavyWater"}
    nombre_usuario = st.selectbox("Sustancia:", list(sustancias_map.keys()))
    sustancia = sustancias_map[nombre_usuario]

    col1, col2 = st.columns(2)
    with col1:
        p_bar = st.number_input("Presión (bar)", value=10.0, step=1.0)
        p_pa = p_bar * 100000
    with col2:
        h_kj = st.number_input("Entalpía (kJ/kg)", value=2000.0, step=50.0)
        h_j = h_kj * 1000

    try:
        # 1. Obtener valores de saturación reales
        hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
        hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
        sf = PropsSI('S', 'P', p_pa, 'Q', 0, sustancia) / 1000
        sg = PropsSI('S', 'P', p_pa, 'Q', 1, sustancia) / 1000
        T_sat = PropsSI('T', 'P', p_pa, 'Q', 0, sustancia) - 273.15
        
        # 2. Diagnóstico de fase y cálculo de S actual
        s_act = 0
        estado = ""
        
        if h_kj < hf:
            estado = "Líquido Comprimido"
            s_act = PropsSI('S', 'P', p_pa, 'H', h_j, sustancia) / 1000
            t_act = PropsSI('T', 'P', p_pa, 'H', h_j, sustancia) - 273.15
            st.info(f"🔹 **Estado: {estado}**")
        elif hf <= h_kj <= hg:
            estado = "Mezcla"
            x = (h_kj - hf) / (hg - hf)
            s_act = sf + x * (sg - sf)
            t_act = T_sat
            st.success(f"🔸 **Estado: {estado} (Título x={x:.3f})**")
        else:
            estado = "Vapor Sobrecalentado"
            s_act = PropsSI('S', 'P', p_pa, 'H', h_j, sustancia) / 1000
            t_act = PropsSI('T', 'P', p_pa, 'H', h_j, sustancia) - 273.15
            st.warning(f"🔥 **Estado: {estado}**")

        # --- GENERACIÓN DEL GRÁFICO T-s ---
        # Creamos la campana de saturación
        t_crit = PropsSI('Tcrit', sustancia)
        t_min = PropsSI('Tmin', sustancia)
        temps = np.linspace(t_min, t_crit - 0.1, 50)
        
        sf_curve = [PropsSI('S', 'T', t, 'Q', 0, sustancia) / 1000 for t in temps]
        sg_curve = [PropsSI('S', 'T', t, 'Q', 1, sustancia) / 1000 for t in temps]

        fig = go.Figure()
        
        # Dibujar campana
        fig.add_trace(go.Scatter(x=sf_curve + sg_curve[::-1], 
                                 y=[t-273.15 for t in temps] + [t-273.15 for t in temps][::-1],
                                 fill='toself', fillcolor='rgba(200, 200, 200, 0.2)',
                                 line=dict(color='black'), name='Campana Sat.'))
        
        # Dibujar punto actual
        fig.add_trace(go.Scatter(x=[s_act], y=[t_act], 
                                 mode='markers+text',
                                 marker=dict(color='red', size=12),
                                 text=[" PUNTO ACTUAL"], textposition="top right",
                                 name='Estado Actual'))

        fig.update_layout(title=f"Diagrama T-s para {nombre_usuario}",
                          xaxis_title="Entropía (s) [kJ/kg·K]",
                          yaxis_title="Temperatura (T) [°C]",
                          template="plotly_white")

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error en el cálculo: {e}")