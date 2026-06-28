import type { PageModelExport, UserWorkflowPageModel } from "../types/userWorkflow";

export interface PageModelLoadResult {
  exportPayload: PageModelExport;
  sourceUrl: string;
}

export async function loadPageModelExport(url: string): Promise<PageModelLoadResult> {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Page model export request failed: ${response.status}`);
  }

  const payload = (await response.json()) as unknown;
  const exportPayload = validatePageModelExport(payload);
  return { exportPayload, sourceUrl: url };
}

export function validatePageModelExport(payload: unknown): PageModelExport {
  if (!isRecord(payload)) {
    throw new Error("Page model export must be an object.");
  }

  if (payload.page_model_version !== "1") {
    throw new Error("Unsupported page model export version.");
  }

  if (typeof payload.exported_at !== "string" || payload.exported_at.length === 0) {
    throw new Error("Page model export is missing exported_at.");
  }

  if (!isRecord(payload.source)) {
    throw new Error("Page model export is missing source metadata.");
  }

  const pageModel = validatePageModel(payload.page_model);
  return {
    page_model_version: payload.page_model_version,
    exported_at: payload.exported_at,
    source: payload.source,
    page_model: pageModel,
  };
}

function validatePageModel(payload: unknown): UserWorkflowPageModel {
  if (!isRecord(payload)) {
    throw new Error("Page model must be an object.");
  }

  if (typeof payload.title !== "string" || payload.title.length === 0) {
    throw new Error("Page model is missing title.");
  }

  if (payload.generated_at !== null && typeof payload.generated_at !== "string") {
    throw new Error("Page model generated_at must be a string or null.");
  }

  if (!Array.isArray(payload.summary_cards)) {
    throw new Error("Page model summary_cards must be an array.");
  }

  if (!Array.isArray(payload.rows)) {
    throw new Error("Page model rows must be an array.");
  }

  if (payload.empty_state !== null && typeof payload.empty_state !== "string") {
    throw new Error("Page model empty_state must be a string or null.");
  }

  return {
    title: payload.title,
    generated_at: payload.generated_at,
    summary_cards: payload.summary_cards,
    rows: payload.rows,
    empty_state: payload.empty_state,
  };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
