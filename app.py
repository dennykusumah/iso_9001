import streamlit as st

import db
from entities import ENTITIES, GROUP_ORDER

st.set_page_config(
    page_title="QMS ISO 9001",
    page_icon="✅",
    layout="wide",
)

db.init_db()

st.title("✅ Sistem Manajemen Mutu (ISO 9001)")
st.caption(
    "Aplikasi Streamlit — hasil migrasi dari modul Odoo `qms` "
    "(Quality Management System ISO 9001)."
)

st.divider()

# Ringkasan jumlah data per grup
for group in GROUP_ORDER:
    keys_in_group = [k for k, v in ENTITIES.items() if v["group"] == group]
    if not keys_in_group:
        continue
    st.markdown(f"### {group}")
    cols = st.columns(min(len(keys_in_group), 5))
    for i, key in enumerate(keys_in_group):
        spec = ENTITIES[key]
        with cols[i % len(cols)]:
            st.metric(spec["label_plural"], db.count_records(key))

st.divider()
st.info(
    "Gunakan menu di sebelah kiri (sidebar) untuk membuka setiap modul, "
    "menambah, mengedit, mencari, dan menghapus data."
)
