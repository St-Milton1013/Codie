CREATE TABLE ingestion_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    pipeline_name TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL,
    objects_processed INTEGER DEFAULT 0,
    objects_inserted INTEGER DEFAULT 0,
    objects_updated INTEGER DEFAULT 0,
    objects_failed INTEGER DEFAULT 0,
    log_path TEXT,
    config_json TEXT,
    error_summary TEXT
);

CREATE TABLE provider_objects (
    provider_object_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    object_type TEXT NOT NULL,
    provider_id TEXT,
    source_url TEXT,
    retrieved_at TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    raw_payload_json TEXT,
    raw_file_path TEXT,
    run_id INTEGER,
    UNIQUE(provider, object_type, provider_id, payload_hash),
    FOREIGN KEY(run_id) REFERENCES ingestion_runs(run_id)
);

CREATE TABLE source_events (
    source_event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    provider_event_id TEXT,
    source_url TEXT,
    original_source TEXT,
    original_source_url TEXT,
    event_name TEXT,
    normalized_event_name TEXT,
    event_date TEXT,
    format TEXT,
    source_region TEXT,
    source_country TEXT,
    source_store_tag TEXT,
    source_language TEXT,
    source_reported_player_count INTEGER,
    source_reported_deck_count INTEGER,
    source_participants INTEGER,
    tournament_size_bucket TEXT,
    raw_json TEXT,
    provider_object_id INTEGER,
    imported_at TEXT NOT NULL,
    canonical_event_id INTEGER,
    dedupe_status TEXT DEFAULT 'pending',
    FOREIGN KEY(provider_object_id) REFERENCES provider_objects(provider_object_id)
);

CREATE TABLE source_decks (
    source_deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    provider_deck_id TEXT,
    source_event_id INTEGER,
    source_url TEXT,
    source_download_url TEXT,
    source_visual_url TEXT,
    source_export_urls_json TEXT,
    source_same_tournament_url TEXT,
    source_same_archetype_url TEXT,
    deck_title TEXT,
    commander_text TEXT,
    source_archetype_name TEXT,
    source_player_name TEXT,
    source_rank INTEGER,
    source_rank_label TEXT,
    source_score_label TEXT,
    source_record TEXT,
    source_win_rate REAL,
    source_price_paper REAL,
    source_price_mtgo REAL,
    source_store_tag TEXT,
    deck_hash TEXT,
    raw_json TEXT,
    provider_object_id INTEGER,
    imported_at TEXT NOT NULL,
    canonical_deck_id INTEGER,
    dedupe_status TEXT DEFAULT 'pending',
    FOREIGN KEY(source_event_id) REFERENCES source_events(source_event_id),
    FOREIGN KEY(provider_object_id) REFERENCES provider_objects(provider_object_id)
);

CREATE TABLE source_deck_cards (
    source_deck_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_deck_id INTEGER NOT NULL,
    raw_name TEXT NOT NULL,
    normalized_name TEXT,
    quantity INTEGER NOT NULL DEFAULT 1,
    source_zone TEXT DEFAULT 'mainboard',
    source_order INTEGER,
    scryfall_id TEXT,
    oracle_id TEXT,
    resolution_status TEXT NOT NULL DEFAULT 'pending',
    resolution_note TEXT,
    raw_entry TEXT,
    FOREIGN KEY(source_deck_id) REFERENCES source_decks(source_deck_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);

CREATE TABLE deck_auxiliary_cards (
    auxiliary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_deck_id INTEGER NOT NULL,
    canonical_deck_id INTEGER,
    name TEXT NOT NULL,
    normalized_name TEXT,
    auxiliary_type TEXT NOT NULL,
    source_zone TEXT,
    is_game_piece INTEGER DEFAULT 0,
    is_deck_card INTEGER DEFAULT 0,
    scryfall_id TEXT,
    oracle_id TEXT,
    mtgjson_id TEXT,
    legality_profile_json TEXT,
    raw_entry TEXT,
    validation_status TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(source_deck_id) REFERENCES source_decks(source_deck_id)
);

CREATE TABLE source_primers (
    source_primer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    deck_url TEXT,
    primer_url TEXT NOT NULL,
    commander_text TEXT,
    partner_text TEXT,
    deck_title TEXT,
    primer_title TEXT,
    author TEXT,
    author_url TEXT,
    published_at TEXT,
    modified_at TEXT,
    source_tags_json TEXT,
    raw_metadata_json TEXT,
    imported_at TEXT NOT NULL
);

CREATE TABLE source_combos (
    source_combo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    provider_combo_id TEXT,
    combo_url TEXT,
    combo_name TEXT,
    components_json TEXT,
    outputs_json TEXT,
    raw_json TEXT,
    imported_at TEXT NOT NULL
);
