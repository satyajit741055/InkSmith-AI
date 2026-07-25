import { FileText, Download, Eye, ArrowLeft } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { useState } from "react";
import { getFileUrl, type QueryResponse } from "../api";

interface Props {
  result: QueryResponse;
  onReset: () => void;
}

export default function BlogResult({ result, onReset }: Props) {
  const [view, setView] = useState<"preview" | "raw">("preview");

  const mdUrl = result.md_url ? getFileUrl(result.md_url) : null;
  const pdfUrl = result.pdf_url ? getFileUrl(result.pdf_url) : null;

  return (
    <div className="mx-auto w-full max-w-4xl">
      {/* Top bar */}
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <button
          onClick={onReset}
          className="flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-600 shadow-sm transition hover:bg-gray-50"
        >
          <ArrowLeft className="h-4 w-4" />
          New Blog
        </button>

        <div className="flex items-center gap-2">
          {/* View toggle */}
          <div className="flex rounded-lg border border-gray-200 bg-white p-0.5 shadow-sm">
            <button
              onClick={() => setView("preview")}
              className={`rounded-md px-3 py-1.5 text-sm font-medium transition ${
                view === "preview"
                  ? "bg-indigo-600 text-white"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              <Eye className="mr-1 inline h-4 w-4" />
              Preview
            </button>
            <button
              onClick={() => setView("raw")}
              className={`rounded-md px-3 py-1.5 text-sm font-medium transition ${
                view === "raw"
                  ? "bg-indigo-600 text-white"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              <FileText className="mr-1 inline h-4 w-4" />
              Markdown
            </button>
          </div>

          {/* Download buttons */}
          {mdUrl && (
            <a
              href={mdUrl}
              download
              className="flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-600 shadow-sm transition hover:bg-gray-50"
            >
              <Download className="h-4 w-4" />
              .md
            </a>
          )}
          {pdfUrl && (
            <a
              href={pdfUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-indigo-700"
            >
              <Download className="h-4 w-4" />
              PDF
            </a>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="rounded-xl border border-gray-200 bg-white shadow-sm">
        {view === "preview" ? (
          <div className="prose prose-indigo max-w-none p-8">
            <ReactMarkdown>{result.final}</ReactMarkdown>
          </div>
        ) : (
          <pre className="max-h-[70vh] overflow-auto p-6 text-sm text-gray-700 bg-gray-50 rounded-xl">
            <code>{result.final}</code>
          </pre>
        )}
      </div>
    </div>
  );
}
