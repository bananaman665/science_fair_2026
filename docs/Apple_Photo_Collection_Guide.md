# 📸 Apple Photo Collection Guide
## Simple Daily Data Collection for ML Training

### 🍎 One-Time Apple Purchase
- **3 Gala** apples
- **3 Granny Smith** apples  
- **3 Red Delicious** apples

**Total: 9 apples for complete dataset**

### 📋 Quick Photo Collection (3 days total)

#### 🔄 **Daily Routine (Same for Each Apple Type)**

**Day 0** (Purchase Day - Fresh):
1. Take apple out of bag
2. **Photo 1**: Whole apple front view (camera at apple's eye level)
3. **Photo 2**: Whole apple top view (camera directly above, 90°)
4. Cut apple in half horizontally
5. **Photo 3**: First cut half - surface view (camera 90° perpendicular to cut)
6. **Photo 4**: First cut half - surface view (camera 30-45° angle to cut)
7. **Photo 5**: Second cut half - surface view (camera 90° perpendicular to cut)
8. **Photo 6**: Second cut half - surface view (camera 30-45° angle to cut)
9. Store cut apple on counter (room temperature for faster oxidation)

**Result: 6 photos per apple × 9 apples = 54 photos on Day 0**

**Day 1** (Light Oxidation - 24 hours later):
1. **Photo 1**: First cut half - surface showing browning (camera 90° perpendicular)
2. **Photo 2**: First cut half - surface showing browning (camera 30-45° angle)
3. **Photo 3**: Second cut half - surface showing browning (camera 90° perpendicular)
4. **Photo 4**: Second cut half - surface showing browning (camera 30-45° angle)
5. Leave on counter for continued oxidation

**Result: 4 photos per apple × 9 apples = 36 photos on Day 1**

**Day 2** (Heavy Oxidation - 48 hours later):
1. **Photo 1**: First cut half - heavy browning (camera 90° perpendicular)
2. **Photo 2**: First cut half - heavy browning (camera 30-45° angle)
3. **Photo 3**: Second cut half - heavy browning (camera 90° perpendicular)
4. **Photo 4**: Second cut half - heavy browning (camera 30-45° angle)
5. Dispose of apple

**Result: 4 photos per apple × 9 apples = 36 photos on Day 2**

---

### 📸 **Photo Setup Instructions**

#### 🎯 **Camera Setup**
- Use phone camera (portrait mode OFF)
- Good lighting (near window or bright room light)
- White background (paper plate or white paper)
- Hold camera 12 inches away from apple

#### 📐 **Camera Angle Guide**
**90° Perpendicular Shot:**
- Camera directly above the cut surface
- Phone parallel to the counter/surface
- Looking straight down at the cut surface

**30-45° Angle Shot:**
- Tilt camera 30-45 degrees from perpendicular
- Still 12 inches away from apple
- Captures cut surface with slight depth/dimension
- Shows oxidation patterns more clearly

#### 📏 **Photo Composition & Camera Angles**
- Apple should fill about 60% of the photo
- Keep background plain and clean
- **Straight angle:** Camera directly above cut surface (90° perpendicular)
- **Slight angle:** Camera tilted 30-45° from perpendicular
- 12 inches distance from apple to camera
- Make sure cut surface and oxidation are clearly visible

#### 📁 **File Naming**
Save photos as: `[apple_type]_day[X]_photo[1-3].jpg`

**Examples:**
- `gala_day0_photo1.jpg`
- `granny_smith_day3_photo2.jpg`
- `red_delicious_day6_photo3.jpg`

---

### 🗂️ **Storage Organization**
```
01_raw_images/
├── fresh/ (day_0 photos)
├── light_oxidation/ (day_1 photos) 
├── heavy_oxidation/ (day_2 photos)
└── by_apple_type/
    ├── gala/
    ├── granny_smith/
    └── red_delicious/
```

---

### ⚡ **Quick Checklist**
- [ ] Buy 9 apples total (3 of each type) - ONE TIME PURCHASE
- [ ] Set up photo station with white background
- [ ] Day 0: Take photos and cut all 9 apples
- [ ] Day 1: Photo session (light oxidation)
- [ ] Day 2: Final photo session (heavy oxidation)
- [ ] Upload photos to correct folders

### 🎯 **Goal**
**Total Photos**: 90 photos (10 per apple × 9 apples)
- Day 0 (Fresh): 54 photos (6 per apple)
- Day 1 (Light): 36 photos (4 per apple)  
- Day 2 (Heavy): 36 photos (4 per apple)

### 💡 **Tips for Best Results**
1. **Same time daily** - take photos at same time each day
2. **Same lighting** - use same location/lighting setup
3. **Clean surfaces** - wipe apple surfaces before photos
4. **Consistent angles** - stick to 90° and 30-45° angles exactly
5. **Clear focus** - tap screen to focus on apple before taking photo
6. **Mark your position** - put tape on floor where you stand for consistency
7. **Check angles** - use phone's built-in level/grid if available

---

### 🏷️ **Expected Oxidation Progression**
- **Day 0**: Fresh (bright, no browning)
- **Day 1**: Light oxidation (browning around edges)
- **Day 2**: Heavy oxidation (significant browning)

**Room temperature storage accelerates oxidation for faster data collection!**

**This gives you perfect training data for the 3 ML classes in just 3 days!** 🎯