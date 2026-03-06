export class ImageService {
  // Convert image URI to Blob for API upload
  async uriToBlob(uri: string): Promise<Blob> {
    try {
      console.log(`🖼️ [uriToBlob] URI type: ${uri.startsWith('data:') ? 'base64 data URI' : uri.substring(0, 50)}...`);
      console.log(`🖼️ [uriToBlob] URI length: ${uri.length} chars`);

      // Handle base64 data URIs directly (more reliable on native Capacitor)
      if (uri.startsWith('data:')) {
        const [header, base64] = uri.split(',');
        const mimeType = header.split(':')[1].split(';')[0];
        console.log(`🖼️ [uriToBlob] Base64 decode - mime: ${mimeType}, base64 length: ${base64.length}`);

        const byteCharacters = atob(base64);
        const byteArray = new Uint8Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteArray[i] = byteCharacters.charCodeAt(i);
        }
        const blob = new Blob([byteArray], { type: mimeType });
        console.log(`🖼️ [uriToBlob] Created blob from base64: ${blob.size} bytes, type: ${blob.type}`);
        return blob;
      }

      // For other URIs (capacitor://, http://, https://) use fetch
      console.log(`🖼️ [uriToBlob] Fetching URI...`);
      const response = await fetch(uri);
      console.log(`🖼️ [uriToBlob] Fetch response: status=${response.status}, ok=${response.ok}, type=${response.headers.get('content-type')}`);

      if (!response.ok) {
        throw new Error(`Failed to fetch image: ${response.status} ${response.statusText}`);
      }
      const blob = await response.blob();
      console.log(`🖼️ [uriToBlob] Created blob from fetch: ${blob.size} bytes, type: ${blob.type}`);
      return blob;
    } catch (error: any) {
      console.error('🖼️ [uriToBlob] ERROR:', error.message);
      console.error('🖼️ [uriToBlob] Full error:', error);
      throw error;
    }
  }

  // Compress image if needed (optional)
  async compressImage(blob: Blob, maxSizeKB: number = 2000): Promise<Blob> {
    console.log(`🗜️ [compressImage] Input: ${blob.size} bytes (${(blob.size / 1024).toFixed(1)} KB), max: ${maxSizeKB} KB`);

    // If image is already small enough, return as-is
    if (blob.size / 1024 <= maxSizeKB) {
      console.log(`🗜️ [compressImage] Already under limit, skipping compression`);
      return blob;
    }

    // Create canvas for compression
    return new Promise((resolve) => {
      const img = new Image();
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d')!;

      const timeout = setTimeout(() => {
        console.error('🗜️ [compressImage] TIMEOUT: Image failed to load within 10s');
        resolve(blob); // Return original on timeout
      }, 10000);

      img.onload = () => {
        clearTimeout(timeout);
        console.log(`🗜️ [compressImage] Image loaded: ${img.width}x${img.height}`);

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
          console.log(`🗜️ [compressImage] Resized to: ${Math.round(width)}x${Math.round(height)}`);
        }

        canvas.width = width;
        canvas.height = height;
        ctx.drawImage(img, 0, 0, width, height);

        canvas.toBlob((compressedBlob) => {
          if (compressedBlob) {
            console.log(`🗜️ [compressImage] Compressed: ${compressedBlob.size} bytes (${(compressedBlob.size / 1024).toFixed(1)} KB)`);
            resolve(compressedBlob);
          } else {
            console.error('🗜️ [compressImage] canvas.toBlob returned null, using original');
            resolve(blob);
          }
        }, 'image/jpeg', 0.95);
      };

      img.onerror = (e) => {
        clearTimeout(timeout);
        console.error('🗜️ [compressImage] Image load ERROR:', e);
        resolve(blob); // Return original on error
      };

      img.src = URL.createObjectURL(blob);
      console.log(`🗜️ [compressImage] Loading image into canvas...`);
    });
  }
}

export const imageService = new ImageService();
