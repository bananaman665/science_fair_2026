import React, { useEffect, useState } from 'react';
import { useHistoryStore } from '../store/historyStore';
import { format } from 'date-fns';
import { Trash2, X } from 'lucide-react';
import { HistoryChart } from '../components/scan/HistoryChart';
import { OxidationMeter } from '../components/scan/OxidationMeter';
import { ScanHistoryItem } from '../types/scan.types';

export const HistoryPage: React.FC = () => {
  const { history, loadHistory, deleteFromHistory, clearHistory } = useHistoryStore();
  const [selectedScan, setSelectedScan] = useState<ScanHistoryItem | null>(null);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  if (history.length === 0) {
    return (
      <div className="h-full bg-gray-50 p-4 pb-24 flex items-center justify-center">
        <div className="text-center text-gray-500">
          <p className="text-xl">No scan history yet</p>
          <p className="text-sm mt-2">Start scanning apples to see results here</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-gray-50 p-4 pb-24">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Analysis History</h1>
          <button
            onClick={clearHistory}
            className="text-red-600 text-sm hover:underline"
          >
            Clear All
          </button>
        </div>

        {/* Chart section */}
        <HistoryChart history={history} />

        {/* Detailed scans */}
        <div className="space-y-1">
          <h2 className="text-lg font-bold text-gray-900">Detailed Scans</h2>
          <p className="text-sm text-gray-500">All apple oxidation measurements</p>
        </div>

        <div className="space-y-3">
          {history.map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-lg p-4 shadow-sm cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => setSelectedScan(item)}
            >
              <div className="flex gap-3">
                <img
                  src={item.imageUri}
                  alt="Apple scan"
                  className="w-20 h-20 object-cover rounded"
                />

                <div className="flex-1">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-semibold">{item.days_since_cut.toFixed(1)} days old</p>
                      <p className="text-sm text-gray-600 capitalize">{item.oxidation_level}</p>
                      <p className="text-xs text-gray-500 capitalize">{item.variety}</p>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteFromHistory(item.id);
                      }}
                      className="p-1 hover:bg-gray-100 rounded"
                    >
                      <Trash2 size={16} className="text-red-500" />
                    </button>
                  </div>
                  <p className="text-xs text-gray-400 mt-1">
                    {format(new Date(item.timestamp), 'MMM d, yyyy h:mm a')}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Detail Modal */}
      {selectedScan && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-gray-50 rounded-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
            <div className="p-4 space-y-4">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold text-gray-900">Scan Details</h2>
                <button
                  onClick={() => setSelectedScan(null)}
                  className="p-2 hover:bg-gray-200 rounded-full"
                >
                  <X size={24} />
                </button>
              </div>

              <img
                src={selectedScan.imageUri}
                alt="Scanned apple"
                className="w-full h-56 object-cover rounded-lg"
              />

              <OxidationMeter
                days={selectedScan.days_since_cut}
                level={selectedScan.oxidation_level}
                confidence_lower={selectedScan.confidence_lower}
                confidence_upper={selectedScan.confidence_upper}
              />

              <div className="bg-white p-4 rounded-lg space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">Interpretation:</span>
                  <span className="font-medium text-right">{selectedScan.interpretation}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Confidence Range:</span>
                  <span className="font-medium">
                    {selectedScan.confidence_lower.toFixed(1)} - {selectedScan.confidence_upper.toFixed(1)} days
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Variety:</span>
                  <span className="font-medium capitalize">{selectedScan.variety}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Scanned:</span>
                  <span className="font-medium">
                    {format(new Date(selectedScan.timestamp), 'MMM d, yyyy h:mm a')}
                  </span>
                </div>
              </div>

              <button
                onClick={() => setSelectedScan(null)}
                className="w-full py-3 bg-emerald-600 text-white rounded-lg font-medium hover:bg-emerald-700 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
