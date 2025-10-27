import { Outlet, NavLink } from 'react-router-dom';
import { Home, Search, FileUp, Settings, Scale } from 'lucide-react';
import { motion } from 'framer-motion';

export function Layout() {
  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/search', icon: Search, label: 'Consultas' },
    { path: '/bulk', icon: FileUp, label: 'Lote' },
    { path: '/settings', icon: Settings, label: 'Configurações' }
  ];

  return (
    <div className="flex h-screen titlebar-padding">
      {/* Sidebar */}
      <motion.aside
        initial={{ x: -100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        className="w-72 glass-card m-4 mr-0 rounded-3xl flex flex-col"
      >
        {/* Logo */}
        <div className="p-8 border-b border-white/10">
          <div className="flex items-center gap-3">
            <Scale className="w-10 h-10 text-blue-400" />
            <div>
              <h1 className="text-2xl font-bold gradient-text">JustoBot</h1>
              <p className="text-sm text-gray-400">Consulta Jurídica</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {navItems.map((item) => (
              <li key={item.path}>
                <NavLink
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                      isActive
                        ? 'bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-white/20 text-white'
                        : 'text-gray-400 hover:text-white hover:bg-white/5'
                    }`
                  }
                >
                  <item.icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        {/* Footer */}
        <div className="p-6 border-t border-white/10">
          <div className="text-xs text-gray-500 text-center">
            <p>JustoBot v1.0.0</p>
            <p className="mt-1">Powered by FastAPI + Electron</p>
          </div>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 p-4 overflow-auto">
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
        >
          <Outlet />
        </motion.div>
      </main>
    </div>
  );
}
