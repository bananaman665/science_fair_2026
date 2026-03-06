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
    const startTime = Date.now();
    try {
      console.log('='.repeat(60));
      console.log('🔍 [useAPI] Starting analysis pipeline');
      console.log(`🔍 [useAPI] Variety: ${variety}`);
      console.log(`🔍 [useAPI] Image URI: ${imageUri.substring(0, 80)}...`);
      setLoading(true);
      setError(null);

      // Step 1: Convert URI to Blob
      const step1Start = Date.now();
      console.log('📷 [useAPI] Step 1: Converting URI to blob...');
      const blob = await imageService.uriToBlob(imageUri);
      console.log(`📷 [useAPI] Step 1 DONE: ${blob.size} bytes, took ${Date.now() - step1Start}ms`);

      // Step 2: Compress image
      const step2Start = Date.now();
      console.log('🗜️ [useAPI] Step 2: Compressing image...');
      const compressedBlob = await imageService.compressImage(blob);
      console.log(`🗜️ [useAPI] Step 2 DONE: ${compressedBlob.size} bytes, took ${Date.now() - step2Start}ms`);

      // Step 3: Send to API
      const step3Start = Date.now();
      console.log('📤 [useAPI] Step 3: Sending to API...');
      const result = await apiService.analyzeApple(compressedBlob, variety);
      console.log(`📤 [useAPI] Step 3 DONE: took ${Date.now() - step3Start}ms`);
      console.log(`✅ [useAPI] FULL PIPELINE SUCCESS: ${Date.now() - startTime}ms total`);
      console.log(`✅ [useAPI] Prediction: ${result.prediction.days_since_cut} days`);
      console.log('='.repeat(60));

      setLoading(false);
      return result;
    } catch (err: any) {
      const elapsed = Date.now() - startTime;
      const errorMsg = err.response?.data?.detail || err.message || 'Analysis failed';
      console.error('='.repeat(60));
      console.error(`❌ [useAPI] PIPELINE FAILED after ${elapsed}ms`);
      console.error(`❌ [useAPI] Error message: ${errorMsg}`);
      console.error(`❌ [useAPI] Error code: ${err.code}`);
      console.error(`❌ [useAPI] HTTP status: ${err.response?.status}`);
      console.error(`❌ [useAPI] Response data:`, err.response?.data);
      console.error(`❌ [useAPI] Request URL: ${err.config?.baseURL}${err.config?.url}`);
      console.error(`❌ [useAPI] Was request sent: ${err.request ? 'YES' : 'NO'}`);
      console.error(`❌ [useAPI] Was response received: ${err.response ? 'YES' : 'NO'}`);
      console.error('='.repeat(60));
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
