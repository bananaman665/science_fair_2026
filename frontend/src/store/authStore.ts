import { create } from 'zustand';
import { User, Session } from '@supabase/supabase-js';
import { authService } from '../services/auth.service';
import { SignUpCredentials, SignInCredentials, AuthProvider } from '../types/auth.types';

interface AuthState {
  user: User | null;
  session: Session | null;
  loading: boolean;
  initialized: boolean;
  error: string | null;

  // Actions
  initialize: () => Promise<void>;
  signUp: (credentials: SignUpCredentials) => Promise<void>;
  signIn: (credentials: SignInCredentials) => Promise<void>;
  signInWithProvider: (provider: AuthProvider) => Promise<void>;
  signOut: () => Promise<void>;
  setUser: (user: User | null) => void;
  setSession: (session: Session | null) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  session: null,
  loading: false,
  initialized: false,
  error: null,

  initialize: async () => {
    try {
      const session = await authService.getSession();
      set({ session, user: session?.user ?? null, initialized: true });

      // Listen to auth state changes
      authService.onAuthStateChange((event, session) => {
        set({ session, user: session?.user ?? null });

        // Clear localStorage when user signs in via OAuth
        if (event === 'SIGNED_IN') {
          // Small delay to ensure state is set
          setTimeout(() => {
            const currentUser = get().user;
            if (currentUser) {
              // This handles OAuth callback clearing
              authService['clearLocalData']();
            }
          }, 100);
        }
      });
    } catch (error: any) {
      console.error('Auth initialization error:', error);
      set({ error: error.message, initialized: true });
    }
  },

  signUp: async (credentials) => {
    set({ loading: true, error: null });
    try {
      await authService.signUp(credentials);
      // Don't set user here - wait for email confirmation
      set({ loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  signIn: async (credentials) => {
    set({ loading: true, error: null });
    try {
      const { session, user } = await authService.signIn(credentials);
      set({ session, user, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  signInWithProvider: async (provider) => {
    set({ loading: true, error: null });
    try {
      await authService.signInWithProvider(provider);
      // OAuth redirects, so we don't set loading false here
    } catch (error: any) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  signOut: async () => {
    set({ loading: true, error: null });
    try {
      await authService.signOut();
      set({ user: null, session: null, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  setUser: (user) => set({ user }),
  setSession: (session) => set({ session }),
  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}));
