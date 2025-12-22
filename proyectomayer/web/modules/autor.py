import streamlit as st
import os

def mostrar_autor():
    st.title("👤 Sobre el Autor")
    
    # Esta es la ruta estándar que debería funcionar ahora que limpiaste el repo
    # Probamos con y sin el prefijo de la carpeta principal
    rutas_a_probar = [
        "web/assets/autor.jpg",
        "proyectomayer/web/assets/autor.jpg",
        "assets/autor.jpg"
    ]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        exito = False
        for ruta in rutas_a_probar:
            if os.path.exists(ruta):
                st.image(ruta, width=250, caption="Ing. Gauna")
                exito = True
                break
        
        if not exito:
            # Si aún no la encuentra, ponemos el avatar por defecto
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=200)
            st.warning("Subí la foto a 'web/assets/autor.jpg'")
            
    with col2:
        st.header("Dr. Gauna")
        st.markdown("""
        **Autor del Proyecto MAYER** Doctor en Ingeniería - Mención Tecnologías Químicas por la Universidad Tecnológica Nacional - Facultad Regional Buenos Aires. Ingeniero Químico.
        
        Este entorno digital es el soporte interactivo del libro sobre la 
        **Central Nuclear Atucha II**, diseñado para facilitar el cálculo de 
        balances de masa y energía de forma dinámica.
        """)
        
        st.divider()
        st.write("📩 **Contacto:** [tu-email@correo.com](mailto:tu-email@correo.com)")
        st.write("🔗 **LinkedIn:** [Perfil Profesional](https://linkedin.com)")

    st.divider()
    st.info("💡 **Dato:** Podés navegar a la sección 'Capítulo II' para ver los cálculos en acción.")

