import streamlit as st

import db
from crud_ui import render_entity_page

st.set_page_config(page_title="Perencanaan", page_icon="🗺️", layout="wide")
db.init_db()

st.title("🗺️ Perencanaan Sistem Mutu")

tabs = st.tabs(
    [
        "Proses",
        "Kebijakan",
        "Sasaran Mutu",
        "Pengukuran Sasaran Mutu",
        "Indikator",
        "Pengukuran Indikator",
    ]
)
with tabs[0]:
    render_entity_page("process")
with tabs[1]:
    render_entity_page("policy")
with tabs[2]:
    render_entity_page("goal")
with tabs[3]:
    render_entity_page("goal_measurement")
with tabs[4]:
    render_entity_page("indicator")
with tabs[5]:
    render_entity_page("indicator_measurement")
