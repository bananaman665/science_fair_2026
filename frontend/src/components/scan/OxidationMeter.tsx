import React from 'react';
import { OxidationLevel } from '../../types/api.types';

interface OxidationMeterProps {
  days: number;
  level: OxidationLevel;
  confidence_lower: number;
  confidence_upper: number;
}

const levelConfig: Record<OxidationLevel, { color: string; label: string }> = {
  none: { color: '#10b981', label: 'Fresh' },
  minimal: { color: '#34d399', label: 'Minimal' },
  light: { color: '#fbbf24', label: 'Light' },
  medium: { color: '#fb923c', label: 'Medium' },
  'medium-heavy': { color: '#f87171', label: 'Heavy' },
  heavy: { color: '#dc2626', label: 'Severe' },
};

export const OxidationMeter: React.FC<OxidationMeterProps> = ({
  days,
  level,
  confidence_lower,
  confidence_upper,
}) => {
  const config = levelConfig[level];

  // Normalize days to 0-5 scale for gauge (5+ is max)
  const normalizedDays = Math.min(days, 5);
  const rotation = (normalizedDays / 5) * 180; // 0-180 degrees

  // SVG gauge dimensions
  const size = 300;
  const center = size / 2;
  const outerRadius = 120;
  const innerRadius = 90;

  // Generate arc path for gauge background
  const arcPath = (startAngle: number, endAngle: number, radius: number) => {
    const start = {
      x: center + radius * Math.cos((startAngle - 90) * (Math.PI / 180)),
      y: center + radius * Math.sin((startAngle - 90) * (Math.PI / 180)),
    };
    const end = {
      x: center + radius * Math.cos((endAngle - 90) * (Math.PI / 180)),
      y: center + radius * Math.sin((endAngle - 90) * (Math.PI / 180)),
    };
    const largeArc = endAngle - startAngle > 180 ? 1 : 0;

    return `M ${start.x} ${start.y} A ${radius} ${radius} 0 ${largeArc} 1 ${end.x} ${end.y}`;
  };

  // Color zones for the gauge
  const zones = [
    { start: 0, end: 30, color: '#10b981' }, // green - fresh
    { start: 30, end: 60, color: '#34d399' }, // light green - minimal
    { start: 60, end: 90, color: '#fbbf24' }, // yellow - light
    { start: 90, end: 120, color: '#fb923c' }, // orange - medium
    { start: 120, end: 150, color: '#f87171' }, // light red - heavy
    { start: 150, end: 180, color: '#dc2626' }, // dark red - severe
  ];

  return (
    <div className="w-full max-w-md mx-auto bg-white rounded-2xl shadow-lg p-8 space-y-6">
      {/* Gauge SVG */}
      <div className="flex justify-center">
        <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="drop-shadow-md">
          {/* Background circle */}
          <circle cx={center} cy={center} r={outerRadius} fill="#f8f9fa" />

          {/* Color zones */}
          {zones.map((zone, idx) => (
            <path
              key={idx}
              d={arcPath(zone.start, zone.end, outerRadius)}
              stroke={zone.color}
              strokeWidth="16"
              fill="none"
              strokeLinecap="round"
            />
          ))}

          {/* Inner circle */}
          <circle cx={center} cy={center} r={innerRadius} fill="white" />

          {/* Tick marks and labels */}
          {[0, 1, 2, 3, 4, 5].map((tick) => {
            const angle = (tick / 5) * 180;
            const x1 = center + (outerRadius + 10) * Math.cos((angle - 90) * (Math.PI / 180));
            const y1 = center + (outerRadius + 10) * Math.sin((angle - 90) * (Math.PI / 180));
            const x2 = center + (outerRadius + 20) * Math.cos((angle - 90) * (Math.PI / 180));
            const y2 = center + (outerRadius + 20) * Math.sin((angle - 90) * (Math.PI / 180));

            const labelX = center + (outerRadius + 35) * Math.cos((angle - 90) * (Math.PI / 180));
            const labelY = center + (outerRadius + 35) * Math.sin((angle - 90) * (Math.PI / 180));

            return (
              <g key={`tick-${tick}`}>
                <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="#d1d5db" strokeWidth="2" />
                <text
                  x={labelX}
                  y={labelY}
                  textAnchor="middle"
                  dy="0.3em"
                  className="text-xs font-semibold fill-gray-600"
                >
                  {tick}d
                </text>
              </g>
            );
          })}

          {/* Needle */}
          <g style={{ transform: `rotate(${rotation}deg)`, transformOrigin: `${center}px ${center}px`, transition: 'transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)' }}>
            <polygon
              points={`${center},${center + 15} ${center - 6},${center - 70} ${center},${center - 85} ${center + 6},${center - 70}`}
              fill={config.color}
              filter="drop-shadow(0 2px 4px rgba(0,0,0,0.2))"
            />
          </g>

          {/* Center pivot circle */}
          <circle cx={center} cy={center} r="8" fill={config.color} filter="drop-shadow(0 2px 4px rgba(0,0,0,0.15))" />
        </svg>
      </div>

      {/* Main reading */}
      <div className="text-center space-y-1">
        <div className="text-5xl font-bold text-gray-900 tracking-tight">
          {days.toFixed(1)}
          <span className="text-2xl text-gray-500 ml-1">days</span>
        </div>
        <div className="inline-block px-3 py-1 rounded-full bg-gradient-to-r from-blue-50 to-blue-100 border border-blue-200">
          <p className="text-sm font-semibold text-blue-900 uppercase tracking-wider">{config.label} Oxidation</p>
        </div>
      </div>

      {/* Confidence interval */}
      <div className="bg-slate-50 rounded-lg p-4 space-y-2 border border-slate-200">
        <p className="text-xs font-semibold text-slate-600 uppercase tracking-wide">Confidence Range</p>
        <div className="flex items-center justify-between">
          <div className="text-center">
            <p className="text-2xl font-bold text-slate-900">{confidence_lower.toFixed(1)}</p>
            <p className="text-xs text-slate-500">lower</p>
          </div>
          <div className="flex-1 h-1 mx-3 bg-gradient-to-r from-green-400 to-red-500 rounded-full"></div>
          <div className="text-center">
            <p className="text-2xl font-bold text-slate-900">{confidence_upper.toFixed(1)}</p>
            <p className="text-xs text-slate-500">upper</p>
          </div>
        </div>
      </div>

      {/* Science note */}
      <div className="bg-amber-50 border-l-4 border-amber-400 p-3">
        <p className="text-xs text-amber-900">
          <span className="font-semibold">Science Note:</span> Apple oxidation (browning) is a chemical reaction when cells are cut and exposed to oxygen. Rate varies by variety, temperature, and storage conditions.
        </p>
      </div>
    </div>
  );
};
