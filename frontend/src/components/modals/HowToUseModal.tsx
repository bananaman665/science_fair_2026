import React from 'react';
import { X, Camera, Eye } from 'lucide-react';

interface HowToUseModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const HowToUseModal: React.FC<HowToUseModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-md w-full max-h-[80vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex items-center justify-between rounded-t-2xl">
          <h2 className="text-xl font-bold text-gray-900">How to Use</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X size={20} className="text-gray-500" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          <div className="space-y-4">
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                <span className="text-primary font-bold">1</span>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Select Apple Variety</h3>
                <p className="text-sm text-gray-600">
                  Choose the type of apple you're scanning (Gala, Granny Smith, Red Delicious) or use Auto Detect.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                <Camera size={18} className="text-primary" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Take or Choose Photo</h3>
                <p className="text-sm text-gray-600">
                  Use your camera to capture a fresh photo or select one from your gallery.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                <span className="text-primary font-bold">3</span>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Wait for Analysis</h3>
                <p className="text-sm text-gray-600">
                  Our AI will analyze the apple oxidation in 2-3 seconds using advanced computer vision.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                <Eye size={18} className="text-primary" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">View Results</h3>
                <p className="text-sm text-gray-600">
                  See how many days since the apple was cut, oxidation level, and confidence range.
                </p>
              </div>
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              <strong>Tip:</strong> All your scans are automatically saved to the History tab for future reference.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
