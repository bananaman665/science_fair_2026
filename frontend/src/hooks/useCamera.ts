import { useState } from 'react';
import { cameraService } from '../services/camera.service';

interface CameraResult {
  webPath: string; // Data URL for display and storage
  format: string;
}

export const useCamera = () => {
  const [error, setError] = useState<string | null>(null);

  const capturePhoto = async (): Promise<CameraResult | null> => {
    try {
      setError(null);
      const photo = await cameraService.capturePhoto();
      if (photo.base64String) {
        return {
          webPath: `data:image/${photo.format};base64,${photo.base64String}`,
          format: photo.format,
        };
      }
      return null;
    } catch (err: any) {
      setError(err.message || 'Failed to capture photo');
      return null;
    }
  };

  const selectPhoto = async (): Promise<CameraResult | null> => {
    try {
      setError(null);
      const photo = await cameraService.selectFromGallery();
      if (photo.base64String) {
        return {
          webPath: `data:image/${photo.format};base64,${photo.base64String}`,
          format: photo.format,
        };
      }
      return null;
    } catch (err: any) {
      setError(err.message || 'Failed to select photo');
      return null;
    }
  };

  return { capturePhoto, selectPhoto, error };
};
