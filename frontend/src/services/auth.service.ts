import { auth } from '../lib/firebase';
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup,
  signInWithRedirect,
  getRedirectResult,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  GoogleAuthProvider,
  OAuthProvider,
  User,
} from 'firebase/auth';
import { SignUpCredentials, SignInCredentials, AuthProvider } from '../types/auth.types';
import { storageService } from './storage.service';

class AuthService {
  private googleProvider: GoogleAuthProvider;
  private appleProvider: OAuthProvider;

  constructor() {
    // Initialize OAuth providers
    this.googleProvider = new GoogleAuthProvider();
    this.appleProvider = new OAuthProvider('apple.com');
  }

  /**
   * Sign up with email and password
   */
  async signUp({ email, password }: SignUpCredentials) {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    return { user: userCredential.user };
  }

  /**
   * Sign in with email and password
   */
  async signIn({ email, password }: SignInCredentials) {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);

    // Clear localStorage on successful login
    this.clearLocalData();

    return { user: userCredential.user };
  }

  /**
   * Sign in with OAuth provider (Google or Apple)
   */
  async signInWithProvider(provider: AuthProvider) {
    const isNative = !!(window as any).Capacitor;
    const oauthProvider = provider === 'google' ? this.googleProvider : this.appleProvider;

    if (isNative) {
      // Use redirect for native apps (Capacitor)
      await signInWithRedirect(auth, oauthProvider);
    } else {
      // Use popup for web
      const result = await signInWithPopup(auth, oauthProvider);
      return { user: result.user };
    }
  }

  /**
   * Check for redirect result (for native OAuth)
   */
  async checkRedirectResult() {
    const result = await getRedirectResult(auth);
    return result;
  }

  /**
   * Sign out
   */
  async signOut() {
    await firebaseSignOut(auth);

    // Clear all local data
    this.clearLocalData();
  }

  /**
   * Get current user
   */
  getUser(): User | null {
    return auth.currentUser;
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
  onAuthStateChange(callback: (user: User | null) => void) {
    return onAuthStateChanged(auth, callback);
  }
}

export const authService = new AuthService();
