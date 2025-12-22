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
                x_in = v2
            elif "h" in par:
                v2 = st.number_input("Entalpía (kJ/kg)", value=2000.0)
                h_j = v2 * 1000
            elif "T" in par:
                v2 = st.number_input("Temperatura (°C)", value=20.0)
                t_k = v2 + 273.15
        with i3:
            st.write("") # Espacio
            ejecutar = st.button("🚀 Ejecutar Diagnóstico", use_container_width=True, type="primary")

    if ejecutar:
        try:
            # 1. INICIALIZACIÓN DE VARIABLES DE SALIDA
            t_plot, s_plot, p_plot, v_plot = 0, 0, 0, 0
            cuento = []

            # 2. LÓGICA DE CÁLCULO Y RELATO (EL CUENTO)
            if par == "P y h":
                h_in = v2
                hf = PropsSI('H', 'P', p_pa, 'Q', 0, sustancia) / 1000
                hg = PropsSI('H', 'P', p_pa, 'Q', 1, sustancia) / 1000
                
                cuento.append(f"1. Buscamos en la tabla de **{nombre_user}** a **{v1} bar**.")
                cuento.append(f"2. Obtenemos los valores de saturación: $h_f = {hf:.2f}$ kJ/kg y $h_g = {hg:.2f}$ kJ/kg.")
                
                if h_in < hf:
                    estado = "Líquido Comprimido"
                    cuento.append(f"3. Como $h$ ({h_in}) < $h_f$, el estado es **{estado}**.")
                elif h_in > hg:
                    estado = "Vapor Sobrecalentado"
                    cuento.append(f"3. Como $h$ ({h_in}) > $h_g$, el estado es **{estado}**.")
                else:
                    x = (h_in - hf) / (hg - hf)
                    estado = "Mezcla"
                    cuento.append(f"3. Como $h_f < h < h_g$, es una **Mezcla** con título $x = {x:.4f}$.")
                
                # Propiedades para graficar
                t_plot = PropsSI('T', 'P', p_pa, 'H', h_in*1000, sustancia) - 273.15
                s_plot = PropsSI('S', 'P', p_pa, 'H', h_in*1000, sustancia) / 1000
                p_plot = v1
                v_plot = 1 / PropsSI('D', 'P', p_pa, 'H', h_in*1000, sustancia)

            # (Aquí podés ir agregando los elif para los otros pares siguiendo el mismo esquema)

            # 3. MOSTRAR EL PROCEDIMIENTO
            with st.expander("📖 Procedimiento del Diagnóstico", expanded=True):
                for linea in cuento:
                    st.write(linea)

            # 4. DIBUJAR EL GRÁFICO (RECORREGIDO)
            t_crit = PropsSI('Tcrit', sustancia)
            t_min = PropsSI('Tmin', sustancia)
            t_vec = np.linspace(t_min, t_crit - 0.05, 100)
            
            fig = go.Figure()

            if "T-s" in tipo_grafico:
                sf = [PropsSI('S', 'T', t, 'Q', 0, sustancia)/1000 for t in t_vec]
                sg = [PropsSI('S', 'T', t, 'Q', 1, sustancia)/1000 for t in t_vec]
                # Unimos las dos curvas para cerrar la campana correctamente
                fig.add_trace(go.Scatter(x=sf + sg[::-1], 
                                         y=[t-273.15 for t in t_vec] + [t-273.15 for t in t_vec][::-1], 
                                         fill='toself', fillcolor='rgba(0,100,255,0.1)', 
                                         line=dict(color='blue'), name='Campana'))
                fig.add_trace(go.Scatter(x=[s_plot], y=[t_plot], mode='markers', 
                                         marker=dict(color='red', size=14, symbol='x'), name='Estado'))
                fig.update_layout(xaxis_title="Entropía (s) [kJ/kgK]", yaxis_title="Temperatura (T) [°C]")
            
            else: # P-v
                vf = [1/PropsSI('D', 'T', t, 'Q', 0, sustancia) for t in t_vec]
                vg = [1/PropsSI('D', 'T', t, 'Q', 1, sustancia) for t in t_vec]
                pf = [PropsSI('P', 'T', t, 'Q', 0, sustancia)/100000 for t in t_vec]
                fig.add_trace(go.Scatter(x=vf + vg[::-1], y=pf + pf[::-1], 
                                         fill='toself', fillcolor='rgba(0,255,100,0.1)', 
                                         line=dict(color='green'), name='Campana'))
                fig.add_trace(go.Scatter(x=[v_plot], y=[p_plot], mode='markers', 
                                         marker=dict(color='red', size=14, symbol='x'), name='Estado'))
                fig.update_layout(xaxis_type="log", xaxis_title="Vol. específico (v) [m³/kg]", yaxis_title="Presión (P) [bar]")

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error en el cálculo: {e}")
    else:
        st.info("Ajustá los valores y presioná el botón para ver el diagnóstico.")