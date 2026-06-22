CREATE TABLE user_decks (
    user_deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
    deck_name TEXT,
    source_url TEXT,
    deck_hash TEXT NOT NULL,
    commander_hash TEXT,
    raw_input TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_temporary INTEGER DEFAULT 1
);

CREATE TABLE user_deck_cards (
    user_deck_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_deck_id INTEGER NOT NULL,
    scryfall_id TEXT,
    oracle_id TEXT,
    raw_name TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    zone TEXT DEFAULT 'mainboard',
    resolution_status TEXT,
    FOREIGN KEY(user_deck_id) REFERENCES user_decks(user_deck_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);

CREATE TABLE saved_analysis (
    saved_analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_deck_id INTEGER,
    deck_hash TEXT NOT NULL,
    analysis_type TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    summary_json TEXT NOT NULL,
    report_path TEXT,
    FOREIGN KEY(user_deck_id) REFERENCES user_decks(user_deck_id)
);

CREATE TABLE user_labels (
    user_label_id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    label TEXT NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE custom_packages (
    custom_package_id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_name TEXT NOT NULL,
    package_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE analysis_sessions (
    analysis_session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_deck_id INTEGER,
    deck_hash TEXT NOT NULL,
    commander_hash TEXT,
    session_type TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    config_json TEXT,
    summary_json TEXT,
    notes TEXT,
    FOREIGN KEY(user_deck_id) REFERENCES user_decks(user_deck_id)
);
