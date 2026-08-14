"""
Komponen UI generik (Streamlit) untuk menampilkan & mengedit satu entitas QMS.
Dipakai oleh semua file di folder pages/.
"""
import datetime

import pandas as pd
import streamlit as st

import db
from entities import ENTITIES


def _option_label(options, value):
    for v, l in options:
        if v == value:
            return l
    return value


def _field_input(entity_key, f, current_value, key_prefix):
    """Render satu widget input sesuai tipe field, kembalikan nilai barunya."""
    label = f["label"] + (" *" if f.get("required") else "")
    widget_key = f"{key_prefix}_{f['name']}"

    if f["type"] == "text":
        return st.text_input(label, value=current_value or "", key=widget_key)

    if f["type"] == "textarea":
        return st.text_area(label, value=current_value or "", key=widget_key)

    if f["type"] == "int":
        val = current_value if current_value is not None else f.get("default", 0)
        return st.number_input(
            label, value=int(val or 0), step=1, key=widget_key, format="%d"
        )

    if f["type"] == "bool":
        val = bool(current_value) if current_value is not None else bool(
            f.get("default", False)
        )
        return st.checkbox(label, value=val, key=widget_key)

    if f["type"] == "date":
        val = None
        if current_value:
            try:
                val = datetime.date.fromisoformat(str(current_value)[:10])
            except ValueError:
                val = None
        d = st.date_input(label, value=val, key=widget_key)
        return d.isoformat() if d else None

    if f["type"] == "datetime":
        val = None
        if current_value:
            try:
                val = datetime.datetime.fromisoformat(str(current_value)[:19])
            except ValueError:
                val = None
        col1, col2 = st.columns(2)
        with col1:
            d = st.date_input(
                label, value=val.date() if val else None, key=widget_key + "_d"
            )
        with col2:
            t = st.time_input(
                "Jam", value=val.time() if val else None, key=widget_key + "_t"
            )
        if d:
            return datetime.datetime.combine(
                d, t or datetime.time(0, 0)
            ).isoformat()
        return None

    if f["type"] == "select":
        options = f["options"]
        values = [v for v, _ in options]
        default = current_value if current_value in values else f.get("default")
        idx = values.index(default) if default in values else 0
        return st.selectbox(
            label,
            options=values,
            index=idx,
            format_func=lambda v: _option_label(options, v),
            key=widget_key,
        )

    if f["type"] == "m2o":
        ref_map = db.get_display_map(f["ref"])
        ids = [None] + list(ref_map.keys())
        default = current_value if current_value in ref_map else None
        idx = ids.index(default) if default in ids else 0
        return st.selectbox(
            label,
            options=ids,
            index=idx,
            format_func=lambda i: "— (kosong) —" if i is None else ref_map.get(i, f"#{i}"),
            key=widget_key,
        )

    raise ValueError(f"Tipe field tidak dikenal: {f['type']}")


def render_form(entity_key, record=None):
    """Tampilkan form tambah/edit untuk satu entitas. record=None berarti mode tambah baru."""
    spec = ENTITIES[entity_key]
    is_edit = record is not None
    key_prefix = f"form_{entity_key}_{record['id'] if is_edit else 'new'}"

    with st.form(key=key_prefix + "_form", clear_on_submit=not is_edit):
        values = {}
        for f in spec["fields"]:
            current = record.get(f["name"]) if is_edit else f.get("default")
            values[f["name"]] = _field_input(entity_key, f, current, key_prefix)

        for m in spec["m2m"]:
            ref_map = db.get_display_map(m["ref"])
            current_ids = record.get(m["field"], []) if is_edit else []
            current_ids = [i for i in current_ids if i in ref_map]
            selected = st.multiselect(
                m["label"],
                options=list(ref_map.keys()),
                default=current_ids,
                format_func=lambda i: ref_map.get(i, f"#{i}"),
                key=f"{key_prefix}_{m['field']}",
            )
            values[m["field"]] = selected

        submit_label = "Simpan Perubahan" if is_edit else f"Tambah {spec['label']}"
        submitted = st.form_submit_button(submit_label, type="primary")

        if submitted:
            missing = [
                f["label"]
                for f in spec["fields"]
                if f.get("required")
                and (values.get(f["name"]) in (None, "", []))
            ]
            if missing:
                st.error("Wajib diisi: " + ", ".join(missing))
            else:
                if is_edit:
                    db.update_record(entity_key, record["id"], values)
                    st.success(f"{spec['label']} berhasil diperbarui.")
                else:
                    db.insert_record(entity_key, values)
                    st.success(f"{spec['label']} baru berhasil ditambahkan.")
                st.rerun()


def _records_to_dataframe(entity_key, records):
    spec = ENTITIES[entity_key]
    if not records:
        return pd.DataFrame()
    select_fields = [f for f in spec["fields"] if f["type"] == "select"]
    m2o_fields = [f for f in spec["fields"] if f["type"] == "m2o"]
    m2o_maps = {f["name"]: db.get_display_map(f["ref"]) for f in m2o_fields}

    rows = []
    for r in records:
        row = {"id": r["id"]}
        for f in spec["fields"]:
            val = r.get(f["name"])
            if f["type"] == "select":
                val = _option_label(f["options"], val)
            elif f["type"] == "m2o":
                val = m2o_maps[f["name"]].get(val, "") if val else ""
            elif f["type"] == "bool":
                val = "✅" if val else ""
            elif f["type"] == "textarea" and val:
                val = (val[:60] + "…") if len(val) > 60 else val
            row[f["label"]] = val
        rows.append(row)
    return pd.DataFrame(rows)


def render_entity_page(entity_key):
    spec = ENTITIES[entity_key]
    st.subheader(spec["label_plural"])

    total = db.count_records(entity_key)
    search = st.text_input(
        "🔍 Cari", key=f"search_{entity_key}", placeholder="Ketik untuk mencari..."
    )
    records = db.list_records(entity_key, search=search or None)
    st.caption(f"{len(records)} dari {total} data ditampilkan.")

    tab_list, tab_add = st.tabs(["📋 Daftar Data", "➕ Tambah Baru"])

    with tab_add:
        render_form(entity_key)

    with tab_list:
        if not records:
            st.info("Belum ada data.")
        else:
            df = _records_to_dataframe(entity_key, records)
            st.dataframe(df, use_container_width=True, hide_index=True)

            display_map = {r["id"]: r.get(spec["display"]) or f"#{r['id']}" for r in records}
            selected_id = st.selectbox(
                "Pilih data untuk diedit / dihapus",
                options=list(display_map.keys()),
                format_func=lambda i: f"#{i} — {display_map[i]}",
                key=f"select_edit_{entity_key}",
            )

            if selected_id:
                full_record = db.get_record(entity_key, selected_id)
                with st.expander(f"✏️ Edit: {display_map[selected_id]}", expanded=True):
                    render_form(entity_key, record=full_record)

                    st.divider()
                    refs = db.referencing_counts(entity_key, selected_id)
                    if refs:
                        ref_text = ", ".join(
                            f"{ENTITIES[k]['label_plural']} ({n})" for k, _, n in refs
                        )
                        st.warning(
                            f"⚠️ Data ini masih dirujuk oleh: {ref_text}. "
                            "Menghapusnya akan mengosongkan rujukan tersebut."
                        )
                    confirm = st.checkbox(
                        "Saya yakin ingin menghapus data ini",
                        key=f"confirm_delete_{entity_key}_{selected_id}",
                    )
                    if st.button(
                        "🗑️ Hapus",
                        disabled=not confirm,
                        key=f"btn_delete_{entity_key}_{selected_id}",
                    ):
                        db.delete_record(entity_key, selected_id)
                        st.success("Data dihapus.")
                        st.rerun()
