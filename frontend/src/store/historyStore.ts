import { create } from 'zustand';
import { ScanHistoryItem } from '../types/scan.types';
import { storageService } from '../services/storage.service';

interface HistoryState {
  history: ScanHistoryItem[];
  loading: boolean;
  error: string | null;

  loadHistory: () => Promise<void>;
  addToHistory: (item: ScanHistoryItem) => Promise<void>;
  deleteFromHistory: (id: string) => Promise<void>;
  clearHistory: () => Promise<void>;
}

export const useHistoryStore = create<HistoryState>((set) => ({
  history: [],
  loading: false,
  error: null,

  loadHistory: async () => {
    set({ loading: true, error: null });
    try {
      const history = storageService.getHistory();
      set({ history, loading: false });
    } catch (error: any) {
      console.error('Error loading history:', error);
      set({ error: error.message, loading: false });
    }
  },

  addToHistory: async (item) => {
    try {
      // Strip imageUri to save localStorage space
      const itemToSave: ScanHistoryItem = {
        ...item,
        imageUri: '',
      };
      storageService.addScan(itemToSave);
      set((state) => ({ history: [itemToSave, ...state.history] }));
    } catch (error: any) {
      console.error('Error adding to history:', error);
      set({ error: error.message });
      throw error;
    }
  },

  deleteFromHistory: async (id) => {
    try {
      storageService.deleteScan(id);
      set((state) => ({
        history: state.history.filter((item) => item.id !== id),
      }));
    } catch (error: any) {
      console.error('Error deleting from history:', error);
      set({ error: error.message });
    }
  },

  clearHistory: async () => {
    try {
      storageService.clearHistory();
      set({ history: [] });
    } catch (error: any) {
      console.error('Error clearing history:', error);
      set({ error: error.message });
    }
  },
}));
