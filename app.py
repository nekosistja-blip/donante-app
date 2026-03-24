import streamlit as st
import pandas as pd


# Cargar Excel
df = pd.read_excel('GRUPO SANGRE.xlsx', sheet_name=None)
vamDonante = df['vamDonante']
vamScreeni = df['vamScreeni']

# Limpiar cédulas y valores relevantes
vamDonante['vdonDocIde'] = vamDonante['vdonDocIde'].astype(str).str.strip()
vamScreeni['vscrLabMed'] = vamScreeni['vscrLabMed'].astype(str).str.strip()

# Función convertir sangre
def convertir_grupo(c):
    grupos = {
        1: "A", 2: "B", 3: "AB", 4: "O",
        5: "A+", 6: "B+", 7: "AB+", 8: "O+",
        9: "A-", 10: "B-", 11: "AB-", 12: "O-"
    }
    return grupos.get(c, "Desconocido")

# Función para identificar rechazo
def obtener_rechazo(valor_labmed):
    if str(valor_labmed).strip().upper() == 'R':
        return 'RECHAZADO'
    return ''

# Función búsqueda
def buscar(cedula):
    d = vamDonante[vamDonante['vdonDocIde'] == str(cedula).strip()]
    if d.empty:
        return None, None
    info = d.iloc[0]
    cod = info['vdonCodDon']
    donaciones = vamScreeni[vamScreeni['vdonCodDon'] == cod].copy()
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
            for _, fila in donaciones.iterrows():
                st.write('---')
                st.write(f"📅 Fecha: {fila.vscrFechas}")
                st.write(f"🩸 Grupo sanguíneo: {convertir_grupo(fila.vscrGrsCon)}")
                st.write(f"💬 Comentario: {fila.vscrComent}")

                rechazo = obtener_rechazo(fila.get('vscrLabMed', ''))
                if rechazo == 'RECHAZADO':
                    st.markdown(
                        "<p style='color:red; font-weight:bold;'>❌ RECHAZADO</p>",
                        unsafe_allow_html=True
                    )
                else:
                    st.write('')
        else:
            st.info("Este donante no tiene donaciones registradas.")
