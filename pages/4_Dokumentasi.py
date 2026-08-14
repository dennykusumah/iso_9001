import streamlit as st

import db
from crud_ui import render_entity_page

st.set_page_config(page_title="Dokumentasi", page_icon="📄", layout="wide")
db.init_db()

st.title("📄 Dokumentasi Mutu")

tabs = st.tabs(
    ["Dokumen (umum)", "Prosedur", "Instruksi Kerja", "Formulir/Rekaman", "Versi Dokumen"]
)
with tabs[0]:
    render_entity_page("document")
with tabs[1]:
    render_entity_page("procedure")
with tabs[2]:
    render_entity_page("instructive")
with tabs[3]:
    render_entity_page("registry")
with tabs[4]:
    render_entity_page("version")
