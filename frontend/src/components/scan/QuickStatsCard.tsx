import React from 'react';
import { Activity, Clock, Award } from 'lucide-react';

interface QuickStatsCardProps {
  totalScans: number;
  lastScanTime: string;
  mostScannedVariety: string;
}

export const QuickStatsCard: React.FC<QuickStatsCardProps> = ({
  totalScans,
  lastScanTime,
  mostScannedVariety,
}) => {
  return (
    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-50 via-white to-green-50 border border-emerald-100 shadow-sm hover:shadow-md transition-all duration-300">
      {/* Subtle organic pattern overlay */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `radial-gradient(circle at 20% 50%, rgba(16, 185, 129, 0.4) 0%, transparent 50%),
                           radial-gradient(circle at 80% 80%, rgba(16, 185, 129, 0.3) 0%, transparent 50%)`
        }}
      />

      {/* Content */}
      <div className="relative p-4">
        <div className="flex items-center gap-2 mb-3">
          <Activity size={18} className="text-emerald-600" strokeWidth={2.5} />
          <h3 className="text-sm font-bold text-gray-800 tracking-tight">Quick Stats</h3>
        </div>

        <div className="grid grid-cols-3 gap-3">
          {/* Total Scans */}
          <div className="group">
            <div className="flex flex-col items-center justify-center p-3 rounded-xl bg-white/60 backdrop-blur-sm border border-emerald-100/50 hover:border-emerald-200 transition-all duration-200 hover:scale-105 min-h-[76px]">
              <div className="text-2xl font-bold text-emerald-600 mb-0.5 tabular-nums">
                {totalScans}
              </div>
              <div className="text-[10px] font-medium text-gray-500 uppercase tracking-wide">
                Scans
              </div>
            </div>
          </div>

          {/* Last Scan */}
          <div className="group">
            <div className="flex flex-col items-center justify-center p-3 rounded-xl bg-white/60 backdrop-blur-sm border border-emerald-100/50 hover:border-emerald-200 transition-all duration-200 hover:scale-105 min-h-[76px]">
              {lastScanTime === 'never' ? (
                <>
                  <div className="text-2xl font-bold text-emerald-600 mb-0.5 tabular-nums">
                    0
                  </div>
                  <div className="text-[10px] font-medium text-gray-500 uppercase tracking-wide">
                    Days Ago
                  </div>
                </>
              ) : (
                <>
                  <Clock size={16} className="text-emerald-500 mb-1" strokeWidth={2.5} />
                  <div className="text-[10px] font-medium text-gray-500 text-center leading-tight uppercase tracking-wide">
                    {lastScanTime}
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Most Scanned */}
          <div className="group">
            <div className="flex flex-col items-center justify-center p-3 rounded-xl bg-white/60 backdrop-blur-sm border border-emerald-100/50 hover:border-emerald-200 transition-all duration-200 hover:scale-105 min-h-[76px]">
              {mostScannedVariety === 'none' ? (
                <>
                  <div className="text-2xl font-bold text-emerald-600 mb-0.5 tabular-nums">
                    0
                  </div>
                  <div className="text-[10px] font-medium text-gray-500 uppercase tracking-wide">
                    Varieties
                  </div>
                </>
              ) : (
                <>
                  <Award size={16} className="text-emerald-500 mb-1" strokeWidth={2.5} />
                  <div className="text-[10px] font-medium text-gray-500 text-center leading-tight uppercase tracking-wide">
                    {mostScannedVariety}
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Decorative corner accent */}
      <div className="absolute -top-8 -right-8 w-24 h-24 bg-emerald-100 rounded-full opacity-20 blur-2xl" />
      <div className="absolute -bottom-6 -left-6 w-20 h-20 bg-green-100 rounded-full opacity-20 blur-xl" />
    </div>
  );
};
