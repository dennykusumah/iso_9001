import streamlit as st

import db
from crud_ui import render_entity_page

st.set_page_config(page_title="Tinjauan Manajemen", page_icon="📊", layout="wide")
db.init_db()

st.title("📊 Tinjauan Manajemen")

tabs = st.tabs(["Tinjauan", "Tinjauan oleh Manajemen Puncak"])
with tabs[0]:
    render_entity_page("review")
with tabs[1]:
    render_entity_page("revision_by_direction")
