import { AppleVariety, OxidationLevel } from './api.types';

export interface ScanHistoryItem {
  id: string;
  imageUri: string;
  variety: AppleVariety;
  days_since_cut: number;
  oxidation_level: OxidationLevel;
  confidence_lower: number;
  confidence_upper: number;
  interpretation: string;
  timestamp: string; // ISO datetime
}

export interface CameraPhoto {
  webPath?: string;
  format: string;
  saved: boolean;
}
