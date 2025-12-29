import React from 'react';
import { X, Sun, Camera, Maximize, CheckCircle } from 'lucide-react';

interface TipsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const TipsModal: React.FC<TipsModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-md w-full max-h-[80vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex items-center justify-between rounded-t-2xl">
          <h2 className="text-xl font-bold text-gray-900">Tips for Best Results</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X size={20} className="text-gray-500" />
          </button>
        </div>

        <div className="p-6 space-y-5">
          <div className="flex gap-3 items-start">
            <Sun size={20} className="text-amber-500 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">Good Lighting</h3>
              <p className="text-sm text-gray-600">
                Take photos in bright, natural light. Avoid shadows or dark areas on the apple surface.
              </p>
            </div>
          </div>

          <div className="flex gap-3 items-start">
            <Camera size={20} className="text-blue-500 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">Hold Steady</h3>
              <p className="text-sm text-gray-600">
                Keep your camera still to avoid blurry photos. Clear, sharp images give better results.
              </p>
            </div>
          </div>

          <div className="flex gap-3 items-start">
            <Maximize size={20} className="text-green-500 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">Fill the Frame</h3>
              <p className="text-sm text-gray-600">
                Get close to the apple so it fills most of the photo. This helps the AI focus on oxidation details.
              </p>
            </div>
          </div>

          <div className="flex gap-3 items-start">
            <CheckCircle size={20} className="text-purple-500 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">Choose the Right Variety</h3>
              <p className="text-sm text-gray-600">
                Selecting the correct apple variety improves accuracy by up to 30%!
              </p>
            </div>
          </div>

          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mt-4">
            <p className="text-sm text-amber-800">
              <strong>Best Practice:</strong> Take photos of the cut surface directly from above at a 90° angle for most accurate results.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
