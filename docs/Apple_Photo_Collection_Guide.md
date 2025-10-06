# 📸 Apple Photo Collection Guide
## Simple Daily Data Collection for ML Training

### 🍎 Apple Types to Buy
- **Gala** apples
- **Granny Smith** apples  
- **Red Delicious** apples

### 📋 Daily Photo Collection (7 days per apple)

#### 🔄 **Daily Routine (Same for Each Apple Type)**

**Day 0** (Purchase Day):
1. Take apple out of bag
2. Take 3 photos: whole apple (front, side, top)
3. Cut apple in half horizontally
4. Take 3 photos: both cut surfaces
5. Store cut apple in refrigerator in labeled container

**Days 1-6** (Daily Check):
1. Remove apple from refrigerator
2. Take 3 photos: both cut surfaces
3. Return to refrigerator

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
├── gala/
│   ├── day_0/ (3 photos)
│   ├── day_1/ (2 photos)
│   ├── day_2/ (2 photos)
│   └── ... day_6/
├── granny_smith/
│   └── (same structure)
└── red_delicious/
    └── (same structure)
```

---

### ⚡ **Quick Checklist**
- [ ] Buy 3 apples of each type (9 total apples)
- [ ] Set up photo station with white background
- [ ] Take Day 0 photos immediately after purchase
- [ ] Cut apples in half and refrigerate
- [ ] Take daily photos for 6 more days
- [ ] Upload photos to correct folders

### 🎯 **Goal**
**Total Photos**: 135 photos (15 per apple × 9 apples)
- Day 0: 45 photos (whole + cut apples)
- Days 1-6: 90 photos (cut surfaces only)

### 💡 **Tips for Best Results**
1. **Same time daily** - take photos at same time each day
2. **Same lighting** - use same location/lighting setup
3. **Clean surfaces** - wipe apple surfaces before photos
4. **Multiple angles** - slightly different angles help ML training
5. **Clear focus** - tap screen to focus on apple before taking photo

---

### 🏷️ **Expected Oxidation Progression**
- **Day 0-1**: Fresh (bright, no browning)
- **Day 2-3**: Light oxidation (slight browning edges)
- **Day 4-5**: Medium oxidation (noticeable browning)
- **Day 6+**: Heavy oxidation (significant browning)

**This gives you perfect training data for the 4 ML classes!** 🎯