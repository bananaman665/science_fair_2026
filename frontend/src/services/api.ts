import axios, { AxiosInstance } from 'axios';
import { AnalyzeResponse, HealthCheckResponse, AppleVariety } from '../types/api.types';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

console.log('🌐 API Service initialized with BASE_URL:', BASE_URL);

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: BASE_URL,
      timeout: 60000, // 60s - Cloud Run cold start + model inference
    });

    // Request interceptor for logging
    this.client.interceptors.request.use(
      (config) => {
        console.log(`📡 [API REQUEST] ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
        console.log(`📡 [API REQUEST] Timeout: ${config.timeout}ms`);
        return config;
      },
      (error) => {
        console.error('📡 [API REQUEST ERROR]', error.message);
        return Promise.reject(error);
      }
    );

    // Response interceptor for logging
    this.client.interceptors.response.use(
      (response) => {
        console.log(`📡 [API RESPONSE] ${response.status} ${response.config.url}`);
        return response;
      },
      (error) => {
        if (error.code === 'ECONNABORTED') {
          console.error('📡 [API TIMEOUT] Request timed out after', error.config?.timeout, 'ms');
        } else if (error.response) {
          console.error(`📡 [API ERROR] ${error.response.status}: ${JSON.stringify(error.response.data)}`);
        } else if (error.request) {
          console.error('📡 [API NO RESPONSE] Request sent but no response received');
          console.error('📡 [API NO RESPONSE] This could be: network issue, CORS block, or server down');
        } else {
          console.error('📡 [API SETUP ERROR]', error.message);
        }
        return Promise.reject(error);
      }
    );
  }

  // Health check
  async healthCheck(): Promise<HealthCheckResponse> {
    const response = await this.client.get<HealthCheckResponse>('/health');
    return response.data;
  }

  // Analyze apple image
  async analyzeApple(
    imageBlob: Blob,
    variety: AppleVariety = 'combined'
  ): Promise<AnalyzeResponse> {
    console.log(`🍎 [analyzeApple] Starting - variety: ${variety}, blob size: ${imageBlob.size} bytes (${(imageBlob.size / 1024).toFixed(1)} KB), type: ${imageBlob.type}`);

    const formData = new FormData();
    formData.append('file', imageBlob, 'apple.jpg');

    const response = await this.client.post<AnalyzeResponse>(
      `/analyze?variety=${variety}`,
      formData
    );
    return response.data;
  }
}

export const apiService = new ApiService();
