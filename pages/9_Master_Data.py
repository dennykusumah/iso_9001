import streamlit as st

import db
from crud_ui import render_entity_page

st.set_page_config(page_title="Master Data", page_icon="⚙️", layout="wide")
db.init_db()

st.title("⚙️ Master Data / Konfigurasi")
st.caption(
    "Data referensi yang dipakai oleh modul-modul lain "
    "(tahapan, asal temuan, penyebab, komponen kebijakan)."
)

tabs = st.tabs(
    [
        "Komponen Kebijakan",
        "Tahapan Aksi",
        "Tahapan Temuan",
        "Asal Temuan",
        "Penyebab Kelemahan",
    ]
)
with tabs[0]:
    render_entity_page("policy_component")
with tabs[1]:
    render_entity_page("action_stage")
with tabs[2]:
    render_entity_page("finding_stage")
with tabs[3]:
    render_entity_page("finding_origin")
with tabs[4]:
    render_entity_page("weakness_cause")
