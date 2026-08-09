import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Sparkles,
  LogOut,
  LayoutDashboard,
  PlusCircle,
  Menu,
  X,
} from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    setMobileOpen(false);
  }, [location.pathname]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div
      className="min-h-screen flex flex-col relative"
      style={{ background: '#0a0a0f', color: '#e2e8f0', overflowX: 'hidden' }}
    >
      {/* Animated mesh gradient background */}
      <div className="mesh-bg">
        <div className="mesh-blob mesh-blob--violet" />
        <div className="mesh-blob mesh-blob--blue" />
        <div className="mesh-blob mesh-blob--cyan" />
      </div>

      {/* Navbar */}
      <nav
        className={`sticky top-0 z-50 transition-all duration-300 ${
          scrolled ? 'nav-glass shadow-lg' : ''
        }`}
        style={
          scrolled
            ? undefined
            : { background: 'transparent', borderBottom: '1px solid rgba(255,255,255,0.04)' }
        }
      >
        <div className="max-w-6xl mx-auto px-6 lg:px-8">
          <div className="flex justify-between items-center" style={{ height: 64 }}>
            {/* Logo */}
            <Link to="/" className="flex items-center gap-3 group relative z-10">
              <div
                className="w-9 h-9 rounded-xl flex items-center justify-center transition-transform duration-300 group-hover:scale-110"
                style={{
                  background: 'linear-gradient(135deg, #7c3aed, #3b82f6)',
                  boxShadow: '0 4px 15px rgba(124, 58, 237, 0.3)',
                }}
              >
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <span className="text-xl font-extrabold text-gradient">InkSmith</span>
            </Link>

            {/* Desktop nav */}
            <div className="hidden md:flex items-center gap-2">
              {isAuthenticated ? (
                <>
                  <Link
                    to="/dashboard"
                    className="flex items-center gap-2 text-sm font-medium px-4 py-2 rounded-lg transition-colors duration-200"
                    style={{
                      color:
                        location.pathname === '/dashboard'
                          ? '#a78bfa'
                          : '#94a3b8',
                      background:
                        location.pathname === '/dashboard'
                          ? 'rgba(139, 92, 246, 0.1)'
                          : 'transparent',
                    }}
                    onMouseEnter={(e) => {
                      if (location.pathname !== '/dashboard') {
                        e.currentTarget.style.color = '#fff';
                        e.currentTarget.style.background = 'rgba(255,255,255,0.05)';
                      }
                    }}
                    onMouseLeave={(e) => {
                      if (location.pathname !== '/dashboard') {
                        e.currentTarget.style.color = '#94a3b8';
                        e.currentTarget.style.background = 'transparent';
                      }
                    }}
                  >
                    <LayoutDashboard size={18} />
                    Dashboard
                  </Link>
                  <Link
                    to="/new"
                    className="btn-glow flex items-center gap-2 text-sm font-semibold px-5 py-2 rounded-xl text-white"
                  >
                    <PlusCircle size={18} />
                    New Blog
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="flex items-center gap-2 text-sm font-medium px-3 py-2 rounded-lg transition-colors duration-200"
                    style={{ color: '#94a3b8' }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.color = '#f87171';
                      e.currentTarget.style.background = 'rgba(248, 113, 113, 0.1)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.color = '#94a3b8';
                      e.currentTarget.style.background = 'transparent';
                    }}
                  >
                    <LogOut size={18} />
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="text-sm font-medium px-4 py-2 rounded-lg transition-colors duration-200"
                    style={{ color: '#94a3b8' }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.color = '#fff';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.color = '#94a3b8';
                    }}
                  >
                    Sign In
                  </Link>
                  <Link
                    to="/login"
                    className="btn-glow text-sm font-semibold px-5 py-2 rounded-xl text-white"
                  >
                    Get Started
                  </Link>
                </>
              )}
            </div>

            {/* Mobile menu toggle */}
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="md:hidden p-2 rounded-lg transition-colors relative z-10"
              style={{ color: '#94a3b8' }}
            >
              {mobileOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        <AnimatePresence>
          {mobileOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
              className="md:hidden overflow-hidden"
              style={{
                background: 'rgba(15, 15, 25, 0.95)',
                borderTop: '1px solid rgba(255,255,255,0.06)',
              }}
            >
              <div className="px-6 py-4 space-y-2">
                {isAuthenticated ? (
                  <>
                    <Link
                      to="/dashboard"
                      className="flex items-center gap-3 text-sm font-medium px-4 py-3 rounded-xl"
                      style={{ color: '#cbd5e1' }}
                    >
                      <LayoutDashboard size={18} />
                      Dashboard
                    </Link>
                    <Link
                      to="/new"
                      className="btn-glow flex items-center gap-3 text-sm font-semibold px-4 py-3 rounded-xl text-white"
                    >
                      <PlusCircle size={18} />
                      New Blog
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="flex items-center gap-3 text-sm font-medium px-4 py-3 rounded-xl w-full"
                      style={{ color: '#94a3b8' }}
                    >
                      <LogOut size={18} />
                      Logout
                    </button>
                  </>
                ) : (
                  <>
                    <Link
                      to="/login"
                      className="block text-sm font-medium px-4 py-3 rounded-xl"
                      style={{ color: '#cbd5e1' }}
                    >
                      Sign In
                    </Link>
                    <Link
                      to="/login"
                      className="btn-glow block text-sm font-semibold px-4 py-3 rounded-xl text-white text-center"
                    >
                      Get Started
                    </Link>
                  </>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>

      {/* Main content */}
      <main className="flex-1 w-full relative z-10">
        <motion.div
          key={location.pathname}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
        >
          {children}
        </motion.div>
      </main>

      {/* Footer */}
      <footer
        className="relative z-10 mt-20"
        style={{ borderTop: '1px solid rgba(255,255,255,0.05)' }}
      >
        <div className="max-w-6xl mx-auto px-6 lg:px-8 py-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div
                className="w-6 h-6 rounded-lg flex items-center justify-center"
                style={{ background: 'linear-gradient(135deg, #7c3aed, #3b82f6)' }}
              >
                <Sparkles className="w-3 h-3 text-white" />
              </div>
              <span className="text-sm font-semibold text-gradient">InkSmith AI</span>
            </div>
            <p className="text-sm" style={{ color: '#64748b' }}>
              &copy; 2026 InkSmith AI. Crafted with intelligence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};
