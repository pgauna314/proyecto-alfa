import numpy as np
import CoolProp.CoolProp as CP

# Forzamos los nombres a formato 'ascii' para evitar el bug de Python 3.13
fluido = 'Water'

try:
    T_crit = CP.PropsSI('T_crit', fluido)
    T_min = 274.15 
    temps = np.linspace(T_min, T_crit - 0.5, 100)

    with open('../libro/datos/campana_agua.dat', 'w') as f:
        f.write('s T\n')
        # Línea líquido saturado
        for t in temps:
            s = CP.PropsSI('S', 'T', t, 'Q', 0, fluido) / 1000
            f.write(f'{s:.4f} {t-273.15:.2f}\n')
        # Línea vapor saturado
        for t in reversed(temps):
            s = CP.PropsSI('S', 'T', t, 'Q', 1, fluido) / 1000
            f.write(f'{s:.4f} {t-273.15:.2f}\n')
    print("¡Listo! Archivo generado.")

except Exception as e:
    print(f"Error: {e}")