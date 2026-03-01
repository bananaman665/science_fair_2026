import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export const SplashScreen: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/scan', { replace: true });
    }, 500);

    return () => clearTimeout(timer);
  }, [navigate]);

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
