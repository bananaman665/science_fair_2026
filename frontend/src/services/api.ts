import axios, { AxiosInstance } from 'axios';
import { AnalyzeResponse, HealthCheckResponse, AppleVariety } from '../types/api.types';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: BASE_URL,
      timeout: 30000,
    });
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
