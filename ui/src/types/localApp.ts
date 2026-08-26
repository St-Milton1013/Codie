export interface LocalApiErrorPayload {
  code: string;
  message: string;
  field?: string;
  details?: Record<string, unknown>;
}

export type LocalApiEnvelope<T> =
  | { ok: true; data: T }
  | { ok: false; error: LocalApiErrorPayload };

export interface HealthStatus {
  service: "ready";
  database_ready: boolean;
  catalog_ready: boolean;
  ui_ready: boolean;
  privacy: string;
}

export interface WorkspaceSummary {
  workspace_root: string;
  database_path: string;
  database_ready: boolean;
  ui_ready: boolean;
  counts: {
    cards: number;
    decks: number;
    saved_analyses: number;
  };
}

export interface BootstrapResult {
  initialized: boolean;
  created: boolean;
  database_path: string;
}

export interface CatalogImportResult {
  imported_count: number;
  rejected_count: number;
  snapshot_hash: string;
  warnings: readonly string[];
  evidence_class: "card_truth";
  from_cache?: boolean;
  source_updated_at?: string | null;
}

export interface DeckSummary {
  user_deck_id: number;
  deck_name: string | null;
  deck_hash: string;
  commander_hash: string | null;
  created_at: string;
  updated_at: string;
  is_temporary: boolean;
  card_count: number;
  saved_analysis_count: number;
  latest_analysis_generated_at: string | null;
}

export interface DeckCard {
  card_name: string;
  quantity: number;
  zone: string | null;
  oracle_id: string | null;
  resolution_status: string | null;
}

export interface DeckDetail {
  summary: DeckSummary;
  cards: readonly DeckCard[];
  analyses: readonly AnalysisSummary[];
  raw_input_included: boolean;
}

export interface DeckImportResult {
  user_deck_id: number;
  analysis_session_id: number;
  deck_hash: string;
  commander_hash: string | null;
  card_count: number;
  unresolved_names: readonly string[];
  source_type: "pasted_decklist" | "moxfield_public_link";
  source_url: string | null;
}

export interface AnalysisSummary {
  saved_analysis_id: number;
  user_deck_id: number | null;
  analysis_type: string;
  generated_at: string;
  deck_hash: string;
}

export interface EvidenceRow {
  oracle_id: string;
  card_name: string;
  evidence_type: string;
  presence_status: "present" | "absent";
  quantity_in_deck: number;
  zones: readonly string[];
  score: number | null;
  sample_size: number | null;
  source_record_id: string | null;
  source_url: string | null;
  evidence_line: string;
}

export interface EvidenceComparison {
  user_deck_id: number;
  deck_hash: string;
  commander_hash: string | null;
  present_count: number;
  absent_count: number;
  generated_at: string;
  rows: readonly EvidenceRow[];
}

export interface AnalysisDetail {
  summary: AnalysisSummary;
  comparison: EvidenceComparison;
  notice: string;
}

export interface ComparisonResult {
  saved_analysis_id: number;
  comparison: EvidenceComparison;
  notice: string;
}

export interface AnalysisExport {
  filename: string;
  media_type: string;
  content: string;
}
