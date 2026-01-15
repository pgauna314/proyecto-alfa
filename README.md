# 📘 Proyecto α: Termodinámica de la Conversión de Energía

Este repositorio contiene el ecosistema integral del libro **"Termodinámica de la Conversión de Energía en Argentina"**. El proyecto combina un manuscrito académico en LaTeX con una plataforma interactiva en Streamlit.

## 🎨 Identidad Visual y Accesibilidad
El proyecto utiliza la **Paleta Okabe-Ito**, un esquema de colores diseñado científicamente para ser accesible a personas con diversas formas de daltonismo (Protanopía, Deuteranopía, etc.). Esta paleta garantiza que la información técnica sea universalmente legible.

### Mapeo Semántico de Colores
Para mantener la coherencia entre el libro físico y la aplicación digital, se utiliza el siguiente código de colores:

| Concepto | Color | Hex | Uso en el Proyecto |
| :--- | :--- | :--- | :--- |
| **Energía Térmica** | Bermellón | `#D55E00` | Calor de entrada (Q_in), Generación Térmica. |
| **Recursos Hídricos** | Azul | `#0072B2` | Ciclos hidráulicos, procesos isobáricos. |
| **Energía Nuclear** | Naranja | `#E69F00` | Generación Nuclear, Trabajo de turbina (W_out). |
| **Sustentabilidad** | Verde Azulado | `#009E73` | Energías Renovables, eficiencia exergética. |
| **Fluido de Trabajo** | Azul Cielo | `#56B4E9` | Vapor de agua, estados de saturación. |

## 🛠️ Estructura del Ecosistema
* **/libro**: Código fuente en LaTeX (`main.tex`, `preamble.tex`).
    * `/datos`: Archivos de respaldo técnico (ej. `campana_agua.dat`).
* **/web**: Aplicación interactiva en Streamlit.
    * `/modules/book_support`: Material pedagógico interactivo por capítulo.
    * `/modules/palettes.py`: Motor central de colores (sincronizado con el preámbulo LaTeX).

## 🚀 Filosofía del Proyecto
El **Proyecto α** se apoya en tres pilares:
1.  **Soberanía Pedagógica:** Contenido adaptado a la realidad energética de Argentina y el SADI.
2.  **Accesibilidad Universal:** Diseño visual inclusivo y preparación para futura sonificación de datos.
3.  **Interactividad:** El libro deja de ser un objeto estático para convertirse en un laboratorio dinámico de cálculo.

---
*Nota: Este proyecto se desarrolla bajo estándares de software libre y rigor científico para la educación pública.*