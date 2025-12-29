import React, { useEffect, useState } from 'react';
import { Camera, ImagePlus, X, Lightbulb } from 'lucide-react';
import { useCamera } from '../hooks/useCamera';
import { useAPI } from '../hooks/useAPI';
import { useQuickStats } from '../hooks/useQuickStats';
import { useScanStore } from '../store/scanStore';
import { useHistoryStore } from '../store/historyStore';
import { Button } from '../components/common/Button';
import { Loading } from '../components/common/Loading';
import { VarietySelector } from '../components/scan/VarietySelector';
import { OxidationDisplay } from '../components/scan/OxidationDisplay';
import { QuickStatsCard } from '../components/scan/QuickStatsCard';
import { PhotoConfirmationModal } from '../components/modals/PhotoConfirmationModal';

// Simple UUID v4 generator
const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};

export const ScanPage: React.FC = () => {
  const { capturePhoto, selectPhoto } = useCamera();
  const { analyzeImage, loading } = useAPI();
  const { addToHistory, loadHistory } = useHistoryStore();
  const stats = useQuickStats();

  // State for photo confirmation
  const [pendingPhoto, setPendingPhoto] = useState<string | null>(null);
  const [showConfirmation, setShowConfirmation] = useState(false);

  // Load history on mount for stats
  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const {
    selectedVariety,
    currentImage,
    scanResult,
    setVariety,
    setImage,
    setScanResult,
    setIsScanning,
    resetScan,
  } = useScanStore();

  const handleCapture = async () => {
    const photo = await capturePhoto();
    if (photo?.webPath) {
      setPendingPhoto(photo.webPath);
      setShowConfirmation(true);
    }
  };

  const handleGallery = async () => {
    const photo = await selectPhoto();
    if (photo?.webPath) {
      setPendingPhoto(photo.webPath);
      setShowConfirmation(true);
    }
  };

  const handleConfirmPhoto = async () => {
    if (pendingPhoto) {
      setShowConfirmation(false);
      setImage(pendingPhoto);
      await analyzeCapturedImage(pendingPhoto);
      setPendingPhoto(null);
    }
  };

  const handleCancelPhoto = () => {
    setShowConfirmation(false);
    setPendingPhoto(null);
  };

  const analyzeCapturedImage = async (imageUri: string) => {
    setIsScanning(true);
    const result = await analyzeImage(imageUri, selectedVariety);

    if (result) {
      setScanResult(result);

      // Add to history
      addToHistory({
        id: generateUUID(),
        imageUri,
        variety: result.model_info.variety_used,
        days_since_cut: result.prediction.days_since_cut,
        oxidation_level: result.prediction.oxidation_level,
        confidence_lower: result.prediction.confidence_interval.lower,
        confidence_upper: result.prediction.confidence_interval.upper,
        interpretation: result.prediction.interpretation,
        timestamp: new Date().toISOString(),
      });
    }

    setIsScanning(false);
  };

  const handleClose = () => {
    resetScan();
  };

  // Show results view
  if (currentImage && scanResult) {
    return (
      <div className="h-full bg-gray-50 p-4 pt-8">
        <div className="max-w-2xl mx-auto space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold text-gray-900">Scan Results</h2>
            <button onClick={handleClose} className="p-2 hover:bg-gray-200 rounded-full">
              <X size={24} />
            </button>
          </div>

          <img
            src={currentImage}
            alt="Scanned apple"
            className="w-full h-64 object-cover rounded-lg"
          />

          <OxidationDisplay
            level={scanResult.prediction.oxidation_level}
            days={scanResult.prediction.days_since_cut}
            interpretation={scanResult.prediction.interpretation}
          />

          <div className="bg-white p-4 rounded-lg space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Confidence Range:</span>
              <span className="font-medium">
                {scanResult.prediction.confidence_interval.lower.toFixed(1)} - {scanResult.prediction.confidence_interval.upper.toFixed(1)} days
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Model Used:</span>
              <span className="font-medium capitalize">{scanResult.model_info.variety_used}</span>
            </div>
          </div>

          <Button onClick={handleClose} fullWidth>
            Scan Another Apple
          </Button>
        </div>
      </div>
    );
  }

  // Show capture view
  return (
    <div className="h-full bg-gray-50 p-4 pt-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-center text-gray-900">Scan Apple</h1>

        <VarietySelector
          selectedVariety={selectedVariety}
          onSelect={setVariety}
        />

        <div className="space-y-3">
          <Button
            onClick={handleCapture}
            fullWidth
            size="lg"
            icon={<Camera size={24} />}
            disabled={loading}
          >
            Take Photo
          </Button>

          <Button
            onClick={handleGallery}
            fullWidth
            size="lg"
            variant="outline"
            icon={<ImagePlus size={24} />}
            disabled={loading}
          >
            Choose from Gallery
          </Button>
        </div>

        <QuickStatsCard
          totalScans={stats.totalScans}
          lastScanTime={stats.lastScanTime}
          mostScannedVariety={stats.mostScannedVariety}
        />

        <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-lg p-4">
          <div className="flex gap-3 items-start">
            <Lightbulb size={20} className="text-amber-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-gray-900 mb-1 text-sm">Photography Tip</h4>
              <p className="text-xs text-gray-700">
                For best results, photograph the cut apple surface directly from above with good lighting. Fill the frame and keep the camera steady!
              </p>
            </div>
          </div>
        </div>

        {loading && <Loading message="Analyzing apple oxidation..." />}
      </div>

      {/* Photo confirmation modal */}
      <PhotoConfirmationModal
        isOpen={showConfirmation}
        imageUri={pendingPhoto}
        onConfirm={handleConfirmPhoto}
        onCancel={handleCancelPhoto}
      />
    </div>
  );
};
