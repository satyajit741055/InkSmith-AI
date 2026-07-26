const BASE = "/api";

function formatSeconds(total: number): string {
  const minutes = Math.floor(total / 60);
  const seconds = Math.max(0, Math.floor(total % 60));
  if (minutes > 0) return `${minutes}m ${seconds}s`;
  return `${seconds}s`;
}

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
    // Gracefully handle rate limiting
    if (res.status === 429) {
      const retryAfter = res.headers.get("retry-after");
      const secs = retryAfter ? Number(retryAfter) : NaN;
      const msg = Number.isFinite(secs)
        ? `You have reached the rate limit. Try again in ${formatSeconds(secs)}.`
        : "You have reached the rate limit. Please try again later.";
      throw new Error(msg);
    }

    // Fallback for other server errors
    const err = await res.json().catch(() => ({} as any));
    throw new Error(err.detail || `Server error: ${res.status}`);
  }

  return res.json();
}

export function getFileUrl(path: string): string {
  return `${BASE}${path}`;
}
