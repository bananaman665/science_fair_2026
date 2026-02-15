import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { App as CapacitorApp } from '@capacitor/app';
import { supabase } from './lib/supabase';
import { SplashScreen } from './pages/SplashScreen';
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';
import { AuthCallbackPage } from './pages/auth/AuthCallbackPage';
import { ScanPage } from './pages/ScanPage';
import { HistoryPage } from './pages/HistoryPage';
import { MainLayout } from './layouts/MainLayout';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { useAuthStore } from './store/authStore';

function App() {
  const { initialize } = useAuthStore();

  useEffect(() => {
    // Initialize auth state on app load
    initialize();
  }, [initialize]);

  // Deep link listener for OAuth callbacks
  useEffect(() => {
    const setupDeepLinkListener = async () => {
      await CapacitorApp.addListener('appUrlOpen', async ({ url }) => {
        console.log('Deep link received:', url);

        if (url.includes('auth/callback')) {
          // Extract tokens from URL hash or query params
          const hashParams = new URLSearchParams(url.split('#')[1] || '');
          const queryParams = new URLSearchParams(url.split('?')[1]?.split('#')[0] || '');

          const accessToken = hashParams.get('access_token') || queryParams.get('access_token');
          const refreshToken = hashParams.get('refresh_token') || queryParams.get('refresh_token');

          if (accessToken && refreshToken) {
            const { error } = await supabase.auth.setSession({
              access_token: accessToken,
              refresh_token: refreshToken,
            });
            if (error) {
              console.error('Error setting session:', error);
            }
          }
        }
      });
    };

    setupDeepLinkListener();

    return () => {
      CapacitorApp.removeAllListeners();
    };
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<SplashScreen />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/auth/callback" element={<AuthCallbackPage />} />

        {/* Protected Routes */}
        <Route
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/scan" element={<ScanPage />} />
          <Route path="/history" element={<HistoryPage />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
