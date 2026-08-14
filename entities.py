"""
Definisi seluruh entitas Quality Management System (ISO 9001).
Ini adalah terjemahan dari model-model Odoo (folder qms/models/*.py)
ke bentuk config yang dipakai oleh mesin CRUD generik di db.py & crud_ui.py.

Setiap entitas punya:
- key         : nama tabel di SQLite
- label       : nama tampilan (singular)
- label_plural: nama tampilan (jamak)
- group       : kelompok menu di sidebar
- display     : nama field yang dipakai sebagai representasi baris (mis. di dropdown)
- fields      : daftar field biasa (bukan many2many)
- m2m         : daftar relasi many2many (disimpan di tabel junction terpisah)

Tipe field yang didukung:
- text        : teks pendek (satu baris)
- textarea    : teks panjang / html (ditampilkan sebagai text_area)
- int         : angka bulat
- date        : tanggal
- datetime    : tanggal + jam
- bool        : ya/tidak
- select      : pilihan tetap (field butuh 'options': list[(value,label)])
- m2o         : many2one, referensi ke entitas lain (field butuh 'ref': key entitas)
"""

# ---------------------------------------------------------------------------
# Opsi selection (disalin dari Odoo, label diindonesiakan seperlunya)
# ---------------------------------------------------------------------------

OPT_ACTION_RESPONSE_TYPE = [
    ("improvement", "Aksi Peningkatan"),
    ("immediate", "Aksi Segera"),
    ("correction", "Aksi Korektif"),
    ("preventive", "Aksi Risiko"),
]
OPT_COMPLEXITY = [
    ("very_low", "Sangat Rendah"),
    ("low", "Rendah"),
    ("medium", "Sedang"),
    ("high", "Tinggi"),
    ("very_high", "Sangat Tinggi"),
]
OPT_KANBAN_STATE = [
    ("normal", "Sedang Berjalan"),
    ("done", "Siap ke Tahap Berikutnya"),
    ("blocked", "Terblokir"),
]
OPT_FINDING_STAGE_STATE = [
    ("draft", "Draft"),
    ("analysis", "Analisis"),
    ("pending", "Rencana Aksi"),
    ("open", "Berjalan"),
    ("done", "Selesai"),
    ("cancel", "Dibatalkan"),
]
OPT_AUDIT_SYSTEM = [
    ("iso9001_2015", "ISO 9001:2015"),
    ("iso9001_2008", "ISO 9001:2008"),
]
OPT_AUDIT_STATE = [("open", "Terbuka"), ("closed", "Tertutup")]
OPT_AUDIT_EVAL_TYPE = [("internal", "Internal"), ("external", "Eksternal")]
OPT_SCORE_10 = [(str(i), str(i)) for i in range(1, 11)] + [("-", "-")]
OPT_DOC_FORMAT = [("paper", "Kertas"), ("electronic", "Elektronik")]
OPT_DOC_RELATION = [("sgc&tmc", "SGC / TMC"), ("sgc", "SGC"), ("tmc", "TMC")]
OPT_DOC_TYPE = [("internal", "Internal"), ("external", "Eksternal")]
OPT_GOAL_STATE = [
    ("draft", "Draft"),
    ("open", "Terbuka"),
    ("closed", "Tertutup"),
    ("cancelled", "Dibatalkan"),
]
OPT_MEASUREMENT_RESULT = [
    ("goal_ok", "Target Tercapai"),
    ("goal_with_obs", "Tercapai dengan Catatan"),
    ("goal_no_ok", "Target Tidak Tercapai"),
]
OPT_INDICATOR_STATE = [("enabled", "Aktif"), ("disabled", "Nonaktif")]
OPT_INDICATOR_FREQ = [
    ("annual", "Tahunan"),
    ("biannual", "Semesteran"),
    ("quarterly", "Kuartalan"),
    ("monthly", "Bulanan"),
]
OPT_IP_TYPE = [("internal", "Internal"), ("external", "Eksternal")]
OPT_LEVEL_1_4 = [
    ("1", "Rendah"),
    ("2", "Sedang"),
    ("3", "Tinggi"),
    ("4", "Sangat Tinggi"),
]
OPT_RESOURCE_TYPE = [("internal", "Internal"), ("external", "Eksternal")]
OPT_RESOURCE_STATE = [
    ("available", "Tersedia"),
    ("in_process", "Dalam Proses"),
    ("not_available", "Tidak Tersedia"),
]
OPT_PROCESS_TYPE = [
    ("strategic", "Strategis"),
    ("central", "Inti"),
    ("support", "Pendukung"),
]
OPT_PROCESS_STATE = [("enabled", "Aktif"), ("disabled", "Nonaktif")]
OPT_HAZARD_PROB = [
    ("1", "Sangat Rendah (Jarang)"),
    ("2", "Rendah (Tidak Mungkin)"),
    ("3", "Sedang (Mungkin)"),
    ("4", "Tinggi (Cukup Mungkin)"),
    ("5", "Sangat Tinggi (Hampir Pasti)"),
]
OPT_HAZARD_IMPACT = [
    ("1", "Sangat Rendah (Tidak Signifikan)"),
    ("2", "Rendah (Kecil)"),
    ("3", "Sedang (Moderat)"),
    ("4", "Tinggi (Besar)"),
    ("5", "Sangat Tinggi (Katastropik)"),
]
OPT_HAZARD_STRATEGY = [
    ("accept", "Terima"),
    ("watch", "Pantau"),
    ("evitar", "Hindari"),
    ("transfer", "Transfer"),
    ("reduce", "Kurangi"),
    ("share", "Bagi"),
]
OPT_HAZARD_STATE = [
    ("draft", "Draft"),
    ("open", "Terbuka"),
    ("closed", "Tertutup"),
    ("cancelled", "Dibatalkan"),
]
OPT_HAZARD_EVAL = [
    ("low", "Rendah"),
    ("medium", "Sedang"),
    ("high", "Tinggi"),
    ("very_high", "Sangat Tinggi"),
]
OPT_HAZARD_TYPE_RISK = [
    ("strategic", "Strategis"),
    ("image", "Citra"),
    ("operative", "Operasional"),
    ("financial", "Finansial"),
    ("compliance", "Kepatuhan"),
    ("technological", "Teknologi"),
    ("corruption", "Korupsi"),
    ("information", "Informasi"),
]
OPT_HAZARD_FACTOR = [
    ("e_economic", "Ekonomi (eksternal)"),
    ("e_politicians", "Politik (eksternal)"),
    ("e_social", "Sosial (eksternal)"),
    ("e_technological", "Teknologi (eksternal)"),
    ("e_enviroment", "Lingkungan (eksternal)"),
    ("e_communication", "Komunikasi (eksternal)"),
    ("i_financial", "Finansial (internal)"),
    ("i_personal", "SDM (internal)"),
    ("i_technological", "Teknologi (internal)"),
    ("i_strategic", "Strategis (internal)"),
    ("i_communication", "Komunikasi (internal)"),
    ("i_factors", "Faktor lain (internal)"),
]
OPT_REVDIR_STATE = [("open", "Terbuka"), ("done", "Tertutup")]
OPT_EFFCHECK_STATE = [("pending", "Menunggu"), ("closed", "Tertutup")]

# ---------------------------------------------------------------------------
# ENTITAS
# ---------------------------------------------------------------------------

ENTITIES = {}


def _e(key, label, label_plural, group, display, fields, m2m=None, order="-id"):
    ENTITIES[key] = {
        "key": key,
        "label": label,
        "label_plural": label_plural,
        "group": group,
        "display": display,
        "fields": fields,
        "m2m": m2m or [],
        "order": order,
    }


# --- Master data sederhana -------------------------------------------------

_e(
    "policy_component",
    "Komponen Kebijakan",
    "Komponen Kebijakan",
    "Master Data",
    "name",
    [{"name": "name", "label": "Nama", "type": "text", "required": True}],
)

_e(
    "action_stage",
    "Tahapan Aksi",
    "Tahapan Aksi",
    "Master Data",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {"name": "sequence", "label": "Urutan", "type": "int", "default": 100},
        {"name": "is_starting", "label": "Tahap Awal", "type": "bool"},
        {"name": "is_ending", "label": "Tahap Akhir", "type": "bool"},
    ],
    order="sequence",
)

_e(
    "finding_stage",
    "Tahapan Temuan",
    "Tahapan Temuan",
    "Master Data",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {"name": "sequence", "label": "Urutan", "type": "int", "default": 100},
        {"name": "is_starting", "label": "Tahap Awal", "type": "bool"},
        {
            "name": "state",
            "label": "Status",
            "type": "select",
            "options": OPT_FINDING_STAGE_STATE,
            "default": "draft",
        },
        {"name": "fold", "label": "Dilipat di Kanban", "type": "bool"},
    ],
    order="sequence",
)

_e(
    "finding_origin",
    "Asal Temuan",
    "Asal Temuan",
    "Master Data",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {"name": "description", "label": "Deskripsi", "type": "textarea"},
        {"name": "sequence", "label": "Urutan", "type": "int", "default": 10},
        {"name": "reference_code", "label": "Kode Referensi", "type": "text"},
        {
            "name": "parent_id",
            "label": "Induk (Grup)",
            "type": "m2o",
            "ref": "finding_origin",
        },
    ],
    order="sequence",
)

_e(
    "weakness_cause",
    "Penyebab Kelemahan",
    "Penyebab Kelemahan",
    "Master Data",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {"name": "description", "label": "Deskripsi", "type": "textarea"},
        {"name": "sequence", "label": "Urutan", "type": "int", "default": 10},
        {"name": "reference_code", "label": "Kode Referensi", "type": "text"},
        {
            "name": "parent_id",
            "label": "Induk (Grup)",
            "type": "m2o",
            "ref": "weakness_cause",
        },
    ],
    order="sequence",
)

# --- Pihak Berkepentingan & Sumber Daya ------------------------------------

_e(
    "interested_party",
    "Pihak Berkepentingan",
    "Pihak Berkepentingan",
    "Konteks Organisasi",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {
            "name": "interested_party_type",
            "label": "Tipe",
            "type": "select",
            "options": OPT_IP_TYPE,
        },
        {"name": "is_organization", "label": "Adalah Organisasi", "type": "bool"},
        {
            "name": "organization_id",
            "label": "Organisasi Induk",
            "type": "m2o",
            "ref": "interested_party",
        },
        {"name": "power", "label": "Kekuatan", "type": "select", "options": OPT_LEVEL_1_4},
        {"name": "interest", "label": "Minat", "type": "select", "options": OPT_LEVEL_1_4},
        {
            "name": "cooperation",
            "label": "Kerja Sama",
            "type": "select",
            "options": OPT_LEVEL_1_4,
        },
        {"name": "impact", "label": "Dampak", "type": "select", "options": OPT_LEVEL_1_4},
        {"name": "area", "label": "Area", "type": "text"},
        {
            "name": "requeriments_interested_party",
            "label": "Kebutuhan/Persyaratan",
            "type": "textarea",
        },
        {"name": "interest_tmc", "label": "Kepentingan Organisasi", "type": "textarea"},
    ],
)

_e(
    "resource",
    "Sumber Daya",
    "Sumber Daya",
    "Konteks Organisasi",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {
            "name": "responsible_id",
            "label": "Penanggung Jawab",
            "type": "m2o",
            "ref": "interested_party",
            "required": True,
        },
        {"name": "description", "label": "Deskripsi", "type": "textarea"},
        {
            "name": "resource_type",
            "label": "Tipe",
            "type": "select",
            "options": OPT_RESOURCE_TYPE,
        },
        {
            "name": "state",
            "label": "Status",
            "type": "select",
            "options": OPT_RESOURCE_STATE,
            "default": "available",
        },
    ],
)

# --- Proses & Kebijakan ------------------------------------------------------

_e(
    "process",
    "Proses",
    "Proses",
    "Perencanaan",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {
            "name": "responsible_id",
            "label": "Penanggung Jawab",
            "type": "m2o",
            "ref": "interested_party",
        },
        {
            "name": "resource_type",
            "label": "Tipe Proses",
            "type": "select",
            "options": OPT_PROCESS_TYPE,
        },
        {
            "name": "state",
            "label": "Status",
            "type": "select",
            "options": OPT_PROCESS_STATE,
            "default": "enabled",
        },
        {"name": "description", "label": "Deskripsi", "type": "textarea"},
        {"name": "inputs", "label": "Input", "type": "textarea"},
        {"name": "outputs", "label": "Output", "type": "textarea"},
    ],
    m2m=[
        {"field": "resource_ids", "ref": "resource", "label": "Sumber Daya"},
        {
            "field": "policy_component_ids",
            "ref": "policy_component",
            "label": "Komponen Kebijakan",
        },
    ],
)

_e(
    "policy",
    "Kebijakan",
    "Kebijakan",
    "Perencanaan",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {"name": "version", "label": "Versi", "type": "int"},
        {"name": "date", "label": "Tanggal", "type": "date"},
        {"name": "approved", "label": "Disetujui", "type": "bool"},
        {"name": "description", "label": "Deskripsi", "type": "textarea"},
    ],
    m2m=[
        {
            "field": "policy_component_ids",
            "ref": "policy_component",
            "label": "Komponen Kebijakan",
        }
    ],
)

# --- Sasaran Mutu (Goal) & Indikator -----------------------------------------

_e(
    "goal",
    "Sasaran Mutu",
    "Sasaran Mutu",
    "Perencanaan",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {"name": "description", "label": "Deskripsi", "type": "textarea"},
        {"name": "date_open", "label": "Tanggal Dibuka", "type": "date"},
        {"name": "date_close", "label": "Tanggal Ditutup", "type": "date"},
        {"name": "approved", "label": "Disetujui", "type": "bool"},
        {
            "name": "state",
            "label": "Status",
            "type": "select",
            "options": OPT_GOAL_STATE,
            "default": "draft",
        },
        {
            "name": "responsible_id",
            "label": "Penanggung Jawab",
            "type": "m2o",
            "ref": "interested_party",
            "required": True,
        },
    ],
    m2m=[
        {"field": "process_ids", "ref": "process", "label": "Proses Terkait"},
        {"field": "resource_ids", "ref": "resource", "label": "Sumber Daya"},
    ],
)

_e(
    "goal_measurement",
    "Pengukuran Sasaran Mutu",
    "Pengukuran Sasaran Mutu",
    "Perencanaan",
    "name",
    [
        {"name": "name", "label": "Pengukuran", "type": "text", "required": True},
        {"name": "goal_id", "label": "Sasaran Mutu", "type": "m2o", "ref": "goal"},
        {"name": "expected_date", "label": "Tanggal Target", "type": "date"},
        {"name": "measurement_date", "label": "Tanggal Pengukuran", "type": "date"},
        {"name": "comments", "label": "Komentar", "type": "textarea"},
        {
            "name": "result",
            "label": "Hasil",
            "type": "select",
            "options": OPT_MEASUREMENT_RESULT,
        },
        {"name": "result_detail", "label": "Detail Hasil", "type": "text"},
    ],
)

_e(
    "indicator",
    "Indikator",
    "Indikator",
    "Perencanaan",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {"name": "number", "label": "Nomor", "type": "int"},
        {
            "name": "responsible_id",
            "label": "Penanggung Jawab",
            "type": "m2o",
            "ref": "interested_party",
            "required": True,
        },
        {
            "name": "state",
            "label": "Status",
            "type": "select",
            "options": OPT_INDICATOR_STATE,
            "default": "enabled",
        },
        {
            "name": "frequency",
            "label": "Frekuensi",
            "type": "select",
            "options": OPT_INDICATOR_FREQ,
            "default": "annual",
        },
        {
            "name": "process_id",
            "label": "Proses",
            "type": "m2o",
            "ref": "process",
            "required": True,
        },
        {"name": "description", "label": "Objektif", "type": "textarea"},
    ],
)

_e(
    "indicator_measurement",
    "Pengukuran Indikator",
    "Pengukuran Indikator",
    "Perencanaan",
    "name",
    [
        {"name": "name", "label": "Pengukuran", "type": "text", "required": True},
        {
            "name": "indicator_id",
            "label": "Indikator",
            "type": "m2o",
            "ref": "indicator",
        },
        {"name": "expected_date", "label": "Tanggal Target", "type": "date"},
        {"name": "measurement_date", "label": "Tanggal Pengukuran", "type": "date"},
        {"name": "comments", "label": "Komentar", "type": "textarea"},
        {
            "name": "result",
            "label": "Hasil",
            "type": "select",
            "options": OPT_MEASUREMENT_RESULT,
        },
        {"name": "result_detail", "label": "Detail Hasil", "type": "text"},
    ],
)

# --- Risiko / Peluang (Hazard) ----------------------------------------------

_e(
    "hazard",
    "Risiko",
    "Risiko",
    "Manajemen Risiko",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {"name": "number", "label": "Nomor", "type": "int"},
        {"name": "date", "label": "Tanggal", "type": "date"},
        {"name": "description", "label": "Deskripsi", "type": "textarea"},
        {"name": "causes", "label": "Penyebab", "type": "textarea"},
        {"name": "consequences", "label": "Konsekuensi", "type": "textarea"},
        {
            "name": "type_risk",
            "label": "Jenis Risiko",
            "type": "select",
            "options": OPT_HAZARD_TYPE_RISK,
        },
        {"name": "factor", "label": "Faktor", "type": "select", "options": OPT_HAZARD_FACTOR},
        {
            "name": "probability",
            "label": "Probabilitas",
            "type": "select",
            "options": OPT_HAZARD_PROB,
        },
        {"name": "impact", "label": "Dampak", "type": "select", "options": OPT_HAZARD_IMPACT},
        {
            "name": "strategy",
            "label": "Strategi",
            "type": "select",
            "options": OPT_HAZARD_STRATEGY,
        },
        {
            "name": "state",
            "label": "Status",
            "type": "select",
            "options": OPT_HAZARD_STATE,
            "default": "draft",
        },
    ],
    m2m=[
        {"field": "process_ids", "ref": "process", "label": "Proses Terkait"},
        {
            "field": "policy_component_ids",
            "ref": "policy_component",
            "label": "Komponen Kebijakan",
        },
    ],
)

# --- Dokumen (document / procedure / instructive / registry) ---------------

_DOC_FIELDS = [
    {"name": "name", "label": "Nama", "type": "text", "required": True},
    {"name": "identification", "label": "Identifikasi/Kode", "type": "text", "required": True},
    {
        "name": "format",
        "label": "Format",
        "type": "select",
        "options": OPT_DOC_FORMAT,
        "default": "electronic",
    },
    {
        "name": "relation",
        "label": "Relasi",
        "type": "select",
        "options": OPT_DOC_RELATION,
        "default": "sgc&tmc",
    },
    {
        "name": "type",
        "label": "Tipe",
        "type": "select",
        "options": OPT_DOC_TYPE,
        "default": "internal",
    },
    {"name": "holding_time", "label": "Masa Simpan", "type": "text"},
    {"name": "storage", "label": "Lokasi Penyimpanan", "type": "text"},
    {"name": "link", "label": "Tautan", "type": "text"},
    {"name": "disposition", "label": "Disposisi", "type": "text"},
    {"name": "description", "label": "Deskripsi", "type": "textarea"},
    {
        "name": "responsible_id",
        "label": "Penanggung Jawab",
        "type": "m2o",
        "ref": "interested_party",
        "required": True,
    },
    {"name": "approved", "label": "Disetujui", "type": "bool"},
]
_DOC_M2M = [{"field": "process_ids", "ref": "process", "label": "Proses Terkait"}]

_e("document", "Dokumen (umum)", "Dokumen (umum)", "Dokumentasi", "name", _DOC_FIELDS, m2m=_DOC_M2M)
_e("procedure", "Prosedur", "Prosedur", "Dokumentasi", "name", _DOC_FIELDS, m2m=_DOC_M2M)
_e("instructive", "Instruksi Kerja", "Instruksi Kerja", "Dokumentasi", "name", _DOC_FIELDS, m2m=_DOC_M2M)
_e("registry", "Formulir/Rekaman", "Formulir/Rekaman", "Dokumentasi", "name", _DOC_FIELDS, m2m=_DOC_M2M)

_e(
    "version",
    "Versi Dokumen",
    "Versi Dokumen",
    "Dokumentasi",
    "version",
    [
        {"name": "version", "label": "Versi", "type": "text", "required": True},
        {"name": "date_open", "label": "Tanggal Berlaku", "type": "date"},
        {"name": "change_history", "label": "Riwayat Perubahan", "type": "textarea"},
        {
            "name": "responsible_id",
            "label": "Penanggung Jawab",
            "type": "m2o",
            "ref": "interested_party",
            "required": True,
        },
        {"name": "policy_id", "label": "Kebijakan", "type": "m2o", "ref": "policy"},
        {"name": "document_id", "label": "Dokumen (umum)", "type": "m2o", "ref": "document"},
        {"name": "procedure_id", "label": "Prosedur", "type": "m2o", "ref": "procedure"},
        {"name": "instructive_id", "label": "Instruksi Kerja", "type": "m2o", "ref": "instructive"},
        {"name": "registry_id", "label": "Formulir/Rekaman", "type": "m2o", "ref": "registry"},
        {"name": "indicator_id", "label": "Indikator", "type": "m2o", "ref": "indicator"},
    ],
)

# --- Tinjauan (Review) -------------------------------------------------------

_e(
    "review",
    "Tinjauan",
    "Tinjauan",
    "Tinjauan Manajemen",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {"name": "date", "label": "Tanggal", "type": "date"},
        {"name": "conclusion", "label": "Kesimpulan", "type": "textarea"},
        {
            "name": "responsible_id",
            "label": "Penanggung Jawab",
            "type": "m2o",
            "ref": "interested_party",
        },
        {"name": "policy_id", "label": "Kebijakan", "type": "m2o", "ref": "policy"},
        {"name": "document_id", "label": "Dokumen", "type": "m2o", "ref": "document"},
        {"name": "goal_id", "label": "Sasaran Mutu", "type": "m2o", "ref": "goal"},
        {"name": "process_id", "label": "Proses", "type": "m2o", "ref": "process"},
        {"name": "hazard_id", "label": "Risiko", "type": "m2o", "ref": "hazard"},
        {"name": "indicator_id", "label": "Indikator", "type": "m2o", "ref": "indicator"},
        {
            "name": "interested_party_id",
            "label": "Pihak Berkepentingan",
            "type": "m2o",
            "ref": "interested_party",
        },
    ],
)

_e(
    "revision_by_direction",
    "Tinjauan oleh Manajemen Puncak",
    "Tinjauan oleh Manajemen Puncak",
    "Tinjauan Manajemen",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {"name": "description", "label": "Deskripsi", "type": "textarea"},
        {"name": "date_open", "label": "Tanggal Dibuka", "type": "date"},
        {"name": "date_close", "label": "Tanggal Ditutup", "type": "date"},
        {
            "name": "state",
            "label": "Status",
            "type": "select",
            "options": OPT_REVDIR_STATE,
            "default": "open",
        },
    ],
    m2m=[{"field": "resource_ids", "ref": "resource", "label": "Sumber Daya"}],
)

# --- Audit -------------------------------------------------------------------

_e(
    "audit",
    "Audit",
    "Audit",
    "Audit",
    "reference",
    [
        {"name": "reference", "label": "Referensi", "type": "text"},
        {
            "name": "system",
            "label": "Sistem",
            "type": "select",
            "options": OPT_AUDIT_SYSTEM,
            "required": True,
        },
        {"name": "date", "label": "Tanggal", "type": "date"},
        {"name": "closing_date", "label": "Tanggal Penutupan", "type": "datetime"},
        {"name": "strong_points", "label": "Poin Kekuatan", "type": "textarea"},
        {
            "name": "state",
            "label": "Status",
            "type": "select",
            "options": OPT_AUDIT_STATE,
            "default": "open",
        },
    ],
    m2m=[
        {"field": "audited_ids", "ref": "interested_party", "label": "Pihak yang Diaudit"},
        {"field": "auditors_ids", "ref": "interested_party", "label": "Auditor"},
        {"field": "process_ids", "ref": "process", "label": "Proses Terkait"},
    ],
)

_e(
    "audit_verification_line",
    "Baris Verifikasi Audit",
    "Baris Verifikasi Audit",
    "Audit",
    "name",
    [
        {"name": "name", "label": "Pertanyaan", "type": "text", "required": True},
        {"name": "clause", "label": "Klausul", "type": "text", "required": True},
        {"name": "audit_id", "label": "Audit", "type": "m2o", "ref": "audit", "required": True},
        {"name": "is_conformed", "label": "Sesuai", "type": "bool"},
        {"name": "comments", "label": "Komentar", "type": "textarea"},
        {"name": "seq", "label": "Urutan", "type": "int"},
    ],
    order="seq",
)

_e(
    "audit_evaluation",
    "Evaluasi Auditor",
    "Evaluasi Auditor",
    "Audit",
    "name",
    [
        {"name": "name", "label": "Nama", "type": "text"},
        {"name": "date", "label": "Tanggal", "type": "date"},
        {"name": "description", "label": "Deskripsi", "type": "textarea"},
        {"name": "final_note", "label": "Catatan Akhir", "type": "text"},
        {"name": "competent", "label": "Kompeten", "type": "text"},
        {
            "name": "responsible_id",
            "label": "Penanggung Jawab",
            "type": "m2o",
            "ref": "interested_party",
            "required": True,
        },
        {"name": "type", "label": "Sistem", "type": "select", "options": OPT_AUDIT_EVAL_TYPE},
        {"name": "audit_id", "label": "Audit", "type": "m2o", "ref": "audit"},
        {
            "name": "understanding",
            "label": "Pemahaman",
            "type": "select",
            "options": OPT_SCORE_10,
            "default": "-",
        },
        {
            "name": "compliance",
            "label": "Kepatuhan",
            "type": "select",
            "options": OPT_SCORE_10,
            "default": "-",
        },
        {
            "name": "planning",
            "label": "Perencanaan",
            "type": "select",
            "options": OPT_SCORE_10,
            "default": "-",
        },
        {
            "name": "report",
            "label": "Laporan",
            "type": "select",
            "options": OPT_SCORE_10,
            "default": "-",
        },
    ],
    m2m=[{"field": "auditors_ids", "ref": "interested_party", "label": "Auditor"}],
)

# --- Temuan (Finding): Ketidaksesuaian, Observasi, Keluhan, Peluang ---------

_FINDING_BASE_FIELDS = [
    {"name": "name", "label": "Judul", "type": "text"},
    {"name": "reference", "label": "Referensi", "type": "text"},
    {
        "name": "claimant_id",
        "label": "Pelapor",
        "type": "m2o",
        "ref": "interested_party",
        "required": True,
    },
    {
        "name": "interested_party_id",
        "label": "Pihak Terkait",
        "type": "m2o",
        "ref": "interested_party",
        "required": True,
    },
    {"name": "description", "label": "Deskripsi", "type": "textarea", "required": True},
    {"name": "closing_date", "label": "Tanggal Penutupan", "type": "datetime"},
    {
        "name": "stage_id",
        "label": "Tahapan",
        "type": "m2o",
        "ref": "finding_stage",
    },
    {
        "name": "kanban_state",
        "label": "Status Kanban",
        "type": "select",
        "options": OPT_KANBAN_STATE,
        "default": "normal",
    },
    {"name": "audit_id", "label": "Audit Terkait", "type": "m2o", "ref": "audit"},
]
_FINDING_BASE_M2M = [
    {"field": "origin_ids", "ref": "finding_origin", "label": "Asal Temuan"},
    {"field": "process_ids", "ref": "process", "label": "Proses Terkait"},
]

_WEAKNESS_FIELDS = [
    {"name": "analysis", "label": "Analisis", "type": "textarea"},
]
_WEAKNESS_M2M = [{"field": "cause_ids", "ref": "weakness_cause", "label": "Penyebab"}]

_e(
    "non_conformity",
    "Ketidaksesuaian",
    "Ketidaksesuaian",
    "Temuan",
    "reference",
    _FINDING_BASE_FIELDS
    + _WEAKNESS_FIELDS
    + [
        {
            "name": "revision_by_direction_id",
            "label": "Tinjauan Manajemen",
            "type": "m2o",
            "ref": "revision_by_direction",
        },
        {"name": "indicator_id", "label": "Indikator", "type": "m2o", "ref": "indicator"},
    ],
    m2m=_FINDING_BASE_M2M + _WEAKNESS_M2M,
)

_e(
    "observation",
    "Observasi",
    "Observasi",
    "Temuan",
    "reference",
    _FINDING_BASE_FIELDS
    + _WEAKNESS_FIELDS
    + [
        {
            "name": "revision_by_direction_id",
            "label": "Tinjauan Manajemen",
            "type": "m2o",
            "ref": "revision_by_direction",
        },
        {"name": "indicator_id", "label": "Indikator", "type": "m2o", "ref": "indicator"},
    ],
    m2m=_FINDING_BASE_M2M + _WEAKNESS_M2M,
)

_e(
    "complaint",
    "Keluhan",
    "Keluhan",
    "Temuan",
    "reference",
    _FINDING_BASE_FIELDS + _WEAKNESS_FIELDS,
    m2m=_FINDING_BASE_M2M + _WEAKNESS_M2M,
)

_e(
    "opportunity",
    "Peluang",
    "Peluang",
    "Temuan",
    "reference",
    _FINDING_BASE_FIELDS
    + [
        {
            "name": "revision_by_direction_id",
            "label": "Tinjauan Manajemen",
            "type": "m2o",
            "ref": "revision_by_direction",
        },
        {"name": "indicator_id", "label": "Indikator", "type": "m2o", "ref": "indicator"},
    ],
    m2m=_FINDING_BASE_M2M,
)

# --- Aksi & Verifikasi Efektivitas ------------------------------------------

_e(
    "action",
    "Aksi",
    "Aksi",
    "Tindak Lanjut",
    "reference",
    [
        {"name": "name", "label": "Nama", "type": "text", "required": True},
        {"name": "reference", "label": "Referensi", "type": "text"},
        {"name": "active", "label": "Aktif", "type": "bool", "default": True},
        {
            "name": "response_type",
            "label": "Tipe Respons",
            "type": "select",
            "options": OPT_ACTION_RESPONSE_TYPE,
            "required": True,
        },
        {
            "name": "complexity",
            "label": "Kompleksitas",
            "type": "select",
            "options": OPT_COMPLEXITY,
            "required": True,
        },
        {
            "name": "stage_id",
            "label": "Tahapan",
            "type": "m2o",
            "ref": "action_stage",
        },
        {
            "name": "responsible_id",
            "label": "Penanggung Jawab",
            "type": "m2o",
            "ref": "interested_party",
            "required": True,
        },
        {"name": "description", "label": "Deskripsi", "type": "textarea"},
        {"name": "date_deadline", "label": "Tenggat Waktu", "type": "date"},
        {"name": "opening_date", "label": "Tanggal Dibuka", "type": "date"},
        {"name": "date_closed", "label": "Tanggal Ditutup", "type": "date"},
        {"name": "cancel_date", "label": "Tanggal Dibatalkan", "type": "date"},
        {
            "name": "observation_id",
            "label": "Terkait Observasi",
            "type": "m2o",
            "ref": "observation",
        },
        {
            "name": "non_conformity_id",
            "label": "Terkait Ketidaksesuaian",
            "type": "m2o",
            "ref": "non_conformity",
        },
        {
            "name": "complaint_id",
            "label": "Terkait Keluhan",
            "type": "m2o",
            "ref": "complaint",
        },
        {
            "name": "opportunity_id",
            "label": "Terkait Peluang",
            "type": "m2o",
            "ref": "opportunity",
        },
        {"name": "hazard_id", "label": "Terkait Risiko", "type": "m2o", "ref": "hazard"},
        {"name": "goal_id", "label": "Terkait Sasaran Mutu", "type": "m2o", "ref": "goal"},
        {
            "name": "revision_by_direction_id",
            "label": "Terkait Tinjauan Manajemen",
            "type": "m2o",
            "ref": "revision_by_direction",
        },
    ],
)

_e(
    "effectiveness_check",
    "Verifikasi Efektivitas",
    "Verifikasi Efektivitas",
    "Tindak Lanjut",
    "id",
    [
        {"name": "action_id", "label": "Aksi", "type": "m2o", "ref": "action", "required": True},
        {"name": "expected_date", "label": "Tanggal Rencana", "type": "date"},
        {"name": "verification_date", "label": "Tanggal Verifikasi", "type": "date"},
        {"name": "was_effective", "label": "Efektif", "type": "bool"},
        {
            "name": "state",
            "label": "Status",
            "type": "select",
            "options": OPT_EFFCHECK_STATE,
            "default": "pending",
        },
        {"name": "observations", "label": "Catatan", "type": "textarea"},
    ],
)

# Urutan grup untuk sidebar
GROUP_ORDER = [
    "Konteks Organisasi",
    "Perencanaan",
    "Manajemen Risiko",
    "Dokumentasi",
    "Audit",
    "Temuan",
    "Tindak Lanjut",
    "Tinjauan Manajemen",
    "Master Data",
]
