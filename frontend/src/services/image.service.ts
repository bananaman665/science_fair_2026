export class ImageService {
  // Convert image URI to Blob for API upload
  async uriToBlob(uri: string): Promise<Blob> {
    try {
      // Handle base64 data URIs directly (more reliable on native Capacitor)
      if (uri.startsWith('data:')) {
        const [header, base64] = uri.split(',');
        const mimeType = header.split(':')[1].split(';')[0];
        const byteCharacters = atob(base64);
        const byteArray = new Uint8Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteArray[i] = byteCharacters.charCodeAt(i);
        }
        return new Blob([byteArray], { type: mimeType });
      }

      // For other URIs (capacitor://, http://, https://) use fetch
      const response = await fetch(uri);
      if (!response.ok) {
        throw new Error(`Failed to fetch image: ${response.statusText}`);
      }
      return await response.blob();
    } catch (error) {
      console.error('Error converting URI to blob:', error);
      throw error;
    }
  }

  // Compress image if needed (optional)
  async compressImage(blob: Blob, maxSizeKB: number = 2000): Promise<Blob> {
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
        const maxDimension = 2048;

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
        }, 'image/jpeg', 0.95);
      };

      img.src = URL.createObjectURL(blob);
    });
  }
}

export const imageService = new ImageService();
