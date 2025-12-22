import streamlit as st
from CoolProp.CoolProp import PropsSI
import plotly.graph_objects as go
import numpy as np

def mostrar_laboratorio():
    st.title("🧪 Laboratorio de Propiedades Termodinámicas")
    
    # --- ÁREA DE CONFIGURACIÓN ---
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 2, 2])
        with c1:
            sustancias_map = {"Agua": "Water", "Amoníaco": "Ammonia", "Aire": "Air", "R134a": "R134a"}
            nombre_user = st.selectbox("Sustancia:", list(sustancias_map.keys()))
            sustancia = sustancias_map[nombre_user]
        with c2:
            par = st.selectbox("Par de variables:", ["P y h", "P y T", "P y x", "T y x"])
        with c3:
            tipo_grafico = st.selectbox("Diagrama:", ["T-s (Temp-Entropía)", "P-v (Presión-Vol)"])

        i1, i2, i3 = st.columns([2, 2, 2])
        with i1:
            if "P" in par:
                v1 = st.number_input("Presión (bar)", value=10.0, format="%.2f")
                p_pa = v1 * 100000
            else:
                v1 = st.number_input("Temperatura (°C)", value=100.0)
                t_k = v1 + 273.15
        with i2:
            if "x" in par:
                v2 = st.slider("Título (x)", 0.0, 1.0, 0.5)
            elif "h" in par:
                v2 = st.number_input("Entalpía (kJ/kg)", value=2000.0)
            elif "T" in par:
                v2 = st.number_input("Temperatura (°C)", value=20.0)
        with i3:
            st.write("") 
            ejecutar = st.button("🚀 Ejecutar Diagnóstico", use_container_width=True, type="primary")

    if ejecutar:
        try:
            # Cálculos de estado
            if par == "P y h":
                h_in = v2
                hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
                hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
                
                with st.expander("📖 Procedimiento del Diagnóstico", expanded=True):
                    st.write(f"1. Entramos a la tabla de **{nombre_user}** por presión: **{v1} bar**.")
                    st.write(f"2. Identificamos los límites de la campana: $h_f = {hf:.2f}$ kJ/kg y $h_g = {hg:.2f}$ kJ/kg.")
                    
                    if h_in < hf:
                        estado = "Líquido Comprimido"
                        st.info(f"**Resultado:** Como el valor de entalpía ingresado ({h_in} kJ/kg) es **menor** a $h_f$, el estado es **{estado}**.")
                    elif h_in > hg:
                        estado = "Vapor Sobrecalentado"
                        st.warning(f"**Resultado:** Como el valor de entalpía ingresado ({h_in} kJ/kg) es **mayor** a $h_g$, el estado es **{estado}**.")
                    else:
                        estado = "Mezcla"
                        x = (h_in - hf) / (hg - hf)
                        st.success(f"**Resultado:** Dado que el punto está entre estos valores ($h_f < h < h_g$), el estado es **Mezcla**.")
                        st.latex(r"x = \frac{h - h_f}{h_g - h_f} = " + f"{x:.4f}")

                # Propiedades para el punto rojo
                t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15
                s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000
                p_plot = v1
                v_plot = 1 / PropsSI('D', 'P', p_pa, 'H', h_in*1000, sustancia)

            # --- GRÁFICOS ROBUSTOS ---
            t_crit = PropsSI('Tcrit', sustancia)
            t_min = PropsSI('Tmin', sustancia)
            t_range = np.linspace(t_min + 0.1, t_crit - 0.1, 100)
            
            fig = go.Figure()

            if "T-s" in tipo_grafico:
                # Campana (línea continua única)
                sf = [PropsSI('S', 'T', t, 'Q', 0, sustancia)/1000 for t in t_range]
                sg = [PropsSI('S', 'T', t, 'Q', 1, sustancia)/1000 for t in t_range]
                fig.add_trace(go.Scatter(x=sf + sg[::-1], y=[t-273.15 for t in t_range] + [t-273.15 for t in t_range][::-1], 
                                         fill='toself', fillcolor='rgba(0,100,255,0.1)', line=dict(color='blue'), name='Campana'))
                
                # Isobara
                s_vals = np.linspace(min(sf)*0.5, max(sg)*1.5, 50)
                t_iso = [PropsSI('T', 'P', p_pa, 'S', s*1000, sustancia)-273.15 for s in s_vals]
                fig.add_trace(go.Scatter(x=s_vals, y=t_iso, line=dict(color='orange', dash='dash'), name=f'P = {v1} bar'))
                
                fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers', marker=dict(color='red', size=12), name='Estado'))
                fig.update_layout(xaxis_title="s [kJ/kgK]", yaxis_title="T [°C]", xaxis=dict(range=[min(sf)-1, max(sg)+1]))

            else: # P-v
                vf = [1/PropsSI('D', 'T', t, 'Q', 0, sustancia) for t in t_range]
                vg = [1/PropsSI('D', 'T', t, 'Q', 1, sustancia) for t in t_range]
                p_sat = [PropsSI('P', 'T', t, 'Q', 0, sustancia)/100000 for t in t_range]
                
                fig.add_trace(go.Scatter(x=vf + vg[::-1], y=p_sat + p_sat[::-1], fill='toself', 
                                         fillcolor='rgba(0,255,100,0.1)', line=dict(color='green'), name='Campana'))
                
                # Isoterma
                v_vals = np.logspace(np.log10(min(vf)*0.1), np.log10(max(vg)*10), 50)
                p_iso = [PropsSI('P', 'T', t_plot+273.15, 'D', 1/v, sustancia)/100000 for v in v_vals]
                fig.add_trace(go.Scatter(x=v_vals, y=p_iso, line=dict(color='purple', dash='dash'), name=f'T = {t_plot:.1f} °C'))

                fig.add_trace(go.Scatter(x=[v_plot], y=[p_plot], mode='markers', marker=dict(color='red', size=12), name='Estado'))
                fig.update_layout(xaxis_type="log", yaxis_type="log", xaxis_title="v [m³/kg]", yaxis_title="P [bar]")

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error("Hubo un error con los valores ingresados. Por favor verifica que el punto exista para esta sustancia.")