import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, FileCheck, Search as SearchIcon, TrendingUp } from 'lucide-react';
import { GlassCard, GlassPanel } from '../components/GlassCard';
import { useStore } from '../store';

export function Dashboard() {
  const { tribunals, fetchTribunals, jobs, fetchJobs } = useStore();
  const [stats, setStats] = useState({
    totalSearches: 0,
    completedJobs: 0,
    activeJobs: 0,
    successRate: 0
  });

  useEffect(() => {
    fetchTribunals();
    fetchJobs();
  }, []);

  useEffect(() => {
    if (jobs.length > 0) {
      const completed = jobs.filter(j => j.status === 'completed').length;
      const active = jobs.filter(j => j.status === 'processing').length;
      const totalSearches = jobs.reduce((acc, j) => acc + (j.total_items || 0), 0);
      const successfulItems = jobs.reduce((acc, j) => acc + (j.successful_items || 0), 0);
      const totalItems = jobs.reduce((acc, j) => acc + (j.processed_items || 0), 0);

      setStats({
        totalSearches,
        completedJobs: completed,
        activeJobs: active,
        successRate: totalItems > 0 ? (successfulItems / totalItems * 100).toFixed(1) : 0
      });
    }
  }, [jobs]);

  const statCards = [
    {
      title: 'Total de Consultas',
      value: stats.totalSearches,
      icon: SearchIcon,
      color: 'blue',
      trend: '+12%'
    },
    {
      title: 'Jobs Concluídos',
      value: stats.completedJobs,
      icon: FileCheck,
      color: 'green',
      trend: '+8%'
    },
    {
      title: 'Jobs Ativos',
      value: stats.activeJobs,
      icon: Activity,
      color: 'purple',
      trend: '...'
    },
    {
      title: 'Taxa de Sucesso',
      value: `${stats.successRate}%`,
      icon: TrendingUp,
      color: 'emerald',
      trend: '+2.5%'
    }
  ];

  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
    emerald: 'from-emerald-500 to-emerald-600'
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-card p-8 rounded-3xl">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-4xl font-bold mb-2">
            Bem-vindo ao <span className="gradient-text">JustoBot</span>
          </h1>
          <p className="text-gray-400">
            Sistema inteligente de consulta de processos jurídicos
          </p>
        </motion.div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <GlassCard hover className="p-6">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">{stat.title}</p>
                  <p className="text-3xl font-bold">{stat.value}</p>
                  <p className="text-xs text-green-400 mt-2">{stat.trend}</p>
                </div>
                <div className={`p-3 rounded-xl bg-gradient-to-br ${colorClasses[stat.color]}`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </GlassCard>
          </motion.div>
        ))}
      </div>

      {/* Tribunals */}
      <GlassPanel title="Tribunais Disponíveis" icon={SearchIcon}>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {tribunals.length > 0 ? (
            tribunals.map((tribunal) => (
              <div
                key={tribunal.code}
                className="p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-green-400"></div>
                  <div>
                    <p className="font-semibold">{tribunal.code}</p>
                    <p className="text-sm text-gray-400">{tribunal.name}</p>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-400 col-span-3 text-center py-8">
              Carregando tribunais...
            </p>
          )}
        </div>
      </GlassPanel>

      {/* Recent Jobs */}
      <GlassPanel title="Jobs Recentes" icon={FileCheck}>
        <div className="space-y-3">
          {jobs.slice(0, 5).map((job) => (
            <div
              key={job.job_id}
              className="p-4 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between"
            >
              <div>
                <p className="font-medium">{job.tribunal}</p>
                <p className="text-sm text-gray-400">
                  {job.processed_items}/{job.total_items} processados
                </p>
              </div>
              <div className="text-right">
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  job.status === 'completed'
                    ? 'bg-green-500/20 text-green-400'
                    : job.status === 'processing'
                    ? 'bg-blue-500/20 text-blue-400'
                    : 'bg-gray-500/20 text-gray-400'
                }`}>
                  {job.status}
                </span>
                <p className="text-sm text-gray-500 mt-1">
                  {job.progress_percentage.toFixed(0)}%
                </p>
              </div>
            </div>
          ))}
        </div>
      </GlassPanel>
    </div>
  );
}
