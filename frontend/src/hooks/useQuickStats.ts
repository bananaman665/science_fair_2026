import { useMemo } from 'react';
import { useHistoryStore } from '../store/historyStore';
import { formatDistanceToNow } from 'date-fns';

export const useQuickStats = () => {
  const { history } = useHistoryStore();

  const stats = useMemo(() => {
    const totalScans = history.length;

    // Last scan time
    const lastScanTime = history.length > 0
      ? formatDistanceToNow(new Date(history[0].timestamp), { addSuffix: true })
      : 'never';

    // Most scanned variety
    const varietyCounts = history.reduce((acc, scan) => {
      acc[scan.variety] = (acc[scan.variety] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const mostScannedVariety = Object.entries(varietyCounts).length > 0
      ? Object.entries(varietyCounts).reduce((a, b) => a[1] > b[1] ? a : b)[0]
      : 'none';

    // Format variety name for display
    const formatVariety = (variety: string) => {
      const names: Record<string, string> = {
        'combined': 'Mixed',
        'gala': 'Gala',
        'smith': 'G. Smith',
        'red_delicious': 'Red Del.',
      };
      return names[variety] || variety;
    };

    return {
      totalScans,
      lastScanTime,
      mostScannedVariety: formatVariety(mostScannedVariety),
    };
  }, [history]);

  return stats;
};
