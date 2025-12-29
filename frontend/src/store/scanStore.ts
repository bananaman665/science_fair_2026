import { create } from 'zustand';
import { AppleVariety, AnalyzeResponse } from '../types/api.types';

interface ScanState {
  selectedVariety: AppleVariety;
  currentImage: string | null;
  scanResult: AnalyzeResponse | null;
  isScanning: boolean;
  error: string | null;

  setVariety: (variety: AppleVariety) => void;
  setImage: (imageUri: string) => void;
  setScanResult: (result: AnalyzeResponse | null) => void;
  setIsScanning: (isScanning: boolean) => void;
  setError: (error: string | null) => void;
  resetScan: () => void;
}

export const useScanStore = create<ScanState>((set) => ({
  selectedVariety: 'combined',
  currentImage: null,
  scanResult: null,
  isScanning: false,
  error: null,

  setVariety: (variety) => set({ selectedVariety: variety }),
  setImage: (imageUri) => set({ currentImage: imageUri }),
  setScanResult: (result) => set({ scanResult: result }),
  setIsScanning: (isScanning) => set({ isScanning }),
  setError: (error) => set({ error }),
  resetScan: () => set({
    currentImage: null,
    scanResult: null,
    error: null,
    isScanning: false
  }),
}));
