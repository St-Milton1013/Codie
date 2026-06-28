import { SummaryCards } from "../components/SummaryCards";
import type { UserWorkflowPageModel } from "../types/userWorkflow";

interface SavedAnalysesViewProps {
  model: UserWorkflowPageModel;
  compact?: boolean;
}

export function SavedAnalysesView({ model, compact = false }: SavedAnalysesViewProps) {
  return (
    <section className={compact ? "panel panel-compact" : "panel"}>
      <div className="panel-heading">
        <div>
          <p className="eyebrow">{compact ? "Empty state" : "Saved analyses"}</p>
          <h2>{model.title}</h2>
        </div>
        <GeneratedAt value={model.generated_at} />
      </div>

      <SummaryCards cards={model.summary_cards} />

      {model.rows.length === 0 ? (
        <p className="empty-state">{model.empty_state}</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Type</th>
                <th>Generated</th>
                <th>Deck hash</th>
                <th>Report</th>
              </tr>
            </thead>
            <tbody>
              {model.rows.map((row) => (
                <tr key={String(row.saved_analysis_id)}>
                  <td>{row.saved_analysis_id}</td>
                  <td>{row.analysis_type}</td>
                  <td>{row.generated_at}</td>
                  <td className="mono">{row.deck_hash}</td>
                  <td>{row.report_path ?? "No report path"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function GeneratedAt({ value }: { value: string | null }) {
  return <span className="timestamp">{value ?? "No generated timestamp"}</span>;
}
