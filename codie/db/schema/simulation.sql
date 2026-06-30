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
