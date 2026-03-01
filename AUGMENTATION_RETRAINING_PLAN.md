# Augmentation Retraining Plan

## The Problem

Our CNN models predict accurately when given the original digital training images (0.84 day average error), but predict poorly when given phone photos of those same images (~1.2 days predicted for a 6-day-old apple).

This happens because the model has only ever seen clean, controlled images. A phone camera introduces visual differences the model doesn't understand:

- Different brightness and contrast
- Warm or cool color casts from room lighting
- Slight blur from hand movement or autofocus
- Paper/screen texture and reflections
- JPEG compression from the phone
- Slight angle/perspective changes

The model mistakes these camera artifacts for "freshness" because they wash out the brown oxidation tones it learned to detect.

## The Solution: Data Augmentation During Training

We retrain using the **same 312 images** we already have. During training, each image is randomly modified on-the-fly to simulate real-world phone conditions. The model sees thousands of variations and learns to ignore camera artifacts, focusing only on oxidation color.

### Augmentations Applied

| Augmentation | What It Simulates | Range |
|---|---|---|
| Brightness shift | Different room lighting | ±30% |
| Contrast shift | Phone auto-exposure | ±30% |
| Color temperature | Warm/cool light sources | Random R/G/B channel scaling |
| Gaussian blur | Slight hand shake or focus | 0-1.5px radius |
| Gaussian noise | Camera sensor noise | σ = 0-15 |
| JPEG compression | Phone image compression | Quality 50-95% |
| Rotation | Slight tilt when holding phone | ±15 degrees |
| Perspective warp | Angled phone capture | Slight random corners shift |
| Horizontal flip | Different orientations | 50% chance |

Each training image gets a **random combination** of these augmentations every time the model sees it. Over many training epochs, one image produces hundreds of unique variations.

## What Changes in the Training Script

1. Add a `phone_augment(image)` function that applies the augmentations above randomly
2. Integrate it into the data loading pipeline (applied on-the-fly, no extra disk space)
3. Keep the same model architecture (3 Conv2D + Dense layers, 224x224 input)
4. Keep the same train/validation split
5. May increase epochs slightly since the model needs more time to learn from varied inputs

## What Does NOT Change

- No new photos needed
- Same 312 training images from November 2024
- Same 4 models (combined, gala, smith, red_delicious)
- Same model architecture and output (predicted days 0-6.5)
- Same API interface

## Expected Outcome

- Phone photos should predict within ~1-1.5 days of actual (vs ~5 day error currently)
- Original digital images should maintain similar accuracy (~0.84 day avg error)
- Models may become slightly less precise on perfect lab images, but much more robust to real-world conditions

## Validation Plan

1. Retrain all 4 models with augmentation
2. Test on the 8 images in `sf-test-pics/` — confirm accuracy stays close to 0.84 avg error
3. Test on phone photos of printed test images — confirm accuracy improves dramatically
4. If results look good, deploy to Cloud Run

## Timeline

- Modify training script: ~30 minutes
- Retrain 4 models: ~10-30 minutes (depending on hardware)
- Test and validate: ~15 minutes
- Deploy: ~5 minutes
