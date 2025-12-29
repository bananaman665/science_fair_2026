import { create } from 'zustand';
import { ScanHistoryItem } from '../types/scan.types';
import { supabase } from '../lib/supabase';

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
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        set({ history: [], loading: false });
        return;
      }

      const { data, error } = await supabase
        .from('user_scans')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) throw error;

      // Transform Supabase data to ScanHistoryItem format
      const history: ScanHistoryItem[] = (data || []).map((item) => ({
        id: item.id,
        imageUri: item.image_uri,
        variety: item.variety,
        days_since_cut: item.days_since_cut,
        oxidation_level: item.oxidation_level,
        confidence_lower: item.confidence_lower,
        confidence_upper: item.confidence_upper,
        interpretation: item.interpretation,
        timestamp: item.created_at,
      }));

      set({ history, loading: false });
    } catch (error: any) {
      console.error('Error loading history:', error);
      set({ error: error.message, loading: false });
    }
  },

  addToHistory: async (item) => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('User not authenticated');

      const { error } = await supabase.from('user_scans').insert({
        id: item.id,
        user_id: user.id,
        image_uri: item.imageUri,
        variety: item.variety,
        days_since_cut: item.days_since_cut,
        oxidation_level: item.oxidation_level,
        confidence_lower: item.confidence_lower,
        confidence_upper: item.confidence_upper,
        interpretation: item.interpretation,
      });

      if (error) throw error;

      // Add to local state
      set((state) => ({ history: [item, ...state.history] }));
    } catch (error: any) {
      console.error('Error adding to history:', error);
      set({ error: error.message });
    }
  },

  deleteFromHistory: async (id) => {
    try {
      const { error } = await supabase
        .from('user_scans')
        .delete()
        .eq('id', id);

      if (error) throw error;

      // Remove from local state
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
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;

      const { error } = await supabase
        .from('user_scans')
        .delete()
        .eq('user_id', user.id);

      if (error) throw error;

      set({ history: [] });
    } catch (error: any) {
      console.error('Error clearing history:', error);
      set({ error: error.message });
    }
  },
}));
