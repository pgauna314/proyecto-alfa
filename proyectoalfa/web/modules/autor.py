import streamlit as st
from pathlib import Path

def mostrar_autor():
    """Muestra la información del autor con su foto."""
    
    st.title("👨‍💻 Autor del Proyecto α")
    st.divider()
    
    # --- RUTA A LA FOTO ---
    # Navega desde modules/ hasta web/, luego a assets/autor.jpg
    directorio_base = Path(__file__).parent.parent
    ruta_foto = directorio_base / "assets" / "autor.jpg"
    
    # --- COLUMNAS CON DISEÑO MEJORADO ---
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader("")
        try:
            # Estilo CSS para imagen redondeada con borde
            st.markdown("""
            <style>
                .autor-foto {
                    border-radius: 15px;
                    border: 3px solid #4CAF50;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    display: block;
                    margin: 0 auto;
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Mostrar imagen con estilo
            st.image(
                str(ruta_foto),
                caption="",
                width=250,
                output_format="auto",
                use_container_width=False
            )
            
        except FileNotFoundError:
            # Mensaje si la foto no existe
            st.error("⚠️ No se encontró la foto del autor.")
            st.info("Asegúrate de que el archivo 'autor.jpg' esté en la carpeta 'web/assets/'")
            st.markdown("""
            <div style='text-align: center; padding: 20px; border: 2px solid #4CAF50; 
                        border-radius: 10px; background-color: #f0f8ff;'>
            <span style='font-size: 50px;'>📷</span><br>
            <strong>Foto del autor</strong><br>
            <small>(Lugar para tu foto)</small>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al cargar la imagen: {e}")
    
    with col2:
        st.subheader("Dr. Pablo Gauna")
        st.markdown("""
        **📧 Contacto:** pgauna@campus.ungs.edu.ar  
        **🐙 GitHub:** [pgauna314](https://github.com/pgauna314)  
        **🎓 Formación:** Doctor en Ingeniería - Ingeniero Químico 
        
        **📍 Ubicación:** Universidad Nacional de General Sarmiento, Argentina.
        
        ---
        
        ### 🔧 Tecnologías utilizadas
        - **Frontend:** Streamlit, Plotly
        - **Análisis de datos:** Pandas, NumPy
        - **Termodinámica:** CoolProp
        - **Control de versiones:** Git, GitHub
        """)
    
    st.divider()
    
    # Sección de motivación
    st.markdown("""
    ### 🚀 Motivación del Proyecto
    
    Este proyecto nace de la necesidad de contar con **herramientas educativas propias** 
    para el estudio de la termodinámica, adaptadas a la realidad energética argentina.
    
    **Objetivos principales:**
    
    1.  **📚 Crear software educativo libre y accesible** - Democratizar el acceso a 
        herramientas de cálculo termodinámico.
    2.  **🏭 Contextualizar la teoría con casos de centrales argentinas** - Vincular 
        conceptos abstractos con aplicaciones reales de nuestra industria.
    3.  **🎓 Promover la soberanía tecnológica en la formación de ingenieros** - 
        Desarrollar capacidades locales para la creación de herramientas técnicas.
    4.  **🌐 Construir una comunidad de aprendizaje colaborativo** - Fomentar el 
        intercambio de conocimiento sobre energía en Argentina.
    
    ### 💡 Filosofía
    
    > "No podemos depender únicamente de manuales extranjeros que ignoran 
    > nuestra matriz energética. La termodinámica se aprende aplicándola 
    > a casos reales de nuestra industria: **Río Turbio, Yacyretá, Cañadón León**, 
    > no solo a ciclos teóricos descontextualizados."
    
    ---
    
    ### 📈 Próximos desarrollos
    
    - **Simulador de ciclos combinados** para centrales de alta eficiencia
    - **Base de datos** de propiedades de combustibles argentinos
    - **Análisis de impacto ambiental** integrado en los balances energéticos
    - **Módulo didáctico** para instituciones educativas
    """)
    
    # Pie de página con contacto
    st.divider()
    col_contacto1, col_contacto2, col_contacto3 = st.columns(3)
    with col_contacto1:
        st.markdown("**📧 Contacto rápido**")
        st.write("pgauna314@gmail.com")
    with col_contacto2:
        st.markdown("**🐙 Contribuciones**")
        st.write("[GitHub Issues](https://github.com/pgauna314/proyecto-alfa/issues)")
    with col_contacto3:
        st.markdown("**📚 Recursos**")
        st.write("[Documentación técnica](#)")

if __name__ == "__main__":
    # Para probar este módulo de forma independiente
    mostrar_autor()