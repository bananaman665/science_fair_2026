import React from 'react';
import { X, Trophy, Target, Lightbulb, Award } from 'lucide-react';

interface ScienceFairModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ScienceFairModal: React.FC<ScienceFairModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-md w-full max-h-[80vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex items-center justify-between rounded-t-2xl">
          <h2 className="text-xl font-bold text-gray-900">Science Fair 2026</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X size={20} className="text-gray-500" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          <div className="text-center">
            <div className="text-5xl mb-3">🏆</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">AI Food Quality Assessment</h3>
            <p className="text-sm text-gray-500">Using Computer Vision for Freshness Detection</p>
          </div>

          <div className="space-y-4">
            <div className="flex gap-3 items-start">
              <Target size={20} className="text-blue-500 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Project Goal</h4>
                <p className="text-sm text-gray-600">
                  Develop a mobile app that uses artificial intelligence to determine apple freshness by analyzing oxidation levels in photographs.
                </p>
              </div>
            </div>

            <div className="flex gap-3 items-start">
              <Lightbulb size={20} className="text-amber-500 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Scientific Method</h4>
                <p className="text-sm text-gray-600">
                  Collected 300+ images of apple oxidation over 7 days. Trained variety-specific machine learning models. Achieved 21.2% improvement through optimization.
                </p>
              </div>
            </div>

            <div className="flex gap-3 items-start">
              <Award size={20} className="text-green-500 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Key Findings</h4>
                <p className="text-sm text-gray-600">
                  Variety-specific models outperform general models by up to 36%. Image preprocessing significantly impacts accuracy. Domain shift was solved through strategic cropping.
                </p>
              </div>
            </div>

            <div className="flex gap-3 items-start">
              <Trophy size={20} className="text-purple-500 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Real-World Impact</h4>
                <p className="text-sm text-gray-600">
                  This technology could help reduce food waste, assist quality control in food processing, and educate consumers about produce freshness.
                </p>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-r from-primary/10 to-green-50 border border-primary/20 rounded-lg p-4">
            <p className="text-sm text-gray-800 text-center">
              <strong>Predicting apple freshness through computer vision</strong>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
