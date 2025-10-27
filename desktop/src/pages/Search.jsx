import { useState, useEffect } from 'react';
import { Search as SearchIcon, FileText, User, Hash } from 'lucide-react';
import { GlassPanel } from '../components/GlassCard';
import { useStore } from '../store';
import { motion } from 'framer-motion';

export function Search() {
  const { tribunals, fetchTribunals, searchCases, loading } = useStore();
  const [formData, setFormData] = useState({
    tribunal: 'TJSP',
    searchType: 'cpf',
    query: ''
  });
  const [results, setResults] = useState(null);

  useEffect(() => {
    fetchTribunals();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await searchCases(formData.tribunal, formData.searchType, formData.query);
      setResults(data);
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  const searchTypes = [
    { value: 'cpf', label: 'CPF', icon: User },
    { value: 'name', label: 'Nome', icon: User },
    { value: 'case_number', label: 'Nº Processo', icon: Hash }
  ];

  return (
    <div className="space-y-6">
      <GlassPanel title="Consulta de Processos" icon={SearchIcon}>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Tribunal */}
          <div>
            <label className="block text-sm font-medium mb-2">Tribunal</label>
            <select
              value={formData.tribunal}
              onChange={(e) => setFormData({ ...formData, tribunal: e.target.value })}
              className="glass-input"
            >
              {tribunals.map((t) => (
                <option key={t.code} value={t.code} className="bg-dark-800">
                  {t.code} - {t.name}
                </option>
              ))}
            </select>
          </div>

          {/* Search Type */}
          <div>
            <label className="block text-sm font-medium mb-3">Tipo de Busca</label>
            <div className="grid grid-cols-3 gap-3">
              {searchTypes.map((type) => (
                <button
                  key={type.value}
                  type="button"
                  onClick={() => setFormData({ ...formData, searchType: type.value })}
                  className={`p-4 rounded-xl border transition-all ${
                    formData.searchType === type.value
                      ? 'bg-gradient-to-r from-blue-500/20 to-purple-500/20 border-blue-500'
                      : 'bg-white/5 border-white/10 hover:border-white/20'
                  }`}
                >
                  <type.icon className="w-6 h-6 mx-auto mb-2" />
                  <p className="text-sm font-medium">{type.label}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Query Input */}
          <div>
            <label className="block text-sm font-medium mb-2">
              {searchTypes.find(t => t.value === formData.searchType)?.label}
            </label>
            <input
              type="text"
              value={formData.query}
              onChange={(e) => setFormData({ ...formData, query: e.target.value })}
              placeholder={`Digite o ${searchTypes.find(t => t.value === formData.searchType)?.label.toLowerCase()}`}
              className="glass-input"
              required
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="glass-button-primary w-full"
          >
            {loading ? 'Buscando...' : 'Buscar Processos'}
          </button>
        </form>
      </GlassPanel>

      {/* Results */}
      {results && (
        <GlassPanel title="Resultados" icon={FileText}>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-blue-500/10 rounded-xl border border-blue-500/20">
              <p className="text-sm text-gray-300">
                Encontrados <span className="font-bold text-white">{results.total_found}</span> processos
              </p>
              <p className="text-xs text-gray-500">
                {new Date(results.search_date).toLocaleString('pt-BR')}
              </p>
            </div>

            {results.cases.map((caseItem, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-6 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold mb-1">{caseItem.case_number}</h3>
                    <p className="text-sm text-gray-400">{caseItem.tribunal}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    caseItem.status === 'ativo'
                      ? 'bg-green-500/20 text-green-400'
                      : 'bg-gray-500/20 text-gray-400'
                  }`}>
                    {caseItem.status}
                  </span>
                </div>

                {caseItem.court && (
                  <p className="text-sm text-gray-400 mb-2">
                    <span className="font-medium">Comarca:</span> {caseItem.court}
                  </p>
                )}

                {caseItem.subject && (
                  <p className="text-sm text-gray-400 mb-4">
                    <span className="font-medium">Assunto:</span> {caseItem.subject}
                  </p>
                )}

                {caseItem.parties.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-white/10">
                    <p className="text-xs font-medium text-gray-500 mb-2">PARTES</p>
                    <div className="space-y-2">
                      {caseItem.parties.map((party, i) => (
                        <div key={i} className="flex items-center gap-2 text-sm">
                          <span className="text-gray-500">{party.role}:</span>
                          <span className="text-gray-300">{party.name}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </GlassPanel>
      )}
    </div>
  );
}
