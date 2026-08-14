import streamlit as st

import db
from crud_ui import render_entity_page

st.set_page_config(page_title="Temuan", page_icon="🧾", layout="wide")
db.init_db()

st.title("🧾 Temuan")

tabs = st.tabs(["Ketidaksesuaian", "Observasi", "Keluhan", "Peluang"])
with tabs[0]:
    render_entity_page("non_conformity")
with tabs[1]:
    render_entity_page("observation")
with tabs[2]:
    render_entity_page("complaint")
with tabs[3]:
    render_entity_page("opportunity")
