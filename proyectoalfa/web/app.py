# proyectoalfa/web/app.py
import streamlit as st
import importlib

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Proyecto α - Termodinámica",
    layout="wide",
    page_icon="α",
    initial_sidebar_state="expanded"
)

# --- ÍNDICE DEL LIBRO (FIJO Y PEDAGÓGICO) ---
CAPITULOS_LIBRO = [
    ("Capítulo 1", "La matriz energética argentina: potencia, recursos y restricciones"),
    ("Capítulo 2", "Conservación de masa y energía en sistemas abiertos (caso Yacyretá)"),
    ("Capítulo 3", "El límite de la conversión: ciclo de potencia real vs. ideal (caso Central Térmica Luján de Cuyo)"),
    ("Capítulo 4", "Irreversibilidades: el costo de la transformación real (caso Turbina de vapor)"),
    ("Capítulo 5", "Mejoras al ciclo Rankine y análisis exergético (caso Centrales termoeléctricas avanzadas)"),
    ("Capítulo 6", "Combustión y ciclos de gas: nueva sustancia, mismos principios (caso Turbina de gas)"),
    ("Capítulo 7", "Integración exergética: ciclos combinados (caso Central de ciclo combinado)"),
    ("Capítulo 8", "Recursos variables: límites físicos de la conversión renovable"),
    ("Capítulo 9", "Metodología del análisis termodinámico aplicado"),
    ("Capítulo 10", "Diseñar la matriz energética del futuro")
]

# --- SIDEBAR: NAVEGACIÓN PRINCIPAL ---
with st.sidebar:
    st.title("Proyecto α")
    st.markdown(
        """
        <div style="text-align: justify; font-style: italic; font-weight: bold; 
                    font-size: 1.1em; color: #808495; line-height: 1.3;">
            Termodinámica de la Conversión de Energía en Argentina
        </div>
        """,
        unsafe_allow_html=True
    )
    st.divider()

    # Construir opciones de menú
    opciones_menu = [
        "🏠 Inicio",
        "⚙️ Calculadora de Propiedades"
    ]
    
    for i, (cap_num, titulo) in enumerate(CAPITULOS_LIBRO, start=1):
        display = f"{i}. {titulo[:50]}..." if len(titulo) > 50 else f"{i}. {titulo}"
        opciones_menu.append(display)
    
    opciones_menu.extend(["🔍 Wiki", "👤 Autor"])

    opcion = st.radio(
        label="Navegación Principal:",
        options=opciones_menu,
        help="Seleccione una sección para cambiar el contenido principal."
    )
    st.divider()
    st.caption("⚡ Soberanía Educativa y Tecnológica")

# --- ENRUTAMIENTO DE CONTENIDO ---
if opcion == "🏠 Inicio":
    from modules.inicio import mostrar_inicio
    mostrar_inicio()

elif opcion == "⚙️ Calculadora de Propiedades":
    from modules.laboratorio import mostrar_laboratorio
    mostrar_laboratorio()

elif opcion == "🔍 Wiki":
    from modules.wiki import main as wiki_main
    wiki_main()

elif opcion == "👤 Autor":
    from modules.autor import mostrar_autor
    mostrar_autor()

# --- CAPÍTULOS 1 A 10: CARGA DINÁMICA ---
elif opcion.startswith(tuple(f"{i}." for i in range(1, 11))):
    try:
        num_str = opcion.split(".")[0]
        num = int(num_str)
        cap_nombre, cap_titulo = CAPITULOS_LIBRO[num - 1]
        
        st.title(f"📘 {cap_titulo}")
        st.divider()
        
        # Cargar capX_main.render() desde modules.capituloX
        modulo_nombre = f"modules.capitulo{num}.cap{num}_main"
        try:
            modulo = importlib.import_module(modulo_nombre)
            importlib.reload(modulo)
            if hasattr(modulo, 'render'):
                modulo.render()
            else:
                st.info("🛠️ Contenido interactivo en desarrollo.")
        except ImportError:
            st.info("🛠️ Contenido interactivo en desarrollo.")
            
    except Exception as e:
        st.error(f"Error al cargar el capítulo: {e}")

else:
    st.info("Seleccione una opción del menú.")