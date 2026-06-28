export interface UserWorkflowSummaryCard {
  label: string;
  value: string;
  detail: string | null;
}

export type UserWorkflowTableCell =
  | string
  | number
  | boolean
  | null
  | readonly string[];

export interface UserWorkflowTableRow {
  [key: string]: UserWorkflowTableCell;
}

export interface UserWorkflowPageModel {
  title: string;
  generated_at: string | null;
  summary_cards: readonly UserWorkflowSummaryCard[];
  rows: readonly UserWorkflowTableRow[];
  empty_state: string | null;
}

export interface PageModelExport {
  page_model_version: "1";
  exported_at: string;
  source: Record<string, unknown>;
  page_model: UserWorkflowPageModel;
}
