import streamlit as st
import os

def mostrar_autor():
    st.title("👤 Sobre el Autor y el Proyecto")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Buscamos la imagen en la carpeta assets
        # 'web/assets/autor.jpg' si estás ejecutando desde la raíz
        ruta_foto = "web/assets/fotoGauna2.jpg" 
        
        if os.path.exists(ruta_foto):
            st.image(ruta_foto, width=250, caption="Ing. Tu Nombre")
        else:
            # Si la foto no carga, ponemos un avatar por defecto
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=200)
    
    with col2:
        # Acá va tu bio...
        st.subheader("Tu Nombre")
        st.write("Escribe aquí tu trayectoria y visión...")
        
        st.markdown("### Contacto y Redes")
        st.write("📩 [tu@email.com](mailto:tu@email.com)")
        st.write("🔗 [LinkedIn / Portfolio](https://linkedin.com)")

    st.divider()
    
    st.subheader("La Visión del Proyecto")
    st.info("""
    "La ingeniería no se aprende solo leyendo, se aprende rompiendo y reconstruyendo balances." 
    Este entorno interactivo es el resultado de buscar una pedagogía 4.0 para la ingeniería nuclear argentina.
    """)


