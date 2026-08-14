import streamlit as st

import db
from crud_ui import render_entity_page

st.set_page_config(page_title="Audit", page_icon="🔍", layout="wide")
db.init_db()

st.title("🔍 Audit Internal/Eksternal")

tabs = st.tabs(["Audit", "Baris Verifikasi Audit", "Evaluasi Auditor"])
with tabs[0]:
    render_entity_page("audit")
with tabs[1]:
    render_entity_page("audit_verification_line")
with tabs[2]:
    render_entity_page("audit_evaluation")
