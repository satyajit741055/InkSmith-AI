import { useEffect, useRef, useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import AuthPage from "./components/AuthPage";
import Header from "./components/Header";
import BlogForm from "./components/BlogForm";
import BlogResult from "./components/BlogResult";
import {
  submitBlogJob,
  getJobStatus,
  type JobStatusResponse,
} from "./api";
import { AlertCircle } from "lucide-react";

const POLL_INTERVAL_MS = 2000;

function Home() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const [result, setResult] = useState<JobStatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const clearPoll = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  const handleGenerate = async (title: string) => {
    clearPoll();
    setLoading(true);
    setStatus("Submitting...");
    setError(null);
    setResult(null);

    try {
      const { job_id } = await submitBlogJob(title);
      setStatus("Job queued. Starting soon...");

      intervalRef.current = setInterval(async () => {
        try {
          const data = await getJobStatus(job_id);

          if (data.status === "failed") {
            clearPoll();
            setLoading(false);
            setStatus(null);
            setError(data.error || "Blog generation failed");
            return;
          }

          if (data.status === "success") {
            clearPoll();
            setLoading(false);
            setStatus(null);
            setResult(data);
            return;
          }

          setStatus(
            data.status === "pending"
              ? "Waiting in queue..."
              : "Generating your blog..."
          );
        } catch (err) {
          clearPoll();
          setLoading(false);
          setStatus(null);
          setError(err instanceof Error ? err.message : "Polling failed");
        }
      }, POLL_INTERVAL_MS);
    } catch (err) {
      setLoading(false);
      setStatus(null);
      setError(err instanceof Error ? err.message : "Failed to start job");
    }
  };

  const handleReset = () => {
    clearPoll();
    setResult(null);
    setError(null);
    setStatus(null);
    setLoading(false);
  };

  useEffect(() => {
    return () => clearPoll();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="px-6 py-12">
        {error && (
          <div className="mx-auto mb-6 flex max-w-2xl items-center gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
            <AlertCircle className="h-5 w-5 shrink-0" />
            <p className="text-sm">{error}</p>
          </div>
        )}

        {status && !error && (
          <div className="mx-auto mb-6 flex max-w-2xl items-center justify-center gap-3 rounded-xl border border-indigo-200 bg-indigo-50 p-4 text-indigo-700">
            <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-indigo-400 border-t-transparent" />
            <p className="text-sm font-medium">{status}</p>
          </div>
        )}

        {result?.status === "success" ? (
          <BlogResult result={result} onReset={handleReset} />
        ) : (
          <BlogForm onSubmit={handleGenerate} loading={loading} />
        )}
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<AuthPage mode="login" />} />
        <Route path="/register" element={<AuthPage mode="register" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
