export type Topic = "Electricity" | "Renewables" | "Energy system";
export type Kind = "Data portal" | "Overview" | "Statistics";
export type EnergySource = {
  id: number;
  title: string;
  publisher: string;
  description: string;
  url: string;
  topic: Topic;
  kind: Kind;
  saved: boolean;
};
export type Overview = {
  sources: number;
  saved: number;
  publishers: number;
  database: string;
};
export type NewSource = Omit<EnergySource, "id" | "saved">;

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, init);
  if (!response.ok) {
    if (response.status >= 500) throw new Error("The API is unavailable. Check that the FastAPI server is running on port 8010, then retry.");
    const body = await response.json().catch(() => ({}));
    throw new Error(typeof body.detail === "string" ? body.detail : "Please check your source details and try again.");
  }
  return response.json() as Promise<T>;
}

export async function loadLibrary(q: string, topic: string, saved: boolean, signal: AbortSignal) {
  const params = new URLSearchParams({ q, saved_only: String(saved) });
  if (topic) params.set("topic", topic);
  const [sources, overview] = await Promise.all([
    request<EnergySource[]>("/api/sources?" + params, { signal }),
    request<Overview>("/api/overview", { signal }),
  ]);
  return { sources, overview };
}

export function saveSource(id: number, saved: boolean) {
  return request<EnergySource>("/api/sources/" + id + "/bookmark", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ saved }),
  });
}

export function createSource(data: NewSource) {
  return request<EnergySource>("/api/sources", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}
