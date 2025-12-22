import numpy as np
from CoolProp.CoolProp import PropsSI

fluido = 'Water'
# Generar 100 puntos de temperatura entre 274K y el punto crítico
temps = np.linspace(274, PropsSI('T_crit', fluido) - 0.1, 100)

with open('../libro/datos/campana_agua.dat', 'w') as f:
    f.write('s T\n') # Encabezado para PGFPlots
    # Línea líquido saturado (Q=0)
    for t in temps:
        s = PropsSI('S', 'T', t, 'Q', 0, fluido) / 1000
        f.write(f'{s:.4f} {t-273.15:.2f}\n')
    # Línea vapor saturado (Q=1) en reversa para cerrar la curva
    for t in reversed(temps):
        s = PropsSI('S', 'T', t, 'Q', 1, fluido) / 1000
        f.write(f'{s:.4f} {t-273.15:.2f}\n')