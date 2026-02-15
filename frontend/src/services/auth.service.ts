import { supabase } from '../lib/supabase';
import { SignUpCredentials, SignInCredentials, AuthProvider } from '../types/auth.types';
import { storageService } from './storage.service';

class AuthService {
  /**
   * Sign up with email and password
   */
  async signUp({ email, password }: SignUpCredentials) {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) throw error;
    return data;
  }

  /**
   * Sign in with email and password
   */
  async signIn({ email, password }: SignInCredentials) {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) throw error;

    // Clear localStorage on successful login
    this.clearLocalData();

    return data;
  }

  /**
   * Sign in with OAuth provider (Google or Apple)
   */
  async signInWithProvider(provider: AuthProvider) {
    const isNative = !!(window as any).Capacitor;
    const redirectTo = isNative
      ? 'com.sciencefair.appleoxidation://auth/callback'
      : `${window.location.origin}/auth/callback`;

    const { data, error } = await supabase.auth.signInWithOAuth({
      provider,
      options: {
        redirectTo,
      },
    });

    if (error) throw error;
    return data;
  }

  /**
   * Sign out
   */
  async signOut() {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;

    // Clear all local data
    this.clearLocalData();
  }

  /**
   * Get current session
   */
  async getSession() {
    const { data, error } = await supabase.auth.getSession();
    if (error) throw error;
    return data.session;
  }

  /**
   * Get current user
   */
  async getUser() {
    const { data, error } = await supabase.auth.getUser();
    if (error) throw error;
    return data.user;
  }

  /**
   * Clear local storage data
   */
  private clearLocalData() {
    storageService.clearHistory();
    // Clear any other localStorage keys if needed
  }

  /**
   * Listen to auth state changes
   */
  onAuthStateChange(callback: (event: string, session: any) => void) {
    return supabase.auth.onAuthStateChange(callback);
  }
}

export const authService = new AuthService();
