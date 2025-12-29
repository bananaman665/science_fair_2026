import React from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Camera, History } from 'lucide-react';
import { Header } from '../components/common/Header';

export const MainLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const tabs = [
    { path: '/scan', label: 'Scan', icon: <Camera size={24} /> },
    { path: '/history', label: 'History', icon: <History size={24} /> },
  ];

  return (
    <div className="w-full h-full flex flex-col bg-white">
      {/* Top header bar */}
      <Header />

      {/* Main content */}
      <div className="flex-1 overflow-auto bg-white">
        <Outlet />
      </div>

      {/* Bottom tab navigation */}
      <nav className="bg-white border-t border-gray-200 flex-shrink-0 safe-area-bottom h-20">
        <div className="flex h-full">
          {tabs.map((tab) => (
            <button
              key={tab.path}
              onClick={() => navigate(tab.path)}
              className={`flex-1 flex flex-col items-center justify-start pt-5 gap-0.5 transition-colors ${
                location.pathname === tab.path
                  ? 'text-primary'
                  : 'text-gray-500'
              }`}
            >
              <div className="flex-shrink-0">
                {tab.icon}
              </div>
              <span className="text-xs font-medium leading-none">{tab.label}</span>
            </button>
          ))}
        </div>
      </nav>
    </div>
  );
};
