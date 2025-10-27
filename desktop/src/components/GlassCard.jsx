import { motion } from 'framer-motion';

export function GlassCard({ children, className = '', hover = false, ...props }) {
  const baseClass = hover ? 'glass-card-hover' : 'glass-card';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`${baseClass} ${className}`}
      {...props}
    >
      {children}
    </motion.div>
  );
}

export function GlassPanel({ title, children, icon: Icon, action }) {
  return (
    <GlassCard className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          {Icon && <Icon className="w-6 h-6 text-blue-400" />}
          <h2 className="text-xl font-semibold">{title}</h2>
        </div>
        {action}
      </div>
      {children}
    </GlassCard>
  );
}
