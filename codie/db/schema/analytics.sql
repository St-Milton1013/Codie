CREATE TABLE card_performance_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    oracle_id TEXT NOT NULL,
    scryfall_id TEXT,
    time_window TEXT NOT NULL,
    window_end_date TEXT NOT NULL,
    raw_inclusion_rate REAL,
    weighted_inclusion_rate REAL,
    winner_inclusion_rate REAL,
    topcut_inclusion_rate REAL,
    winrate_with_card REAL,
    winrate_without_card REAL,
    winrate_delta REAL,
    topcut_delta REAL,
    confidence_score REAL,
    sample_size INTEGER,
    trend_30d REAL,
    trend_90d REAL,
    trend_180d REAL,
    trend_365d REAL,
    updated_at TEXT NOT NULL,
    UNIQUE(oracle_id, time_window, window_end_date)
);

CREATE TABLE historical_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date TEXT NOT NULL,
    window_type TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(snapshot_date, window_type)
);

CREATE TABLE historical_commander_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id INTEGER NOT NULL,
    commander_signature TEXT NOT NULL,
    meta_share REAL,
    weighted_meta_share REAL,
    deck_count INTEGER,
    FOREIGN KEY(snapshot_id) REFERENCES historical_snapshots(snapshot_id)
);

CREATE TABLE historical_card_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id INTEGER NOT NULL,
    oracle_id TEXT NOT NULL,
    inclusion_rate REAL,
    weighted_inclusion_rate REAL,
    sample_size INTEGER,
    FOREIGN KEY(snapshot_id) REFERENCES historical_snapshots(snapshot_id)
);

CREATE TABLE evidence_counts (
    evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    tournament_evidence_count INTEGER DEFAULT 0,
    primer_evidence_count INTEGER DEFAULT 0,
    combo_evidence_count INTEGER DEFAULT 0,
    package_evidence_count INTEGER DEFAULT 0,
    simulation_evidence_count INTEGER DEFAULT 0,
    updated_at TEXT NOT NULL,
    UNIQUE(entity_type, entity_id)
);

CREATE TABLE card_statistics_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scope_type TEXT NOT NULL,
    scope_key TEXT,
    time_window TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    config_json TEXT,
    source_count INTEGER,
    canonical_event_count INTEGER,
    canonical_deck_count INTEGER
);

CREATE TABLE card_statistics (
    card_stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id INTEGER NOT NULL,
    scryfall_id TEXT,
    oracle_id TEXT,
    inclusion_count INTEGER DEFAULT 0,
    inclusion_rate REAL,
    placement_weighted_usage REAL,
    top_cut_count INTEGER DEFAULT 0,
    top_cut_rate REAL,
    winner_count INTEGER DEFAULT 0,
    win_rate_with_card REAL,
    win_rate_without_card REAL,
    win_rate_delta REAL,
    p_value REAL,
    confidence REAL,
    sample_size INTEGER,
    FOREIGN KEY(snapshot_id) REFERENCES card_statistics_snapshots(snapshot_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);

CREATE TABLE recommendation_runs (
    recommendation_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_deck_hash TEXT NOT NULL,
    commander_hash TEXT,
    generated_at TEXT NOT NULL,
    config_json TEXT,
    source_snapshot_id INTEGER,
    notes TEXT
);

CREATE TABLE recommendation_candidates (
    candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recommendation_run_id INTEGER NOT NULL,
    scryfall_id TEXT,
    oracle_id TEXT,
    candidate_type TEXT NOT NULL,
    recommendation_score REAL,
    inclusion_rate REAL,
    lift_score REAL,
    confidence_score REAL,
    similarity_score REAL,
    package_completion_score REAL,
    generic_staple_penalty REAL,
    evidence_json TEXT NOT NULL,
    explanation_text TEXT,
    FOREIGN KEY(recommendation_run_id) REFERENCES recommendation_runs(recommendation_run_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);
