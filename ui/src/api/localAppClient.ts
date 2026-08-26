import type {
  AnalysisDetail,
  AnalysisExport,
  AnalysisSummary,
  BootstrapResult,
  CatalogImportResult,
  ComparisonResult,
  DeckDetail,
  DeckImportResult,
  DeckSummary,
  HealthStatus,
  LocalApiEnvelope,
  LocalApiErrorPayload,
  WorkspaceSummary,
} from "../types/localApp";

export class LocalApiError extends Error {
  readonly code: string;
  readonly field?: string;
  readonly details?: Record<string, unknown>;

  constructor(payload: LocalApiErrorPayload) {
    super(payload.message);
    this.name = "LocalApiError";
    this.code = payload.code;
    this.field = payload.field;
    this.details = payload.details;
  }
}

export const localApi = {
  health: () => request<HealthStatus>("/local/health"),
  workspace: () => request<WorkspaceSummary>("/local/workspace"),
  bootstrap: () => post<BootstrapResult>("/local/database/bootstrap", {}),
  importCatalog: (snapshot: unknown) =>
    post<CatalogImportResult>("/local/catalog/import", { snapshot }),
  prepareCatalog: (refresh = false) =>
    post<CatalogImportResult>("/local/catalog/prepare", {
      allow_network: true,
      refresh,
    }),
  listDecks: () => request<{ decks: DeckSummary[] }>("/local/decks"),
  getDeck: (deckId: number) => request<DeckDetail>(`/local/decks/${deckId}`),
  importDeck: (deckName: string, deckInput: string) =>
    post<DeckImportResult>("/local/decks/import", {
      deck_name: deckName || null,
      deck_input: deckInput,
      allow_network: true,
    }),
  listAnalyses: (deckId: number) =>
    request<{ analyses: AnalysisSummary[] }>(`/local/decks/${deckId}/analyses`),
  compareDeck: (deckId: number, candidates: unknown[]) =>
    post<ComparisonResult>(`/local/decks/${deckId}/comparisons`, { candidates }),
  getAnalysis: (analysisId: number) =>
    request<AnalysisDetail>(`/local/analyses/${analysisId}`),
  exportAnalysis: (analysisId: number, format: "json" | "markdown") =>
    request<AnalysisExport>(`/local/analyses/${analysisId}/export?format=${format}`),
};

async function post<T>(path: string, body: Record<string, unknown>): Promise<T> {
  return request<T>(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, { ...init, cache: "no-store" });
  let payload: LocalApiEnvelope<T>;
  try {
    payload = (await response.json()) as LocalApiEnvelope<T>;
  } catch {
    throw new Error("Codie returned an unreadable local response.");
  }
  if (!response.ok || !payload.ok) {
    if (!payload.ok) {
      throw new LocalApiError(payload.error);
    }
    throw new Error(`Codie local request failed (${response.status}).`);
  }
  return payload.data;
}
