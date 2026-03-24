import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistema de Consulta de Donantes", page_icon="🩸", layout="centered")

# Cargar Excel
DF = pd.read_excel('GRUPO SANGRE.xlsx', sheet_name=None)
vamDonante = DF['vamDonante'].copy()
vamScreeni = DF['vamScreeni'].copy()

# Limpiar datos clave
vamDonante['vdonDocIde'] = vamDonante['vdonDocIde'].astype(str).str.strip()
vamScreeni['vdonCodDon'] = vamScreeni['vdonCodDon'].astype(str).str.strip()
if 'vscrLabMed' in vamScreeni.columns:
    vamScreeni['vscrLabMed'] = vamScreeni['vscrLabMed'].astype(str).str.strip()
if 'vscrNroEti' in vamScreeni.columns:
    vamScreeni['vscrNroEti'] = vamScreeni['vscrNroEti'].astype(str).str.strip()


def convertir_grupo(codigo):
    grupos = {
        1: "A", 2: "B", 3: "AB", 4: "O",
        5: "A+", 6: "B+", 7: "AB+", 8: "O+",
        9: "A-", 10: "B-", 11: "AB-", 12: "O-"
    }
    return grupos.get(codigo, "Desconocido")


def buscar(cedula):
    cedula = str(cedula).strip()
    d = vamDonante[vamDonante['vdonDocIde'] == cedula]
    if d.empty:
        return None, None

    info = d.iloc[0]
    cod = str(info['vdonCodDon']).strip()
    donaciones = vamScreeni[vamScreeni['vdonCodDon'] == cod].copy()
    return info, donaciones


def obtener_rechazo(valor):
    return "RECHAZADO" if str(valor).strip().upper() == "R" else ""


def obtener_puesto(vscr_nro_eti):
    prefijo = str(vscr_nro_eti).strip()[:3]
    if prefijo == "001":
        return "PUESTO FIJO"
    if prefijo == "002":
        return "PUESTO MOVIL"
    return ""


st.markdown("""
    <style>
    #MainMenu,
    header,
    footer,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
    }
    .main-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 1.2rem;
    }
    .card {
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        background: #ffffff;
    }
    .donation-date {
        font-weight: 700;
        margin-bottom: 8px;
    }
    .field-line {
        margin: 3px 0;
    }
    .status-line {
        margin-top: 8px;
        font-weight: 800;
    }
    .status-rechazado {
        color: #b91c1c;
    }
    .status-puesto-fijo {
        color: #16a34a;
    }
    .status-puesto-movil {
        color: #dc2626;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🩸 Sistema de Consulta de Donantes</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Consulta rápida de datos y donaciones</div>', unsafe_allow_html=True)

cedula = st.text_input('📘 Ingresa Cédula de Identidad:')

if st.button('🔎 Buscar', use_container_width=True):
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
                rechazo = obtener_rechazo(fila.get('vscrLabMed', ''))
                puesto = obtener_puesto(fila.get('vscrNroEti', ''))
                comentario = fila.get('vscrComent', '')
                fecha = fila.get('vscrFechas', '')
                grupo = convertir_grupo(fila.get('vscrGrsCon', None))

                rechazo_html = ''
                if rechazo:
                    rechazo_html = '<div class="status-line status-rechazado">RECHAZADO</div>'

                puesto_html = ''
                if puesto == 'PUESTO FIJO':
                    puesto_html = '<div class="status-line status-puesto-fijo">PUESTO FIJO</div>'
                elif puesto == 'PUESTO MOVIL':
                    puesto_html = '<div class="status-line status-puesto-movil">PUESTO MOVIL</div>'

                st.markdown(
                    f"""
                    <div class="card">
                        <div class="donation-date">📅 Fecha: {fecha}</div>
                        <div class="field-line"><strong>🩸 Grupo sanguíneo:</strong> {grupo}</div>
                        <div class="field-line"><strong>💬 Comentario:</strong> {comentario}</div>
                        {rechazo_html}
                        {puesto_html}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info('Este donante no tiene donaciones registradas.')
