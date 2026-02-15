import React, { useMemo, useState } from 'react';
import { OxidationLevel } from '../../types/api.types';
import { TrendingUp, Info } from 'lucide-react';

interface HistoryItem {
  id: string;
  timestamp: string;
  days_since_cut: number;
  oxidation_level: OxidationLevel;
  variety: string;
}

interface HistoryChartProps {
  history: HistoryItem[];
}

const varietyColors = {
  gala: '#f59e0b',
  smith: '#ef4444',
  red_delicious: '#7c3aed',
  combined: '#3b82f6',
};

const oxidationColorMap: Record<OxidationLevel, string> = {
  none: '#10b981',
  minimal: '#34d399',
  light: '#fbbf24',
  medium: '#fb923c',
  'medium-heavy': '#f87171',
  heavy: '#dc2626',
};

export const HistoryChart: React.FC<HistoryChartProps> = ({ history }) => {
  const [selectedVariety, setSelectedVariety] = useState<string | 'all'>('all');

  // Filter history by variety
  const filteredHistory = useMemo(() => {
    if (selectedVariety === 'all') {
      return history.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
    }
    return history
      .filter((item) => item.variety === selectedVariety)
      .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
  }, [history, selectedVariety]);

  // Get unique varieties
  const varieties = useMemo(() => {
    return Array.from(new Set(history.map((item) => item.variety)));
  }, [history]);

  // Check if we have enough data for a full chart
  const hasEnoughData = filteredHistory.length >= 2;

  if (history.length === 0) {
    return (
      <div className="w-full bg-gradient-to-br from-slate-50 to-slate-100 rounded-2xl p-8 border border-slate-200">
        <div className="flex flex-col items-center justify-center text-center space-y-4 py-8">
          <TrendingUp size={48} className="text-slate-300" />
          <div>
            <h3 className="text-lg font-semibold text-slate-900 mb-1">No scan history yet</h3>
            <p className="text-sm text-slate-600">
              Scan apples at different times to see oxidation progression over time
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Chart dimensions
  const chartWidth = 800;
  const chartHeight = 300;
  const padding = { top: 30, right: 40, bottom: 50, left: 50 };
  const plotWidth = chartWidth - padding.left - padding.right;
  const plotHeight = chartHeight - padding.top - padding.bottom;

  // Find min/max for scaling
  const maxDays = Math.max(...filteredHistory.map((h) => h.days_since_cut), 5);
  const minDays = 0;

  // Calculate scale factors
  const xScale = plotWidth / (Math.max(filteredHistory.length - 1, 1));
  const yScale = plotHeight / (maxDays - minDays || 1);

  // Generate SVG path for line chart (only if >= 2 points)
  const pathData = hasEnoughData
    ? filteredHistory
        .map((item, idx) => {
          const x = padding.left + idx * xScale;
          const y = padding.top + plotHeight - (item.days_since_cut - minDays) * yScale;
          return `${idx === 0 ? 'M' : 'L'} ${x} ${y}`;
        })
        .join(' ')
    : '';

  // Generate area fill path (only if >= 2 points)
  const areaPathData = hasEnoughData
    ? pathData +
      ` L ${padding.left + (filteredHistory.length - 1) * xScale} ${padding.top + plotHeight} L ${padding.left} ${padding.top + plotHeight} Z`
    : '';

  // Grid lines (y-axis) - lighter when not enough data
  const gridLines = Array.from({ length: 6 }, (_, i) => {
    const value = (maxDays / 5) * i;
    const y = padding.top + plotHeight - (value - minDays) * yScale;
    return { y, value };
  });

  // Pluralization helper
  const scanText = filteredHistory.length === 1 ? '1 scan' : `${filteredHistory.length} scans`;

  return (
    <div className="w-full bg-white rounded-2xl shadow-lg p-6 space-y-6">
      {/* Header */}
      <div>
        <h3 className="text-xl font-bold text-gray-900">Oxidation Progression</h3>
        <p className="text-sm text-gray-500 mt-1">{scanText} over time</p>
      </div>

      {/* Variety filter */}
      {varieties.length > 1 && (
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => setSelectedVariety('all')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              selectedVariety === 'all'
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All Varieties
          </button>
          {varieties.map((variety) => (
            <button
              key={variety}
              onClick={() => setSelectedVariety(variety)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all capitalize ${
                selectedVariety === variety
                  ? 'shadow-md text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              style={
                selectedVariety === variety
                  ? { backgroundColor: varietyColors[variety as keyof typeof varietyColors] }
                  : {}
              }
            >
              {variety}
            </button>
          ))}
        </div>
      )}

      {/* Chart or Not Enough Data message */}
      {hasEnoughData ? (
        <>
          <div className="overflow-x-auto pl-4">
            <svg width={chartWidth} height={chartHeight} className="mx-auto" viewBox={`0 0 ${chartWidth} ${chartHeight}`} style={{ overflow: 'visible' }}>
              {/* Background gradient */}
              <defs>
                <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.3" />
                  <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.05" />
                </linearGradient>
              </defs>

              {/* Grid lines */}
              {gridLines.map((line, idx) => (
                <g key={`grid-${idx}`}>
                  <line
                    x1={padding.left}
                    y1={line.y}
                    x2={chartWidth - padding.right}
                    y2={line.y}
                    stroke="#e5e7eb"
                    strokeWidth="1"
                  />
                  <text
                    x={padding.left - 10}
                    y={line.y}
                    textAnchor="end"
                    dy="0.3em"
                    className="text-xs fill-gray-500"
                  >
                    {line.value.toFixed(1)}d
                  </text>
                </g>
              ))}

              {/* Y-axis */}
              <line
                x1={padding.left}
                y1={padding.top}
                x2={padding.left}
                y2={padding.top + plotHeight}
                stroke="#374151"
                strokeWidth="2"
              />

              {/* X-axis */}
              <line
                x1={padding.left}
                y1={padding.top + plotHeight}
                x2={chartWidth - padding.right}
                y2={padding.top + plotHeight}
                stroke="#374151"
                strokeWidth="2"
              />

              {/* Area fill */}
              <path d={areaPathData} fill="url(#areaGradient)" />

              {/* Line path */}
              <path d={pathData} stroke="#3b82f6" strokeWidth="2.5" fill="none" strokeLinecap="round" strokeLinejoin="round" />

              {/* Data points */}
              {filteredHistory.map((item, idx) => {
                const x = padding.left + idx * xScale;
                const y = padding.top + plotHeight - (item.days_since_cut - minDays) * yScale;
                const color = oxidationColorMap[item.oxidation_level];

                return (
                  <g key={`point-${idx}`}>
                    {/* Outer glow */}
                    <circle cx={x} cy={y} r="6" fill={color} opacity="0.2" />
                    {/* Point */}
                    <circle cx={x} cy={y} r="4" fill={color} stroke="white" strokeWidth="2" />
                  </g>
                );
              })}

              {/* Y-axis label */}
              <text
                x={5}
                y={chartHeight / 2}
                textAnchor="middle"
                transform={`rotate(-90 5 ${chartHeight / 2})`}
                className="text-xs font-semibold fill-gray-700"
              >
                Days Since Cut
              </text>

              {/* X-axis label */}
              <text
                x={chartWidth / 2}
                y={chartHeight - 5}
                textAnchor="middle"
                className="text-xs font-semibold fill-gray-700"
              >
                Scan Date
              </text>
            </svg>
          </div>

          {/* Info caption */}
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <Info size={14} className="flex-shrink-0" />
            <span>Each point represents a scan of the apple's surface.</span>
          </div>
        </>
      ) : (
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <TrendingUp size={40} className="text-gray-300 mb-3" />
          <p className="text-gray-500 text-sm">Not enough data yet</p>
          <p className="text-gray-400 text-xs mt-1">Scan again to see trends</p>
        </div>
      )}

      {/* Legend */}
      <div className="grid grid-cols-3 gap-3 pt-4 border-t border-gray-200">
        <div className="space-y-2">
          <p className="text-xs font-semibold text-gray-600 uppercase">Oxidation Levels</p>
          <div className="space-y-1 text-xs">
            {(
              [
                { level: 'none', label: 'Fresh' },
                { level: 'light', label: 'Light' },
                { level: 'medium', label: 'Medium' },
                { level: 'heavy', label: 'Heavy' },
              ] as const
            ).map(({ level, label }) => (
              <div key={level} className="flex items-center gap-2">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: oxidationColorMap[level] }}
                ></div>
                <span className="text-gray-600">{label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-2">
          <p className="text-xs font-semibold text-gray-600 uppercase">Statistics</p>
          <div className="space-y-1 text-xs">
            {filteredHistory.length === 1 ? (
              <p className="text-gray-600">
                <span className="font-semibold text-gray-900">
                  {filteredHistory[0].days_since_cut.toFixed(1)}d
                </span>{' '}
                since cut
              </p>
            ) : (
              <>
                <div>
                  <span className="text-gray-600">Average: </span>
                  <span className="font-semibold text-gray-900">
                    {(filteredHistory.reduce((sum, h) => sum + h.days_since_cut, 0) / filteredHistory.length).toFixed(1)}d
                  </span>
                </div>
                <div>
                  <span className="text-gray-600">Max: </span>
                  <span className="font-semibold text-gray-900">
                    {Math.max(...filteredHistory.map((h) => h.days_since_cut)).toFixed(1)}d
                  </span>
                </div>
                <div>
                  <span className="text-gray-600">Min: </span>
                  <span className="font-semibold text-gray-900">
                    {Math.min(...filteredHistory.map((h) => h.days_since_cut)).toFixed(1)}d
                  </span>
                </div>
              </>
            )}
          </div>
        </div>

        <div className="space-y-2">
          <p className="text-xs font-semibold text-gray-600 uppercase">Data Points</p>
          <div className="space-y-1 text-xs">
            {varieties.map((variety) => {
              const count = history.filter((h) => h.variety === variety).length;
              return (
                <div key={variety} className="flex items-center gap-2">
                  <div
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: varietyColors[variety as keyof typeof varietyColors] }}
                  ></div>
                  <span className="text-gray-600 capitalize">
                    {variety}: <span className="font-semibold">{count}</span>
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
