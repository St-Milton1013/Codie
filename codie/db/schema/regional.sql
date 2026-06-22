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
