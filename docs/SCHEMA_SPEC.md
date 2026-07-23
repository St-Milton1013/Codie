## 10. DATABASE SPECIFICATION

This is a first‑pass schema contract. DeepSeek implements this as structured SQL files, not redesign it mid‑flight.

### 10.1 Core Card Tables

#### `cards`

```sql
CREATE TABLE cards (
    scryfall_id TEXT PRIMARY KEY,
    oracle_id TEXT,
    name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    mana_cost TEXT,
    mana_value REAL,
    type_line TEXT,
    oracle_text TEXT,
    colors_json TEXT,
    color_identity_json TEXT,
    legalities_json TEXT,
    produced_mana_json TEXT,
    keywords_json TEXT,
    layout TEXT,
    card_faces_json TEXT,
    image_uris_json TEXT,
    prices_json TEXT,
    set_code TEXT,
    collector_number TEXT,
    rarity TEXT,
    released_at TEXT,
    is_reserved INTEGER DEFAULT 0,
    is_digital INTEGER DEFAULT 0,
    is_legal_commander INTEGER DEFAULT 0,
    is_commander_candidate INTEGER DEFAULT 0,
    raw_json TEXT NOT NULL,
    imported_at TEXT NOT NULL
);
```

**Indexes:**
```sql
CREATE INDEX idx_cards_oracle_id ON cards(oracle_id);
CREATE INDEX idx_cards_normalized_name ON cards(normalized_name);
CREATE INDEX idx_cards_color_identity ON cards(color_identity_json);
```

#### `commanders`

```sql
CREATE TABLE commanders (
    commander_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scryfall_id TEXT NOT NULL,
    oracle_id TEXT,
    canonical_name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    color_identity_json TEXT NOT NULL,
    is_partner INTEGER DEFAULT 0,
    is_background_compatible INTEGER DEFAULT 0,
    is_doctor_companion INTEGER DEFAULT 0,
    is_friends_forever INTEGER DEFAULT 0,
    legal_status TEXT,
    raw_source TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);
```

### 10.2 Source Tables

#### `ingestion_runs`

```sql
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
```

#### `provider_objects`

```sql
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
```

#### `source_events`

```sql
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
```

#### `source_decks`

```sql
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
```

#### `source_deck_cards`

```sql
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
```

#### `deck_auxiliary_cards`

```sql
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
```

**Supported auxiliary types:**
```text
commander_candidate
companion
sticker_sheet
attraction
real_sideboard_card
unknown_auxiliary
```

**Auxiliary game pieces never count toward:**
```text
Mainboard inclusion
Staple detection
Recommendation scoring
Deck similarity
Package detection
Card frequency stats
```

### 10.3 Canonical Tables

#### `canonical_events`

```sql
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
```

#### `canonical_event_sources`

```sql
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
```

#### `canonical_decks`

```sql
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
```

#### `canonical_deck_sources`

```sql
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
```

#### `canonical_deck_cards`

```sql
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
```

#### `canonical_deck_commanders`

```sql
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
```

#### `event_deck_entries`

```sql
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
```

#### `tournament_rounds`

```sql
CREATE TABLE tournament_rounds (
    round_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_event_id INTEGER NOT NULL,
    round_number INTEGER NOT NULL,
    round_type TEXT,
    raw_json TEXT,
    FOREIGN KEY(canonical_event_id) REFERENCES canonical_events(canonical_event_id)
);
```

#### `match_results`

```sql
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
```

### 10.4 Primer Tables

#### `source_primers`

```sql
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
```

#### `primer_registry`

```sql
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
```

### 10.5 Combo And Package Tables

#### `source_combos`

```sql
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
```

#### `combos`

```sql
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
```

#### `combo_cards`

```sql
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
```

#### `package_registry`

```sql
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
```

#### `package_cards`

```sql
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
```

### 10.6 Analytics Tables

#### `card_performance_metrics`

```sql
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
```

**Oracle ID note:** `oracle_id` is an indexed analytics grouping key, not an enforced foreign key target, because multiple Scryfall printings can share one oracle ID.

#### `historical_snapshots`

```sql
CREATE TABLE historical_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date TEXT NOT NULL,
    window_type TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(snapshot_date, window_type)
);
```

#### `historical_commander_metrics`

```sql
CREATE TABLE historical_commander_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id INTEGER NOT NULL,
    commander_signature TEXT NOT NULL,
    meta_share REAL,
    weighted_meta_share REAL,
    deck_count INTEGER,
    FOREIGN KEY(snapshot_id) REFERENCES historical_snapshots(snapshot_id)
);
```

#### `historical_card_metrics`

```sql
CREATE TABLE historical_card_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id INTEGER NOT NULL,
    oracle_id TEXT NOT NULL,
    inclusion_rate REAL,
    weighted_inclusion_rate REAL,
    sample_size INTEGER,
    FOREIGN KEY(snapshot_id) REFERENCES historical_snapshots(snapshot_id)
);
```

#### `evidence_counts`

```sql
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
```

#### `card_statistics_snapshots`

```sql
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
```

#### `card_statistics`

```sql
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
```

#### `recommendation_runs`

```sql
CREATE TABLE recommendation_runs (
    recommendation_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_deck_hash TEXT NOT NULL,
    commander_hash TEXT,
    generated_at TEXT NOT NULL,
    config_json TEXT,
    source_snapshot_id INTEGER,
    notes TEXT
);
```

#### `recommendation_candidates`

```sql
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
```

#### `innovation_snapshot_runs`

```sql
CREATE TABLE innovation_snapshot_runs (
    innovation_snapshot_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    generated_at TEXT NOT NULL,
    config_hash TEXT NOT NULL,
    config_json TEXT NOT NULL,
    notes TEXT,
    UNIQUE(generated_at, config_hash)
);
```

#### `innovation_snapshot_items`

```sql
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
```

### 10.7 Regional Metrics Tables

#### `regional_commander_metrics`

```sql
CREATE TABLE regional_commander_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_code TEXT NOT NULL,
    country_code TEXT,
    time_window TEXT NOT NULL,
    window_end_date TEXT NOT NULL,
    commander_signature TEXT NOT NULL,
    meta_share REAL,
    weighted_meta_share REAL,
    sample_size INTEGER,
    updated_at TEXT NOT NULL,
    UNIQUE(region_code, country_code, time_window, window_end_date, commander_signature)
);
```

#### `regional_card_metrics`

```sql
CREATE TABLE regional_card_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_code TEXT NOT NULL,
    country_code TEXT,
    time_window TEXT NOT NULL,
    window_end_date TEXT NOT NULL,
    oracle_id TEXT NOT NULL,
    inclusion_rate REAL,
    weighted_inclusion_rate REAL,
    sample_size INTEGER,
    updated_at TEXT NOT NULL,
    UNIQUE(region_code, country_code, time_window, window_end_date, oracle_id)
);
```

#### `regional_package_metrics`

```sql
CREATE TABLE regional_package_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_code TEXT NOT NULL,
    country_code TEXT,
    time_window TEXT NOT NULL,
    window_end_date TEXT NOT NULL,
    package_id INTEGER NOT NULL,
    adoption_rate REAL,
    performance_score REAL,
    sample_size INTEGER,
    updated_at TEXT NOT NULL,
    UNIQUE(region_code, country_code, time_window, window_end_date, package_id),
    FOREIGN KEY(package_id) REFERENCES package_registry(package_id)
);
```

**Region codes:**
```text
global
north_america
europe
japan
other
```

### 10.8 Simulation Tables

#### `simulation_batches`

```sql
CREATE TABLE simulation_batches (
    batch_id TEXT PRIMARY KEY,
    deck_hash TEXT NOT NULL,
    decklist_source TEXT,
    games_requested INTEGER NOT NULL,
    games_completed INTEGER NOT NULL DEFAULT 0,
    min_mulligan_keep INTEGER NOT NULL,
    mulligan_mode TEXT,
    elapsed_ms INTEGER,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    completed_at TEXT,
    raw_config_json TEXT
);
```

#### `simulation_batch_results`

```sql
CREATE TABLE simulation_batch_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id TEXT NOT NULL,
    target_card TEXT NOT NULL,
    target_card_id TEXT,
    target_zone TEXT NOT NULL,
    turn INTEGER NOT NULL,
    win_count INTEGER NOT NULL,
    win_rate REAL NOT NULL,
    margin_of_error REAL,
    missing_cards_json TEXT,
    raw_payload_json TEXT,
    FOREIGN KEY(batch_id) REFERENCES simulation_batches(batch_id)
);
```

#### `simulation_traces`

```sql
CREATE TABLE simulation_traces (
    trace_id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id TEXT NOT NULL,
    result_id INTEGER,
    game_index INTEGER,
    success INTEGER,
    mulligan_count INTEGER,
    opening_hand_json TEXT,
    final_state_json TEXT,
    action_trace_json TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(batch_id) REFERENCES simulation_batches(batch_id),
    FOREIGN KEY(result_id) REFERENCES simulation_batch_results(result_id)
);
```

#### `simulation_line_reviews`

```sql
CREATE TABLE simulation_line_reviews (
    review_id TEXT PRIMARY KEY,
    challenge_id TEXT NOT NULL,
    batch_id TEXT,
    result_id INTEGER,
    trace_id INTEGER,
    deck_hash TEXT NOT NULL,
    target_card TEXT NOT NULL,
    target_turn INTEGER NOT NULL,
    simulator_success INTEGER NOT NULL,
    simulator_status TEXT NOT NULL,
    action_trace_json TEXT NOT NULL,
    review_status TEXT NOT NULL,
    review_reason TEXT NOT NULL,
    review_note TEXT,
    affected_cards_json TEXT NOT NULL,
    affected_actions_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(batch_id) REFERENCES simulation_batches(batch_id),
    FOREIGN KEY(result_id) REFERENCES simulation_batch_results(result_id),
    FOREIGN KEY(trace_id) REFERENCES simulation_traces(trace_id)
);
```

Recommended indexes:

```sql
CREATE INDEX idx_simulation_line_reviews_challenge_id ON simulation_line_reviews(challenge_id);
CREATE INDEX idx_simulation_line_reviews_deck_hash ON simulation_line_reviews(deck_hash);
CREATE INDEX idx_simulation_line_reviews_target_card ON simulation_line_reviews(target_card);
CREATE INDEX idx_simulation_line_reviews_trace_id ON simulation_line_reviews(trace_id);
CREATE INDEX idx_simulation_line_reviews_review_status ON simulation_line_reviews(review_status);
```

### 10.9 User Tables

#### `user_decks`

```sql
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
```

#### `user_deck_cards`

```sql
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
```

#### `saved_analysis`

```sql
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
```

#### `user_labels`

```sql
CREATE TABLE user_labels (
    user_label_id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    label TEXT NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL
);
```

#### `custom_packages`

```sql
CREATE TABLE custom_packages (
    custom_package_id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_name TEXT NOT NULL,
    package_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

#### `analysis_sessions`

```sql
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
```

## Relationship Intelligence Persistence

Relationship Intelligence measurements are analytics-owned, append-only
records. Population manifests freeze the exact canonical observation units
used for a measurement. Recalculation creates new versioned identities rather
than updating historical rows.

### `relationship_population_specs`

Stores deterministic population filters and policy JSON. Identity is unique
on `(population_spec_hash, population_spec_version)`.

### `relationship_population_manifests`

Stores immutable realized population counts and source snapshot references.
Each row references one population specification and is unique on
`(population_manifest_hash, population_manifest_version)`.

### `relationship_population_members`

Stores the stable ordered membership of a manifest. Applicable canonical deck
and event references use foreign keys. Member sequence and observation-unit
identity are unique within a manifest.

### `relationship_measurements`

Stores endpoint identity, directionality, manifest identity, raw `N`, `nA`,
`nB`, and `nAB` counts, population disclosure counts, observed and expected
co-occurrence, provenance, caveats, and metric-bundle version. Count checks
enforce:

```text
0 <= nAB <= nA <= N
0 <= nAB <= nB <= N
N > 0
```

Identity is unique on
`(relationship_measurement_hash, relationship_measurement_version)`.

### `relationship_measurement_metrics`

Stores each constitutional metric separately. Allowed names are `support`,
`directional_confidence`, `dependence_delta`, `lift`, `leverage`,
`jaccard_similarity`, and `pmi`. A null value requires a visible
`undefined_reason`; a defined value prohibits one. No combined relationship
or synergy score is stored.

### Relationship indexes

Indexes cover specification, manifest, measurement, endpoint-pair, metric,
member-order, version, and audit-time retrieval. `AnalyticsRepository` is the
sole owner of this persistence family.
