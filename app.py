import streamlit as st
import pandas as pd
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# Cargar Excel
df = pd.read_excel('GRUPO SANGRE.xlsx', sheet_name=None)
vamDonante = df['vamDonante']
vamScreeni = df['vamScreeni']

# Limpiar cédulas
vamDonante['vdonDocIde'] = vamDonante['vdonDocIde'].astype(str).str.strip()

# Función convertir sangre
def convertir_grupo(c):
    grupos = {1:"A+", 2:"B+", 3:"AB+", 4:"O+", 5:"A-", 6:"B-", 7:"AB-", 8:"O-", 9:" ",10:" ",11:"IN+",12:"B+"}
    return grupos.get(c, "Desconocido")

# Función búsqueda
def buscar(cedula):
    d = vamDonante[vamDonante['vdonDocIde'] == cedula]
    if d.empty:
        return None, None
    info = d.iloc[0]
    cod = info['vdonCodDon']
    donaciones = vamScreeni[vamScreeni['vdonCodDon'] == cod]
    return info, donaciones

# UI
st.title('🩸 Sistema de Consulta de Donantes')

cedula = st.text_input('📘 Ingresa Cédula de Identidad:')
if st.button('🔎 Buscar'):
    info, donaciones = buscar(cedula)
    if info is None:
        st.error('No se encontró el donante.')
    else:
        st.subheader('👤 Datos del Donante')
        st.write(f"**Código:** {info.vdonCodDon}")
        st.write(f"**Nombre:** {info.vdonNombre} {info.vdonPatern} {info.vdonMatern}")
        st.write(f"**Dirección:** {info.vdonDirecc}")
        st.write(f"**Celular:** {info.vdonTelCel}")

        if not donaciones.empty:
            st.subheader('🩺 Historial de Donaciones')
            for i, fila in donaciones.iterrows():
                st.write("---")
                st.write(f"📅 Fecha: {fila.vscrFechas}")
                st.write(f"🩸 Grupo sanguíneo: {convertir_grupo(fila.vscrGrsCon)}")
                st.write(f"💬 Comentario: {fila.vscrComent}")
        else:
            st.info("Este donante no tiene donaciones registradas.")
