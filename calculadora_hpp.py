import streamlit as st

st.set_page_config(
    page_title="Calculadora FA & Guía Paraclínica HPP",
    page_icon="🩺",
    layout="centered"
)

# Advertencia de uso profesional
st.warning("""
**⚠️ ADVERTENCIA DE USO PROFESIONAL**

Esta aplicación es una herramienta de apoyo y consulta diseñada **exclusivamente para el personal médico y el profesional de la salud especializado**. 

* No constituye una guía de autodiagnóstico ni sustituye el criterio médico individualizado.
* Los resultados deben correlacionarse con el cuadro clínico, la historia clínica del paciente y los rangos de referencia analíticos del laboratorio local.
""")

st.title("🩺 Niveles de FA & Screening de HPP")
st.caption("🔒 **100% Anónimo:** Esta herramienta no almacena ni transmite ningún dato del paciente.")

# Organización mediante pestañas (Tabs)
tab_calculadora, tab_guia_paraclinica, tab_hpp_protocolo = st.tabs([
    "🧮 Calculadora de FA", 
    "🔬 Guía de Estudios Paraclínicos", 
    "🧬 Confirmación de HPP"
])

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

# ==========================================
# PESTAÑA 1: CALCULADORA Y EVALUACIÓN
# ==========================================
with tab_calculadora:
    st.markdown("""
    Evalúe si el nivel de fosfatasa alcalina (FA) en sangre está **anormalmente bajo** 
    para la edad y sexo del paciente, criterio bioquímico clave para la sospecha de **Hipofosfatasia (HPP)**.
    """)
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        edad_valor = st.number_input("Edad", min_value=0.0, max_value=120.0, value=5.0, step=1.0)
        sexo = st.selectbox("Sexo biológico", ["Masculino", "Femenino"])

    with col2:
        edad_unidad = st.selectbox("Unidad de tiempo", ["Años", "Meses", "Días"])
        fa_valor = st.number_input("Fosfatasa Alcalina (IU/L)", min_value=0.0, max_value=3000.0, value=45.0, step=1.0)

    if st.button("Evaluar Resultado", type="primary"):
        fa_min, fa_max = obtener_rango_fa(edad_valor, edad_unidad, sexo)
        
        st.subheader("Resultado de la Evaluación")
        st.info(f"**Rango de referencia esperado:** {fa_min} - {fa_max} IU/L (para {sexo.lower()}, {edad_valor} {edad_unidad.lower()})")
        
        if fa_valor < fa_min:
            st.error(f"🔴 **VALOR ANORMALMENTE BAJO:** {fa_valor} IU/L")
            st.markdown("""
            **Conducta clínica recomendada:**
            1. **Confirmación:** Repetir la toma en tubo seco (evitar EDTA) para confirmar FA persistentemente baja.
            2. **Descarte de causas secundarias:** Consulte la pestaña *Guía de Estudios Paraclínicos*.
            3. **Estudio específico de HPP:** Consulte la pestaña *Confirmación de HPP*.
            """)
        elif fa_valor > fa_max:
            st.warning(f"🟡 **VALOR ELEVADO:** {fa_valor} IU/L")
            st.write("El valor se encuentra por encima del límite superior ajustado para la edad y sexo.")
        else:
            st.success(f"🟢 **VALOR NORMAL:** {fa_valor} IU/L")
            st.write("El valor se encuentra dentro del rango de referencia biológico esperado.")

# ==========================================
# PESTAÑA 2: GUÍA DE PARACLÍNICOS
# ==========================================
with tab_guia_paraclinica:
    st.subheader("📋 Orientación Paraclínica según Causa Secundaria")
    st.write("Seleccione una condición sospechada para revisar el panel de estudios de laboratorio e imágenes recomendados:")

    estudios_causas = {
        # PERSISTENTES
        "[PERSISTENTE] Displasia Cleidocraneal": """
        **Mecanismo:** Trastorno genético del desarrollo óseo.
        
        **Estudios recomendados:**
        * **Serie radiológica ósea:** Rx de tórax/clavículas (hipoplasia o aplasia clavicular), Rx de cráneo (fontanelas abiertas, huesos wormianos).
        * **Estudio genético:** Mutación en el gen *RUNX2*.
        """,
        "[PERSISTENTE] Hipofosfatasemia Familiar Benigna": """
        **Mecanismo:** Condición hereditaria benigna sin compromiso sintomático.
        
        **Estudios recomendados:**
        * **FA en familiares de 1.º grado:** Medición sérica en padres/hermanos.
        * **Sustratos normales:** Niveles de PLP o de PEA dentro de los límites normales.
        """,
        "[PERSISTENTE] Enfermedad Articular de Mseleni": """
        **Mecanismo:** Osteoartropatía endémica.
        
        **Estudios recomendados:**
        * **Estudio radiológico articular:** Evaluación de osteoartropatía severa en las caderas y en las articulaciones periféricas.
        """,

        # TEMPORALES - ENDOCRINAS / METABÓLICAS ÓSEAS
        "[TEMPORAL] Hipotiroidismo Severo": """
        **Mecanismo:** Reducción de la tasa general de recambio óseo.
        
        **Estudios recomendados:**
        * **Perfil tiroideo completo:** TSH (elevada), T4 libre y T3 libre (disminuidas).
        """,
        "[TEMPORAL] Síndrome de Cushing": """
        **Mecanismo:** Inhibición de la función osteoblástica por exceso de glucocorticoides.
        
        **Estudios recomendados:**
        * **Cortisol libre en orina de 24 horas** o **Cortisol en saliva nocturna**.
        * **Prueba de supresión con 1 mg de dexametasona**.
        """,
        "[TEMPORAL] Osteogénesis Imperfecta (Tipo II)": """
        **Mecanismo:** Alta fragilidad ósea perinatal y baja remodelación ósea.
        
        **Estudios recomendados:**
        * **Estudio genético:** Genes *COL1A1* y *COL1A2*.
        * **Radiografías perinatales / Ecografía fetal:** Fracturas múltiples intrauterinas.
        """,
        "[TEMPORAL] Enfermedad Ósea Adinámica": """
        **Mecanismo:** Muy baja remodelación en la insuficiencia renal.
        
        **Estudios recomendados:**
        * **Paratohormona intacta (iPTH):** Típicamente baja o suprimida.
        * **Marcadores de remodelado óseo:** Osteocalcina, PINP, CTX-1 (reducidos).
        """,

        # TEMPORALES - NUTRICIONALES Y DIGESTIVAS
        "[TEMPORAL] Deficiencia de Zinc": """
        **Mecanismo:** El zinc es un cofactor estructural esencial de la enzima FA.
        
        **Estudios recomendados:**
        * **Zinc sérico o plasmático:** Disminuido.
        """,
        "[TEMPORAL] Deficiencia de Magnesio": """
        **Mecanismo:** El magnesio es un cofactor activador catalítico de la TNSALP.
        
        **Estudios recomendados:**
        * **Magnesio sérico y magnesio en orina de 24 h:** Disminuidos.
        """,
        "[TEMPORAL] Deficiencia de Vitamina C (Escorbuto)": """
        **Mecanismo:** Alteración en la síntesis del colágeno y de la matriz ósea.
        
        **Estudios recomendados:**
        * **Ácido ascórbico en plasma:** Niveles francamente disminuidos.
        """,
        "[TEMPORAL] Intoxicación por Vitamina D": """
        **Mecanismo:** Hipercalcemia severa que suprime la remodelación ósea.
        
        **Estudios recomendados:**
        * **25-OH vitamina D sérica:** Niveles elevadísimos (>100-150 ng/mL).
        * **Calcio y Fósforo séricos y urinarios:** Hipercalcemia e hipercalciuria.
        """,
        "[TEMPORAL] Inanición / Malnutrición Severa": """
        **Mecanismo:** Deficiencia global de sustratos proteicos para la síntesis enzimática.
        
        **Estudios recomendados:**
        * **Albúmina y prealbúmina séricas:** Disminuidas.
        * **Perfil proteico completo y reactivos de fase aguda.**
        """,
        "[TEMPORAL] Síndrome de Leche-Álcali": """
        **Mecanismo:** Hipercalcemia y alcalosis metabólica que suprimen la remodelación.
        
        **Estudios recomendados:**
        * **Gasometría (arterial/venosa):** Alcalosis metabólica.
        * **Calcio sérico (elevado)** y **PTH (suprimida)**.
        """,
        "[TEMPORAL] Enfermedad Celíaca": """
        **Mecanismo:** Malabsorción intestinal crónica de cofactores (Zn, Mg).
        
        **Estudios recomendados:**
        * **Anticuerpos IgA anti-transglutaminasa tisular (tTG-IgA)** e **IgA total**.
        * **Biopsia duodenal:** Si la serología es positiva.
        """,

        # TEMPORALES - FÁRMACOS
        "[TEMPORAL] Uso de bifosfonatos o denosumab": """
        **Mecanismo:** Potente supresión de la remodelación ósea.
        
        **Estudios recomendados:**
        * **Anamnesis farmacológica detallada.**
        * **Marcadores de recambio óseo (CTX, PINP):** Suprimidos.
        """,
        "[TEMPORAL] Uso de Glucocorticoides / Clofibrato / Tamoxifeno": """
        **Mecanismo:** Inhibición directa osteoblástica o metabólica.
        
        **Estudios recomendados:**
        * **Revisión de dosis y tiempo de exposición farmacológica.**
        """,

        # TEMPORALES - HEMATOLÓGICAS Y SISTÉMICAS
        "[TEMPORAL] Anemia Perniciosa / Déficit Severo de B12": """
        **Mecanismo:** Disminución de la síntesis y de la remodelación celulares.
        
        **Estudios recomendados:**
        * **Hemograma:** Anemia macrocítica.
        * **Vitamina B12 y ácido fólico sérico.**
        * **Ácido Metilmalónico y Homocisteína:** Elevados.
        * **Anticuerpos anti-factor intrínseco / células parietales.**
        """,
        "[TEMPORAL] Mieloma Múltiple": """
        **Mecanismo:** Infiltración medular y supresión osteoblástica.
        
        **Estudios recomendados:**
        * **Electroforesis de proteínas en suero y orina (SPEP / UPEP).**
        * **Cadenas ligeras libres en suero (Kappa/Lambda).**
        * **Aspirado / Biopsia de médula ósea.**
        """,
        "[TEMPORAL] Transfusión Masiva / Cirugía de Bypass": """
        **Mecanismo:** Quelación de Zn y Mg mediante citrato o mediante hemodilución.
        
        **Estudios recomendados:**
        * **Calcio iónico y gasometría.**
        * **Repetir FA tras estabilización del paciente.**
        """,
        "[TEMPORAL] Enfermedad de Wilson": """
        **Mecanismo:** Acumulación tóxica de cobre en el centro catalítico enzimático.
        
        **Estudios recomendados:**
        * **Ceruloplasmina sérica:** Disminuida.
        * **Cobre en orina de 24 horas:** Elevado.
        * **Examen con lámpara de hendidura:** Anillo de Kayser-Fleischer.
        """,
        "[TEMPORAL] Hemocromatosis": """
        **Mecanismo:** Depósito tóxico de hierro en los tejidos.
        
        **Estudios recomendados:**
        * **Saturación de transferrina (>45-50%).**
        * **Ferritina sérica:** Marcadamente elevada.
        * **Estudio genético:** Gen *HFE* (C282Y/H63D).
        """,

        # FACTORES PREANALÍTICOS
        "[LABORATORIO] Muestra con EDTA u Oxalato": """
        **Mecanismo:** Falso positivo. El anticoagulante quela los iones Mg y Zn, lo que anula la medición.
        
        **Acción requerida:**
        * **Repetir la toma de muestra en tubo seco (suero) o con heparina de litio.** Evitar tubos con tapa morada (EDTA) o gris (oxalato).
        """
    }

    causa_sel = st.selectbox("Seleccione la causa diferencial a evaluar:", list(estudios_causas.keys()))
    st.info(estudios_causas[causa_sel])

# ==========================================
# PESTAÑA 3: PROTOCOLO DE CONFIRMACIÓN HPP
# ==========================================
with tab_hpp_protocolo:
    st.subheader("🧬 Estudios Paraclínicos para Confirmación de Hipofosfatasia")
    st.markdown("""
    Ante la confirmación de valores de fosfatasa alcalina persistentemente bajos en al menos **dos mediciones distintas** (sin presencia de causas secundarias), se recomienda el siguiente panel paraclínico específico:
    """)
    
    st.markdown("""
    ### 1. Estudio Genético
    * **Secuenciación del gen *ALPL*:** Identificación de variantes patogénicas o probablemente patogénicas para la confirmación diagnóstica definitiva y el asesoramiento genético familiar.

    ### 2. Evaluación de Imagen y Densidad Ósea
    * **Radiografía de huesos largos y pies/manos:** Buscar bandas radiotransparentes subcondrales, edentulismo prematuro, pseudofracturas (zonas de Looser) o condrocalcinosis.
    * **Densitometría Ósea (DXA):** Evaluación del grado de compromiso mineral.

    ### 3. Marcadores Bioquímicos Específicos (Sustratos de TNSALP)
    * **Piridoxal-5'-Fosfato (PLP / vitamina B6 activa en suero):** Sustrato directo de la enzima; se encuentra **marcadamente elevado** en HPP. *(Solicitar preferentemente sin suplementación previa de B6)*.
    * **Fosfoetanolamina (PEA) y orina de 24 horas:** Acumulación debida a la falta de degradación enzimática (**elevada**).
    * **Pirofosfato inorgánico (PPi) en plasma/orina:** Acumulación del principal inhibidor de la mineralización ósea.

    """)

st.divider()

# Referencia Bibliográfica
st.markdown("""
**Referencia de Criterios y Rangos de Referencia:**
* *Diagnosis, treatment, and follow-up of patients with hypophosphatasia.* **Endocrine**, 87(2), 400-419 (2025). DOI: [10.1007/s12020-024-04054-1](https://doi.org/10.1007/s12020-024-04054-1)
""")

st.caption("⚠️ **Aviso legal:** Herramienta estrictamente reservada para profesionales de la salud capacitados para la interpretación clínica de pruebas de laboratorio.")
