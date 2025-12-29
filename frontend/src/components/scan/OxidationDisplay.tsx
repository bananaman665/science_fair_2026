import React from 'react';
import { OxidationLevel } from '../../types/api.types';

interface OxidationDisplayProps {
  level: OxidationLevel;
  days: number;
  interpretation: string;
}

const levelColors: Record<OxidationLevel, string> = {
  none: 'bg-green-100 text-green-800 border-green-300',
  minimal: 'bg-green-50 text-green-700 border-green-200',
  light: 'bg-yellow-50 text-yellow-700 border-yellow-200',
  medium: 'bg-orange-50 text-orange-700 border-orange-200',
  'medium-heavy': 'bg-red-50 text-red-700 border-red-200',
  heavy: 'bg-red-100 text-red-800 border-red-300',
};

export const OxidationDisplay: React.FC<OxidationDisplayProps> = ({
  level,
  days,
  interpretation,
}) => {
  return (
    <div className={`p-4 rounded-lg border-2 ${levelColors[level]}`}>
      <div className="text-center space-y-2">
        <div className="text-4xl font-bold">{days.toFixed(1)} days</div>
        <div className="text-sm font-medium uppercase tracking-wide">{level}</div>
        <div className="text-sm">{interpretation}</div>
      </div>
    </div>
  );
};
