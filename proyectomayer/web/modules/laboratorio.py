import streamlit as st
from CoolProp.CoolProp import PropsSI
import plotly.graph_objects as go
import numpy as np

def mostrar_laboratorio():
    st.title("🧪 Laboratorio de Propiedades Termodinámicas")
    st.write("Configurá el estado, elegí el diagrama y ejecutá el diagnóstico pedagógico.")

    # --- PANEL DE CONFIGURACIÓN ---
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 2, 2])
        with c1:
            sustancias_map = {
                "Agua": "Water", 
                "Amoníaco": "Ammonia", 
                "Aire": "Air", 
                "R134a": "R134a"
            }
            nombre_user = st.selectbox("Sustancia:", list(sustancias_map.keys()))
            sustancia = sustancias_map[nombre_user]
        with c2:
            par = st.selectbox("Par de variables:", ["P y T", "P y h", "P y x", "T y x"])
        with c3:
            tipo_grafico = st.selectbox("Diagrama:", ["T-s (Temp-Entropía)", "P-v (Presión-Vol)"])

        i1, i2, i3 = st.columns([2, 2, 2])
        with i1:
            if "P" in par:
                v1 = st.number_input("Presión (bar)", value=10.0, format="%.2f", min_value=0.01)
                p_pa_in = v1 * 100000
            else:
                v1 = st.number_input("Temperatura (°C)", value=150.0, format="%.2f")
                t_k_in = v1 + 273.15
        with i2:
            if "x" in par:
                v2 = st.slider("Título (x)", 0.0, 1.0, 0.5)
                x_val = v2
            elif "h" in par:
                v2 = st.number_input("Entalpía (kJ/kg)", value=2000.0)
                h_val = v2 * 1000
            elif "T" in par:
                v2 = st.number_input("Temperatura (°C)", value=150.0)
                t_k_val = v2 + 273.15
        with i3:
            st.write("") 
            ejecutar = st.button("🚀 Ejecutar Diagnóstico", use_container_width=True, type="primary")

    if ejecutar:
        try:
            # Inicialización de variables de dibujo
            t_plot, s_plot, p_plot, v_plot, h_plot, u_plot = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

            with st.expander("📖 Procedimiento del Diagnóstico", expanded=True):
                # 1. CÁLCULO DE PROPIEDADES SEGÚN ENTRADA
                if par == "P y T":
                    t_in_c = v2
                    t_sat = PropsSI('T', 'P', p_pa_in, 'Q', 0, sustancia) - 273.15
                    st.write(f"1. A **{v1} bar**, la temperatura de saturación es **{t_sat:.2f} °C**.")
                    if t_in_c < t_sat - 0.1:
                        st.info(f"**Resultado:** Líquido Comprimido ({t_in_c} < {t_sat:.2f})")
                    elif t_in_c > t_sat + 0.1:
                        st.warning(f"**Resultado:** Vapor Sobrecalentado ({t_in_c} > {t_sat:.2f})")
                    else:
                        st.success("**Resultado:** Estado de Saturación.")
                    
                    p_plot = v1
                    t_plot = t_in_c
                    s_plot = PropsSI('S', 'P', p_pa_in, 'T', t_in_c + 273.15, sustancia) / 1000
                    v_plot = 1 / PropsSI('D', 'P', p_pa_in, 'T', t_in_c + 273.15, sustancia)
                    h_plot = PropsSI('H', 'P', p_pa_in, 'T', t_in_c + 273.15, sustancia) / 1000
                    u_plot = PropsSI('U', 'P', p_pa_in, 'T', t_in_c + 273.15, sustancia) / 1000

                elif par == "P y h":
                    hf = PropsSI('H', 'P', p_pa_in, 'Q', 0, sustancia) / 1000
                    hg = PropsSI('H', 'P', p_pa_in, 'Q', 1, sustancia) / 1000
                    st.write(f"1. Límites a **{v1} bar**: $h_f = {hf:.2f}$ y $h_g = {hg:.2f}$ kJ/kg.")
                    if h_val/1000 < hf:
                        st.info("Resultado: Líquido Comprimido")
                    elif h_val/1000 > hg:
                        st.warning("Resultado: Vapor Sobrecalentado")
                    else:
                        x = (h_val/1000 - hf) / (hg - hf)
                        st.success(f"Resultado: Mezcla con título $x = {x:.4f}$")
                    
                    p_plot = v1
                    t_plot = PropsSI('T', 'P', p_pa_in, 'H', h_val, sustancia) - 273.15
                    s_plot = PropsSI('S', 'P', p_pa_in, 'H', h_val, sustancia) / 1000
                    v_plot = 1 / PropsSI('D', 'P', p_pa_in, 'H', h_val, sustancia)
                    h_plot = h_val / 1000
                    u_plot = PropsSI('U', 'P', p_pa_in, 'H', h_val, sustancia) / 1000

                elif par == "P y x":
                    st.success(f"**Resultado:** Mezcla definida por título $x = {x_val}$")
                    p_plot = v1
                    t_plot = PropsSI('T', 'P', p_pa_in, 'Q', x_val, sustancia) - 273.15
                    s_plot = PropsSI('S', 'P', p_pa_in, 'Q', x_val, sustancia) / 1000
                    v_plot = 1 / PropsSI('D', 'P', p_pa_in, 'Q', x_val, sustancia)
                    h_plot = PropsSI('H', 'P', p_pa_in, 'Q', x_val, sustancia) / 1000
                    u_plot = PropsSI('U', 'P', p_pa_in, 'Q', x_val, sustancia) / 1000

                elif par == "T y x":
                    p_pa_calc = PropsSI('P', 'T', t_k_in, 'Q', x_val, sustancia)
                    p_plot = p_pa_calc / 100000
                    t_plot = v1
                    st.success(f"**Resultado:** Mezcla a {v1} °C. Presión calculada: **{p_plot:.4f} bar**")
                    s_plot = PropsSI('S', 'T', t_k_in, 'Q', x_val, sustancia) / 1000
                    v_plot = 1 / PropsSI('D', 'T', t_k_in, 'Q', x_val, sustancia)
                    h_plot = PropsSI('H', 'T', t_k_in, 'Q', x_val, sustancia) / 1000
                    u_plot = PropsSI('U', 'T', t_k_in, 'Q', x_val, sustancia) / 1000

            # --- 2. TABLA DE TODAS LAS PROPIEDADES ---
            st.subheader("📊 Tabla de Propiedades Resultantes")
            c_res1, c_res2, c_res3 = st.columns(3)
            with c_res1:
                st.metric("Presión (P)", f"{p_plot:.4f} bar")
                st.metric("Entalpía (h)", f"{h_plot:.2f} kJ/kg")
            with c_res2:
                st.metric("Temperatura (T)", f"{t_plot:.2f} °C")
                st.metric("Energía Interna (u)", f"{u_plot:.2f} kJ/kg")
            with c_res3:
                st.metric("Vol. Específico (v)", f"{v_plot:.5f} m³/kg")
                st.metric("Entropía (s)", f"{s_plot:.4f} kJ/kgK")

            # --- 3. GRÁFICOS (con escalas y rangos seguros) ---
            t_crit = PropsSI('Tcrit', sustancia) - 273.15
            t_min = PropsSI('Tmin', sustancia) - 273.15
            t_vec = np.linspace(t_min + 0.5, t_crit - 0.2, 100)
            fig = go.Figure()

            if "T-s" in tipo_grafico:
                sf = [PropsSI('S', 'T', t+273.15, 'Q', 0, sustancia)/1000 for t in t_vec]
                sg = [PropsSI('S', 'T', t+273.15, 'Q', 1, sustancia)/1000 for t in t_vec]
                fig.add_trace(go.Scatter(x=sf + sg[::-1], y=list(t_vec) + list(t_vec)[::-1], fill='toself', fillcolor='rgba(0,100,255,0.05)', line=dict(color='blue'), name='Campana'))
                
                # Isobara segura
                s_range = np.linspace(min(sf)*0.8, max(sg)*1.2, 50)
                t_iso, s_iso_f = [], []
                for s in s_range:
                    try:
                        temp = PropsSI('T', 'P', p_plot*100000, 'S', s*1000, sustancia) - 273.15
                        if temp < 1000:
                            t_iso.append(temp); s_iso_f.append(s)
                    except: continue
                fig.add_trace(go.Scatter(x=s_iso_f, y=t_iso, line=dict(color='orange', dash='dot'), name=f'Isobara {p_plot:.2f} bar'))
                fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers', marker=dict(color='red', size=14, symbol='x'), name='Estado'))
                fig.update_layout(yaxis=dict(range=[t_min-10, max(t_crit, t_plot)+50]), xaxis_title="s [kJ/kgK]", yaxis_title="T [°C]")

            else: # P-v
                vf = [1/PropsSI('D', 'T', t+273.15, 'Q', 0, sustancia) for t in t_vec]
                vg = [1/PropsSI('D', 'T', t+273.15, 'Q', 1, sustancia) for t in t_vec]
                psat = [PropsSI('P', 'T', t+273.15, 'Q', 0, sustancia)/100000 for t in t_vec]
                fig.add_trace(go.Scatter(x=vf + vg[::-1], y=psat + psat[::-1], fill='toself', fillcolor='rgba(0,255,100,0.05)', line=dict(color='green'), name='Campana'))
                
                # Isoterma segura
                v_range = np.logspace(np.log10(min(vf)*0.3), np.log10(max(vg)*8), 50)
                p_iso, v_iso_f = [], []
                for v in v_range:
                    try:
                        pres = PropsSI('P', 'T', t_plot+273.15, 'D', 1/v, sustancia)/100000
                        if pres < 1000:
                            p_iso.append(pres); v_iso_f.append(v)
                    except: continue
                fig.add_trace(go.Scatter(x=v_iso_f, y=p_iso, line=dict(color='purple', dash='dot'), name=f'Isoterma {t_plot:.1f}°C'))
                fig.add_trace(go.Scatter(x=[v_plot], y=[p_plot], mode='markers', marker=dict(color='red', size=14, symbol='x'), name='Estado'))
                fig.update_layout(xaxis_type="log", yaxis_type="log", xaxis_title="v [m³/kg]", yaxis_title="P [bar]")

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error en el cálculo: {e}")
    else:
        st.info("💡 Configurá los datos y presioná **Ejecutar Diagnóstico**.")