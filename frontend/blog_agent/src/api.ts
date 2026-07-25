const BASE = "/api";

export interface QueryResponse {
  final: string;
  fileName: string;
  mdFilePath: string;
  pdfFilePath: string;
  md_url: string | null;
  pdf_url: string | null;
}

export async function generateBlog(title: string): Promise<QueryResponse> {
  const res = await fetch(`${BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Server error: ${res.status}`);
  }

  return res.json();
}

export function getFileUrl(path: string): string {
  return `${BASE}${path}`;
}
