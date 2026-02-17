import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { Loading } from '../../components/common/Loading';

export const AuthCallbackPage: React.FC = () => {
  const navigate = useNavigate();
  const { user, initialized } = useAuthStore();

  useEffect(() => {
    if (!initialized) return;

    if (user) {
      navigate('/scan', { replace: true });
    } else {
      navigate('/login', { replace: true });
    }
  }, [user, initialized, navigate]);

  return (
    <div className="h-screen flex items-center justify-center bg-gradient-to-br from-primary to-green-700">
      <div className="text-center text-white">
        <Loading message="Completing sign in..." />
      </div>
    </div>
  );
};
