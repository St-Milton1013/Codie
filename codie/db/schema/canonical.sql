CREATE TABLE canonical_events (
    canonical_event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    normalized_event_name TEXT NOT NULL,
    event_date TEXT,
    format TEXT,
    region TEXT,
    country TEXT,
    venue_or_store TEXT,
    player_count INTEGER,
    deck_count INTEGER,
    event_size_bucket TEXT,
    confidence_score REAL DEFAULT 0,
    dedupe_key TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(dedupe_key)
);

CREATE TABLE canonical_event_sources (
    canonical_event_source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_event_id INTEGER NOT NULL,
    source_event_id INTEGER NOT NULL,
    provider TEXT NOT NULL,
    source_url TEXT,
    source_confidence REAL DEFAULT 1.0,
    merge_reason TEXT,
    created_at TEXT NOT NULL,
    UNIQUE(canonical_event_id, source_event_id),
    FOREIGN KEY(canonical_event_id) REFERENCES canonical_events(canonical_event_id),
    FOREIGN KEY(source_event_id) REFERENCES source_events(source_event_id)
);

CREATE TABLE canonical_decks (
    canonical_deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
    deck_hash TEXT NOT NULL UNIQUE,
    commander_hash TEXT NOT NULL,
    format TEXT DEFAULT 'commander',
    card_count INTEGER NOT NULL,
    commander_count INTEGER NOT NULL,
    color_identity_json TEXT,
    first_seen_at TEXT,
    last_seen_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE canonical_deck_sources (
    canonical_deck_source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_deck_id INTEGER NOT NULL,
    source_deck_id INTEGER NOT NULL,
    source_event_id INTEGER,
    provider TEXT NOT NULL,
    source_url TEXT,
    pilot_name TEXT,
    placement INTEGER,
    placement_label TEXT,
    record_text TEXT,
    source_confidence REAL DEFAULT 1.0,
    created_at TEXT NOT NULL,
    UNIQUE(canonical_deck_id, source_deck_id),
    FOREIGN KEY(canonical_deck_id) REFERENCES canonical_decks(canonical_deck_id),
    FOREIGN KEY(source_deck_id) REFERENCES source_decks(source_deck_id),
    FOREIGN KEY(source_event_id) REFERENCES source_events(source_event_id)
);

CREATE TABLE canonical_deck_cards (
    canonical_deck_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_deck_id INTEGER NOT NULL,
    scryfall_id TEXT NOT NULL,
    oracle_id TEXT,
    quantity INTEGER NOT NULL DEFAULT 1,
    zone TEXT NOT NULL DEFAULT 'mainboard',
    is_commander INTEGER DEFAULT 0,
    is_companion INTEGER DEFAULT 0,
    FOREIGN KEY(canonical_deck_id) REFERENCES canonical_decks(canonical_deck_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id),
    UNIQUE(canonical_deck_id, scryfall_id, zone)
);

CREATE TABLE canonical_deck_commanders (
    canonical_deck_commander_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_deck_id INTEGER NOT NULL,
    scryfall_id TEXT NOT NULL,
    oracle_id TEXT,
    commander_order INTEGER DEFAULT 1,
    commander_role TEXT DEFAULT 'commander',
    FOREIGN KEY(canonical_deck_id) REFERENCES canonical_decks(canonical_deck_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id),
    UNIQUE(canonical_deck_id, scryfall_id)
);

CREATE TABLE event_deck_entries (
    event_deck_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_event_id INTEGER NOT NULL,
    canonical_deck_id INTEGER NOT NULL,
    source_deck_id INTEGER,
    pilot_name TEXT,
    placement INTEGER,
    placement_label TEXT,
    record_text TEXT,
    wins INTEGER,
    losses INTEGER,
    draws INTEGER,
    top_cut_made INTEGER DEFAULT 0,
    final_pod INTEGER DEFAULT 0,
    winner INTEGER DEFAULT 0,
    entry_weight REAL DEFAULT 1.0,
    created_at TEXT NOT NULL,
    FOREIGN KEY(canonical_event_id) REFERENCES canonical_events(canonical_event_id),
    FOREIGN KEY(canonical_deck_id) REFERENCES canonical_decks(canonical_deck_id),
    FOREIGN KEY(source_deck_id) REFERENCES source_decks(source_deck_id)
);

CREATE TABLE tournament_rounds (
    round_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_event_id INTEGER NOT NULL,
    round_number INTEGER NOT NULL,
    round_type TEXT,
    raw_json TEXT,
    FOREIGN KEY(canonical_event_id) REFERENCES canonical_events(canonical_event_id)
);

CREATE TABLE match_results (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    round_id INTEGER NOT NULL,
    player_a_entry_id INTEGER,
    player_b_entry_id INTEGER,
    player_c_entry_id INTEGER,
    player_d_entry_id INTEGER,
    winner_entry_id INTEGER,
    result TEXT,
    raw_json TEXT,
    FOREIGN KEY(round_id) REFERENCES tournament_rounds(round_id)
);
