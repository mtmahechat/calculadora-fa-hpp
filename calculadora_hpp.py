import streamlit as st

st.set_page_config(
    page_title="Calculadora FA - Screening HPP",
    page_icon="🩺",
    layout="centered"
)

# Advertencia de uso profesional
st.warning("""
**⚠️ ADVERTENCIA DE USO PROFESIONAL**

Esta aplicación es una herramienta de apoyo y consulta diseñada **exclusivamente para uso por personal médico y profesional de la salud especializado**. 

* No constituye una guía de auto-diagnóstico ni sustituye el criterio médico individualizado.
* Los resultados deben correlacionarse con el cuadro clínico, la historia del paciente y los rangos de referencia analíticos del laboratorio local.
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
        st.markdown("""
        **Atención clínica:**
        * Se requiere confirmar con al menos **dos mediciones distintas** de FA persistentemente bajas[cite: 1].
        * Evaluar presencia de criterios mayores/menores de **Hipofosfatasia (HPP)**[cite: 1].
        * Descartar las causas secundarias de FA baja que se muestran a continuación[cite: 1].
        """)
    elif fa_valor > fa_max:
        st.warning(f"🟡 **VALOR ELEVADO:** {fa_valor} IU/L")
        st.write("El valor se encuentra por encima del límite superior ajustado para la edad y sexo[cite: 1].")
    else:
        st.success(f"🟢 **VALOR NORMAL:** {fa_valor} IU/L")
        st.write("El valor se encuentra dentro del rango de referencia biológico esperado[cite: 1].")

st.divider()

# --- DIAGNÓSTICO DIFERENCIAL DE CAUSAS SECUNDARIAS ---
st.subheader("📋 Diagnósticos Diferenciales (Causas Secundarias de FA Baja)")
st.write("Seleccione una causa secundaria para consultar sus características o descartarla durante la evaluación[cite: 1]:")

causas_secundarias = {
    "Ninguna / Evaluación General": """Seleccione una condición de la lista para ver la orientación clínica correspondiente.""",
    "Uso de Bifosfonatos": """El tratamiento previo o actual con anti-resortivos (ej. alendronato, zoledronato) suprime fuertemente la remodelación ósea y reduce la FA circulante[cite: 1].""",
    "Deficiencia de Zinc": """El zinc es un cofactor enzimático indispensable para la estructura y función de la fosfatasa alcalina. Su deficiencia disminuye la actividad sintética de la enzima[cite: 1].""",
    "Deficiencia de Magnesio": """El magnesio es un cofactor esencial para la activación catalítica de la TNSALP. Niveles séricos bajos de Mg reducen la lectura analítica de la FA[cite: 1].""",
    "Intoxicación por Vitamina D": """Niveles muy elevados de vitamina D o hipercalcemia severa pueden generar supresión de la remodelación ósea y disminución secundaria de la FA[cite: 1].""",
    "Hipotiroidismo Severo": """El déficit de hormonas tiroideas disminuye la tasa general de recambio óseo y la síntesis de FA por parte de los osteoblastos[cite: 1].""",
    "Anemia Severa / Enfermedad Celíaca": """La malabsorción intestinal crónica o estados de desnutrición severa limitan la disponibilidad de cofactores esenciales para la enzima[cite: 1].""",
    "Síndrome de Cushing": """El exceso de glucocorticoides endógenos o exógenos inhíbe la función osteoblástica y la expresión de la fosfatasa alcalina[cite: 1].""",
    "Transfusión Sanguínea Masiva": """El citrato utilizado como anticoagulante en los hemoderivados quela los cationes divalentes (Mg y Zn) necesarios para la lectura de la FA."""
}

causa_seleccionada = st.selectbox("Seleccionar Condición / Causa Secundaria:", list(causas_secundarias.keys()))

if causa_seleccionada != "Ninguna / Evaluación General":
    st.info(f"**Orientación sobre {causa_seleccionada}:**\n\n{causas_secundarias[causa_seleccionada]}")

st.divider()

# Referencia Bibliográfica
st.markdown("""
**Referencia de Criterios y Rangos de Referencia:**
* *Diagnosis, treatment, and follow-up of patients with hypophosphatasia.* **Endocrine**, 87(2), 400-419 (2025). DOI: [10.1007/s12020-024-04054-1](https://doi.org/10.1007/s12020-024-04054-1)[cite: 1]
""")

st.caption("⚠️ **Aviso legal:** Herramienta reservada estrictamente a profesionales de la salud capacitados para la interpretación clínica de pruebas de laboratorio[cite: 1].")
