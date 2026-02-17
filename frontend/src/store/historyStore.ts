import { create } from 'zustand';
import { ScanHistoryItem } from '../types/scan.types';
import { auth, db } from '../lib/firebase';
import {
  collection,
  query,
  where,
  orderBy,
  getDocs,
  addDoc,
  deleteDoc,
  doc,
  serverTimestamp,
  Timestamp,
} from 'firebase/firestore';

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
      const user = auth.currentUser;
      if (!user) {
        set({ history: [], loading: false });
        return;
      }

      // Query Firestore for user scans
      const scansRef = collection(db, 'user_scans');
      const q = query(
        scansRef,
        where('user_id', '==', user.uid),
        orderBy('created_at', 'desc')
      );

      const querySnapshot = await getDocs(q);

      // Transform Firestore data to ScanHistoryItem format
      const history: ScanHistoryItem[] = querySnapshot.docs.map((doc) => {
        const data = doc.data();
        return {
          id: doc.id,
          imageUri: data.image_uri,
          variety: data.variety,
          days_since_cut: data.days_since_cut,
          oxidation_level: data.oxidation_level,
          confidence_lower: data.confidence_lower,
          confidence_upper: data.confidence_upper,
          interpretation: data.interpretation,
          timestamp: data.created_at?.toDate?.()?.toISOString() || new Date().toISOString(),
        };
      });

      set({ history, loading: false });
    } catch (error: any) {
      console.error('Error loading history:', error);
      set({ error: error.message, loading: false });
    }
  },

  addToHistory: async (item) => {
    try {
      const user = auth.currentUser;
      if (!user) {
        console.error('❌ Cannot save: User not authenticated');
        throw new Error('User not authenticated');
      }

      console.log('💾 Saving scan to Firestore...', { variety: item.variety, days: item.days_since_cut });

      // Add to Firestore and capture the document reference
      const scansRef = collection(db, 'user_scans');
      const docRef = await addDoc(scansRef, {
        user_id: user.uid,
        image_uri: item.imageUri,
        variety: item.variety,
        days_since_cut: item.days_since_cut,
        oxidation_level: item.oxidation_level,
        confidence_lower: item.confidence_lower,
        confidence_upper: item.confidence_upper,
        interpretation: item.interpretation,
        created_at: serverTimestamp(),
      });

      console.log('✅ Saved to Firestore with ID:', docRef.id);

      // Add to local state with the Firestore document ID
      const savedItem: ScanHistoryItem = {
        ...item,
        id: docRef.id, // Use Firestore's ID, not the app-generated one
      };

      set((state) => ({ history: [savedItem, ...state.history] }));
      console.log('✅ Added to local state');
    } catch (error: any) {
      console.error('❌ Error adding to history:', error);
      set({ error: error.message });
      throw error; // Re-throw so the ScanPage knows it failed
    }
  },

  deleteFromHistory: async (id) => {
    try {
      // Delete from Firestore
      const docRef = doc(db, 'user_scans', id);
      await deleteDoc(docRef);

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
      const user = auth.currentUser;
      if (!user) return;

      // Query all user scans
      const scansRef = collection(db, 'user_scans');
      const q = query(scansRef, where('user_id', '==', user.uid));
      const querySnapshot = await getDocs(q);

      // Delete all documents
      const deletePromises = querySnapshot.docs.map((document) =>
        deleteDoc(doc(db, 'user_scans', document.id))
      );
      await Promise.all(deletePromises);

      set({ history: [] });
    } catch (error: any) {
      console.error('Error clearing history:', error);
      set({ error: error.message });
    }
  },
}));
