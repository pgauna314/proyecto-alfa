import streamlit as st
import os

def mostrar_autor():
    st.title("👤 Verificación de Carpeta Assets")

    # 1. Intentamos mostrar la foto
    nombre_archivo = "autor.jpg"
    
    # Lista de posibles lugares donde puede estar la foto
    rutas = [
        f"web/assets/{nombre_archivo}",
        f"assets/{nombre_archivo}",
        nombre_archivo
    ]

    encontrada = False
    for r in rutas:
        if os.path.exists(r):
            st.success(f"✅ Foto encontrada en: {r}")
            st.image(r, width=300)
            encontrada = True
            break

    if not encontrada:
        st.error("❌ No se encuentra 'autor.jpg' en ninguna ruta conocida.")
        
        # 2. DEBUG: Vamos a ver qué carpetas existen realmente
        st.write("### Diagnóstico de carpetas:")
        st.write("Directorios presentes:", os.listdir("."))
        
        if os.path.exists("web"):
            st.write("Contenido de 'web/':", os.listdir("web"))
            if os.path.exists("web/assets"):
                st.write("Contenido de 'web/assets/':", os.listdir("web/assets"))

