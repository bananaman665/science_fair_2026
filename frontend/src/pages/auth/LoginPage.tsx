import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { AppleIcon, GoogleIcon } from '../../components/auth/AuthIcons';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { signInWithProvider, user, loading, error, clearError } = useAuthStore();

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      navigate('/scan', { replace: true });
    }
  }, [user, navigate]);

  const handleOAuthLogin = async (provider: 'google' | 'apple') => {
    clearError();
    try {
      await signInWithProvider(provider);
    } catch (error) {
      console.error(`${provider} login failed:`, error);
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-gradient-to-b from-blue-500 to-blue-400 overflow-y-auto">
      {/* Header with App Name */}
      <div className="flex-shrink-0 pt-20 pb-12">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white">Apple Oxidation</h1>
        </div>
      </div>

      {/* Card Container */}
      <div className="flex-1 flex items-start justify-center px-4 pb-8">
        <div className="bg-white rounded-3xl shadow-2xl w-full max-w-md p-8">
          {/* Heading */}
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-gray-900">Welcome to<br />Apple Oxidation!</h2>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 text-sm">
              {error}
            </div>
          )}

          {/* Social Login Buttons */}
          <div className="space-y-4">
            <button
              onClick={() => handleOAuthLogin('google')}
              disabled={loading}
              className="w-full flex items-center justify-center gap-3 px-6 py-4 bg-white border-2 border-gray-300 rounded-full hover:bg-gray-50 hover:border-blue-500 transition disabled:opacity-50 font-semibold text-gray-700"
              title="Sign in with Google"
            >
              <GoogleIcon />
              <span>Sign in with Google</span>
            </button>

            <button
              onClick={() => handleOAuthLogin('apple')}
              disabled={loading}
              className="w-full flex items-center justify-center gap-3 px-6 py-4 bg-black text-white rounded-full hover:bg-gray-900 transition disabled:opacity-50 font-semibold"
              title="Sign in with Apple"
            >
              <AppleIcon />
              <span>Sign in with Apple</span>
            </button>
          </div>

          {/* Sign Up Link */}
          <p className="text-center text-gray-600 mt-6">
            No Account?{' '}
            <button
              onClick={() => navigate('/register')}
              className="text-blue-500 font-semibold hover:underline"
            >
              Sign up!
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};
