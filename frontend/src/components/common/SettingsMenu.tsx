import React, { useState, useRef, useEffect } from 'react';
import { Settings, X, BookOpen, Lightbulb, BarChart3, Trash2, Info, Trophy, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { HowToUseModal } from '../modals/HowToUseModal';
import { TipsModal } from '../modals/TipsModal';
import { AboutModal } from '../modals/AboutModal';
import { ScienceFairModal } from '../modals/ScienceFairModal';
import { useAuthStore } from '../../store/authStore';
import { useHistoryStore } from '../../store/historyStore';

export const SettingsMenu: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [showHowToUse, setShowHowToUse] = useState(false);
  const [showTips, setShowTips] = useState(false);
  const [showAbout, setShowAbout] = useState(false);
  const [showScienceFair, setShowScienceFair] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const { signOut } = useAuthStore();
  const { clearHistory } = useHistoryStore();

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-2 hover:bg-gray-100 rounded-full transition-colors"
        aria-label="Settings"
      >
        <Settings size={24} className="text-gray-700" />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
          <div className="p-4 border-b border-gray-200 flex items-center justify-between">
            <h3 className="font-semibold text-gray-900">Settings</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 hover:bg-gray-100 rounded"
            >
              <X size={16} className="text-gray-500" />
            </button>
          </div>

          <div className="p-2">
            <button
              onClick={() => {
                setShowHowToUse(true);
                setIsOpen(false);
              }}
              className="w-full px-3 py-2 hover:bg-gray-50 rounded text-sm text-left flex items-center gap-3"
            >
              <BookOpen size={18} className="text-gray-600" />
              <span className="text-gray-700">How to Use</span>
            </button>

            <button
              onClick={() => {
                setShowTips(true);
                setIsOpen(false);
              }}
              className="w-full px-3 py-2 hover:bg-gray-50 rounded text-sm text-left flex items-center gap-3"
            >
              <Lightbulb size={18} className="text-gray-600" />
              <span className="text-gray-700">Tips for Best Results</span>
            </button>

            <button
              onClick={() => {
                navigate('/history');
                setIsOpen(false);
              }}
              className="w-full px-3 py-2 hover:bg-gray-50 rounded text-sm text-left flex items-center gap-3"
            >
              <BarChart3 size={18} className="text-gray-600" />
              <span className="text-gray-700">View All Scans</span>
            </button>

            <div className="border-t border-gray-200 my-2"></div>

            <button
              onClick={async () => {
                if (confirm('Are you sure you want to clear all your scan history? This cannot be undone.')) {
                  await clearHistory();
                  setIsOpen(false);
                }
              }}
              className="w-full px-3 py-2 hover:bg-red-50 rounded text-sm text-left text-red-600 flex items-center gap-3"
            >
              <Trash2 size={18} className="text-red-600" />
              <span>Clear Scan History</span>
            </button>

            <div className="border-t border-gray-200 my-2"></div>

            <button
              onClick={async () => {
                await signOut();
                setIsOpen(false);
                navigate('/login', { replace: true });
              }}
              className="w-full px-3 py-2 hover:bg-red-50 rounded text-sm text-left text-red-600 flex items-center gap-3"
            >
              <LogOut size={18} className="text-red-600" />
              <span>Logout</span>
            </button>

            <div className="border-t border-gray-200 my-2"></div>

            <button
              onClick={() => {
                setShowAbout(true);
                setIsOpen(false);
              }}
              className="w-full px-3 py-2 hover:bg-gray-50 rounded text-sm text-left flex items-center gap-3"
            >
              <Info size={18} className="text-gray-600" />
              <span className="text-gray-700">About This App</span>
            </button>

            <button
              onClick={() => {
                setShowScienceFair(true);
                setIsOpen(false);
              }}
              className="w-full px-3 py-2 hover:bg-gray-50 rounded text-sm text-left flex items-center gap-3"
            >
              <Trophy size={18} className="text-gray-600" />
              <span className="text-gray-700">Science Fair 2026</span>
            </button>
          </div>
        </div>
      )}

      {/* Modals */}
      <HowToUseModal isOpen={showHowToUse} onClose={() => setShowHowToUse(false)} />
      <TipsModal isOpen={showTips} onClose={() => setShowTips(false)} />
      <AboutModal isOpen={showAbout} onClose={() => setShowAbout(false)} />
      <ScienceFairModal isOpen={showScienceFair} onClose={() => setShowScienceFair(false)} />
    </div>
  );
};
