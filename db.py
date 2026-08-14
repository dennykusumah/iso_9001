"""
Layer database generik untuk QMS Streamlit.
Membuat skema SQLite dari entities.ENTITIES lalu menyediakan fungsi
CRUD generik (list/get/insert/update/delete) yang dipakai semua halaman.
"""
import sqlite3
import os
from contextlib import contextmanager

from entities import ENTITIES

DB_PATH = os.path.join(os.path.dirname(__file__), "qms_data.db")

_TYPE_TO_SQL = {
    "text": "TEXT",
    "textarea": "TEXT",
    "int": "INTEGER",
    "date": "TEXT",
    "datetime": "TEXT",
    "bool": "INTEGER",
    "select": "TEXT",
    "m2o": "INTEGER",
}


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _m2m_table(entity_key, field_name):
    return f"{entity_key}__{field_name}"


def init_db():
    """Buat semua tabel (entitas + junction many2many) jika belum ada."""
    with get_conn() as conn:
        cur = conn.cursor()
        for key, spec in ENTITIES.items():
            cols = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
            for f in spec["fields"]:
                sql_type = _TYPE_TO_SQL[f["type"]]
                cols.append(f'"{f["name"]}" {sql_type}')
            cur.execute(f'CREATE TABLE IF NOT EXISTS "{key}" ({", ".join(cols)})')

            for m in spec["m2m"]:
                jt = _m2m_table(key, m["field"])
                cur.execute(
                    f'CREATE TABLE IF NOT EXISTS "{jt}" ('
                    f'"{key}_id" INTEGER NOT NULL, '
                    f'"{m["ref"]}_id" INTEGER NOT NULL, '
                    f'PRIMARY KEY ("{key}_id", "{m["ref"]}_id"))'
                )
        conn.commit()


def list_records(entity_key, search=None, limit=None):
    spec = ENTITIES[entity_key]
    field_names = [f["name"] for f in spec["fields"]]
    order = spec.get("order", "-id")
    order_sql = (
        f'"{order[1:]}" DESC' if order.startswith("-") else f'"{order}" ASC'
    )
    sql = f'SELECT * FROM "{entity_key}"'
    params = []
    if search:
        text_fields = [
            f["name"] for f in spec["fields"] if f["type"] in ("text", "textarea")
        ]
        if text_fields:
            clauses = " OR ".join([f'"{fn}" LIKE ?' for fn in text_fields])
            sql += f" WHERE {clauses}"
            params = [f"%{search}%"] * len(text_fields)
    sql += f" ORDER BY {order_sql}"
    if limit:
        sql += f" LIMIT {int(limit)}"
    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]


def get_record(entity_key, record_id):
    with get_conn() as conn:
        row = conn.execute(
            f'SELECT * FROM "{entity_key}" WHERE id = ?', (record_id,)
        ).fetchone()
        if not row:
            return None
        rec = dict(row)
        spec = ENTITIES[entity_key]
        for m in spec["m2m"]:
            jt = _m2m_table(entity_key, m["field"])
            ids = conn.execute(
                f'SELECT "{m["ref"]}_id" FROM "{jt}" WHERE "{entity_key}_id" = ?',
                (record_id,),
            ).fetchall()
            rec[m["field"]] = [r[0] for r in ids]
        return rec


def count_records(entity_key):
    with get_conn() as conn:
        return conn.execute(f'SELECT COUNT(*) FROM "{entity_key}"').fetchone()[0]


def insert_record(entity_key, values):
    spec = ENTITIES[entity_key]
    field_names = [f["name"] for f in spec["fields"]]
    cols = [fn for fn in field_names if fn in values]
    placeholders = ", ".join(["?"] * len(cols))
    col_sql = ", ".join([f'"{c}"' for c in cols])
    with get_conn() as conn:
        cur = conn.cursor()
        if cols:
            cur.execute(
                f'INSERT INTO "{entity_key}" ({col_sql}) VALUES ({placeholders})',
                [values[c] for c in cols],
            )
        else:
            cur.execute(f'INSERT INTO "{entity_key}" DEFAULT VALUES')
        new_id = cur.lastrowid
        _save_m2m(conn, entity_key, new_id, values, spec)
        conn.commit()
        return new_id


def update_record(entity_key, record_id, values):
    spec = ENTITIES[entity_key]
    field_names = [f["name"] for f in spec["fields"]]
    cols = [fn for fn in field_names if fn in values]
    with get_conn() as conn:
        cur = conn.cursor()
        if cols:
            set_sql = ", ".join([f'"{c}" = ?' for c in cols])
            cur.execute(
                f'UPDATE "{entity_key}" SET {set_sql} WHERE id = ?',
                [values[c] for c in cols] + [record_id],
            )
        _save_m2m(conn, entity_key, record_id, values, spec)
        conn.commit()


def _save_m2m(conn, entity_key, record_id, values, spec):
    for m in spec["m2m"]:
        if m["field"] not in values:
            continue
        jt = _m2m_table(entity_key, m["field"])
        conn.execute(f'DELETE FROM "{jt}" WHERE "{entity_key}_id" = ?', (record_id,))
        ref_ids = values[m["field"]] or []
        for rid in ref_ids:
            conn.execute(
                f'INSERT OR IGNORE INTO "{jt}" ("{entity_key}_id", "{m["ref"]}_id") '
                f"VALUES (?, ?)",
                (record_id, rid),
            )


def delete_record(entity_key, record_id):
    spec = ENTITIES[entity_key]
    with get_conn() as conn:
        cur = conn.cursor()
        for m in spec["m2m"]:
            jt = _m2m_table(entity_key, m["field"])
            cur.execute(f'DELETE FROM "{jt}" WHERE "{entity_key}_id" = ?', (record_id,))
        # Hapus juga referensi many2many dari entitas lain yang menunjuk kesini
        for other_key, other_spec in ENTITIES.items():
            for m in other_spec["m2m"]:
                if m["ref"] == entity_key:
                    jt = _m2m_table(other_key, m["field"])
                    cur.execute(
                        f'DELETE FROM "{jt}" WHERE "{entity_key}_id" = ?', (record_id,)
                    )
        cur.execute(f'DELETE FROM "{entity_key}" WHERE id = ?', (record_id,))
        conn.commit()


def get_display_map(entity_key):
    """{id: label} untuk dipakai di dropdown many2one / many2many."""
    spec = ENTITIES[entity_key]
    display_field = spec["display"]
    with get_conn() as conn:
        if display_field == "id":
            rows = conn.execute(f'SELECT id FROM "{entity_key}"').fetchall()
            return {r["id"]: f"#{r['id']}" for r in rows}
        rows = conn.execute(
            f'SELECT id, "{display_field}" FROM "{entity_key}"'
        ).fetchall()
        out = {}
        for r in rows:
            label = r[display_field]
            out[r["id"]] = label if label else f"#{r['id']} (tanpa nama)"
        return out


def referencing_counts(entity_key, record_id):
    """Cari entitas lain mana saja yang masih mereferensikan record ini (m2o),
    supaya user diperingatkan sebelum menghapus."""
    refs = []
    for other_key, other_spec in ENTITIES.items():
        for f in other_spec["fields"]:
            if f["type"] == "m2o" and f.get("ref") == entity_key:
                with get_conn() as conn:
                    n = conn.execute(
                        f'SELECT COUNT(*) FROM "{other_key}" WHERE "{f["name"]}" = ?',
                        (record_id,),
                    ).fetchone()[0]
                if n:
                    refs.append((other_key, f["name"], n))
    return refs
