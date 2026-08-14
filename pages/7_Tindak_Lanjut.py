import streamlit as st

import db
from crud_ui import render_entity_page

st.set_page_config(page_title="Tindak Lanjut", page_icon="🛠️", layout="wide")
db.init_db()

st.title("🛠️ Tindak Lanjut")

tabs = st.tabs(["Aksi", "Verifikasi Efektivitas"])
with tabs[0]:
    render_entity_page("action")
with tabs[1]:
    render_entity_page("effectiveness_check")
