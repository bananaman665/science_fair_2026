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

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: false,
  initialized: false,
  error: null,

  initialize: async () => {
    try {
      console.log('Auth: Initializing...');

      // Step 1: Check redirect result FIRST, before setting up listener.
      // This must complete before we set initialized to true,
      // otherwise onAuthStateChanged fires with null and we redirect to login.
      let redirectUser: User | null = null;
      try {
        const redirectResult = await authService.checkRedirectResult();
        if (redirectResult?.user) {
          redirectUser = redirectResult.user;
          console.log('Auth: OAuth redirect completed:', redirectResult.user.email);
        }
      } catch (error: any) {
        console.warn('Auth: Redirect check (non-fatal):', error.message);
      }

      // Step 2: If redirect gave us a user, set it immediately
      if (redirectUser) {
        set({ user: redirectUser, initialized: true });
      }

      // Step 3: Set up ongoing auth state listener.
      // Now safe because any redirect has already been processed.
      authService.onAuthStateChange((user) => {
        console.log('Auth: State changed:', user?.email || 'Logged out');
        set({ user, initialized: true });
      });

      // Step 4: If no redirect user, check current auth state and mark initialized
      if (!redirectUser) {
        const currentUser = authService.getUser();
        console.log('Auth: Current user:', currentUser?.email || 'None');
        set({ user: currentUser, initialized: true });
      }

      console.log('Auth: Initialized');
    } catch (error: any) {
      console.error('Auth: Initialization error:', error);
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
      const result = await authService.signInWithProvider(provider);
      if (result?.user) {
        // Popup flow (web) - set user immediately
        console.log('Auth: Popup sign-in success:', result.user.email);
        set({ user: result.user, loading: false });
      }
      // Redirect flow (native) - page will reload, initialize() handles it
    } catch (error: any) {
      console.error('Auth: OAuth error:', error.code, error.message);
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
