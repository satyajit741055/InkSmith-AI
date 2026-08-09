import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authAPI } from '../api/auth';
import { Layout } from '../components/Layout';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Mail, Lock, User, ArrowRight, Loader2, Eye, EyeOff } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const { setToken } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = isLogin
        ? await authAPI.login({ email, password })
        : await authAPI.register({ username, email, password });
      setToken(response.data.access_token);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div
        className="flex items-center justify-center px-6 py-20"
        style={{ minHeight: '80vh' }}
      >
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="w-full max-w-md relative z-10"
        >
          <div
            style={{
              background: '#161625',
              border: '1px solid #2a2a40',
              borderRadius: 24,
              padding: '40px 36px',
              boxShadow: '0 8px 40px rgba(0,0,0,0.5)',
            }}
          >
            {/* Header */}
            <div style={{ textAlign: 'center', marginBottom: 32 }}>
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.1, type: 'spring', stiffness: 200 }}
                style={{
                  width: 56,
                  height: 56,
                  borderRadius: 16,
                  background: 'linear-gradient(135deg, #7c3aed, #3b82f6)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 20px',
                  boxShadow: '0 8px 30px rgba(124, 58, 237, 0.35)',
                }}
              >
                <Sparkles style={{ width: 28, height: 28, color: 'white' }} />
              </motion.div>

              <AnimatePresence mode="wait">
                <motion.div
                  key={isLogin ? 'login' : 'register'}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.2 }}
                >
                  <h2 style={{ fontSize: 28, fontWeight: 700, color: 'white', margin: '0 0 8px' }}>
                    {isLogin ? 'Welcome back' : 'Create account'}
                  </h2>
                  <p style={{ fontSize: 14, color: '#94a3b8', margin: 0 }}>
                    {isLogin
                      ? 'Sign in to continue creating amazing blogs'
                      : 'Start your AI-powered content journey'}
                  </p>
                </motion.div>
              </AnimatePresence>
            </div>

            {/* Error */}
            <AnimatePresence>
              {error && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  style={{ marginBottom: 24, overflow: 'hidden' }}
                >
                  <div
                    style={{
                      borderRadius: 12,
                      padding: 14,
                      textAlign: 'center',
                      background: '#2a1520',
                      border: '1px solid #4a2030',
                    }}
                  >
                    <p style={{ fontSize: 14, fontWeight: 500, color: '#f87171', margin: 0 }}>
                      {error}
                    </p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Form */}
            <form onSubmit={handleSubmit}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
                <AnimatePresence>
                  {!isLogin && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      style={{ overflow: 'hidden' }}
                    >
                      <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#cbd5e1', marginBottom: 8 }}>
                        Username
                      </label>
                      <div style={{ position: 'relative' }}>
                        <User
                          size={18}
                          style={{
                            position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)',
                            color: '#64748b',
                          }}
                        />
                        <input
                          type="text"
                          value={username}
                          onChange={(e) => setUsername(e.target.value)}
                          placeholder="johndoe"
                          className="input-field"
                          style={{
                            width: '100%', paddingLeft: 44, paddingRight: 16,
                            paddingTop: 14, paddingBottom: 14, borderRadius: 12, fontSize: 14,
                          }}
                          required
                        />
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                <div>
                  <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#cbd5e1', marginBottom: 8 }}>
                    Email
                  </label>
                  <div style={{ position: 'relative' }}>
                    <Mail
                      size={18}
                      style={{
                        position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)',
                        color: '#64748b',
                      }}
                    />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="you@example.com"
                      className="input-field"
                      style={{
                        width: '100%', paddingLeft: 44, paddingRight: 16,
                        paddingTop: 14, paddingBottom: 14, borderRadius: 12, fontSize: 14,
                      }}
                      required
                    />
                  </div>
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#cbd5e1', marginBottom: 8 }}>
                    Password
                  </label>
                  <div style={{ position: 'relative' }}>
                    <Lock
                      size={18}
                      style={{
                        position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)',
                        color: '#64748b',
                      }}
                    />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Enter your password"
                      className="input-field"
                      style={{
                        width: '100%', paddingLeft: 44, paddingRight: 48,
                        paddingTop: 14, paddingBottom: 14, borderRadius: 12, fontSize: 14,
                      }}
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      style={{
                        position: 'absolute', right: 14, top: '50%', transform: 'translateY(-50%)',
                        color: '#64748b', background: 'none', border: 'none', cursor: 'pointer',
                        padding: 0, display: 'flex',
                      }}
                    >
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="btn-glow"
                  style={{
                    width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                    gap: 8, padding: '16px 0', borderRadius: 12, fontSize: 15, fontWeight: 700,
                    color: 'white', marginTop: 4, border: 'none', cursor: loading ? 'not-allowed' : 'pointer',
                    opacity: loading ? 0.6 : 1,
                  }}
                >
                  {loading ? (
                    <>
                      <Loader2 style={{ width: 20, height: 20 }} className="animate-spin" />
                      Please wait...
                    </>
                  ) : (
                    <>
                      {isLogin ? 'Sign In' : 'Create Account'}
                      <ArrowRight style={{ width: 20, height: 20 }} />
                    </>
                  )}
                </button>
              </div>
            </form>

            {/* Toggle */}
            <div style={{ marginTop: 28, textAlign: 'center' }}>
              <div
                style={{
                  display: 'flex', alignItems: 'center', gap: 12,
                  margin: '0 0 16px',
                }}
              >
                <div style={{ flex: 1, height: 1, background: '#2a2a40' }} />
                <span style={{ fontSize: 13, color: '#64748b', whiteSpace: 'nowrap' }}>
                  {isLogin ? 'New to InkSmith?' : 'Already have an account?'}
                </span>
                <div style={{ flex: 1, height: 1, background: '#2a2a40' }} />
              </div>
              <button
                onClick={() => {
                  setIsLogin(!isLogin);
                  setError('');
                }}
                style={{
                  fontSize: 14, fontWeight: 600, color: '#a78bfa',
                  background: 'none', border: 'none', cursor: 'pointer',
                  padding: 0,
                }}
                onMouseEnter={(e) => { e.currentTarget.style.color = '#c4b5fd'; }}
                onMouseLeave={(e) => { e.currentTarget.style.color = '#a78bfa'; }}
              >
                {isLogin ? 'Create a free account' : 'Sign in instead'}
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </Layout>
  );
};
