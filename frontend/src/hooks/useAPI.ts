import { useState } from 'react';
import { apiService } from '../services/api';
import { imageService } from '../services/image.service';
import { AppleVariety, AnalyzeResponse } from '../types/api.types';

export const useAPI = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeImage = async (
    imageUri: string,
    variety: AppleVariety
  ): Promise<AnalyzeResponse | null> => {
    try {
      console.log('🔍 Starting analysis for variety:', variety);
      setLoading(true);
      setError(null);

      // Convert URI to Blob
      console.log('📷 Converting image URI to blob...');
      const blob = await imageService.uriToBlob(imageUri);
      console.log('✅ Blob created, size:', blob.size);

      // Optional: Compress image
      console.log('🗜️ Compressing image...');
      const compressedBlob = await imageService.compressImage(blob);
      console.log('✅ Image compressed, size:', compressedBlob.size);

      // Send to API
      console.log('📤 Sending to API...');
      const result = await apiService.analyzeApple(compressedBlob, variety);
      console.log('✅ API response received:', result);

      setLoading(false);
      return result;
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || err.message || 'Analysis failed';
      console.error('❌ Analysis error:', errorMsg);
      console.error('Full error details:', {
        message: err.message,
        code: err.code,
        status: err.response?.status,
        data: err.response?.data,
        config: err.config,
      });
      setError(errorMsg);
      setLoading(false);
      return null;
    }
  };

  const checkHealth = async () => {
    try {
      const health = await apiService.healthCheck();
      return health;
    } catch (err) {
      console.error('Health check failed:', err);
      return null;
    }
  };

  return { analyzeImage, checkHealth, loading, error };
};
