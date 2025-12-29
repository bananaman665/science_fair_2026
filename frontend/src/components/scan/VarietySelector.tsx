import React from 'react';
import { AppleVariety } from '../../types/api.types';

interface VarietySelectorProps {
  selectedVariety: AppleVariety;
  onSelect: (variety: AppleVariety) => void;
}

const varieties: { value: AppleVariety; label: string; color: string }[] = [
  { value: 'combined', label: 'Auto Detect', color: 'bg-gray-500' },
  { value: 'gala', label: 'Gala', color: 'bg-red-500' },
  { value: 'smith', label: 'Granny Smith', color: 'bg-green-600' },
  { value: 'red_delicious', label: 'Red Delicious', color: 'bg-red-700' },
];

export const VarietySelector: React.FC<VarietySelectorProps> = ({
  selectedVariety,
  onSelect,
}) => {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-gray-700">Apple Variety</label>
      <div className="grid grid-cols-2 gap-2">
        {varieties.map((variety) => (
          <button
            key={variety.value}
            onClick={() => onSelect(variety.value)}
            className={`p-3 rounded-lg border-2 transition-all ${
              selectedVariety === variety.value
                ? 'border-primary bg-primary/10'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center gap-2">
              <div className={`w-4 h-4 rounded-full ${variety.color}`} />
              <span className="text-sm font-medium text-gray-800">{variety.label}</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};
