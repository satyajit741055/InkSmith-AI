import React, { useState } from 'react';
import { blogAPI } from '../api/blog';
import { motion } from 'framer-motion';
import { Sparkles, Loader2, Lightbulb } from 'lucide-react';

interface BlogFormProps {
  onSubmit: (threadId: string) => void;
  isLoading?: boolean;
}

const SUGGESTIONS = [
  'The Future of AI in Software Development',
  'Building Microservices with Python and FastAPI',
  'A Guide to Modern CSS Techniques in 2026',
  'Machine Learning for Beginners',
];

export const BlogForm: React.FC<BlogFormProps> = ({ onSubmit, isLoading = false }) => {
  const [prompt, setPrompt] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!prompt.trim()) {
      setError('Please enter a blog topic');
      return;
    }
    setSubmitting(true);
    try {
      const response = await blogAPI.createBlog({ prompt: prompt.trim() });
      onSubmit(response.data.thread_id);
    } catch (err) {
      setError('Failed to create blog. Please try again.');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-semibold text-white mb-3">
          Blog Topic
        </label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Example: Write a comprehensive blog about the future of AI in software development, covering breakthroughs, practical applications, and what developers should learn..."
          rows={6}
          disabled={isLoading || submitting}
          className="input-field w-full rounded-xl px-5 py-4 text-sm resize-none leading-relaxed disabled:opacity-50"
        />

        {/* Suggestions */}
        <div className="mt-4">
          <div className="flex items-center gap-2 text-xs font-medium mb-2.5" style={{ color: '#64748b' }}>
            <Lightbulb size={13} />
            Quick suggestions
          </div>
          <div className="flex flex-wrap gap-2">
            {SUGGESTIONS.map((s) => (
              <button
                key={s}
                type="button"
                onClick={() => setPrompt(s)}
                className="text-xs px-3 py-1.5 rounded-lg transition-all duration-200"
                style={{
                  background: 'rgba(255,255,255,0.03)',
                  border: '1px solid rgba(255,255,255,0.06)',
                  color: '#94a3b8',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.color = '#c4b5fd';
                  e.currentTarget.style.borderColor = 'rgba(139,92,246,0.3)';
                  e.currentTarget.style.background = 'rgba(139,92,246,0.08)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.color = '#94a3b8';
                  e.currentTarget.style.borderColor = 'rgba(255,255,255,0.06)';
                  e.currentTarget.style.background = 'rgba(255,255,255,0.03)';
                }}
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      </div>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl p-4"
          style={{
            background: 'rgba(239, 68, 68, 0.1)',
            border: '1px solid rgba(239, 68, 68, 0.2)',
          }}
        >
          <p className="text-sm font-medium" style={{ color: '#f87171' }}>{error}</p>
        </motion.div>
      )}

      <button
        type="submit"
        disabled={isLoading || submitting || !prompt.trim()}
        className="btn-glow w-full flex items-center justify-center gap-2 py-4 rounded-xl font-bold text-base text-white"
      >
        {submitting ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Creating Blog...
          </>
        ) : (
          <>
            <Sparkles className="w-5 h-5" />
            Generate Blog Post
          </>
        )}
      </button>
    </form>
  );
};
