import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

export const SplashScreen: React.FC = () => {
  const navigate = useNavigate();
  const { user, initialized } = useAuthStore();

  useEffect(() => {
    // Wait for auth to initialize
    if (!initialized) return;

    const timer = setTimeout(() => {
      if (user) {
        navigate('/scan', { replace: true });
      } else {
        navigate('/login', { replace: true });
      }
    }, 2000);

    return () => clearTimeout(timer);
  }, [user, initialized, navigate]);

  return (
    <div className="h-screen bg-gradient-to-br from-primary to-green-700 flex items-center justify-center">
      <div className="text-center text-white space-y-4">
        <div className="text-6xl mb-4">🍎</div>
        <h1 className="text-4xl font-bold">Apple Oxidation</h1>
        <p className="text-xl opacity-90">Science Fair 2026</p>
      </div>
    </div>
  );
};
