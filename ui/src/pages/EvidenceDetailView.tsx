import { SummaryCards } from "../components/SummaryCards";
import type { UserWorkflowPageModel } from "../types/userWorkflow";

interface EvidenceDetailViewProps {
  model: UserWorkflowPageModel;
}

export function EvidenceDetailView({ model }: EvidenceDetailViewProps) {
  return (
    <section className="panel detail-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Evidence detail</p>
          <h2>{model.title}</h2>
        </div>
        <span className="timestamp">{model.generated_at ?? "No generated timestamp"}</span>
      </div>

      <SummaryCards cards={model.summary_cards} />

      {model.rows.length === 0 ? (
        <p className="empty-state">{model.empty_state}</p>
      ) : (
        <div className="evidence-list">
          {model.rows.map((row) => (
            <article className="evidence-row" key={String(row.source_record_id)}>
              <div className="evidence-row-header">
                <h3>{row.card_name}</h3>
                <span>{row.presence_status}</span>
              </div>
              <p>{row.evidence_line}</p>
              <dl>
                <div>
                  <dt>Evidence type</dt>
                  <dd>{row.evidence_type}</dd>
                </div>
                <div>
                  <dt>Sample size</dt>
                  <dd>{row.sample_size ?? "Not provided"}</dd>
                </div>
                <div>
                  <dt>Source record</dt>
                  <dd className="mono">{row.source_record_id ?? "Not provided"}</dd>
                </div>
                <div>
                  <dt>Source URL</dt>
                  <dd>
                    {typeof row.source_url === "string" ? (
                      <a href={row.source_url}>{row.source_url}</a>
                    ) : (
                      "Not provided"
                    )}
                  </dd>
                </div>
              </dl>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
