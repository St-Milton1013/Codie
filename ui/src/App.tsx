import { useCallback, useEffect, useState } from "react";
import { LocalApiError, localApi } from "./api/localAppClient";
import type {
  AnalysisDetail,
  AnalysisSummary,
  CatalogImportResult,
  DeckDetail,
  DeckSummary,
  HealthStatus,
  WorkspaceSummary,
} from "./types/localApp";

type BusyAction = "catalog" | "deck" | "comparison" | "refresh" | "export";

export default function App() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [workspace, setWorkspace] = useState<WorkspaceSummary | null>(null);
  const [decks, setDecks] = useState<DeckSummary[]>([]);
  const [selectedDeck, setSelectedDeck] = useState<DeckDetail | null>(null);
  const [analyses, setAnalyses] = useState<AnalysisSummary[]>([]);
  const [selectedAnalysis, setSelectedAnalysis] = useState<AnalysisDetail | null>(null);
  const [catalogResult, setCatalogResult] = useState<CatalogImportResult | null>(null);
  const [deckName, setDeckName] = useState("");
  const [decklist, setDecklist] = useState("");
  const [evidenceFile, setEvidenceFile] = useState<File | null>(null);
  const [busy, setBusy] = useState<BusyAction | null>("refresh");
  const [notice, setNotice] = useState("Checking the contained local workspace.");
  const [actionError, setActionError] = useState<string | null>(null);
  const [unresolvedNames, setUnresolvedNames] = useState<string[]>([]);

  const refresh = useCallback(async () => {
    const [nextHealth, nextWorkspace] = await Promise.all([
      localApi.health(),
      localApi.workspace(),
    ]);
    setHealth(nextHealth);
    setWorkspace(nextWorkspace);
    if (nextWorkspace.database_ready) {
      const deckResponse = await localApi.listDecks();
      setDecks(deckResponse.decks);
    } else {
      setDecks([]);
      setSelectedDeck(null);
      setAnalyses([]);
      setSelectedAnalysis(null);
    }
  }, []);

  useEffect(() => {
    let cancelled = false;
    refresh()
      .then(() => {
        if (!cancelled) {
          setNotice("Local service connected. Choose the next safe action below.");
          setActionError(null);
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) setActionError(errorMessage(error));
      })
      .finally(() => {
        if (!cancelled) setBusy(null);
      });
    return () => {
      cancelled = true;
    };
  }, [refresh]);

  async function prepareCodie(refreshCards = false) {
    setBusy("catalog");
    try {
      const result = await localApi.prepareCatalog(refreshCards);
      setCatalogResult(result);
      await refresh();
      setNotice(
        result.from_cache
          ? `Codie is ready with ${result.imported_count} locally cached cards.`
          : `Codie is ready with ${result.imported_count} current cards.`,
      );
      setActionError(null);
    } catch (error) {
      setActionError(errorMessage(error));
    } finally {
      setBusy(null);
    }
  }

  async function importDeck() {
    setBusy("deck");
    try {
      const result = await localApi.importDeck(deckName, decklist);
      setUnresolvedNames([]);
      setDecklist("");
      await refresh();
      await selectDeck(result.user_deck_id);
      setNotice(
        result.source_type === "moxfield_public_link"
          ? `Loaded and remembered the public Moxfield deck with ${result.card_count} cards.`
          : `Remembered deck ${result.user_deck_id} with ${result.card_count} cards.`,
      );
      setActionError(null);
    } catch (error) {
      setUnresolvedNames(unresolvedFrom(error));
      setActionError(errorMessage(error));
    } finally {
      setBusy(null);
    }
  }

  async function selectDeck(deckId: number) {
    const [detail, analysisResponse] = await Promise.all([
      localApi.getDeck(deckId),
      localApi.listAnalyses(deckId),
    ]);
    setSelectedDeck(detail);
    setAnalyses(analysisResponse.analyses);
    setSelectedAnalysis(null);
  }

  async function runComparison() {
    if (!selectedDeck) {
      setActionError("Select a remembered deck before running a comparison.");
      return;
    }
    if (!evidenceFile) {
      setActionError("Select a local evidence-candidate JSON packet first.");
      return;
    }
    setBusy("comparison");
    try {
      const packet = await readJsonFile(evidenceFile);
      const candidates = evidenceCandidates(packet);
      const result = await localApi.compareDeck(selectedDeck.summary.user_deck_id, candidates);
      await refresh();
      await selectDeck(selectedDeck.summary.user_deck_id);
      const detail = await localApi.getAnalysis(result.saved_analysis_id);
      setSelectedAnalysis(detail);
      setNotice(`Saved evidence comparison ${result.saved_analysis_id}. Presence remains descriptive, not advice.`);
      setActionError(null);
    } catch (error) {
      setActionError(errorMessage(error));
    } finally {
      setBusy(null);
    }
  }

  async function selectAnalysis(analysisId: number) {
    setBusy("refresh");
    try {
      setSelectedAnalysis(await localApi.getAnalysis(analysisId));
      setNotice(`Loaded saved analysis ${analysisId} from local SQLite.`);
      setActionError(null);
    } catch (error) {
      setActionError(errorMessage(error));
    } finally {
      setBusy(null);
    }
  }

  async function download(format: "json" | "markdown") {
    if (!selectedAnalysis) return;
    setBusy("export");
    try {
      const exported = await localApi.exportAnalysis(
        selectedAnalysis.summary.saved_analysis_id,
        format,
      );
      const url = URL.createObjectURL(new Blob([exported.content], { type: exported.media_type }));
      const link = document.createElement("a");
      link.href = url;
      link.download = exported.filename;
      link.click();
      URL.revokeObjectURL(url);
      setNotice(`Downloaded ${exported.filename}.`);
      setActionError(null);
    } catch (error) {
      setActionError(errorMessage(error));
    } finally {
      setBusy(null);
    }
  }

  const disabled = busy !== null;
  const databaseReady = health?.database_ready ?? false;
  const catalogReady = health?.catalog_ready ?? false;

  return (
    <main className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Codie · local working iteration v0.1</p>
          <h1>Your evidence workspace, running only here.</h1>
          <p className="hero-copy">
            Prepare Codie once, remember a deck from a public Moxfield link or pasted list, and compare evidence.
          </p>
        </div>
        <div className={`service-badge ${health ? "is-ready" : "is-waiting"}`}>
          <span className="status-dot" aria-hidden="true" />
          {health ? "Local service ready" : "Connecting locally"}
        </div>
      </header>

      <section className="boundary-strip" aria-label="Privacy and evidence boundary">
        <span>127.0.0.1 only</span>
        <span>Local SQLite</span>
        <span>No telemetry</span>
        <span>Evidence is not advice</span>
      </section>

      {actionError && (
        <section className="alert error-alert" role="alert">
          <div>
            <strong>Action needs attention</strong>
            <p>{actionError}</p>
          </div>
          <button type="button" className="button button-quiet" onClick={() => setActionError(null)}>
            Dismiss
          </button>
        </section>
      )}

      <section className="notice-line" aria-live="polite">
        {busy ? "Working locally…" : notice}
      </section>

      <section className="readiness-grid" aria-label="Workspace readiness">
        <StatusCard label="Service" value={health?.service ?? "checking"} ready={Boolean(health)} />
        <StatusCard label="Workspace" value={databaseReady ? "ready" : "needs preparation"} ready={databaseReady} />
        <StatusCard label="Card data" value={catalogReady ? `${workspace?.counts.cards ?? 0} cards ready` : "needs preparation"} ready={catalogReady} />
        <StatusCard label="Saved work" value={`${workspace?.counts.decks ?? 0} decks · ${workspace?.counts.saved_analyses ?? 0} analyses`} ready={databaseReady} />
      </section>

      <section className="workspace-paths panel">
        <div>
          <p className="eyebrow">Contained workspace</p>
          <p className="mono">{workspace?.workspace_root ?? "Checking…"}</p>
        </div>
        <div>
          <p className="eyebrow">SQLite database</p>
          <p className="mono">{workspace?.database_path ?? "Checking…"}</p>
        </div>
      </section>

      <section className="workflow-grid">
        <article className="panel step-card">
          <StepHeading number="1" title="Prepare Codie" state={catalogReady ? "Ready" : "Required"} />
          <p>One click prepares the private workspace and keeps its local card data ready for name matching.</p>
          <button type="button" className="button" disabled={disabled} onClick={() => prepareCodie(catalogReady)}>
            {busy === "catalog" ? "Preparing Codie…" : catalogReady ? "Refresh card data" : "Prepare Codie"}
          </button>
          {catalogResult && <p className="result-line">{catalogResult.imported_count} cards ready locally.</p>}
        </article>

        <article className="panel step-card deck-import-card">
          <StepHeading number="2" title="Remember a Commander deck" state={decks.length ? `${decks.length} saved` : "Waiting"} />
          <label>
            <span>Deck name</span>
            <input value={deckName} disabled={disabled || !catalogReady} onChange={(event) => setDeckName(event.target.value)} placeholder="My local deck" />
          </label>
          <label>
            <span>Public Moxfield link or pasted decklist</span>
            <textarea value={decklist} disabled={disabled || !catalogReady} onChange={(event) => setDecklist(event.target.value)} placeholder={"https://www.moxfield.com/decks/…\n\nor paste:\nCommander\n1 Commander Name\n\nMainboard\n1 Card Name"} rows={10} />
          </label>
          <button type="button" className="button" disabled={disabled || !catalogReady || !decklist.trim()} onClick={importDeck}>
            {busy === "deck" ? "Resolving locally…" : "Import and remember deck"}
          </button>
          {unresolvedNames.length > 0 && (
            <div className="unresolved-panel">
              <strong>Unresolved card names</strong>
              <ul>{unresolvedNames.map((name) => <li key={name}>{name}</li>)}</ul>
              <p>No partial deck was saved.</p>
            </div>
          )}
        </article>

        <article className="panel step-card">
          <StepHeading number="3" title="Choose remembered work" state={selectedDeck ? `Deck ${selectedDeck.summary.user_deck_id}` : "Select one"} />
          {decks.length === 0 ? (
            <EmptyState>Import a resolved deck to create the first remembered workspace item.</EmptyState>
          ) : (
            <div className="selection-list">
              {decks.map((deck) => (
                <button
                  type="button"
                  className={`selection-row ${selectedDeck?.summary.user_deck_id === deck.user_deck_id ? "is-selected" : ""}`}
                  key={deck.user_deck_id}
                  disabled={disabled}
                  onClick={() => selectDeck(deck.user_deck_id).catch((error) => setActionError(errorMessage(error)))}
                >
                  <span><strong>{deck.deck_name || `Deck ${deck.user_deck_id}`}</strong><small>{deck.card_count} cards · {deck.saved_analysis_count} analyses</small></span>
                  <span className="row-action">Open</span>
                </button>
              ))}
            </div>
          )}
          {selectedDeck && (
            <details className="deck-detail">
              <summary>View resolved card rows</summary>
              <ul>{selectedDeck.cards.map((card, index) => <li key={`${card.oracle_id}-${index}`}>{card.quantity} {card.card_name} <span>{card.zone}</span></li>)}</ul>
            </details>
          )}
        </article>

        <article className="panel step-card">
          <StepHeading number="4" title="Run an evidence comparison" state={selectedAnalysis ? "Saved" : "Evidence only"} />
          <p>The selected packet remains typed and provenance-visible. No source is fetched automatically.</p>
          <label className="file-control">
            <span>Local evidence-candidate JSON</span>
            <input type="file" accept="application/json,.json" disabled={disabled || !selectedDeck} onChange={(event) => setEvidenceFile(event.target.files?.[0] ?? null)} />
          </label>
          <button type="button" className="button" disabled={disabled || !selectedDeck || !evidenceFile} onClick={runComparison}>
            {busy === "comparison" ? "Comparing and saving…" : "Run and save comparison"}
          </button>
        </article>

        <article className="panel step-card">
          <StepHeading number="5" title="Open a saved analysis" state={analyses.length ? `${analyses.length} saved` : "Waiting"} />
          {analyses.length === 0 ? (
            <EmptyState>Select a deck and run its first evidence comparison.</EmptyState>
          ) : (
            <div className="selection-list">
              {analyses.map((analysis) => (
                <button type="button" className={`selection-row ${selectedAnalysis?.summary.saved_analysis_id === analysis.saved_analysis_id ? "is-selected" : ""}`} key={analysis.saved_analysis_id} disabled={disabled} onClick={() => selectAnalysis(analysis.saved_analysis_id)}>
                  <span><strong>Analysis {analysis.saved_analysis_id}</strong><small>{formatTimestamp(analysis.generated_at)}</small></span>
                  <span className="row-action">Inspect</span>
                </button>
              ))}
            </div>
          )}
        </article>
      </section>

      <section className="panel analysis-panel" aria-label="Saved analysis detail">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Saved evidence</p>
            <h2>{selectedAnalysis ? `Analysis ${selectedAnalysis.summary.saved_analysis_id}` : "Analysis detail"}</h2>
          </div>
          {selectedAnalysis && (
            <div className="export-actions">
              <button type="button" className="button button-secondary" disabled={disabled} onClick={() => download("json")}>Download JSON</button>
              <button type="button" className="button button-secondary" disabled={disabled} onClick={() => download("markdown")}>Download Markdown</button>
            </div>
          )}
        </div>
        {!selectedAnalysis ? (
          <EmptyState>Open or create a saved comparison to inspect evidence rows and provenance.</EmptyState>
        ) : (
          <>
            <div className="analysis-summary">
              <span><strong>{selectedAnalysis.comparison.present_count}</strong> present</span>
              <span><strong>{selectedAnalysis.comparison.absent_count}</strong> absent</span>
              <span><strong>{selectedAnalysis.comparison.rows.length}</strong> evidence rows</span>
            </div>
            <p className="evidence-notice">{selectedAnalysis.notice}</p>
            <div className="evidence-table-wrap">
              <table>
                <thead><tr><th>Card</th><th>Evidence type</th><th>Presence</th><th>Score / sample</th><th>Provenance</th></tr></thead>
                <tbody>
                  {selectedAnalysis.comparison.rows.map((row) => (
                    <tr key={`${row.evidence_type}-${row.oracle_id}-${row.source_record_id ?? "local"}`}>
                      <td><strong>{row.card_name}</strong><small className="mono">{row.oracle_id}</small></td>
                      <td><span className="evidence-tag">{row.evidence_type}</span></td>
                      <td><span className={`presence ${row.presence_status}`}>{row.presence_status}</span>{row.quantity_in_deck > 0 && <small>{row.quantity_in_deck} in {row.zones.join(", ")}</small>}</td>
                      <td>{row.score ?? "—"}<small>sample {row.sample_size ?? "unknown"}</small></td>
                      <td>{row.source_url ? <a href={row.source_url} target="_blank" rel="noreferrer">Source record</a> : row.source_record_id || "Not supplied"}<small className="mono">{row.source_record_id}</small></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </section>

      <footer>
        <p>Local-first · private by default · zero-cost runtime · Stream Deck supplemental-only and absent</p>
        <p>Card data: identity only · Hareruya: tournament evidence only · Theory/Rules/Corrections unchanged</p>
      </footer>
    </main>
  );
}

function StatusCard({ label, value, ready }: { label: string; value: string; ready: boolean }) {
  return <article className={`status-card ${ready ? "is-ready" : ""}`}><span>{label}</span><strong>{value}</strong></article>;
}

function StepHeading({ number, title, state }: { number: string; title: string; state: string }) {
  return <div className="step-heading"><span className="step-number">{number}</span><div><h2>{title}</h2><small>{state}</small></div></div>;
}

function EmptyState({ children }: { children: string }) {
  return <p className="empty-state">{children}</p>;
}

async function readJsonFile(file: File): Promise<unknown> {
  try {
    return JSON.parse(await file.text()) as unknown;
  } catch {
    throw new Error(`${file.name} is not valid JSON.`);
  }
}

function evidenceCandidates(packet: unknown): unknown[] {
  if (Array.isArray(packet)) return packet;
  if (isRecord(packet) && Array.isArray(packet.candidates)) return packet.candidates;
  throw new Error("The evidence file must be an array or an object with a candidates array.");
}

function unresolvedFrom(error: unknown): string[] {
  if (!(error instanceof LocalApiError)) return [];
  const names = error.details?.unresolved_names;
  return Array.isArray(names) ? names.filter((name): name is string => typeof name === "string") : [];
}

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : "The local action failed safely.";
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function formatTimestamp(value: string): string {
  const parsed = new Date(value);
  return Number.isNaN(parsed.valueOf()) ? value : parsed.toLocaleString();
}
