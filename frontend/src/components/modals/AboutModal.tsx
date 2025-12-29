import React from 'react';
import { X, Brain, Cpu, BarChart } from 'lucide-react';

interface AboutModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AboutModal: React.FC<AboutModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-md w-full max-h-[80vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex items-center justify-between rounded-t-2xl">
          <h2 className="text-xl font-bold text-gray-900">About This App</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X size={20} className="text-gray-500" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          <div className="text-center">
            <div className="text-5xl mb-3">🍎</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">Apple Oxidation Detection</h3>
            <p className="text-sm text-gray-500">AI-Powered Freshness Analysis</p>
          </div>

          <div className="space-y-4">
            <div className="flex gap-3 items-start">
              <Brain size={20} className="text-primary flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Machine Learning</h4>
                <p className="text-sm text-gray-600">
                  Uses advanced neural networks trained on hundreds of apple images to predict freshness.
                </p>
              </div>
            </div>

            <div className="flex gap-3 items-start">
              <Cpu size={20} className="text-primary flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Computer Vision</h4>
                <p className="text-sm text-gray-600">
                  Analyzes oxidation patterns, color changes, and texture to determine how long since the apple was cut.
                </p>
              </div>
            </div>

            <div className="flex gap-3 items-start">
              <BarChart size={20} className="text-primary flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">High Accuracy</h4>
                <p className="text-sm text-gray-600">
                  Variety-specific models achieve accuracy within ±0.75 days on average.
                </p>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-200 pt-4">
            <h4 className="font-semibold text-gray-900 mb-2">Technology Stack</h4>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-primary/10 text-primary text-xs font-medium rounded-full">React</span>
              <span className="px-3 py-1 bg-primary/10 text-primary text-xs font-medium rounded-full">TensorFlow</span>
              <span className="px-3 py-1 bg-primary/10 text-primary text-xs font-medium rounded-full">FastAPI</span>
              <span className="px-3 py-1 bg-primary/10 text-primary text-xs font-medium rounded-full">Capacitor</span>
            </div>
          </div>

          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-center">
            <p className="text-xs text-gray-600">Version 1.0.0</p>
          </div>
        </div>
      </div>
    </div>
  );
};
