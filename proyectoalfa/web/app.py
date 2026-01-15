import streamlit as st
import os
import importlib

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Proyecto α - Termodinámica",
    layout="wide",
    page_icon="α",
    initial_sidebar_state="expanded"
)

# --- LÓGICA DE DETECCIÓN Y FORMATEO ---
def obtener_capitulos():
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(ruta_actual, "modules", "book_support")
    
    if not os.path.exists(base_path):
        return {}
    
    try:
        contenido = os.listdir(base_path)
        carpetas = [d for d in contenido 
                    if os.path.isdir(os.path.join(base_path, d)) and d.startswith("capitulo")]
        
        carpetas_ordenadas = sorted(carpetas, key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
        
        dict_caps = {}
        for c in carpetas_ordenadas:
            num = ''.join(filter(str.isdigit, c))
            nombre_lindo = f"Capítulo {num}"
            dict_caps[nombre_lindo] = c
            
        return dict_caps
    except Exception:
        return {}

# --- SIDEBAR (Navegación de Alto Nivel) ---
with st.sidebar:
    # H1 para el lector de pantalla
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
    
    opcion = st.radio(
        label="Navegación Principal:",
        options=["🏠 Inicio", "📊 Matriz Energética Nacional", "⚙️ Calculadora de Propiedades", "📚 Soporte de Libro", "🔍 Wiki", "👤 Autor"],
        help="Seleccione una sección para cambiar el contenido principal de la pantalla."
    )
    st.divider()
    st.caption("⚡ Soberanía Educativa y Tecnológica")

# --- ENRUTADOR DE CONTENIDO ---
if opcion == "📚 Soporte de Libro":
    # Encabezado principal de la sección
    st.title("📚 Soporte de Libro")
    st.markdown("""
    > **Bienvenido a la sección de apoyo pedagógico.** Aquí vas a encontrar material de soporte del libro como simulaciones interactivas y ejemplos resueltos.
    """)
    st.divider()

    dict_caps = obtener_capitulos()
    
    if dict_caps:
        nombres_lindos = ["--- Selecciona una unidad temática ---"] + list(dict_caps.keys())
        
        col_sel, _ = st.columns([1, 1])
        with col_sel:
            # Accesibilidad: Etiqueta clara e instrucción de ayuda
            seleccion_visual = st.selectbox(
                label="Explorar contenido técnico por unidad:", 
                options=nombres_lindos,
                help="Al seleccionar un capítulo, se cargará automáticamente el material didáctico debajo."
            )
        
        if seleccion_visual != "--- Selecciona una unidad temática ---":
            #st.header(f"📖 {seleccion_visual}")
            #st.divider()

            nombre_carpeta = dict_caps[seleccion_visual]
            try:
                # Extraemos el número de la carpeta (ej: '2' de 'capitulo2')
                numero = ''.join(filter(str.isdigit, nombre_carpeta))
                
                # CAMBIO CLAVE: Ahora buscamos el archivo capX_main
                if numero:
                    ruta_importacion = f"modules.book_support.{nombre_carpeta}.cap{numero}_main"
                else:
                    # Por si tenés carpetas sin número, busca un main.py genérico
                    ruta_importacion = f"modules.book_support.{nombre_carpeta}.main"
                    
                cap_modulo = importlib.import_module(ruta_importacion)
                importlib.reload(cap_modulo)
                
                # Ejecución del contenido principal del capítulo
                cap_modulo.render() 
                
            except Exception as e:
                st.error(f"Error al cargar {seleccion_visual}: {e}")
                st.info(f"Asegurate de que el archivo se llame cap{numero}_main.py")
        else:
            st.info("💡 Por favor, selecciona una unidad del menú superior para desplegar el material de estudio.")
    else:
        st.warning("No se detectaron carpetas de capítulos.")

# --- RESTO DE SECCIONES ---
elif opcion == "🏠 Inicio":
    from modules.inicio import mostrar_inicio
    mostrar_inicio()
elif opcion == "📊 Matriz Energética Nacional":
    from modules.matriz import mostrar_matriz
    mostrar_matriz()
elif opcion == "⚙️ Calculadora de Propiedades":
    from modules.laboratorio import mostrar_laboratorio
    mostrar_laboratorio()
elif opcion == "🔍 Wiki":
    from modules.wiki import main as wiki_main
    wiki_main()
elif opcion == "👤 Autor":
    from modules.autor import mostrar_autor
    mostrar_autor()