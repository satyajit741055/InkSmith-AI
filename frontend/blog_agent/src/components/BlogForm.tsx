import { useState } from "react";
import { Sparkles, Loader2 } from "lucide-react";

interface Props {
  onSubmit: (title: string) => void;
  loading: boolean;
}

const SUGGESTIONS = [
  "How React Works Under the Hood",
  "Building REST APIs with FastAPI",
  "Understanding Transformer Architecture",
  "Docker for Beginners",
];

export default function BlogForm({ onSubmit, loading }: Props) {
  const [title, setTitle] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    onSubmit(title.trim());
  };

  return (
    <div className="mx-auto w-full max-w-2xl">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Generate a Blog Post
        </h2>
        <p className="text-gray-500">
          Enter a topic and let AI write a comprehensive, well-structured blog
          with images.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter blog topic..."
            disabled={loading}
            className="w-full rounded-xl border border-gray-300 bg-white px-5 py-4 text-lg text-gray-900 placeholder-gray-400 shadow-sm transition focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200 disabled:opacity-60"
          />
        </div>

        <button
          type="submit"
          disabled={loading || !title.trim()}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-indigo-600 px-6 py-4 text-lg font-semibold text-white shadow-md transition hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              Generating... This may take a few minutes
            </>
          ) : (
            <>
              <Sparkles className="h-5 w-5" />
              Generate Blog
            </>
          )}
        </button>
      </form>

      {!loading && (
        <div className="mt-6">
          <p className="mb-3 text-center text-sm text-gray-400">
            Try a suggestion
          </p>
          <div className="flex flex-wrap justify-center gap-2">
            {SUGGESTIONS.map((s) => (
              <button
                key={s}
                onClick={() => setTitle(s)}
                className="rounded-lg border border-gray-200 bg-gray-50 px-3 py-1.5 text-sm text-gray-600 transition hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-600"
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
