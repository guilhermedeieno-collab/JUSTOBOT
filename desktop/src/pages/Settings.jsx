import { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Key, Save, Eye, EyeOff, Plus, Trash2, Server } from 'lucide-react';
import { GlassPanel } from '../components/GlassCard';
import { useStore } from '../store';
import { motion } from 'framer-motion';

export function Settings() {
  const { config, setConfig } = useStore();
  const [credentials, setCredentials] = useState([]);
  const [showPassword, setShowPassword] = useState({});
  const [newCredential, setNewCredential] = useState({
    tribunal: '',
    apiKey: '',
    apiSecret: '',
    notes: ''
  });

  useEffect(() => {
    // Load credentials from config
    const loadCredentials = async () => {
      const stored = await window.electron?.config.get('credentials');
      if (stored) {
        setCredentials(JSON.parse(stored));
      }
    };
    loadCredentials();
  }, []);

  const saveCredentials = async (newCreds) => {
    await setConfig('credentials', JSON.stringify(newCreds));
    setCredentials(newCreds);
  };

  const handleAddCredential = () => {
    if (!newCredential.tribunal || !newCredential.apiKey) return;

    const updated = [
      ...credentials,
      {
        ...newCredential,
        id: Date.now(),
        createdAt: new Date().toISOString()
      }
    ];

    saveCredentials(updated);
    setNewCredential({ tribunal: '', apiKey: '', apiSecret: '', notes: '' });
  };

  const handleDeleteCredential = (id) => {
    const updated = credentials.filter(c => c.id !== id);
    saveCredentials(updated);
  };

  const togglePasswordVisibility = (id) => {
    setShowPassword(prev => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div className="space-y-6">
      {/* API Credentials */}
      <GlassPanel title="Credenciais de API" icon={Key}>
        <div className="space-y-6">
          {/* Add New Credential Form */}
          <div className="p-6 rounded-xl bg-gradient-to-br from-blue-500/10 to-purple-500/10 border border-white/10">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Plus className="w-5 h-5" />
              Adicionar Nova Credencial
            </h3>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Tribunal</label>
                <input
                  type="text"
                  value={newCredential.tribunal}
                  onChange={(e) => setNewCredential({ ...newCredential, tribunal: e.target.value })}
                  placeholder="ex: TJSP, TJRJ"
                  className="glass-input"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">API Key</label>
                <input
                  type="text"
                  value={newCredential.apiKey}
                  onChange={(e) => setNewCredential({ ...newCredential, apiKey: e.target.value })}
                  placeholder="Sua API Key"
                  className="glass-input"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">API Secret (Opcional)</label>
                <input
                  type="password"
                  value={newCredential.apiSecret}
                  onChange={(e) => setNewCredential({ ...newCredential, apiSecret: e.target.value })}
                  placeholder="Sua API Secret"
                  className="glass-input"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Notas (Opcional)</label>
                <input
                  type="text"
                  value={newCredential.notes}
                  onChange={(e) => setNewCredential({ ...newCredential, notes: e.target.value })}
                  placeholder="Notas ou descrição"
                  className="glass-input"
                />
              </div>
            </div>

            <button
              onClick={handleAddCredential}
              className="glass-button-primary mt-4 flex items-center gap-2"
            >
              <Save className="w-4 h-4" />
              Adicionar Credencial
            </button>
          </div>

          {/* Credentials List */}
          <div className="space-y-3">
            <h3 className="text-sm font-medium text-gray-400">Credenciais Salvas</h3>

            {credentials.length === 0 ? (
              <div className="p-8 text-center text-gray-500 bg-white/5 rounded-xl border border-white/10">
                <Key className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Nenhuma credencial cadastrada</p>
                <p className="text-sm mt-1">Adicione suas primeiras credenciais acima</p>
              </div>
            ) : (
              credentials.map((cred, index) => (
                <motion.div
                  key={cred.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="p-6 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h4 className="text-lg font-semibold">{cred.tribunal}</h4>
                      {cred.notes && (
                        <p className="text-sm text-gray-400 mt-1">{cred.notes}</p>
                      )}
                    </div>
                    <button
                      onClick={() => handleDeleteCredential(cred.id)}
                      className="p-2 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-all"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <label className="text-xs text-gray-500 mb-1 block">API Key</label>
                      <div className="flex items-center gap-2">
                        <input
                          type={showPassword[`key-${cred.id}`] ? 'text' : 'password'}
                          value={cred.apiKey}
                          readOnly
                          className="glass-input flex-1 text-sm"
                        />
                        <button
                          onClick={() => togglePasswordVisibility(`key-${cred.id}`)}
                          className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-all"
                        >
                          {showPassword[`key-${cred.id}`] ? (
                            <EyeOff className="w-4 h-4" />
                          ) : (
                            <Eye className="w-4 h-4" />
                          )}
                        </button>
                      </div>
                    </div>

                    {cred.apiSecret && (
                      <div>
                        <label className="text-xs text-gray-500 mb-1 block">API Secret</label>
                        <div className="flex items-center gap-2">
                          <input
                            type={showPassword[`secret-${cred.id}`] ? 'text' : 'password'}
                            value={cred.apiSecret}
                            readOnly
                            className="glass-input flex-1 text-sm"
                          />
                          <button
                            onClick={() => togglePasswordVisibility(`secret-${cred.id}`)}
                            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-all"
                          >
                            {showPassword[`secret-${cred.id}`] ? (
                              <EyeOff className="w-4 h-4" />
                            ) : (
                              <Eye className="w-4 h-4" />
                            )}
                          </button>
                        </div>
                      </div>
                    )}

                    <p className="text-xs text-gray-600">
                      Adicionado em: {new Date(cred.createdAt).toLocaleString('pt-BR')}
                    </p>
                  </div>
                </motion.div>
              ))
            )}
          </div>
        </div>
      </GlassPanel>

      {/* Server Settings */}
      <GlassPanel title="Configurações do Servidor" icon={Server}>
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-green-500/10 border border-green-500/20">
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse"></div>
              <div>
                <p className="font-medium text-green-400">Servidor Ativo</p>
                <p className="text-sm text-gray-400">Backend rodando em http://127.0.0.1:8000</p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-white/5 border border-white/10">
              <p className="text-sm text-gray-400 mb-1">Porta</p>
              <p className="text-2xl font-bold">8000</p>
            </div>
            <div className="p-4 rounded-xl bg-white/5 border border-white/10">
              <p className="text-sm text-gray-400 mb-1">Ambiente</p>
              <p className="text-2xl font-bold">Local</p>
            </div>
          </div>
        </div>
      </GlassPanel>

      {/* About */}
      <GlassPanel title="Sobre o JustoBot" icon={SettingsIcon}>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 rounded-xl bg-white/5">
            <span className="text-gray-400">Versão</span>
            <span className="font-medium">1.0.0</span>
          </div>
          <div className="flex items-center justify-between p-4 rounded-xl bg-white/5">
            <span className="text-gray-400">Electron</span>
            <span className="font-medium">{window.electron?.version || 'N/A'}</span>
          </div>
          <div className="flex items-center justify-between p-4 rounded-xl bg-white/5">
            <span className="text-gray-400">Plataforma</span>
            <span className="font-medium">{window.electron?.platform || 'Web'}</span>
          </div>
        </div>
      </GlassPanel>
    </div>
  );
}
