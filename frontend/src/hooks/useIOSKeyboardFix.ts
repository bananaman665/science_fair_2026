import { useEffect } from 'react';

/**
 * Hook to prevent iOS viewport scrolling when keyboard appears
 * Locks the scroll position when any input focuses and restores it when unfocused
 */
export const useIOSKeyboardFix = () => {
  useEffect(() => {
    // Only run on iOS
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
    if (!isIOS) return;

    // Lock viewport when keyboard shows (on input focus)
    const handleFocusIn = () => {
      const scrollY = window.scrollY;
      document.body.style.position = 'fixed';
      document.body.style.width = '100%';
      document.body.style.top = `-${scrollY}px`;
    };

    // Restore viewport when keyboard hides (on input blur)
    const handleFocusOut = () => {
      const scrollY = parseInt(document.body.style.top || '0') * -1;
      document.body.style.position = '';
      document.body.style.top = '';
      window.scrollTo(0, scrollY);
    };

    window.addEventListener('focusin', handleFocusIn);
    window.addEventListener('focusout', handleFocusOut);

    return () => {
      window.removeEventListener('focusin', handleFocusIn);
      window.removeEventListener('focusout', handleFocusOut);
    };
  }, []);
};
