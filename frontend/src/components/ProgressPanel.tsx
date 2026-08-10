import React, { useEffect, useState } from 'react';
import { blogAPI, BlogStatusResponse } from '../api/blog';
import { motion, AnimatePresence } from 'framer-motion';
import {
  CheckCircle2,
  Circle,
  Loader2,
  AlertCircle,
  Sparkles,
} from 'lucide-react';

interface ProgressPanelProps {
  threadId: string;
  onComplete: (status: BlogStatusResponse) => void;
}

const STAGES = [
  { key: 'routing', label: 'Routing', desc: 'Analyzing prompt & deciding approach' },
  { key: 'researching', label: 'Researching', desc: 'Searching the web for sources' },
  { key: 'planning', label: 'Planning', desc: 'Creating blog outline & structure' },
  { key: 'writing', label: 'Writing', desc: 'Generating content sections' },
  { key: 'merging', label: 'Merging', desc: 'Combining all sections together' },
  { key: 'image_planning', label: 'Image Planning', desc: 'Deciding image placements' },
  { key: 'generating_images', label: 'Generating Images', desc: 'Creating AI images for the blog' },
  { key: 'completed', label: 'Completed', desc: 'Blog is ready for download' },
];

export const ProgressPanel: React.FC<ProgressPanelProps> = ({ threadId, onComplete }) => {
  const [status, setStatus] = useState<BlogStatusResponse | null>(null);
  const [error, setError] = useState('');
  const [isPolling, setIsPolling] = useState(true);

  useEffect(() => {
    if (!isPolling) return;
    const pollStatus = async () => {
      try {
        const response = await blogAPI.getBlogStatus(threadId);
        setStatus(response.data);
        setError('');
        if (response.data.status === 'completed' || response.data.status === 'failed') {
          setIsPolling(false);
          onComplete(response.data);
        }
      } catch (err) {
        setError('Failed to fetch status');
        console.error(err);
      }
    };
    pollStatus();
    const interval = setInterval(pollStatus, 2000);
    return () => clearInterval(interval);
  }, [threadId, isPolling, onComplete]);

  const stageKeys = STAGES.map((s) => s.key);
  const currentStageIndex = status ? stageKeys.indexOf(status.status as string) : -1;
  const progressPercent = status
    ? status.status === 'completed'
      ? 100
      : status.status === 'failed'
      ? 0
      : Math.max(0, ((currentStageIndex + 0.5) / STAGES.length) * 100)
    : 0;

  if (!status) {
    return (
      <div
        style={{
          background: '#161625',
          border: '1px solid #2a2a40',
          borderRadius: 20,
          padding: 32,
          textAlign: 'center',
          boxShadow: '0 4px 24px rgba(0,0,0,0.4)',
        }}
      >
        <div
          style={{
            width: 48, height: 48, borderRadius: 12,
            background: 'rgba(139,92,246,0.15)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto 16px',
          }}
        >
          <Loader2 className="w-6 h-6 animate-spin" style={{ color: '#a78bfa' }} />
        </div>
        <p style={{ color: '#94a3b8', fontSize: 14, fontWeight: 500 }}>
          Initializing generation...
        </p>
      </div>
    );
  }

  return (
    <div
      style={{
        background: '#161625',
        border: '1px solid #2a2a40',
        borderRadius: 20,
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        boxShadow: '0 4px 24px rgba(0,0,0,0.4)',
      }}
    >
      {/* Top accent */}
      <div
        style={{
          height: 3,
          background: 'linear-gradient(90deg, #7c3aed, #3b82f6, #06b6d4)',
        }}
      />

      <div
        style={{
          padding: 18,
          display: 'flex',
          flexDirection: 'column',
          flex: 1,
          overflow: 'hidden',
        }}
      >
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
          <div
            style={{
              width: 30, height: 30, borderRadius: 8,
              background: 'linear-gradient(135deg, #7c3aed, #3b82f6)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: '0 4px 15px rgba(124,58,237,0.3)',
              flexShrink: 0,
            }}
          >
            <Sparkles style={{ width: 14, height: 14, color: 'white' }} />
          </div>
          <div>
            <h3 style={{ fontSize: 15, fontWeight: 700, color: 'white', margin: 0 }}>Progress</h3>
            <p style={{ fontSize: 11, color: '#64748b', margin: 0 }}>Real-time tracking</p>
          </div>
        </div>

        {/* Progress bar */}
        <div style={{ marginBottom: 16 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
            <span style={{ fontSize: 12, fontWeight: 500, color: '#94a3b8' }}>Overall Progress</span>
            <span style={{ fontSize: 12, fontWeight: 700, color: '#a78bfa' }}>{Math.round(progressPercent)}%</span>
          </div>
          <div
            style={{
              height: 6, borderRadius: 3,
              background: '#1e1e35',
              overflow: 'hidden',
            }}
          >
            <motion.div
              style={{
                height: '100%', borderRadius: 4,
                background: 'linear-gradient(90deg, #7c3aed, #3b82f6)',
              }}
              initial={{ width: 0 }}
              animate={{ width: `${progressPercent}%` }}
              transition={{ duration: 0.8, ease: 'easeInOut' }}
            />
          </div>
        </div>

        {/* Error */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              style={{ marginBottom: 20, overflow: 'hidden' }}
            >
              <div
                style={{
                  borderRadius: 12, padding: 12,
                  background: 'rgba(239,68,68,0.1)',
                  border: '1px solid rgba(239,68,68,0.2)',
                }}
              >
                <p style={{ fontSize: 12, fontWeight: 500, color: '#f87171', display: 'flex', alignItems: 'center', gap: 8, margin: 0 }}>
                  <AlertCircle size={14} />
                  {error}
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Failed */}
        {status.status === 'failed' && (
          <div
            style={{
              borderRadius: 12, padding: 16, marginBottom: 24,
              background: 'rgba(239,68,68,0.1)',
              border: '1px solid rgba(239,68,68,0.2)',
            }}
          >
            <p style={{ fontSize: 14, fontWeight: 600, color: '#f87171', display: 'flex', alignItems: 'center', gap: 8, margin: 0 }}>
              <AlertCircle size={16} />
              Generation Failed
            </p>
            {status.error_message && (
              <p style={{ fontSize: 12, color: 'rgba(248,113,113,0.7)', marginTop: 8 }}>
                {status.error_message}
              </p>
            )}
          </div>
        )}

        {/* Stages */}
        <div style={{ flex: 1, overflowY: 'auto', minHeight: 0, marginTop: 16 }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {STAGES.map((stage, index) => {
            const isCompleted = index < currentStageIndex || status.status === 'completed';
            const isActive =
              index === currentStageIndex &&
              status.status !== 'completed' &&
              status.status !== 'failed';

            return (
              <motion.div
                key={stage.key}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                style={{
                  display: 'flex', alignItems: 'flex-start', gap: 10,
                  padding: '8px 10px', borderRadius: 10,
                  background: isActive ? 'rgba(139,92,246,0.08)' : 'transparent',
                  border: isActive ? '1px solid rgba(139,92,246,0.15)' : '1px solid transparent',
                  transition: 'all 0.2s',
                }}
              >
                <div style={{ flexShrink: 0, marginTop: 2 }}>
                  {isCompleted ? (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: 'spring', stiffness: 300 }}
                    >
                      <CheckCircle2 style={{ width: 18, height: 18, color: '#34d399' }} />
                    </motion.div>
                  ) : isActive ? (
                    <div
                      style={{
                        width: 18, height: 18, borderRadius: '50%',
                        background: 'rgba(139,92,246,0.15)',
                        border: '1px solid rgba(139,92,246,0.3)',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                      }}
                    >
                      <Loader2
                        className="animate-spin"
                        style={{ width: 11, height: 11, color: '#a78bfa' }}
                      />
                    </div>
                  ) : (
                    <Circle style={{ width: 18, height: 18, color: '#334155' }} />
                  )}
                </div>

                <div style={{ flex: 1, minWidth: 0 }}>
                  <p
                    style={{
                      fontSize: 13, fontWeight: 600, margin: 0,
                      color: isCompleted ? '#34d399' : isActive ? '#c4b5fd' : '#475569',
                    }}
                  >
                    {stage.label}
                  </p>
                  <p
                    style={{
                      fontSize: 12, margin: '2px 0 0',
                      color: isActive ? '#94a3b8' : '#475569',
                    }}
                  >
                    {isActive && status.current_step ? status.current_step : stage.desc}
                  </p>
                </div>
              </motion.div>
            );
            })}
          </div>

        {/* Completed */}
        <AnimatePresence>
          {status.status === 'completed' && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              style={{ marginTop: 24, overflow: 'hidden' }}
            >
              <div
                style={{
                  padding: 16, borderRadius: 14,
                  background: 'rgba(16,185,129,0.08)',
                  border: '1px solid rgba(16,185,129,0.2)',
                }}
              >
                <p
                  style={{
                    fontSize: 14, fontWeight: 700,
                    color: '#34d399',
                    display: 'flex', alignItems: 'center', gap: 8,
                    margin: 0,
                  }}
                >
                  <CheckCircle2 size={18} />
                  Blog ready! View the PDF preview on the right.
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        </div>
      </div>
    </div>
  );
};
