import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { App as CapacitorApp } from '@capacitor/app';
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

  // Deep link listener for OAuth callbacks (Firebase handles this automatically)
  useEffect(() => {
    const setupDeepLinkListener = async () => {
      await CapacitorApp.addListener('appUrlOpen', async ({ url }) => {
        console.log('Deep link received:', url);
        // Firebase automatically handles OAuth redirects
        // The authStore will pick up the auth state change
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
