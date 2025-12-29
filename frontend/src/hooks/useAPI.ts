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
      setLoading(true);
      setError(null);

      // Convert URI to Blob
      const blob = await imageService.uriToBlob(imageUri);

      // Optional: Compress image
      const compressedBlob = await imageService.compressImage(blob);

      // Send to API
      const result = await apiService.analyzeApple(compressedBlob, variety);

      setLoading(false);
      return result;
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || err.message || 'Analysis failed';
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
