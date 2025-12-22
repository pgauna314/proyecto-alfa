import streamlit as st
from CoolProp.CoolProp import PropsSI
import plotly.graph_objects as go
import numpy as np

def mostrar_laboratorio():
    st.title("🧪 Laboratorio de Diagnóstico Termodinámico")
    
    # 1. Configuración de entrada
    sustancias_map = {"Agua": "Water", "R134a": "R134a", "D2O": "HeavyWater"}
    nombre_user = st.selectbox("Sustancia:", list(sustancias_map.keys()))
    sustancia = sustancias_map[nombre_user]

    par = st.selectbox("Variables de entrada:", ["P y h", "P y T", "P y u"])

    col1, col2 = st.columns(2)
    with col1:
        p_bar = st.number_input("Presión (bar)", value=10.0, format="%.2f")
    with col2:
        val2 = st.number_input("Segunda variable (h o T o u)", value=2000.0 if "h" in par or "u" in par else 200.0)

    st.divider()

    try:
        # Conversión a SI (Pascal, Kelvin, J/kg)
        p_pa = p_bar * 100000
        
        # --- BUSCAMOS VALORES DE SATURACIÓN PARA EL DIAGNÓSTICO ---
        # hf y hg siempre son necesarios para comparar
        hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
        hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
        Tsat = PropsSI('T', 'P', p_pa, 'Q', 0, sustancia) - 273.15
        sf = PropsSI('S', 'P', p_pa, 'Q', 0, sustancia) / 1000
        sg = PropsSI('S', 'P', p_pa, 'Q', 1, sustancia) / 1000

        st.subheader("🔍 Diagnóstico de Fase")
        
        # LÓGICA SEGÚN EL PAR ELEGIDO
        if "h" in par:
            h_in = val2
            if h_in < hf:
                estado = "Líquido Comprimido"
                st.info(f"🔹 **{estado}**: $h$ ({h_in}) < $h_f$ ({hf:.2f})")
                s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000
                t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15
            elif hf <= h_in <= hg:
                estado = "Mezcla"
                x = (h_in - hf) / (hg - hf)
                st.success(f"🔸 **{estado}**: Título $x = {x:.4f}$")
                st.latex(rf"x = \frac{{{h_in} - {hf:.2f}}}{{{hg:.2f} - {hf:.2f}}}")
                s_plot = sf + x * (sg - sf)
                t_plot = Tsat
            else:
                estado = "Vapor Sobrecalentado"
                st.warning(f"🔥 **{estado}**: $h$ ({h_in}) > $h_g$ ({hg:.2f})")
                s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000
                t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15

        # --- GRÁFICO T-s ---
        t_crit = PropsSI('Tcrit', sustancia)
        t_min = PropsSI('Tmin', sustancia)
        t_range = np.linspace(t_min, t_crit - 0.1, 50)
        
        sf_line = [PropsSI('S', 'T', t, 'Q', 0, sustancia)/1000 for t in t_range]
        sg_line = [PropsSI('S', 'T', t, 'Q', 1, sustancia)/1000 for t in t_range]
        t_celsius = [t - 273.15 for t in t_range]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sf_line + sg_line[::-1], y=t_celsius + t_celsius[::-1], 
                                 fill='toself', name='Campana', line=dict(color='gray')))
        fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers', 
                                 marker=dict(color='red', size=12), name='Estado'))
        
        fig.update_layout(title="Ubicación en Diagrama T-s", xaxis_title="s [kJ/kgK]", yaxis_title="T [°C]")
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error en los datos o sustancia: {e}")