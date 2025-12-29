import React from 'react';
import { Apple } from 'lucide-react';
import { SettingsMenu } from './SettingsMenu';

export const Header: React.FC = () => {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
      <div className="px-4 pt-12 pb-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Apple size={28} style={{ color: '#E4002B' }} strokeWidth={2} />
          <div>
            <h1 className="text-lg font-bold text-gray-900">Apple Oxidation</h1>
            <p className="text-xs text-gray-500">Science Fair 2026</p>
          </div>
        </div>

        <SettingsMenu />
      </div>
    </header>
  );
};
