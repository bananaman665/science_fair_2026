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
2. Take 2 photos: whole apple (front, top)
3. Cut apple in half horizontally
4. Take 4 photos: both cut surfaces (2 angles each)
5. Store cut apple on counter (room temperature for faster oxidation)

**Day 1** (Light Oxidation - 24 hours later):
1. Take 4 photos: both cut surfaces showing browning
2. Leave on counter for continued oxidation

**Day 2** (Heavy Oxidation - 48 hours later):
1. Take 4 photos: both cut surfaces showing heavy browning
2. Dispose of apple

---

### 📸 **Photo Setup Instructions**

#### 🎯 **Camera Setup**
- Use phone camera (portrait mode OFF)
- Good lighting (near window or bright room light)
- White background (paper plate or white paper)
- Hold camera 12 inches away from apple

#### 📏 **Photo Composition**
- Apple should fill about 60% of the photo
- Keep background plain and clean
- Same angle each day for consistency
- Make sure cut surface is clearly visible

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
4. **Multiple angles** - slightly different angles help ML training
5. **Clear focus** - tap screen to focus on apple before taking photo

---

### 🏷️ **Expected Oxidation Progression**
- **Day 0**: Fresh (bright, no browning)
- **Day 1**: Light oxidation (browning around edges)
- **Day 2**: Heavy oxidation (significant browning)

**Room temperature storage accelerates oxidation for faster data collection!**

**This gives you perfect training data for the 3 ML classes in just 3 days!** 🎯