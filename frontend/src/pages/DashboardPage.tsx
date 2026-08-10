import { Link } from 'react-router-dom';
import { Layout } from '../components/Layout';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { blogAPI, BlogStatusResponse } from '../api/blog';
import {
  FileText,
  CheckCircle,
  Download,
  PlusCircle,
  Clock,
  Sparkles,
  ArrowRight,
  Eye,
  Loader2,
  X,
  AlertTriangle,
} from 'lucide-react';

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.08, duration: 0.5, ease: 'easeOut' },
  }),
};

export const DashboardPage: React.FC = () => {
  const [blogs, setBlogs] = useState<BlogStatusResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [pdfError, setPdfError] = useState<string | null>(null);

  const openPdf = async (threadId: string) => {
    setPdfLoading(true);
    setPdfError(null);
    try {
      const response = await blogAPI.downloadPdf(threadId);
      const url = URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
      setPdfUrl(url);
    } catch (err: any) {
      const status = err?.response?.status;
      const message = status === 404
        ? 'PDF not found. The file may have been deleted or generation failed.'
        : 'Failed to load PDF. Please try again.';
      setPdfError(message);
      console.error('Failed to load PDF:', err);
    } finally {
      setPdfLoading(false);
    }
  };

  const closePdf = () => {
    if (pdfUrl) URL.revokeObjectURL(pdfUrl);
    setPdfUrl(null);
    setPdfError(null);
  };

  useEffect(() => {
    const fetchBlogs = async () => {
      try {
        const response = await blogAPI.listBlogs();
        setBlogs(response.data);
      } catch (error) {
        console.error('Failed to fetch blogs:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchBlogs();
  }, []);

  const totalBlogs = blogs.length;
  const completedBlogs = blogs.filter((b) => b.status === 'completed').length;

  const stats = [
    {
      label: 'Total Blogs',
      value: String(totalBlogs),
      icon: <FileText size={20} className="text-white" />,
      bg: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
      shadow: '0 8px 25px rgba(139, 92, 246, 0.25)',
    },
    {
      label: 'Completed',
      value: String(completedBlogs),
      icon: <CheckCircle size={20} className="text-white" />,
      bg: 'linear-gradient(135deg, #10b981, #0d9488)',
      shadow: '0 8px 25px rgba(16, 185, 129, 0.25)',
    },
    {
      label: 'Downloads',
      value: '--',
      icon: <Download size={20} className="text-white" />,
      bg: 'linear-gradient(135deg, #3b82f6, #0891b2)',
      shadow: '0 8px 25px rgba(59, 130, 246, 0.25)',
    },
    {
      label: 'Avg. Time',
      value: '--',
      icon: <Clock size={20} className="text-white" />,
      bg: 'linear-gradient(135deg, #f59e0b, #ea580c)',
      shadow: '0 8px 25px rgba(245, 158, 11, 0.25)',
    },
  ];

  return (
    <Layout>
      <div className="max-w-6xl mx-auto px-6 lg:px-8 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-6 mb-10"
        >
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div
                className="w-2 h-2 rounded-full animate-pulse"
                style={{ background: '#34d399' }}
              />
              <span className="text-sm font-medium" style={{ color: '#34d399' }}>
                Online
              </span>
            </div>
            <h1 className="text-4xl sm:text-5xl font-bold text-white tracking-tight">
              Dashboard
            </h1>
            <p className="mt-2 text-lg" style={{ color: '#94a3b8' }}>
              Welcome back! Ready to create something great?
            </p>
          </div>
          <Link
            to="/new"
            className="btn-glow group inline-flex items-center gap-2 text-white px-7 py-3.5 rounded-xl font-semibold shrink-0"
          >
            <PlusCircle size={20} />
            New Blog
            <ArrowRight
              size={16}
              className="opacity-0 -ml-4 group-hover:opacity-100 group-hover:ml-0 transition-all duration-200"
            />
          </Link>
        </motion.div>

        {/* Stats */}
        <motion.div
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-10"
          initial="hidden"
          animate="visible"
        >
          {stats.map((stat, i) => (
            <motion.div
              key={stat.label}
              variants={fadeUp}
              custom={i}
              className="card-glass p-6 group transition-transform duration-300 hover:-translate-y-1"
            >
              <div className="flex items-center justify-between mb-4">
                <div
                  className="w-11 h-11 rounded-xl flex items-center justify-center transition-transform duration-300 group-hover:scale-110"
                  style={{ background: stat.bg, boxShadow: stat.shadow }}
                >
                  {stat.icon}
                </div>
              </div>
              <p className="text-3xl font-bold text-white">{stat.value}</p>
              <p className="text-sm font-medium mt-1" style={{ color: '#64748b' }}>
                {stat.label}
              </p>
            </motion.div>
          ))}
        </motion.div>

        {/* Recent Blogs header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-white">Recent Blogs</h2>
          </div>

          {loading ? (
            <div className="card-glass p-16 text-center" style={{ borderRadius: 24 }}>
              <Loader2 className="w-8 h-8 animate-spin mx-auto" style={{ color: '#a78bfa' }} />
              <p className="mt-4" style={{ color: '#94a3b8' }}>Loading blogs...</p>
            </div>
          ) : blogs.length === 0 ? (
            <div
              className="card-glass p-16 text-center relative overflow-hidden"
              style={{ borderRadius: 24 }}
            >
              <div
                className="absolute inset-0 pointer-events-none"
                style={{
                  background: 'linear-gradient(135deg, rgba(124,58,237,0.04), transparent, rgba(59,130,246,0.04))',
                }}
              />

              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.5, type: 'spring', stiffness: 150 }}
                className="relative z-10"
              >
                <div
                  className="w-24 h-24 rounded-2xl flex items-center justify-center mx-auto mb-8"
                  style={{
                    background: 'linear-gradient(135deg, rgba(124,58,237,0.15), rgba(59,130,246,0.15))',
                    border: '1px solid rgba(139, 92, 246, 0.1)',
                  }}
                >
                  <Sparkles className="w-12 h-12" style={{ color: '#a78bfa' }} />
                </div>

                <h3 className="text-2xl font-bold text-white mb-3">No blogs yet</h3>
                <p className="mb-10 max-w-md mx-auto leading-relaxed" style={{ color: '#94a3b8' }}>
                  Create your first AI-powered blog post. Describe your topic and let InkSmith
                  handle the rest. It takes less than 2 minutes.
                </p>

                <Link
                  to="/new"
                  className="btn-glow group inline-flex items-center gap-3 text-white px-8 py-4 rounded-xl font-semibold"
                >
                  <PlusCircle size={20} />
                  Create Your First Blog
                  <ArrowRight
                    size={18}
                    className="group-hover:translate-x-1 transition-transform"
                  />
                </Link>
              </motion.div>
            </div>
          ) : (
            <div className="grid gap-4">
              {blogs.map((blog, i) => (
                <motion.div
                  key={blog.thread_id}
                  variants={fadeUp}
                  initial="hidden"
                  animate="visible"
                  custom={i}
                  className="card-glass p-5 flex items-center justify-between group hover:-translate-y-0.5 transition-transform"
                  style={{ borderRadius: 16 }}
                >
                  <div className="flex items-center gap-4">
                    <div
                      className="w-10 h-10 rounded-lg flex items-center justify-center"
                      style={{
                        background: 'linear-gradient(135deg, rgba(124,58,237,0.15), rgba(59,130,246,0.15))',
                      }}
                    >
                      <FileText size={18} style={{ color: '#a78bfa' }} />
                    </div>
                    <div>
                      <p className="text-white font-medium truncate max-w-xs">
                        {blog.file_name || blog.thread_id}
                      </p>
                      <p className="text-sm" style={{ color: '#64748b' }}>
                        {blog.current_step || blog.status}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span
                      className="px-3 py-1 rounded-full text-xs font-medium"
                      style={{
                        background: blog.status === 'completed' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                        color: blog.status === 'completed' ? '#34d399' : '#fbbf24',
                      }}
                    >
                      {blog.status}
                    </span>
                    {blog.status === 'completed' && (
                      <button
                        onClick={() => openPdf(blog.thread_id)}
                        className="p-2 rounded-lg hover:bg-white/5 transition-colors"
                        title="View PDF"
                      >
                        <Eye size={18} style={{ color: '#94a3b8' }} />
                      </button>
                    )}
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </div>

      {/* PDF Modal */}
      {(pdfUrl || pdfLoading || pdfError) && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          style={{ background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(6px)' }}
          onClick={closePdf}
        >
          <div
            className="relative w-full max-w-5xl rounded-2xl overflow-hidden"
            style={{ height: '88vh', background: '#0f172a', border: '1px solid rgba(139,92,246,0.2)' }}
            onClick={(e) => e.stopPropagation()}
          >
            <div
              className="flex items-center justify-between px-5 py-3"
              style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}
            >
              <p className="text-white font-semibold text-sm">Blog PDF</p>
              <button
                onClick={closePdf}
                className="p-1.5 rounded-lg hover:bg-white/10 transition-colors"
              >
                <X size={18} style={{ color: '#94a3b8' }} />
              </button>
            </div>
            {pdfLoading ? (
              <div className="flex items-center justify-center h-full">
                <Loader2 className="w-8 h-8 animate-spin" style={{ color: '#a78bfa' }} />
              </div>
            ) : pdfError ? (
              <div className="flex flex-col items-center justify-center h-full px-6 text-center">
                <div className="w-16 h-16 rounded-2xl flex items-center justify-center mb-4" style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)' }}>
                  <AlertTriangle size={28} style={{ color: '#f87171' }} />
                </div>
                <p className="text-white font-semibold mb-2">Unable to load PDF</p>
                <p style={{ color: '#94a3b8' }}>{pdfError}</p>
              </div>
            ) : (
              <iframe
                src={pdfUrl!}
                className="w-full"
                style={{ height: 'calc(88vh - 52px)', border: 'none' }}
                title="Blog PDF"
              />
            )}
          </div>
        </div>
      )}
    </Layout>
  );
};
