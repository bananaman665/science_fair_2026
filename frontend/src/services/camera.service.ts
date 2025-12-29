import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';

export class CameraService {
  // Capture photo from camera
  async capturePhoto() {
    return await Camera.getPhoto({
      quality: 90,
      allowEditing: false,
      resultType: CameraResultType.Uri,
      source: CameraSource.Camera,
    });
  }

  // Select photo from gallery
  async selectFromGallery() {
    return await Camera.getPhoto({
      quality: 90,
      allowEditing: false,
      resultType: CameraResultType.Uri,
      source: CameraSource.Photos,
    });
  }

  // Request camera permissions
  async requestPermissions() {
    return await Camera.requestPermissions();
  }
}

export const cameraService = new CameraService();
