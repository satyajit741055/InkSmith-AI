import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Layout } from '../components/Layout';
import { motion } from 'framer-motion';
import {
  PenLine,
  Brain,
  Gauge,
  DownloadCloud,
  ArrowRight,
  Sparkles,
  Zap,
  Shield,
  Clock,
  FileText,
  Star,
} from 'lucide-react';

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.6, ease: 'easeOut' },
  }),
};

const stagger = {
  visible: { transition: { staggerChildren: 0.08 } },
};

export const LandingPage: React.FC = () => {
  const { isAuthenticated } = useAuth();

  const steps = [
    {
      icon: <PenLine size={20} className="text-white" />,
      label: 'Describe Your Idea',
      desc: 'Enter your blog topic and any specific details you want covered.',
      num: '01',
    },
    {
      icon: <Brain size={20} className="text-white" />,
      label: 'AI Plans & Outlines',
      desc: 'Our AI creates a structured outline with key sections and talking points.',
      num: '02',
    },
    {
      icon: <Gauge size={20} className="text-white" />,
      label: 'Content Generation',
      desc: 'Each section is written in parallel with high-quality, engaging prose.',
      num: '03',
    },
    {
      icon: <DownloadCloud size={20} className="text-white" />,
      label: 'Export & Download',
      desc: 'Get your finished blog as a beautifully formatted PDF, ready to publish.',
      num: '04',
    },
  ];

  const features = [
    {
      title: 'Lightning Fast',
      icon: <Zap size={22} className="text-white" />,
      desc: "Generate publication-ready blogs in under 2 minutes. No waiting, no writer's block.",
      bg: 'linear-gradient(135deg, #f59e0b, #ea580c)',
      shadow: '0 8px 25px rgba(245, 158, 11, 0.25)',
    },
    {
      title: 'AI-Powered Intelligence',
      icon: <Brain size={22} className="text-white" />,
      desc: 'Powered by cutting-edge language models that understand context, tone, and structure.',
      bg: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
      shadow: '0 8px 25px rgba(139, 92, 246, 0.25)',
    },
    {
      title: 'PDF Export',
      icon: <FileText size={22} className="text-white" />,
      desc: 'Beautiful, professionally formatted PDF output ready for distribution or publishing.',
      bg: 'linear-gradient(135deg, #3b82f6, #0891b2)',
      shadow: '0 8px 25px rgba(59, 130, 246, 0.25)',
    },
    {
      title: 'Real-Time Progress',
      icon: <Clock size={22} className="text-white" />,
      desc: 'Watch your blog come to life with live progress tracking through every generation stage.',
      bg: 'linear-gradient(135deg, #10b981, #0d9488)',
      shadow: '0 8px 25px rgba(16, 185, 129, 0.25)',
    },
    {
      title: 'Secure & Private',
      icon: <Shield size={22} className="text-white" />,
      desc: 'Your content stays yours. Enterprise-grade security with token-based authentication.',
      bg: 'linear-gradient(135deg, #f43f5e, #e11d48)',
      shadow: '0 8px 25px rgba(244, 63, 94, 0.25)',
    },
    {
      title: 'Smart Orchestration',
      icon: <Sparkles size={22} className="text-white" />,
      desc: 'Multi-agent architecture plans, writes, and assembles your blog with precision.',
      bg: 'linear-gradient(135deg, #6366f1, #7c3aed)',
      shadow: '0 8px 25px rgba(99, 102, 241, 0.25)',
    },
  ];

  const stats = [
    { value: '10x', label: 'Faster Writing' },
    { value: '100%', label: 'AI Powered' },
    { value: '<2min', label: 'Generation Time' },
    { value: 'PDF', label: 'Export Ready' },
  ];

  return (
    <Layout>
      {/* ===== HERO SECTION ===== */}
      <section className="relative flex flex-col items-center justify-center px-6 pt-20 pb-32 overflow-hidden" style={{ minHeight: '88vh' }}>
        {/* Floating dots */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          {[...Array(6)].map((_, i) => (
            <div
              key={i}
              className="absolute rounded-full"
              style={{
                width: 3 + i,
                height: 3 + i,
                background: 'rgba(139, 92, 246, 0.25)',
                top: `${15 + i * 14}%`,
                left: `${8 + i * 17}%`,
                animation: `float ${4 + i}s ease-in-out infinite ${i * 0.4}s`,
              }}
            />
          ))}
        </div>

        <motion.div
          className="relative z-10 w-full max-w-4xl mx-auto text-center"
          initial="hidden"
          animate="visible"
          variants={stagger}
        >
          {/* Badge */}
          <motion.div variants={fadeUp} custom={0} className="mb-8">
            <span
              className="inline-flex items-center gap-2 px-5 py-2 rounded-full text-sm font-medium"
              style={{
                background: 'rgba(139, 92, 246, 0.1)',
                border: '1px solid rgba(139, 92, 246, 0.2)',
                color: '#c4b5fd',
              }}
            >
              <Sparkles size={14} style={{ color: '#a78bfa' }} />
              AI-Powered Blog Generation
              <ArrowRight size={14} style={{ color: '#a78bfa' }} />
            </span>
          </motion.div>

          {/* Heading */}
          <motion.h1
            variants={fadeUp}
            custom={1}
            className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-black tracking-tight"
            style={{ lineHeight: 1.05 }}
          >
            <span className="text-white">Write Blogs</span>
            <br />
            <span className="text-gradient-hero">with AI Magic</span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            variants={fadeUp}
            custom={2}
            className="mt-7 text-lg sm:text-xl max-w-2xl mx-auto leading-relaxed font-light"
            style={{ color: '#94a3b8' }}
          >
            Transform your ideas into polished, publication-ready blog posts in minutes.
            InkSmith uses multi-agent AI to plan, write, and format your content.
          </motion.p>

          {/* CTA Button */}
          <motion.div
            variants={fadeUp}
            custom={3}
            className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <Link
              to={isAuthenticated ? '/new' : '/login'}
              className="btn-glow group inline-flex items-center gap-3 text-white text-lg font-bold rounded-2xl px-10 py-4"
            >
              {isAuthenticated ? 'Start Writing' : 'Get Started Free'}
              <ArrowRight
                size={20}
                className="group-hover:translate-x-1 transition-transform"
              />
            </Link>
            <span className="text-sm font-medium" style={{ color: '#64748b' }}>
              No credit card required
            </span>
          </motion.div>

          {/* Stats */}
          <motion.div
            variants={fadeUp}
            custom={4}
            className="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-8 max-w-2xl mx-auto"
          >
            {stats.map((stat) => (
              <div key={stat.label} className="text-center">
                <p className="text-2xl sm:text-3xl font-bold text-white">{stat.value}</p>
                <p className="text-xs sm:text-sm mt-1" style={{ color: '#64748b' }}>
                  {stat.label}
                </p>
              </div>
            ))}
          </motion.div>
        </motion.div>

        {/* Bottom fade */}
        <div
          className="absolute bottom-0 left-0 right-0 pointer-events-none"
          style={{
            height: 160,
            background: 'linear-gradient(to top, #0a0a0f, transparent)',
          }}
        />
      </section>

      {/* ===== FEATURES ===== */}
      <section className="relative z-10 py-28">
        <div className="max-w-6xl mx-auto px-6 lg:px-8">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-5">
              Everything you need to
              <br />
              <span className="text-gradient">create amazing blogs</span>
            </h2>
            <p className="text-lg max-w-xl mx-auto" style={{ color: '#94a3b8' }}>
              Powerful features designed to make blog writing effortless and enjoyable.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.08, duration: 0.5 }}
                className="card-glass p-8 group cursor-default transition-transform duration-300 hover:-translate-y-2"
              >
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center mb-5 transition-transform duration-300 group-hover:scale-110"
                  style={{ background: feature.bg, boxShadow: feature.shadow }}
                >
                  {feature.icon}
                </div>
                <h3 className="text-lg font-bold text-white mb-2">{feature.title}</h3>
                <p className="text-sm leading-relaxed" style={{ color: '#94a3b8' }}>
                  {feature.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== HOW IT WORKS ===== */}
      <section className="relative z-10 py-28">
        <div className="max-w-6xl mx-auto px-6 lg:px-8">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-5">
              How it <span className="text-gradient">works</span>
            </h2>
            <p className="text-lg max-w-xl mx-auto" style={{ color: '#94a3b8' }}>
              Four simple steps from idea to published blog post.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {steps.map((step, i) => (
              <motion.div
                key={step.num}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.12, duration: 0.5 }}
                className="card-glass p-8 group transition-transform duration-300 hover:-translate-y-2 relative overflow-hidden"
              >
                {/* Big number watermark */}
                <span
                  className="absolute top-2 right-4 text-7xl font-black pointer-events-none select-none"
                  style={{ color: 'rgba(255,255,255,0.02)' }}
                >
                  {step.num}
                </span>
                <div className="relative z-10">
                  <div
                    className="w-11 h-11 rounded-xl flex items-center justify-center mb-5 transition-transform duration-300 group-hover:scale-110"
                    style={{
                      background: 'linear-gradient(135deg, #7c3aed, #3b82f6)',
                      boxShadow: '0 8px 25px rgba(124, 58, 237, 0.25)',
                    }}
                  >
                    {step.icon}
                  </div>
                  <h4 className="text-base font-bold text-white mb-2">{step.label}</h4>
                  <p className="text-sm leading-relaxed" style={{ color: '#94a3b8' }}>
                    {step.desc}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== TESTIMONIAL ===== */}
      <section className="relative z-10 py-28">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="card-glass p-10 sm:p-14 text-center relative overflow-hidden"
            style={{ borderRadius: 24 }}
          >
            {/* Glow */}
            <div
              className="absolute pointer-events-none"
              style={{
                top: -40,
                left: '50%',
                transform: 'translateX(-50%)',
                width: 300,
                height: 120,
                background: 'radial-gradient(ellipse, rgba(124,58,237,0.15), transparent 70%)',
                filter: 'blur(40px)',
              }}
            />
            <div className="relative z-10">
              <div className="flex justify-center gap-1 mb-6">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} size={20} className="text-amber-400 fill-amber-400" />
                ))}
              </div>
              <blockquote
                className="text-lg sm:text-xl md:text-2xl font-medium leading-relaxed max-w-2xl mx-auto mb-8"
                style={{ color: '#e2e8f0', fontStyle: 'italic' }}
              >
                "InkSmith completely changed how I create content. What used to take me hours
                now takes minutes, and the quality is consistently impressive."
              </blockquote>
              <div className="flex items-center justify-center gap-3">
                <div
                  className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm"
                  style={{ background: 'linear-gradient(135deg, #8b5cf6, #3b82f6)' }}
                >
                  AK
                </div>
                <div className="text-left">
                  <p className="text-white font-semibold text-sm">Alex Kim</p>
                  <p className="text-xs" style={{ color: '#64748b' }}>
                    Content Creator
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ===== FINAL CTA ===== */}
      <section className="relative z-10 py-28">
        <div className="max-w-4xl mx-auto px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="relative overflow-hidden"
            style={{
              borderRadius: 24,
              background: 'linear-gradient(135deg, #1a1040, #141430, #0f1a30)',
              border: '1px solid #2a2a45',
              boxShadow: '0 4px 24px rgba(0,0,0,0.4)',
            }}
          >
            <div className="relative z-10 px-8 sm:px-16 py-16 sm:py-20 text-center">
              <h3 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-5">
                Ready to start writing?
              </h3>
              <p className="text-lg max-w-lg mx-auto mb-10" style={{ color: '#94a3b8' }}>
                Join thousands of content creators using AI to produce better blogs, faster.
              </p>
              <Link
                to={isAuthenticated ? '/new' : '/login'}
                className="btn-glow group inline-flex items-center gap-3 text-white text-lg font-bold rounded-2xl px-10 py-4"
              >
                {isAuthenticated ? 'Create New Blog' : 'Get Started Free'}
                <ArrowRight
                  size={20}
                  className="group-hover:translate-x-1 transition-transform"
                />
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </Layout>
  );
};
