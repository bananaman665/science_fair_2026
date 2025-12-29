import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Eye, EyeOff } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { AppleIcon, GoogleIcon } from '../../components/auth/AuthIcons';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { signIn, signInWithProvider, user, loading, error, clearError } = useAuthStore();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      navigate('/scan', { replace: true });
    }
  }, [user, navigate]);

  const handleEmailLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();

    try {
      await signIn({ email, password });
      navigate('/scan', { replace: true });
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

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
      <div className="flex-shrink-0 pt-8 pb-12">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white">Apple Oxidation</h1>
        </div>
      </div>

      {/* Card Container */}
      <div className="flex-1 flex items-start justify-center px-4 pb-8">
        <div className="bg-white rounded-3xl shadow-2xl w-full max-w-md p-8">
          {/* Heading */}
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-gray-900">Welcome to<br />Apple Oxidation login now!</h2>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 text-sm">
              {error}
            </div>
          )}

          {/* Login Form */}
          <form onSubmit={handleEmailLogin} className="space-y-6">
            {/* Email Field */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition"
                placeholder="joedoe75@gmail.com"
                required
                disabled={loading}
              />
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition"
                  placeholder="••••••••"
                  required
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 transition"
                  disabled={loading}
                >
                  {showPassword ? (
                    <EyeOff size={18} />
                  ) : (
                    <Eye size={18} />
                  )}
                </button>
              </div>
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  disabled={loading}
                  className="w-4 h-4 rounded border-gray-300 text-blue-500 cursor-pointer"
                />
                <span className="text-sm text-gray-700">Remember me</span>
              </label>
              <Link
                to="#"
                className="text-sm font-semibold text-blue-500 hover:text-blue-600 transition"
              >
                Forgot password?
              </Link>
            </div>

            {/* Login Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white font-semibold rounded-full transition duration-200 transform hover:scale-105 active:scale-95"
            >
              {loading ? 'Signing in...' : 'Login'}
            </button>
          </form>

          {/* Divider */}
          <div className="relative my-8">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center">
              <span className="px-3 bg-white text-sm text-gray-600">Or Sign in with</span>
            </div>
          </div>

          {/* Social Login Icons */}
          <div className="flex items-center justify-center gap-6">
            <button
              onClick={() => handleOAuthLogin('google')}
              disabled={loading}
              className="w-12 h-12 rounded-full border-2 border-gray-300 flex items-center justify-center hover:border-blue-500 hover:bg-blue-50 transition disabled:opacity-50"
              title="Sign in with Google"
            >
              <GoogleIcon />
            </button>

            <button
              onClick={() => handleOAuthLogin('apple')}
              disabled={loading}
              className="w-12 h-12 rounded-full border-2 border-gray-300 flex items-center justify-center hover:border-blue-500 hover:bg-blue-50 transition disabled:opacity-50"
              title="Sign in with Apple"
            >
              <AppleIcon />
            </button>
          </div>

          {/* Sign Up Link */}
          <p className="text-center text-gray-700 mt-8">
            Don't have an account?{' '}
            <Link to="/register" className="font-semibold text-blue-500 hover:text-blue-600 transition">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
