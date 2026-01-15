# web/modules/palettes.py

# Paleta Japonesa Okabe-Ito (Accesibilidad Universal)
OKABE_ITO = {
    "naranja": "#E69F00",
    "azul_cielo": "#56B4E9",
    "verde_azulado": "#009E73",
    "amarillo": "#F0E442",
    "azul": "#0072B2",
    "bermellon": "#D55E00",
    "purpura_rojizo": "#CC79A7",
    "negro": "#000000"
}

# Identidad Semántica para Termodinámica (Capítulo 2 y resto)
# Esto garantiza que el lector siempre asocie un color a un concepto
TERMO_THEME = {
    "linea_saturacion": OKABE_ITO["negro"],
    "proceso_isobarico": OKABE_ITO["azul"],
    "calor_entrada": OKABE_ITO["bermellon"],    # Q_in (Caldera)
    "trabajo_salida": OKABE_ITO["naranja"],     # W_out (Turbina)
    "fluido_trabajo": OKABE_ITO["azul_cielo"],
    "anomalias": OKABE_ITO["purpura_rojizo"]    # Irreversibilidades
}

# Colores para la Matriz Energética (Soberanía Nacional)
ENERGY_THEME = {
    "Termica": OKABE_ITO["bermellon"],
    "Hidraulica": OKABE_ITO["azul"],
    "Nuclear": OKABE_ITO["naranja"],
    "Renovables": OKABE_ITO["verde_azulado"]
}