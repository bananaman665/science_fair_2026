import { create } from 'zustand';
import { User } from 'firebase/auth';
import { authService } from '../services/auth.service';
import { SignUpCredentials, SignInCredentials, AuthProvider } from '../types/auth.types';

interface AuthState {
  user: User | null;
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
  setError: (error: string | null) => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  loading: false,
  initialized: false,
  error: null,

  initialize: async () => {
    try {
      // Check for redirect result (for native OAuth callbacks)
      const redirectResult = await authService.checkRedirectResult();
      if (redirectResult?.user) {
        set({ user: redirectResult.user });
      }

      // Get current user
      const currentUser = authService.getUser();
      set({ user: currentUser, initialized: true });

      // Listen to auth state changes
      authService.onAuthStateChange((user) => {
        set({ user });
      });
    } catch (error: any) {
      console.error('Auth initialization error:', error);
      set({ error: error.message, initialized: true });
    }
  },

  signUp: async (credentials) => {
    set({ loading: true, error: null });
    try {
      const { user } = await authService.signUp(credentials);
      set({ user, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  signIn: async (credentials) => {
    set({ loading: true, error: null });
    try {
      const { user } = await authService.signIn(credentials);
      set({ user, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  signInWithProvider: async (provider) => {
    set({ loading: true, error: null });
    try {
      await authService.signInWithProvider(provider);
      // OAuth redirects for native, popup for web
      // Reset loading after a delay in case redirect fails
      setTimeout(() => {
        if (get().loading) {
          set({ loading: false });
        }
      }, 3000);
    } catch (error: any) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  signOut: async () => {
    set({ loading: true, error: null });
    try {
      await authService.signOut();
      set({ user: null, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  setUser: (user) => set({ user }),
  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}));
