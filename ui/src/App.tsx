import savedAnalysisDetail from "./fixtures/savedAnalysisDetail.json";
import savedAnalysisEmpty from "./fixtures/savedAnalysisEmpty.json";
import savedAnalysisList from "./fixtures/savedAnalysisList.json";
import { EvidenceDetailView } from "./pages/EvidenceDetailView";
import { SavedAnalysesView } from "./pages/SavedAnalysesView";
import type { UserWorkflowPageModel } from "./types/userWorkflow";

const listModel = savedAnalysisList as UserWorkflowPageModel;
const detailModel = savedAnalysisDetail as UserWorkflowPageModel;
const emptyModel = savedAnalysisEmpty as UserWorkflowPageModel;

export default function App() {
  return (
    <main className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">Local evidence dashboard</p>
          <h1>Codie User Workflow</h1>
        </div>
        <p className="status-pill">Fixture-backed preview</p>
      </header>

      <section className="layout-grid" aria-label="Saved analysis overview">
        <SavedAnalysesView model={listModel} />
        <SavedAnalysesView model={emptyModel} compact />
      </section>

      <EvidenceDetailView model={detailModel} />
    </main>
  );
}
