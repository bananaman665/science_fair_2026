import { ScanHistoryItem } from '../types/scan.types';

const STORAGE_KEY = 'apple_scan_history';

export class StorageService {
  // Get all scan history
  getHistory(): ScanHistoryItem[] {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  }

  // Add new scan to history
  addScan(scan: ScanHistoryItem): void {
    const history = this.getHistory();
    history.unshift(scan); // Add to beginning
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
  }

  // Clear all history
  clearHistory(): void {
    localStorage.removeItem(STORAGE_KEY);
  }

  // Delete specific scan
  deleteScan(id: string): void {
    const history = this.getHistory().filter(item => item.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
  }
}

export const storageService = new StorageService();
