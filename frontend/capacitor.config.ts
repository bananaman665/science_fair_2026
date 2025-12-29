import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.sciencefair.appleoxidation',
  appName: 'Apple Oxidation',
  webDir: 'dist',
  server: {
    androidScheme: 'https',
    // For development with live reload:
    // url: 'http://192.168.1.X:5173',
    // cleartext: true
  },
  plugins: {
    Camera: {
      permissions: ['camera', 'photos'],
    },
    Keyboard: {
      resize: 'body',
      resizeOnFullScreen: true,
    },
  },
};

export default config;
