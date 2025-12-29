import React, { useEffect } from 'react';
import { useHistoryStore } from '../store/historyStore';
import { format } from 'date-fns';
import { Trash2 } from 'lucide-react';

export const HistoryPage: React.FC = () => {
  const { history, loadHistory, deleteFromHistory, clearHistory } = useHistoryStore();

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  if (history.length === 0) {
    return (
      <div className="h-full bg-gray-50 p-4 flex items-center justify-center">
        <div className="text-center text-gray-500">
          <p className="text-xl">No scan history yet</p>
          <p className="text-sm mt-2">Start scanning apples to see results here</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-gray-50 p-4 pb-20">
      <div className="max-w-2xl mx-auto space-y-4">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Scan History</h1>
          <button
            onClick={clearHistory}
            className="text-red-600 text-sm hover:underline"
          >
            Clear All
          </button>
        </div>

        <div className="space-y-3">
          {history.map((item) => (
            <div key={item.id} className="bg-white rounded-lg p-4 shadow-sm">
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
                      onClick={() => deleteFromHistory(item.id)}
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
    </div>
  );
};
