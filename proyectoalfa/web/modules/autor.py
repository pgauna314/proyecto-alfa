<<<<<<< HEAD
import streamlit as st
import os

def mostrar_autor():
    st.title("👤 Autor")
    
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
                st.image(ruta, width=250, caption="Dr. Gauna")
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

=======
import streamlit as st

def mostrar_autor():
    st.title("👨‍💻 Autor del Proyecto α")
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 15px; border: 2px solid #4CAF50; border-radius: 10px;'>
        <span style='font-size: 60px;'>👤</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Pablo Gauna")
        st.markdown("""
        **📧 Contacto:** pgauna314@gmail.com  
        **🐙 GitHub:** [pgauna314](https://github.com/pgauna314)  
        **🎓 Formación:** Ingeniería en Energía  
        **📍 Ubicación:** Argentina
        """)
    
    st.divider()
    
    st.markdown("""
    ### 🚀 Motivación del Proyecto
    
    Este proyecto nace de la necesidad de contar con **herramientas educativas propias** 
    para el estudio de la termodinámica, adaptadas a la realidad energética argentina.
    
    **Objetivos principales:**
    1. Crear software educativo libre y accesible
    2. Contextualizar la teoría con casos de centrales argentinas
    3. Promover la soberanía tecnológica en la formación de ingenieros
    
    ### 💡 Filosofía
    > "No podemos depender únicamente de manuales extranjeros que ignoran 
    > nuestra matriz energética. La termodinámica se aprende aplicándola 
    > a casos reales de nuestra industria."
    """)
>>>>>>> 1a24feb0dbd31b1b70938b2c48315a35e76f7756
