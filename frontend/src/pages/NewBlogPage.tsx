import { useState } from 'react';
import { Layout } from '../components/Layout';
import { BlogForm } from '../components/BlogForm';
import { ProgressPanel } from '../components/ProgressPanel';
import { BlogStatusResponse } from '../api/blog';
import { motion, AnimatePresence } from 'framer-motion';
import { Download, RotateCcw, CheckCircle, AlertTriangle, Sparkles } from 'lucide-react';

export const NewBlogPage: React.FC = () => {
  const [threadId, setThreadId] = useState<string | null>(null);
  const [finalStatus, setFinalStatus] = useState<BlogStatusResponse | null>(null);

  const handleFormSubmit = (id: string) => {
    setThreadId(id);
    setFinalStatus(null);
  };

  const handleProgressComplete = (status: BlogStatusResponse) => {
    setFinalStatus(status);
  };

  const handleReset = () => {
    setThreadId(null);
    setFinalStatus(null);
  };

  const cardStyle: React.CSSProperties = {
    background: '#161625',
    border: '1px solid #2a2a40',
    borderRadius: 24,
    boxShadow: '0 4px 24px rgba(0,0,0,0.4)',
  };

  return (
    <Layout>
      <div className="max-w-6xl mx-auto px-6 lg:px-8 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-10 text-center"
        >
          <h1 className="text-4xl sm:text-5xl font-bold text-white tracking-tight">
            Create New Blog
          </h1>
          <p className="mt-3 text-lg" style={{ color: '#94a3b8' }}>
            Describe your topic and let AI do the heavy lifting.
          </p>
        </motion.div>

        <AnimatePresence mode="wait">
          {!threadId ? (
            /* ===== FORM ===== */
            <motion.div
              key="form"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
              className="max-w-3xl mx-auto"
            >
              <div style={cardStyle} className="p-8 sm:p-10 relative overflow-hidden">
                <div className="relative z-10">
                  <div className="mb-8">
                    <div className="flex items-center gap-3 mb-3">
                      <div
                        className="w-10 h-10 rounded-xl flex items-center justify-center"
                        style={{
                          background: 'linear-gradient(135deg, #7c3aed, #3b82f6)',
                          boxShadow: '0 8px 25px rgba(124,58,237,0.25)',
                        }}
                      >
                        <Sparkles className="w-5 h-5 text-white" />
                      </div>
                      <h2 className="text-2xl font-bold text-white">What's on your mind?</h2>
                    </div>
                    <p className="text-sm ml-[52px]" style={{ color: '#94a3b8' }}>
                      Describe your blog topic in detail. The more context you provide, the better
                      the result.
                    </p>
                  </div>
                  <BlogForm onSubmit={handleFormSubmit} />
                </div>
              </div>
            </motion.div>
          ) : (
            /* ===== PROGRESS ===== */
            <motion.div
              key="progress"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
              className="grid grid-cols-1 lg:grid-cols-5 gap-8"
            >
              {/* Sidebar */}
              <div className="lg:col-span-2">
                <ProgressPanel threadId={threadId} onComplete={handleProgressComplete} />
              </div>

              {/* Main */}
              <div className="lg:col-span-3">
                <AnimatePresence mode="wait">
                  {/* Writing in progress */}
                  {!finalStatus && (
                    <motion.div
                      key="writing"
                      initial={{ opacity: 0, scale: 0.98 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.98 }}
                      style={cardStyle}
                      className="p-12 sm:p-16 text-center"
                    >
                      <div
                        className="w-24 h-24 rounded-2xl flex items-center justify-center mx-auto mb-8 relative"
                        style={{
                          background: 'rgba(139,92,246,0.12)',
                          border: '1px solid rgba(139,92,246,0.2)',
                        }}
                      >
                        <div
                          className="absolute inset-0 rounded-2xl animate-spin-slow"
                          style={{
                            border: '2px solid transparent',
                            borderTopColor: 'rgba(139,92,246,0.4)',
                          }}
                        />
                        <Sparkles className="w-10 h-10" style={{ color: '#a78bfa' }} />
                      </div>

                      <h3 className="text-2xl font-bold text-white mb-3">
                        AI is writing your blog...
                      </h3>
                      <p style={{ color: '#94a3b8' }} className="max-w-md mx-auto">
                        Watch the progress panel to see each step being completed in real-time.
                      </p>

                      <div className="flex justify-center gap-2 mt-8">
                        {[0, 1, 2].map((i) => (
                          <motion.div
                            key={i}
                            className="w-2 h-2 rounded-full"
                            style={{ background: '#8b5cf6' }}
                            animate={{ opacity: [0.3, 1, 0.3] }}
                            transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.3 }}
                          />
                        ))}
                      </div>
                    </motion.div>
                  )}

                  {/* Success */}
                  {finalStatus && finalStatus.status === 'completed' && (
                    <motion.div
                      key="success"
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      style={cardStyle}
                      className="p-12 sm:p-16 text-center"
                    >
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: 'spring', stiffness: 200, delay: 0.1 }}
                        className="w-24 h-24 rounded-2xl flex items-center justify-center mx-auto mb-8"
                        style={{
                          background: 'rgba(16,185,129,0.12)',
                          border: '1px solid rgba(16,185,129,0.25)',
                        }}
                      >
                        <CheckCircle className="w-12 h-12" style={{ color: '#34d399' }} />
                      </motion.div>

                      <h3 className="text-3xl font-bold text-white mb-3">Your blog is ready!</h3>
                      <p className="mb-10 max-w-md mx-auto" style={{ color: '#94a3b8' }}>
                        Your AI-generated blog post has been created and exported successfully.
                      </p>

                      <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        {finalStatus.pdf_url && (
                          <a
                            href={`http://localhost:8001${finalStatus.pdf_url}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl font-semibold text-white transition-all duration-200 hover:-translate-y-0.5"
                            style={{
                              background: 'linear-gradient(135deg, #10b981, #0d9488)',
                              boxShadow: '0 8px 25px rgba(16,185,129,0.3)',
                            }}
                          >
                            <Download size={20} />
                            Download PDF
                          </a>
                        )}
                        <button
                          onClick={handleReset}
                          className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl font-semibold transition-all duration-200 hover:-translate-y-0.5"
                          style={{
                            background: '#1e1e35',
                            border: '1px solid #2a2a40',
                            color: '#cbd5e1',
                          }}
                        >
                          <RotateCcw size={18} />
                          Create Another
                        </button>
                      </div>
                    </motion.div>
                  )}

                  {/* Failure */}
                  {finalStatus && finalStatus.status === 'failed' && (
                    <motion.div
                      key="failed"
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      style={{
                        ...cardStyle,
                        borderColor: 'rgba(239,68,68,0.15)',
                      }}
                      className="p-12 sm:p-16 text-center"
                    >
                      <div
                        className="w-24 h-24 rounded-2xl flex items-center justify-center mx-auto mb-8"
                        style={{
                          background: 'rgba(239,68,68,0.12)',
                          border: '1px solid rgba(239,68,68,0.25)',
                        }}
                      >
                        <AlertTriangle className="w-12 h-12" style={{ color: '#f87171' }} />
                      </div>

                      <h3 className="text-2xl font-bold text-white mb-3">Generation Failed</h3>
                      <p className="mb-10 max-w-md mx-auto" style={{ color: 'rgba(248,113,113,0.8)' }}>
                        {finalStatus.error_message || 'An unexpected error occurred'}
                      </p>

                      <button
                        onClick={handleReset}
                        className="btn-glow inline-flex items-center justify-center gap-2 text-white px-8 py-4 rounded-xl font-semibold"
                      >
                        <RotateCcw size={18} />
                        Try Again
                      </button>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </Layout>
  );
};
