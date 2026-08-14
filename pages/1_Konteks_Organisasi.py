import streamlit as st

import db
from crud_ui import render_entity_page

st.set_page_config(page_title="Konteks Organisasi", page_icon="🏢", layout="wide")
db.init_db()

st.title("🏢 Konteks Organisasi")

tabs = st.tabs(["Pihak Berkepentingan", "Sumber Daya"])
with tabs[0]:
    render_entity_page("interested_party")
with tabs[1]:
    render_entity_page("resource")
