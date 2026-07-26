const BASE = "/api";

function formatSeconds(total: number): string {
  const minutes = Math.floor(total / 60);
  const seconds = Math.max(0, Math.floor(total % 60));
  if (minutes > 0) return `${minutes}m ${seconds}s`;
  return `${seconds}s`;
}

export interface JobResponse {
  job_id: string;
}

export interface JobStatusResponse {
  status: "pending" | "running" | "success" | "failed" | string;
  final: string | null;
  file_name: string | null;
  md_url: string | null;
  pdf_url: string | null;
  error: string | null;
}

export async function submitBlogJob(title: string): Promise<JobResponse> {
  const res = await fetch(`${BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });

  if (!res.ok) {
    if (res.status === 429) {
      const retryAfter = res.headers.get("retry-after");
      const secs = retryAfter ? Number(retryAfter) : NaN;
      const msg = Number.isFinite(secs)
        ? `You have reached the rate limit. Try again in ${formatSeconds(secs)}.`
        : "You have reached the rate limit. Please try again later.";
      throw new Error(msg);
    }

    const err = await res.json().catch(() => ({} as any));
    throw new Error(err.detail || `Server error: ${res.status}`);
  }

  return res.json();
}

export async function getJobStatus(jobId: string): Promise<JobStatusResponse> {
  const res = await fetch(`${BASE}/job_status/${jobId}`);

  if (!res.ok) {
    const err = await res.json().catch(() => ({} as any));
    throw new Error(err.detail || `Server error: ${res.status}`);
  }

  return res.json();
}

export function getFileUrl(path: string): string {
  return `${BASE}${path}`;
}
