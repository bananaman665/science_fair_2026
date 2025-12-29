import React from 'react';
import { X } from 'lucide-react';
import { Button } from '../common/Button';

interface PhotoConfirmationModalProps {
  isOpen: boolean;
  imageUri: string | null;
  onConfirm: () => void;
  onCancel: () => void;
}

export const PhotoConfirmationModal: React.FC<PhotoConfirmationModalProps> = ({
  isOpen,
  imageUri,
  onConfirm,
  onCancel,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-md w-full overflow-hidden shadow-lg">
        {/* Close button */}
        <div className="flex justify-end p-3 border-b border-gray-200">
          <button
            onClick={onCancel}
            className="p-1 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X size={20} className="text-gray-500" />
          </button>
        </div>

        {/* Photo preview */}
        {imageUri && (
          <div className="w-full aspect-square overflow-hidden">
            <img
              src={imageUri}
              alt="Captured photo"
              className="w-full h-full object-cover"
            />
          </div>
        )}

        {/* Content */}
        <div className="p-6 space-y-6">
          <div className="text-center">
            <h2 className="text-xl font-bold text-gray-900 mb-2">
              Do you want to save this?
            </h2>
            <p className="text-sm text-gray-600">
              Review your photo and confirm to proceed with analysis.
            </p>
          </div>

          {/* Buttons */}
          <div className="flex gap-3">
            <Button
              onClick={onCancel}
              variant="outline"
              fullWidth
              size="lg"
            >
              No
            </Button>
            <Button
              onClick={onConfirm}
              variant="primary"
              fullWidth
              size="lg"
            >
              Yes
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};
