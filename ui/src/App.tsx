import { useEffect, useMemo, useState } from "react";
import savedAnalysisDetail from "./fixtures/savedAnalysisDetail.json";
import savedAnalysisEmpty from "./fixtures/savedAnalysisEmpty.json";
import savedAnalysisList from "./fixtures/savedAnalysisList.json";
import { loadPageModelExport } from "./data/pageModelLoader";
import { EvidenceDetailView } from "./pages/EvidenceDetailView";
import { SavedAnalysesView } from "./pages/SavedAnalysesView";
import type { PageModelExport, UserWorkflowPageModel } from "./types/userWorkflow";

const listModel = savedAnalysisList as UserWorkflowPageModel;
const detailModel = savedAnalysisDetail as UserWorkflowPageModel;
const emptyModel = savedAnalysisEmpty as UserWorkflowPageModel;
const defaultListExportUrl = "/page-models/saved-analysis-list.json";
const defaultDetailExportUrl = "/page-models/saved-analysis-detail.json";

interface LoadedModelState {
  payload: PageModelExport;
  sourceUrl: string;
  status: "loading" | "loaded" | "fallback";
  message: string;
}

export default function App() {
  const listUrl = useMemo(() => pageModelUrl("listModel", defaultListExportUrl), []);
  const detailUrl = useMemo(() => pageModelUrl("detailModel", defaultDetailExportUrl), []);
  const [listState, setListState] = useState<LoadedModelState>(() =>
    fallbackState(listModel, listUrl, "Loading generated saved-analysis list export."),
  );
  const [detailState, setDetailState] = useState<LoadedModelState>(() =>
    fallbackState(detailModel, detailUrl, "Loading generated saved-analysis detail export."),
  );

  useEffect(() => {
    let cancelled = false;
    loadPageModelExport(listUrl)
      .then((result) => {
        if (!cancelled) {
          setListState({
            payload: result.exportPayload,
            sourceUrl: result.sourceUrl,
            status: "loaded",
            message: "Loaded generated saved-analysis list export.",
          });
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setListState(
            fallbackState(
              listModel,
              listUrl,
              `Using fallback saved-analysis list fixture: ${errorMessage(error)}`,
            ),
          );
        }
      });

    return () => {
      cancelled = true;
    };
  }, [listUrl]);

  useEffect(() => {
    let cancelled = false;
    loadPageModelExport(detailUrl)
      .then((result) => {
        if (!cancelled) {
          setDetailState({
            payload: result.exportPayload,
            sourceUrl: result.sourceUrl,
            status: "loaded",
            message: "Loaded generated saved-analysis detail export.",
          });
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setDetailState(
            fallbackState(
              detailModel,
              detailUrl,
              `Using fallback saved-analysis detail fixture: ${errorMessage(error)}`,
            ),
          );
        }
      });

    return () => {
      cancelled = true;
    };
  }, [detailUrl]);

  return (
    <main className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">Local evidence dashboard</p>
          <h1>Codie User Workflow</h1>
        </div>
        <p className="status-pill">Static page-model preview</p>
      </header>

      <section className="data-source-panel" aria-label="Loaded page model sources">
        <DataSourceStatus label="Saved list" state={listState} />
        <DataSourceStatus label="Evidence detail" state={detailState} />
      </section>

      <section className="layout-grid" aria-label="Saved analysis overview">
        <SavedAnalysesView model={listState.payload.page_model} />
        <SavedAnalysesView model={emptyModel} compact />
      </section>

      <EvidenceDetailView model={detailState.payload.page_model} />
    </main>
  );
}

function pageModelUrl(queryKey: string, fallbackUrl: string): string {
  const params = new URLSearchParams(window.location.search);
  const value = params.get(queryKey);
  return value && value.startsWith("/") ? value : fallbackUrl;
}

function fallbackState(
  pageModel: UserWorkflowPageModel,
  sourceUrl: string,
  message: string,
): LoadedModelState {
  return {
    payload: {
      page_model_version: "1",
      exported_at: "fixture",
      source: { export_type: "fixture_fallback" },
      page_model: pageModel,
    },
    sourceUrl,
    status: message.startsWith("Loading") ? "loading" : "fallback",
    message,
  };
}

function DataSourceStatus({ label, state }: { label: string; state: LoadedModelState }) {
  return (
    <article className="data-source-card">
      <div>
        <p className="eyebrow">{label}</p>
        <h2>{state.status === "loaded" ? "Generated export" : "Fixture fallback"}</h2>
      </div>
      <dl>
        <div>
          <dt>Source path</dt>
          <dd className="mono">{state.sourceUrl}</dd>
        </div>
        <div>
          <dt>Exported</dt>
          <dd>{state.payload.exported_at}</dd>
        </div>
        <div>
          <dt>Status</dt>
          <dd>{state.message}</dd>
        </div>
      </dl>
    </article>
  );
}

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : "unknown loader error";
}
