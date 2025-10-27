import { useState, useEffect, useCallback } from 'react';
import { Upload, FileCheck, Download, Clock } from 'lucide-react';
import { GlassPanel } from '../components/GlassCard';
import { useStore } from '../store';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';

export function Bulk() {
  const { tribunals, fetchTribunals, uploadBulk, fetchJobStatus, downloadResults, jobs, fetchJobs, loading } = useStore();
  const [formData, setFormData] = useState({
    tribunal: 'TJSP',
    searchType: 'cpf',
    file: null
  });
  const [currentJob, setCurrentJob] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);

  useEffect(() => {
    fetchTribunals();
    fetchJobs();
  }, []);

  // Poll job status
  useEffect(() => {
    if (!currentJob) return;

    const interval = setInterval(async () => {
      const status = await fetchJobStatus(currentJob.job_id);
      if (status) {
        setJobStatus(status);
        if (status.status === 'completed' || status.status === 'failed') {
          clearInterval(interval);
        }
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [currentJob]);

  const onDrop = useCallback((acceptedFiles) => {
    setFormData({ ...formData, file: acceptedFiles[0] });
  }, [formData]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'text/csv': ['.csv']
    },
    maxFiles: 1
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.file) return;

    try {
      const result = await uploadBulk(formData.file, formData.tribunal, formData.searchType);
      setCurrentJob(result);
      fetchJobs();
    } catch (error) {
      console.error('Upload error:', error);
    }
  };

  const handleDownload = async (jobId) => {
    try {
      await downloadResults(jobId);
    } catch (error) {
      console.error('Download error:', error);
    }
  };

  return (
    <div className="space-y-6">
      <GlassPanel title="Processamento em Lote" icon={Upload}>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* File Upload */}
          <div>
            <label className="block text-sm font-medium mb-3">Arquivo</label>
            <div
              {...getRootProps()}
              className={`p-12 rounded-xl border-2 border-dashed transition-all cursor-pointer ${
                isDragActive
                  ? 'border-blue-500 bg-blue-500/10'
                  : 'border-white/20 bg-white/5 hover:border-white/30'
              }`}
            >
              <input {...getInputProps()} />
              <div className="text-center">
                <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                {formData.file ? (
                  <div>
                    <p className="text-white font-medium">{formData.file.name}</p>
                    <p className="text-sm text-gray-400 mt-1">
                      {(formData.file.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                ) : (
                  <div>
                    <p className="text-white font-medium">
                      Arraste um arquivo ou clique para selecionar
                    </p>
                    <p className="text-sm text-gray-400 mt-1">
                      Formatos aceitos: Excel (.xlsx, .xls) ou CSV
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Tribunal & Search Type */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Tribunal</label>
              <select
                value={formData.tribunal}
                onChange={(e) => setFormData({ ...formData, tribunal: e.target.value })}
                className="glass-input"
              >
                {tribunals.map((t) => (
                  <option key={t.code} value={t.code} className="bg-dark-800">
                    {t.code}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Tipo de Busca</label>
              <select
                value={formData.searchType}
                onChange={(e) => setFormData({ ...formData, searchType: e.target.value })}
                className="glass-input"
              >
                <option value="cpf" className="bg-dark-800">CPF</option>
                <option value="name" className="bg-dark-800">Nome</option>
                <option value="case_number" className="bg-dark-800">Nº Processo</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || !formData.file}
            className="glass-button-primary w-full"
          >
            {loading ? 'Processando...' : 'Iniciar Processamento'}
          </button>
        </form>
      </GlassPanel>

      {/* Current Job Status */}
      {jobStatus && (
        <GlassPanel title="Status do Job" icon={Clock}>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">{jobStatus.tribunal}</p>
                <p className="text-sm text-gray-400">Job ID: {jobStatus.job_id.slice(0, 8)}...</p>
              </div>
              <span className={`px-4 py-2 rounded-full text-sm font-medium ${
                jobStatus.status === 'completed'
                  ? 'bg-green-500/20 text-green-400'
                  : jobStatus.status === 'processing'
                  ? 'bg-blue-500/20 text-blue-400'
                  : jobStatus.status === 'failed'
                  ? 'bg-red-500/20 text-red-400'
                  : 'bg-gray-500/20 text-gray-400'
              }`}>
                {jobStatus.status}
              </span>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Progresso</span>
                <span className="font-medium">{jobStatus.progress_percentage.toFixed(0)}%</span>
              </div>
              <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${jobStatus.progress_percentage}%` }}
                  transition={{ duration: 0.5 }}
                  className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                />
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 pt-4">
              <div className="text-center">
                <p className="text-2xl font-bold">{jobStatus.total_items}</p>
                <p className="text-xs text-gray-400">Total</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-green-400">{jobStatus.successful_items}</p>
                <p className="text-xs text-gray-400">Sucesso</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-red-400">{jobStatus.failed_items}</p>
                <p className="text-xs text-gray-400">Falhas</p>
              </div>
            </div>

            {(jobStatus.status === 'completed' || jobStatus.status === 'partial') && (
              <button
                onClick={() => handleDownload(jobStatus.job_id)}
                className="glass-button-primary w-full flex items-center justify-center gap-2"
              >
                <Download className="w-5 h-5" />
                Baixar Resultados
              </button>
            )}
          </div>
        </GlassPanel>
      )}

      {/* Jobs History */}
      <GlassPanel title="Histórico de Jobs" icon={FileCheck}>
        <div className="space-y-3">
          {jobs.map((job) => (
            <div
              key={job.job_id}
              className="p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">{job.tribunal}</p>
                  <p className="text-sm text-gray-400">
                    {job.total_items} itens • {job.progress_percentage.toFixed(0)}%
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    job.status === 'completed'
                      ? 'bg-green-500/20 text-green-400'
                      : job.status === 'processing'
                      ? 'bg-blue-500/20 text-blue-400'
                      : 'bg-gray-500/20 text-gray-400'
                  }`}>
                    {job.status}
                  </span>
                  {(job.status === 'completed' || job.status === 'partial') && (
                    <button
                      onClick={() => handleDownload(job.job_id)}
                      className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-all"
                    >
                      <Download className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </GlassPanel>
    </div>
  );
}
