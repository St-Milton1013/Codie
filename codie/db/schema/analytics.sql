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

CREATE TABLE innovation_snapshot_runs (
    innovation_snapshot_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    generated_at TEXT NOT NULL,
    config_hash TEXT NOT NULL,
    config_json TEXT NOT NULL,
    notes TEXT,
    UNIQUE(generated_at, config_hash)
);

CREATE TABLE innovation_snapshot_items (
    innovation_snapshot_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    innovation_snapshot_run_id INTEGER NOT NULL,
    innovation_id TEXT NOT NULL,
    oracle_id TEXT NOT NULL,
    scryfall_id TEXT,
    commander_signature TEXT,
    region_code TEXT,
    innovation_type TEXT NOT NULL,
    recent_window TEXT NOT NULL,
    baseline_window TEXT NOT NULL,
    recent_inclusion_rate REAL,
    baseline_inclusion_rate REAL,
    usage_delta REAL,
    recent_topcut_count INTEGER DEFAULT 0,
    recent_winner_count INTEGER DEFAULT 0,
    first_recent_seen_at TEXT NOT NULL,
    last_seen_before_recent_window TEXT,
    card_released_at TEXT,
    is_new_release INTEGER DEFAULT 0,
    sample_size INTEGER DEFAULT 0,
    confidence_score REAL,
    source_event_ids_json TEXT NOT NULL,
    source_deck_ids_json TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    UNIQUE(innovation_snapshot_run_id, innovation_id),
    FOREIGN KEY(innovation_snapshot_run_id) REFERENCES innovation_snapshot_runs(innovation_snapshot_run_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);
