import { User } from 'firebase/auth';

export interface AuthState {
  user: User | null;
  loading: boolean;
  initialized: boolean;
}

export interface SignUpCredentials {
  email: string;
  password: string;
}

export interface SignInCredentials {
  email: string;
  password: string;
}

export type AuthProvider = 'google' | 'apple';
