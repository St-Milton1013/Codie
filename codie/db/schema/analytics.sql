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

CREATE TABLE relationship_population_specs (
    population_spec_id INTEGER PRIMARY KEY AUTOINCREMENT,
    population_spec_version TEXT NOT NULL,
    population_spec_hash TEXT NOT NULL,
    observation_unit TEXT NOT NULL,
    scope_type TEXT NOT NULL,
    scope_key TEXT,
    zone_scope TEXT,
    window_start_date TEXT,
    window_end_date TEXT,
    region TEXT,
    store TEXT,
    organizer TEXT,
    minimum_event_size INTEGER CHECK(minimum_event_size IS NULL OR minimum_event_size >= 0),
    placement_filter TEXT,
    deduplication_policy TEXT NOT NULL,
    concentration_policy TEXT NOT NULL,
    spec_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(population_spec_hash, population_spec_version)
);

CREATE TABLE relationship_population_manifests (
    population_manifest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    population_manifest_version TEXT NOT NULL,
    population_manifest_hash TEXT NOT NULL,
    population_spec_id INTEGER NOT NULL,
    population_spec_version TEXT NOT NULL,
    population_spec_hash TEXT NOT NULL,
    source_snapshot_refs_json TEXT NOT NULL,
    candidate_population_count INTEGER NOT NULL CHECK(candidate_population_count >= 0),
    usable_population_count INTEGER NOT NULL CHECK(usable_population_count >= 0),
    unknown_or_excluded_count INTEGER NOT NULL CHECK(unknown_or_excluded_count >= 0),
    deduplicated_population_count INTEGER NOT NULL CHECK(deduplicated_population_count >= 0),
    generated_at TEXT NOT NULL,
    UNIQUE(population_manifest_hash, population_manifest_version),
    FOREIGN KEY(population_spec_id) REFERENCES relationship_population_specs(population_spec_id)
);

CREATE TABLE relationship_population_members (
    population_member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    population_manifest_id INTEGER NOT NULL,
    member_sequence INTEGER NOT NULL CHECK(member_sequence >= 0),
    observation_unit_type TEXT NOT NULL,
    observation_unit_id TEXT NOT NULL,
    canonical_deck_id INTEGER,
    canonical_event_id INTEGER,
    inclusion_status TEXT NOT NULL,
    exclusion_reason TEXT,
    deduplication_key TEXT NOT NULL,
    concentration_group_key TEXT,
    UNIQUE(population_manifest_id, member_sequence),
    UNIQUE(population_manifest_id, observation_unit_type, observation_unit_id),
    FOREIGN KEY(population_manifest_id) REFERENCES relationship_population_manifests(population_manifest_id),
    FOREIGN KEY(canonical_deck_id) REFERENCES canonical_decks(canonical_deck_id),
    FOREIGN KEY(canonical_event_id) REFERENCES canonical_events(canonical_event_id)
);

CREATE TABLE relationship_measurements (
    relationship_measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    relationship_measurement_version TEXT NOT NULL,
    relationship_measurement_hash TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    source_endpoint_type TEXT NOT NULL,
    source_endpoint_id TEXT NOT NULL,
    target_endpoint_type TEXT NOT NULL,
    target_endpoint_id TEXT NOT NULL,
    directionality TEXT NOT NULL,
    population_manifest_id INTEGER NOT NULL,
    population_manifest_version TEXT NOT NULL,
    N INTEGER NOT NULL CHECK(N > 0),
    nA INTEGER NOT NULL CHECK(nA >= 0 AND nA <= N),
    nB INTEGER NOT NULL CHECK(nB >= 0 AND nB <= N),
    nAB INTEGER NOT NULL CHECK(nAB >= 0 AND nAB <= nA AND nAB <= nB),
    candidate_population_count INTEGER NOT NULL CHECK(candidate_population_count >= 0),
    usable_population_count INTEGER NOT NULL CHECK(usable_population_count >= 0),
    unknown_or_excluded_count INTEGER NOT NULL CHECK(unknown_or_excluded_count >= 0),
    deduplicated_population_count INTEGER NOT NULL CHECK(deduplicated_population_count >= 0),
    observed_co_occurrence REAL NOT NULL,
    expected_co_occurrence REAL NOT NULL,
    metric_bundle_version TEXT NOT NULL,
    provenance_refs_json TEXT NOT NULL,
    caveat_refs_json TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    UNIQUE(relationship_measurement_hash, relationship_measurement_version),
    FOREIGN KEY(population_manifest_id) REFERENCES relationship_population_manifests(population_manifest_id)
);

CREATE TABLE relationship_measurement_metrics (
    relationship_measurement_metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    relationship_measurement_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL CHECK(metric_name IN (
        'support', 'directional_confidence', 'dependence_delta', 'lift',
        'leverage', 'jaccard_similarity', 'pmi'
    )),
    metric_version TEXT NOT NULL,
    orientation TEXT NOT NULL,
    metric_value REAL,
    numerator REAL,
    denominator REAL,
    undefined_reason TEXT,
    CHECK(
        (metric_value IS NULL AND undefined_reason IS NOT NULL AND length(trim(undefined_reason)) > 0)
        OR (metric_value IS NOT NULL AND undefined_reason IS NULL)
    ),
    UNIQUE(relationship_measurement_id, metric_name, metric_version, orientation),
    FOREIGN KEY(relationship_measurement_id) REFERENCES relationship_measurements(relationship_measurement_id)
);
