import streamlit as st
from CoolProp.CoolProp import PropsSI
import plotly.graph_objects as go
import numpy as np

def mostrar_laboratorio():
    st.title("🧪 Laboratorio de Propiedades Termodinámicas")
    st.write("Análisis de estado y diagnóstico pedagógico.")

    # 1. Selector de Sustancias
    sustancias_map = {
        "Agua": "Water",
        "Amoníaco": "Ammonia",
        "Aire": "Air",
        "R134a": "R134a",
        "D2O (Agua Pesada)": "HeavyWater"
    }
    nombre_user = st.selectbox("Sustancia:", list(sustancias_map.keys()))
    sustancia = sustancias_map[nombre_user]

    # 2. Selector de Pares de Propiedades
    # Agregamos T y x, P y x, h y s
    par_opciones = [
        "P y T", "P y h", "P y u", "P y x", "T y x", "h y s"
    ]
    par = st.selectbox("Par de variables de entrada:", par_opciones)

    col1, col2 = st.columns(2)
    
    # Configuración dinámica de inputs según el par
    with col1:
        if "P" in par:
            v1 = st.number_input("Presión (bar)", value=1.0, format="%.4f")
            p_pa = v1 * 100000
        elif "T" in par:
            v1 = st.number_input("Temperatura (°C)", value=100.0)
            t_k = v1 + 273.15
        elif par == "h y s":
            v1 = st.number_input("Entalpía (kJ/kg)", value=2500.0)
            h_j = v1 * 1000

    with col2:
        if "x" in par:
            v2 = st.slider("Título de vapor (x)", 0.0, 1.0, 0.5)
            x_in = v2
        elif "T" in par and "P" not in par:
            v2 = st.number_input("Temperatura (°C)", value=20.0)
            t_k = v2 + 273.15
        elif "h" in par:
            v2 = st.number_input("Entalpía (kJ/kg)", value=2000.0)
            h_j = v2 * 1000
        elif "u" in par:
            v2 = st.number_input("E. Interna (u) (kJ/kg)", value=1500.0)
            u_j = v2 * 1000
        elif "s" in par:
            v2 = st.number_input("Entropía (s) (kJ/kgK)", value=6.0)
            s_j = v2 * 1000

    st.divider()

    try:
        # --- CÁLCULOS Y DIAGNÓSTICO ---
        # Definimos variables por defecto para el gráfico
        t_plot, s_plot = 0, 0
        
        if par == "P y x" or par == "T y x":
            st.success("🔸 **Estado: Mezcla Saturada (Bifásico)**")
            if "P" in par:
                t_plot = PropsSI('T', 'P', p_pa, 'Q', x_in, sustancia) - 273.15
                s_plot = PropsSI('S', 'P', p_pa, 'Q', x_in, sustancia) / 1000
                st.write(f"Temperatura de saturación: {t_plot:.2f} °C")
            else:
                p_calc = PropsSI('P', 'T', t_k, 'Q', x_in, sustancia) / 100000
                s_plot = PropsSI('S', 'T', t_k, 'Q', x_in, sustancia) / 1000
                t_plot = v1
                st.write(f"Presión de saturación: {p_calc:.4f} bar")

        elif par == "P y h":
            hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
            hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
            h_in = v2
            if h_in < hf:
                estado = "Líquido Comprimido"
                st.info(f"🔹 **{estado}** ($h < h_f$)")
            elif h_in > hg:
                estado = "Vapor Sobrecalentado"
                st.warning(f"🔥 **{estado}** ($h > h_g$)")
            else:
                x = (h_in - hf) / (hg - hf)
                st.success(f"🔸 **Mezcla** (Título $x={x:.4f}$)")
            
            t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15
            s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000

        elif par == "h y s":
            # Caso avanzado: Determinar fase por h y s
            t_plot = PropsSI('T', 'H', h_j, 'S', s_j, sustancia) - 273.15
            s_plot = v2
            st.write(f"Temperatura calculada: {t_plot:.2f} °C")

            else:
            # Cálculo genérico para cualquier par que no sea de saturación directa
            # Esto permite que P y T o P y u también funcionen
            t_plot = PropsSI('T', par[0], v1_si, par[4], v2_si, sustancia) - 273.15
            s_plot = PropsSI('S', par[0], v1_si, par[4], v2_si, sustancia) / 1000
            st.info(f"Estado calculado para el par {par}")

        # --- GENERAR GRÁFICO T-s ---
        t_crit = PropsSI('Tcrit', sustancia)
        t_min = PropsSI('Tmin', sustancia)
        t_vec = np.linspace(t_min, t_crit - 0.1, 100)
        
        sf_curve = [PropsSI('S', 'T', t, 'Q', 0, sustancia) / 1000 for t in t_vec]
        sg_curve = [PropsSI('S', 'T', t, 'Q', 1, sustancia) / 1000 for t in t_vec]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sf_curve + sg_curve[::-1], 
                                 y=[t-273.15 for t in t_vec] + [t-273.15 for t in t_vec][::-1],
                                 fill='toself', fillcolor='rgba(100, 150, 255, 0.1)',
                                 line=dict(color='blue'), name='Campana'))
        
        fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers+text',
                                 marker=dict(color='red', size=12),
                                 text=[" PUNTO"], textposition="top right"))

        fig.update_layout(title=f"Diagrama T-s - {nombre_user}", xaxis_title="s [kJ/kgK]", yaxis_title="T [°C]")
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}. Probablemente el punto esté fuera de los límites de la sustancia.")