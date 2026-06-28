import type { UserWorkflowSummaryCard } from "../types/userWorkflow";

interface SummaryCardsProps {
  cards: readonly UserWorkflowSummaryCard[];
}

export function SummaryCards({ cards }: SummaryCardsProps) {
  return (
    <div className="summary-grid">
      {cards.map((card) => (
        <div className="summary-card" key={`${card.label}:${card.value}`}>
          <span>{card.label}</span>
          <strong>{card.value}</strong>
          {card.detail ? <small>{card.detail}</small> : null}
        </div>
      ))}
    </div>
  );
}
