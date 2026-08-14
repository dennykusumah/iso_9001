import streamlit as st

import db
from crud_ui import render_entity_page

st.set_page_config(page_title="Manajemen Risiko", page_icon="⚠️", layout="wide")
db.init_db()

st.title("⚠️ Manajemen Risiko & Peluang")
render_entity_page("hazard")
