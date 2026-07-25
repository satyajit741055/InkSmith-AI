import { useState } from "react";
import "./App.css";
import Header from "./components/Header";
import BlogForm from "./components/BlogForm";
import BlogResult from "./components/BlogResult";
import { generateBlog, type QueryResponse } from "./api";
import { AlertCircle } from "lucide-react";

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async (title: string) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await generateBlog(title);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

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

        {result ? (
          <BlogResult result={result} onReset={handleReset} />
        ) : (
          <BlogForm onSubmit={handleGenerate} loading={loading} />
        )}
      </main>
    </div>
  );
}

export default App;
