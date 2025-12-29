import { useState } from 'react';
import { cameraService } from '../services/camera.service';
import { Photo } from '@capacitor/camera';

export const useCamera = () => {
  const [error, setError] = useState<string | null>(null);

  const capturePhoto = async (): Promise<Photo | null> => {
    try {
      setError(null);
      const photo = await cameraService.capturePhoto();
      return photo;
    } catch (err: any) {
      setError(err.message || 'Failed to capture photo');
      return null;
    }
  };

  const selectPhoto = async (): Promise<Photo | null> => {
    try {
      setError(null);
      const photo = await cameraService.selectFromGallery();
      return photo;
    } catch (err: any) {
      setError(err.message || 'Failed to select photo');
      return null;
    }
  };

  return { capturePhoto, selectPhoto, error };
};
