import streamlit as st
from CoolProp.CoolProp import PropsSI

def mostrar_laboratorio():
    st.title("🧪 Laboratorio de Diagnóstico Termodinámico")
    st.write("Esta sección automatiza el diagnóstico de estado siguiendo la lógica de las tablas del libro.")

    # 1. Selección de Sustancia (Mapeo de nombres comunes a nombres de CoolProp)
    sustancias_map = {
        "Agua": "Water",
        "R134a": "R134a",
        "Amoníaco": "Ammonia",
        "Nitrógeno": "Nitrogen",
        "D2O (Agua Pesada)": "HeavyWater"
    }
    nombre_usuario = st.selectbox("Sustancia:", list(sustancias_map.keys()))
    sustancia = sustancias_map[nombre_usuario]

    # 2. Selección de entrada
    opciones_entrada = {
        "P y T": "PT",
        "P y h": "PH",
        "P y u": "PU",
        "P y v": "PD" # D es densidad, 1/v
    }
    par_elegido = st.selectbox("Par de variables de entrada:", list(opciones_entrada.keys()))

    # 3. Inputs de usuario (con unidades comunes bar, °C, kJ/kg)
    col1, col2 = st.columns(2)
    with col1:
        if "P" in par_elegido:
            val1 = st.number_input("Presión (bar)", value=1.0, format="%.4f")
            p_pascal = val1 * 100000  # Convertir bar a Pa para la librería
        else:
            val1 = st.number_input("Temperatura (°C)", value=100.0)
            t_kelvin = val1 + 273.15

    with col2:
        if "T" in par_elegido:
            val2 = st.number_input("Temperatura (°C)", value=25.0)
            t_kelvin = val2 + 273.15
        elif "h" in par_elegido:
            val2 = st.number_input("Entalpía (kJ/kg)", value=2000.0)
            prop_si = val2 * 1000 # kJ a J
        elif "u" in par_elegido:
            val2 = st.number_input("E. Interna (u) (kJ/kg)", value=1500.0)
            prop_si = val2 * 1000
        elif "v" in par_elegido:
            val2 = st.number_input("Vol. específico (m³/kg)", value=0.1, format="%.6f")
            prop_si = 1 / val2 # Densidad en kg/m³

    st.divider()

    try:
        # --- LÓGICA DE DIAGNÓSTICO (Ejemplo para P y h) ---
        if par_elegido == "P y h":
            # 1. Buscar valores de saturación a esa P
            hf = PropsSI('H', 'P', p_pascal, 'Q', 0, sustancia) / 1000
            hg = PropsSI('H', 'P', p_pascal, 'Q', 1, sustancia) / 1000
            uf = PropsSI('U', 'P', p_pascal, 'Q', 0, sustancia) / 1000
            ug = PropsSI('U', 'P', p_pascal, 'Q', 1, sustancia) / 1000
            vf = 1 / PropsSI('D', 'P', p_pascal, 'Q', 0, sustancia)
            vg = 1 / PropsSI('D', 'P', p_pascal, 'Q', 1, sustancia)
            tsat = PropsSI('T', 'P', p_pascal, 'Q', 0, sustancia) - 273.15

            st.subheader("🔍 Análisis del Estado")
            
            # Mostramos los valores de referencia que el alumno buscaría en la tabla
            st.write(f"A **{val1} bar**, los valores de saturación son:")
            st.latex(rf"h_f = {hf:.2f} \text{{ kJ/kg}} \quad | \quad h_g = {hg:.2f} \text{{ kJ/kg}}")

            h_in = val2
            if h_in < hf:
                st.info("🔹 **Estado: Líquido Comprimido (Subenfriado)**")
                st.write(f"Como $h$ ({h_in}) < $h_f$ ({hf:.2f}), la sustancia no ha llegado a saturación.")
            
            elif hf <= h_in <= hg:
                st.success("🔸 **Estado: Mezcla Bifásica (Líquido + Vapor)**")
                st.write(f"Como $h_f \leq h \leq h_g$, calculamos el título:")
                x = (h_in - hf) / (hg - hf)
                st.latex(rf"x = \frac{{{h_in} - {hf:.2f}}}{{{hg:.2f} - {hf:.2f}}} = {x:.4f}")
                
                # Propiedades de mezcla
                u_mix = uf + x * (ug - uf)
                v_mix = vf + x * (vg - vf)
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Título (x)", f"{x:.4f}")
                m2.metric("E. Interna (u)", f"{u_mix:.2f} kJ/kg")
                m3.metric("Vol. Esp. (v)", f"{v_mix:.5f} m³/kg")
            
            else:
                st.warning("🔥 **Estado: Vapor Sobrecalentado**")
                st.write(f"Como $h$ ({h_in}) > $h_g$ ({hg:.2f}), la sustancia es vapor puro a alta temperatura.")
                t_real = PropsSI('T', 'P', p_pascal, 'H', h_in*1000, sustancia) - 273.15
                st.metric("Temperatura Real", f"{t_real:.2f} °C")

        else:
            st.warning("Lógica para este par de variables en desarrollo...")
            
    except Exception as e:
        st.error(f"Error en el cálculo: {e}. Verificá que los datos tengan sentido físico.")