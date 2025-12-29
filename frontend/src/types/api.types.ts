export type AppleVariety = 'combined' | 'gala' | 'smith' | 'red_delicious';

export type OxidationLevel = 'none' | 'minimal' | 'light' | 'medium' | 'medium-heavy' | 'heavy';

export interface AnalyzeResponse {
  success: boolean;
  prediction: {
    days_since_cut: number;
    confidence_interval: {
      lower: number;
      upper: number;
    };
    interpretation: string;
    oxidation_level: OxidationLevel;
  };
  model_info: {
    variety_used: AppleVariety;
    validation_mae?: number;
    training_samples?: number;
  };
}

export interface HealthCheckResponse {
  status: string;
  models_loaded: string[];
  metadata: Record<string, any>;
}
