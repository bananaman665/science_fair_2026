export class ImageService {
  // Convert image URI to Blob for API upload
  async uriToBlob(uri: string): Promise<Blob> {
    try {
      // Fetch the URI (works with capacitor://, http://, https://)
      const response = await fetch(uri);
      if (!response.ok) {
        throw new Error(`Failed to fetch image: ${response.statusText}`);
      }
      const blob = await response.blob();
      return blob;
    } catch (error) {
      console.error('Error converting URI to blob:', error);
      throw error;
    }
  }

  // Compress image if needed (optional)
  async compressImage(blob: Blob, maxSizeKB: number = 500): Promise<Blob> {
    // If image is already small enough, return as-is
    if (blob.size / 1024 <= maxSizeKB) {
      return blob;
    }

    // Create canvas for compression
    return new Promise((resolve) => {
      const img = new Image();
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d')!;

      img.onload = () => {
        // Calculate new dimensions while maintaining aspect ratio
        let width = img.width;
        let height = img.height;
        const maxDimension = 1024;

        if (width > maxDimension || height > maxDimension) {
          if (width > height) {
            height = (height / width) * maxDimension;
            width = maxDimension;
          } else {
            width = (width / height) * maxDimension;
            height = maxDimension;
          }
        }

        canvas.width = width;
        canvas.height = height;
        ctx.drawImage(img, 0, 0, width, height);

        canvas.toBlob((compressedBlob) => {
          resolve(compressedBlob || blob);
        }, 'image/jpeg', 0.85);
      };

      img.src = URL.createObjectURL(blob);
    });
  }
}

export const imageService = new ImageService();
