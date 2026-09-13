import streamlit as st

st.set_page_config(
    page_title="Calculadora FA - Screening HPP",
    page_icon="🩺",
    layout="centered"
)

# Advertencia de uso profesional
st.warning("""
**⚠️ ADVERTENCIA DE USO PROFESIONAL**

Esta aplicación es una herramienta de apoyo y consulta diseñada **exclusivamente para el personal médico y los profesionales de la salud especializados**. 

* No constituye una guía de autodiagnóstico ni sustituye el criterio médico individualizado.
* Los resultados deben correlacionarse con el cuadro clínico, la historia clínica del paciente y los rangos de referencia analíticos del laboratorio local.
""")

st.title("🩺 Vigilancia de niveles de Fosfatasa Alcalina (FA)")
st.caption("🔒 **100% Anónimo:** Esta herramienta no almacena ni transmite ningún dato del paciente.")

st.markdown("""
Esta herramienta evalúa si el nivel de fosfatasa alcalina (FA) en sangre está **anormalmente bajo** 
para la edad y sexo del paciente, lo cual es un criterio bioquímico clave para la sospecha de **Hipofosfatasia (HPP)**.
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
        días = edad * 30.4375
    elif unidad == "Años":
        días = edad * 365.25

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
    st.info(f"**Rango de referencia esperado:** {fa_min} - {fa_max} IU/L (para {sexo.lower()}, {edad_valor} {edad_unidad.lower()})")
    
    if fa_valor < fa_min:
        st.error(f"🔴 **VALOR ANORMALMENTE BAJO:** {fa_valor} IU/L")
        st.markdown("""
        **Atención clínica:**
        * Se requiere confirmar con al menos **dos mediciones distintas** de FA persistentemente bajas.
        * Evaluar presencia de criterios mayores/menores de **Hipofosfatasia (HPP)**.
        * Descartar las causas secundarias de FA baja que se muestran a continuación.
        """)
    elif fa_valor > fa_max:
        st.warning(f"🟡 **VALOR ELEVADO:** {fa_valor} IU/L")
        st.write("El valor se encuentra por encima del límite superior ajustado para la edad y sexo.")
    else:
        st.success(f"🟢 **VALOR NORMAL:** {fa_valor} IU/L")
        st.write("El valor se encuentra dentro del rango de referencia biológico esperado.")

st.divider()

# --- DIAGNÓSTICO DIFERENCIAL COMPLETO (TABLA 4 DEL CONSENSO) ---
st.subheader("📋 Diagnósticos Diferenciales (Tabla 4: Causas de FA Baja)")
st.write("Seleccione cualquier causa de la clasificación oficial para revisar la orientación clínica:")

causas_secundarias = {
    "Ninguna / Evaluación General": """Seleccione una condición de la lista para ver la orientación clínica correspondiente.""",
    
    # Persistentemente bajas
    "[PERSISTENTE] Hipofosfatasia (HPP)": """Causada por variantes patogénicas en el gen ALPL. Cursa con acumulación de sustratos (PPi, PLP, PEA) y síntomas esqueléticos/dentales.""",
    "[PERSISTENTE] Displasia Cleidocraneal": """Trastorno genético del desarrollo óseo con reducción persistente de los niveles de FA.""",
    "[PERSISTENTE] Hipofosfatasemia Familiar Benigna": """Condición hereditaria benigna con valores reducidos de FA sin compromiso óseo ni dental sintomático.""",
    "[PERSISTENTE] Enfermedad Articular de Mseleni": """Osteoartropatía endémica genéticamente asociada a reducciones en la enzima.""",

    # Temporalmente bajas - Endocrinas y Metabólicas Óseas
    "[TEMPORAL] Hipotiroidismo Severo": """El déficit de hormonas tiroideas disminuye la tasa general de recambio óseo y la expresión de FA por osteoblastos.""",
    "[TEMPORAL] Síndrome de Cushing": """El exceso de glucocorticoides endógenos o exógenos inhibe la función y diferenciación osteoblástica.""",
    "[TEMPORAL] Osteogénesis Imperfecta (Tipo II)": """Forma severa perinatal de fragilidad ósea que cursa con baja actividad de remodelación.""",
    "[TEMPORAL] Enfermedad Ósea Adinámica": """Estado de muy baja remodelación ósea, común en pacientes con enfermedad renal crónica.""",

    # Temporalmente bajas - Nutricionales y Digestivas
    "[TEMPORAL] Deficiencia de Zinc": """El zinc es un cofactor catiónico indispensable para la estructura y estabilidad de la enzima FA.""",
    "[TEMPORAL] Deficiencia de Magnesio": """El magnesio es un cofactor esencial para la activación catalítica de la TNSALP. Su déficit reduce la lectura.""",
    "[TEMPORAL] Deficiencia de Vitamina C (Escorbuto)": """Alteración en la síntesis de la matriz de colágeno y reducción en la actividad enzimática.""",
    "[TEMPORAL] Intoxicación por Vitamina D": """La hipercalcemia severa resultante suprime fuertemente la remodelación ósea y la síntesis de FA.""",
    "[TEMPORAL] Inanición / Malnutrición Severa": """La deficiencia global de sustratos y aminoácidos limita la producción y síntesis hepática/ósea de FA.""",
    "[TEMPORAL] Síndrome de Leche-Álcali": """La hipercalcemia y alcalosis metabólica suprimen el recambio óseo.""",
    "[TEMPORAL] Enfermedad Celíaca": """La malabsorción intestinal crónica limita la disponibilidad de zinc, magnesio y otros cofactores esenciales.""",

    # Temporalmente bajas - Fármacos
    "[TEMPORAL] Bifosfonatos (Alendronato, Zoledronato, etc.)": """La terapia anti-resortiva potente suprime la remodelación ósea y disminuye marcadamente la FA circulante.""",
    "[TEMPORAL] Denosumab": """Inhibidor del RANKL que reduce drásticamente el recambio óseo y los marcadores enzimáticos.""",
    "[TEMPORAL] Glucocorticoides": """Inhibición directa sobre la función osteoblástica y síntesis proteica.""",
    "[TEMPORAL] Quimioterapia Antineoplásica": """Toxicidad o supresión celular sobre tejidos con alta tasa de síntesis proteica.""",
    "[TEMPORAL] Clofibrato": """Fármaco hipolipemiante con efecto documentado en la disminución de los niveles plasmáticos de FA.""",
    "[TEMPORAL] Tamoxifeno": """Modulador selectivo del receptor de estrógeno con efecto de reducción en el recambio óseo en ciertos contextos.""",

    # Temporalmente bajas - Hematológicas y Sistémicas
    "[TEMPORAL] Anemia Perniciosa / Déficit Severo B12": """Disminución en la síntesis y actividad celular por déficit de cobalamina.""",
    "[TEMPORAL] Anemia Severa": """La hipoxia tisular crónica y la reducción funcional de la perfusión alteran los niveles circulantes.""",
    "[TEMPORAL] Mieloma Múltiple": """Infiltración medular y supresión del componente osteoblástico normal.""",
    "[TEMPORAL] Transfusión Sanguínea Masiva": """El citrato anticoagulante de los hemoderivados quela el zinc y el magnesio, reduciendo artificialmente la medición analítica.""",
    "[TEMPORAL] Cirugía de Bypass Cardíaco": """La circulación extracorpórea causa hemodilución e inactivación enzimática transitoria.""",
    "[TEMPORAL] Enfermedad de Wilson / Hemocromatosis": """La acumulación tóxica de metales (cobre o hierro) interfiere con el centro catalítico de la enzima.""",
    "[TEMPORAL] Intoxicación por Metales Pesados Radiactivos": """Inhibición de la síntesis o inactivación del centro enzimático activo por metales pesados.""",

    # Factores Preanalíticos y Errores
    "[LABORATORIO] Muestra con Anticoagulante EDTA u Oxalato": """Falso positivo analítico: El EDTA/oxalato quela los iones Mg y Zn de la muestra, anulando la medición enzimática.""",
    "[LABORATORIO] Rangos de Referencia Inadecuados": """Uso de límites de referencia de adultos para evaluar a la población pediátrica, o falta de ajuste específico por edad y sexo."""
}

causa_seleccionada = st.selectbox("Seleccionar Condición / Causa Diferencial:", list(causas_secundarias.keys()))

if causa_seleccionada != "Ninguna / Evaluación General":
    st.info(f"**Orientación sobre {causa_seleccionada}:**\n\n{causas_secundarias[causa_seleccionada]}")

st.divider()

# Referencia Bibliográfica
st.markdown("""
**Referencia de Criterios y Rangos de Referencia:**
* *Diagnosis, treatment, and follow-up of patients with hypophosphatasia.* **Endocrine**, 87(2), 400-419 (2025). DOI: [10.1007/s12020-024-04054-1](https://doi.org/10.1007/s12020-024-04054-1)
""")

st.caption("⚠️ **Aviso legal:** Herramienta estrictamente reservada para profesionales de la salud capacitados para la interpretación clínica de pruebas de laboratorio.")
