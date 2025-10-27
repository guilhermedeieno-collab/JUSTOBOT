import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Search } from './pages/Search';
import { Bulk } from './pages/Bulk';
import { Settings } from './pages/Settings';
import { useStore } from './store';
import { useEffect } from 'react';

function App() {
  const { initializeConfig } = useStore();

  useEffect(() => {
    initializeConfig();
  }, []);

  return (
    <BrowserRouter>
      <div className="min-h-screen animated-bg">
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="search" element={<Search />} />
            <Route path="bulk" element={<Bulk />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
