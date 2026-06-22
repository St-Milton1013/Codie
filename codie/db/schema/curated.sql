CREATE TABLE commander_registry (
    commander_registry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    commander_key TEXT NOT NULL UNIQUE,
    commander_signature TEXT NOT NULL,
    display_name TEXT NOT NULL,
    source TEXT NOT NULL,
    source_url TEXT,
    source_label TEXT,
    is_curated INTEGER DEFAULT 1,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE alias_registry (
    alias_id INTEGER PRIMARY KEY AUTOINCREMENT,
    alias TEXT NOT NULL,
    normalized_alias TEXT NOT NULL UNIQUE,
    target_type TEXT NOT NULL,
    target_scryfall_id TEXT,
    target_oracle_id TEXT,
    target_name TEXT NOT NULL,
    normalized_target_name TEXT NOT NULL,
    source TEXT NOT NULL,
    source_url TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(target_scryfall_id) REFERENCES cards(scryfall_id)
);

CREATE TABLE archetype_label_registry (
    archetype_label_id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL,
    normalized_label TEXT NOT NULL,
    label_type TEXT NOT NULL,
    source TEXT NOT NULL,
    source_url TEXT,
    is_curated INTEGER DEFAULT 1,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(normalized_label, source)
);

CREATE TABLE primer_registry (
    primer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    deck_url TEXT,
    primer_url TEXT NOT NULL UNIQUE,
    commander_key TEXT,
    partner_key TEXT,
    deck_title TEXT,
    primer_title TEXT,
    author TEXT,
    author_url TEXT,
    published_at TEXT,
    modified_at TEXT,
    primer_updated_at_text TEXT,
    primer_updated_at_parsed TEXT,
    likes INTEGER,
    views INTEGER,
    comments INTEGER,
    bracket TEXT,
    has_primer_route INTEGER DEFAULT 0,
    primer_content_present INTEGER DEFAULT 0,
    primer_toc_present INTEGER DEFAULT 0,
    primer_heading_count INTEGER DEFAULT 0,
    primer_section_names_json TEXT,
    primer_external_link_count INTEGER DEFAULT 0,
    primer_video_count INTEGER DEFAULT 0,
    primer_image_count INTEGER DEFAULT 0,
    cedh_title_signal INTEGER DEFAULT 0,
    cedh_tag_signal INTEGER DEFAULT 0,
    competitive_tag_signal INTEGER DEFAULT 0,
    tournament_title_signal INTEGER DEFAULT 0,
    content_length_estimate INTEGER,
    primer_quality_score REAL,
    raw_metadata_json TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE combos (
    combo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL DEFAULT 'commander_spellbook',
    provider_combo_id TEXT,
    combo_url TEXT NOT NULL,
    combo_name TEXT,
    normalized_name TEXT,
    outputs_json TEXT,
    raw_json TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(provider, provider_combo_id)
);

CREATE TABLE combo_cards (
    combo_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    combo_id INTEGER NOT NULL,
    scryfall_id TEXT,
    oracle_id TEXT,
    card_name TEXT NOT NULL,
    role TEXT,
    required INTEGER DEFAULT 1,
    FOREIGN KEY(combo_id) REFERENCES combos(combo_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);

CREATE TABLE package_registry (
    package_id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_name TEXT NOT NULL UNIQUE,
    package_type TEXT NOT NULL,
    source TEXT NOT NULL,
    source_url TEXT,
    description TEXT,
    is_curated INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE package_cards (
    package_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    scryfall_id TEXT,
    oracle_id TEXT,
    card_name TEXT NOT NULL,
    role TEXT,
    required INTEGER DEFAULT 0,
    weight REAL DEFAULT 1.0,
    FOREIGN KEY(package_id) REFERENCES package_registry(package_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);
