import { PenLine } from "lucide-react";
import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-3">
          <PenLine className="h-7 w-7 text-indigo-600" />
          <h1 className="text-xl font-bold tracking-tight text-gray-900">
            InkSmith AI
          </h1>
          <span className="rounded-full bg-indigo-50 px-2.5 py-0.5 text-xs font-medium text-indigo-600">
            Blog Generator
          </span>
        </div>
        <nav className="flex items-center gap-4 text-sm font-medium text-gray-600">
          <Link to="/login" className="hover:text-indigo-600">Login</Link>
          <Link to="/register" className="hover:text-indigo-600">Register</Link>
        </nav>
      </div>
    </header>
  );
}
