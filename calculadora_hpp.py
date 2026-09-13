import streamlit as st

st.set_page_config(
    page_title="Calculadora FA - Screening HPP",
    page_icon="🩺",
    layout="centered"
)

# Advertencia / Disclaimer de uso exclusivo para personal médico
st.warning("""
**⚠️ ADVERTENCIA DE USO PROFESIONAL**

Esta aplicación es una herramienta de apoyo y consulta diseñada **exclusivamente para uso por personal médico y profesional de la salud especializado**. 

* No constituye una guía de auto-diagnóstico ni sustituye el criterio médico individualizado.
* Los resultados deben correlacionarse con el cuadro clínico, la historia del paciente y los rangos de referencia analíticos del laboratorio local[cite: 1].
""")

st.title("🩺 Calculadora de Fosfatasa Alcalina (FA)")
st.caption("🔒 **100% Anónimo:** Esta herramienta no almacena ni transmite ningún dato del paciente.")

st.markdown("""
Esta herramienta evalúa si el nivel de Fosfatasa Alcalina (FA) en sangre está **anormalmente bajo** 
para la edad y sexo del paciente, lo cual es un criterio bioquímico clave para la sospecha de **Hipofosfatasia (HPP)**[cite: 1].
""")

st.divider()

st.subheader("Datos del Paciente")

col1, col2 = st.columns(2)

with col1:
    edad_valor = st.number_input("Edad", min_value=0.0, max_value=120.0, value=5.0, step=1.0)
    sexo = st.selectbox("Sexo biológico", ["Masculino", "Femenino"])

with col2:
    edad_unidad = st.selectbox("Unidad de tiempo", ["Años", "Meses", "Días"])
    fa_valor = st.number_input("Fosfatasa Alcalina (IU/L)", min_value=0.0, max_value=3000.0, value=45.0, step=1.0)

def obtener_rango_fa(edad, unidad, sexo_biologico):
    dias = edad
    if unidad == "Meses":
        dias = edad * 30.4375
    elif unidad == "Años":
        dias = edad * 365.25

    if dias <= 14:
        return 90, 273
    elif dias <= 365:
        return 134, 518
    elif dias <= 3652.5:
        return 156, 369
    elif dias <= 4748.25:
        return 141, 460
    elif dias <= 5478.75:
        return (127, 517) if sexo_biologico == "Masculino" else (62, 280)
    elif dias <= 6209.25:
        return (89, 365) if sexo_biologico == "Masculino" else (54, 128)
    elif dias <= 6939.75:
        return (59, 164) if sexo_biologico == "Masculino" else (48, 95)
    else:
        return 40, 150

if st.button("Evaluar Resultado", type="primary"):
    fa_min, fa_max = obtener_rango_fa(edad_valor, edad_unidad, sexo)
    
    st.subheader("Resultado de la Evaluación")
    st.info(f"**Rango de referencia esperado:** {fa_min} - {fa_max} IU/L (para {sexo.lower()}, {edad_valor} {edad_unidad.lower()})[cite: 1]")
    
    if fa_valor < fa_min:
        st.error(f"🔴 **VALOR ANORMALMENTE BAJO:** {fa_valor} IU/L")
        st.markdown(f"""
        **Atención clínica:**
        * Se requiere confirmar con al menos **dos mediciones distintas** de FA persistentemente bajas[cite: 1].
        * Se recomienda descartar otras causas secundarias de FA baja (ej. uso de bifosfonatos, deficiencia de zinc/magnesio, hipotiroidismo, etc.)[cite: 1].
        * Evaluar presencia de criterios mayores/menores de **Hipofosfatasia (HPP)**[cite: 1].
        """)
    elif fa_valor > fa_max:
        st.warning(f"🟡 **VALOR ELEVADO:** {fa_valor} IU/L")
        st.write("El valor se encuentra por encima del límite superior ajustado para la edad y sexo[cite: 1].")
    else:
        st.success(f"🟢 **VALOR NORMAL:** {fa_valor} IU/L")
        st.write("El valor se encuentra dentro del rango de referencia biológico esperado[cite: 1].")

st.divider()
st.caption("⚠️ **Aviso legal:** Herramienta reservada estrictamente a profesionales de la salud capacitados para la interpretación clínica de pruebas de laboratorio[cite: 1].")
