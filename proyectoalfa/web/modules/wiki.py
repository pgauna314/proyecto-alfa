import streamlit as st
from pathlib import Path

def main():
    st.title("📚 Wiki")
    st.markdown("Explorá la historia y tecnología de las centrales eléctricas argentinas.")

    # Determinar la ruta base del proyecto
    # Este archivo está en /proyectomayer/modules/wiki.py
    # Queremos llegar a /proyectomayer/wiki_data/
    base_dir = Path(__file__).parent.parent  # Sube a /proyectomayer
    wiki_content_dir = base_dir / "wiki_data"

    # Depuración opcional (se puede quitar luego)
    with st.sidebar:
        st.info(f"📂 Directorio de wiki: `{wiki_content_dir.resolve()}`")
        st.write("---")
        st.subheader("🔍 Entradas disponibles")

    # Mapeo de entradas (rutas relativas a wiki_data/)
    entries = {
        "Río Turbio": "centrales/rio-turbio.md",
        # Agregá más entradas aquí
    }

    selected = st.selectbox("Seleccioná una entrada", list(entries.keys()))
    
    # Construir la ruta absoluta al archivo
    file_path = wiki_content_dir / entries[selected]

    if file_path.exists():
        try:
            content = file_path.read_text(encoding="utf-8")
            st.markdown(content)
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
    else:
        st.error("❌ Archivo no encontrado.")
        st.code(f"Ruta buscada:\n{file_path.resolve()}", language="text")
        if wiki_content_dir.exists():
            st.write("Archivos en el directorio:")
            st.write([f.name for f in wiki_content_dir.rglob("*") if f.is_file()])
        else:
            st.warning("⚠️ El directorio `wiki_data` no existe.")