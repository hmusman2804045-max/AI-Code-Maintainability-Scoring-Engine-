export interface ScoreResult {
  error?: boolean;
  message?: string;
  risk_score: number;
  risk_level: "Low" | "Medium" | "High";
  confidence: number;
  top_risk_factors: string[];
}

export interface RefactorResult {
  error?: boolean;
  message?: string;
  initial_code: string;
  final_code: string;
  final_score: number | null;
  iterations_run: number;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

async function post<T>(path: string, body: unknown): Promise<T> {
  const fullPath = `${API_BASE_URL}${path}`;
  const res = await fetch(fullPath, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`Request to ${fullPath} failed with status ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export function scoreCode(code: string): Promise<ScoreResult> {
  return post<ScoreResult>("/api/score", { code });
}

export function refactorCode(
  code: string,
  targetScore = 20.0,
  maxIterations = 3
): Promise<RefactorResult> {
  return post<RefactorResult>("/api/refactor", {
    code,
    target_score: targetScore,
    max_iterations: maxIterations,
  });
}
