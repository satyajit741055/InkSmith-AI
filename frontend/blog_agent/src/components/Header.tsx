import { PenLine } from "lucide-react";

export default function Header() {
  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="mx-auto flex max-w-5xl items-center gap-3 px-6 py-4">
        <PenLine className="h-7 w-7 text-indigo-600" />
        <h1 className="text-xl font-bold tracking-tight text-gray-900">
          InkSmith AI
        </h1>
        <span className="rounded-full bg-indigo-50 px-2.5 py-0.5 text-xs font-medium text-indigo-600">
          Blog Generator
        </span>
      </div>
    </header>
  );
}
