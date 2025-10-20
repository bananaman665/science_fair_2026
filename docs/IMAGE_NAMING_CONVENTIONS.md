# 📝 Image Naming Conventions Documentation

## Science Fair 2026 - Apple Oxidation Detection Project

This document describes all image naming conventions used throughout the project for data organization and ML training.

---

## 🔄 **Evolution of Naming Conventions**

### **Phase 1: Raw Collection (ImageSet Directory)**

**Original naming format from data collection:**
```
[date]-[am|pm]-[gala|smith]-[fruit-index]-[angle-index].JPG
```

**Example:**
```
20251005-pm-gala-1-1.JPG
```

**Field Breakdown:**
- `date`: YYYYMMDD format (e.g., 20251005 = October 5, 2025)
- `am|pm`: Time of day (morning or evening session)
- `gala|smith`: Apple type (gala = Gala, smith = Granny Smith)
- `fruit-index`: Individual fruit number (1 or 2)
- `angle-index`: Camera angle
  - `1` = Top-down (90° perpendicular view)
  - `2` = Angled (45° angle for depth)

**Collection Details:**
- **Period:** October 5-10, 2025 (6 days)
- **Sessions:** 2 per day (AM ~9:00, PM ~18:00)
- **Fruits:** 2 Gala, 2 Granny Smith
- **Total Photos:** 88 images

---

### **Phase 2: Organized Structure (01_raw_images/first_collection_oct2025/)**

**Organized naming format:**
```
[apple_type]_fruit[N]_day[N]_[hours]h_[angle_desc]_[date]-[time].JPG
```

**Example:**
```
gala_fruit1_day2_048h_top_down_20251007-pm.JPG
granny_smith_fruit2_day3_087h_angled_45_20251009-am.JPG
```

**Field Breakdown:**
- `apple_type`: Full apple variety name
  - `gala` = Gala apple
  - `granny_smith` = Granny Smith apple
- `fruitN`: Individual fruit instance (fruit1, fruit2)
- `dayN`: Day number since baseline (day0, day1, day2, etc.)
- `hours`: Hours since baseline cut (000h, 015h, 024h, etc.)
- `angle_desc`: Descriptive angle name
  - `top_down` = 90° perpendicular view
  - `angled_45` = 45° angled view
- `date-time`: Original capture date and session (YYYYMMDD-am/pm)

**Baseline Reference:**
- **Day 0, Hour 0:** October 5, 2025 at 18:00 (6:00 PM)
- All hours calculated from this baseline

**Time Mapping Examples:**
```
000h = Oct 5, 6:00 PM  (Day 0 PM - baseline)
015h = Oct 6, 9:00 AM  (Day 0 AM - next morning)
024h = Oct 6, 6:00 PM  (Day 1 PM - 24 hours)
048h = Oct 7, 6:00 PM  (Day 2 PM - 48 hours)
072h = Oct 8, 6:00 PM  (Day 3 PM - 72 hours)
120h = Oct 10, 6:00 PM (Day 5 PM - 120 hours)
```

---

## 📁 **Directory Structure**

### **Original Collection (Not in Git):**
```
data_repository/ImageSet/
├── 20251005-pm-gala-1-1.JPG
├── 20251005-pm-gala-1-2.JPG
├── 20251005-pm-smith-1-1.JPG
└── ... (88 total files)
```

### **Organized Collection (Not in Git):**
```
data_repository/01_raw_images/first_collection_oct2025/
├── COLLECTION_METADATA.md
├── gala/
│   ├── fruit_1/
│   │   ├── day_0/
│   │   │   ├── gala_fruit1_day0_000h_top_down_20251005-pm.JPG
│   │   │   ├── gala_fruit1_day0_000h_angled_45_20251005-pm.JPG
│   │   │   ├── gala_fruit1_day0_015h_top_down_20251006-am.JPG
│   │   │   └── gala_fruit1_day0_015h_angled_45_20251006-am.JPG
│   │   ├── day_1/
│   │   ├── day_2/
│   │   └── ... (through day_5)
│   └── fruit_2/
│       └── ... (same structure)
└── granny_smith/
    ├── fruit_1/
    └── fruit_2/
```

---

## 🎯 **ML Training Labels**

### **Regression Model Approach:**

The model predicts **continuous days** from the image, extracted from the `hours` field:

```python
hours = int(filename.split('_')[3].replace('h', ''))  # For gala
days = hours / 24.0  # Convert to continuous days

# Examples:
000h → 0.00 days (fresh)
024h → 1.00 days (light oxidation)
048h → 2.00 days (medium oxidation)
072h → 3.00 days (medium-heavy oxidation)
120h → 5.00 days (heavy oxidation)
```

**No manual labeling required** - days are automatically calculated from filename!

---

## 🔧 **Processing Scripts**

### **1. organize_images.py**
- **Input:** `ImageSet/` with original naming
- **Output:** `01_raw_images/first_collection_oct2025/` with organized naming
- **Function:** Converts Phase 1 → Phase 2 naming

### **2. train_regression_model.py**
- **Input:** Organized images from `first_collection_oct2025/`
- **Extracts:** Days from filename (hours / 24)
- **Trains:** CNN regression model to predict days

### **3. apple_api_regression.py**
- **Input:** User-uploaded apple photo
- **Output:** Predicted days since cut (e.g., "2.34 days old")

---

## 📊 **Data Summary**

| Metric | Value |
|--------|-------|
| Total Photos | 88 |
| Apple Varieties | 2 (Gala, Granny Smith) |
| Fruits per Variety | 2 |
| Collection Period | 6 days (Oct 5-10, 2025) |
| Sessions per Day | 2 (AM/PM) |
| Angles per Session | 2 (top-down, 45°) |
| Time Points | 11 unique timestamps |
| Days Range | 0.00 - 5.00 days |

---

## 🚫 **Git Exclusions**

All image files are excluded from git via `.gitignore`:

```gitignore
# Exclude all image files
**/*.jpg
**/*.JPG
**/*.jpeg
**/*.JPEG
**/*.png

# Exclude image directories
ImageSet/
01_raw_images/first_collection_*/
01_raw_images/pilot_study_*/
02_processed_images/labeled_training_set/

# Exclude trained models
backend/*.h5
backend/*.pkl
```

**Why excluded:**
- Large binary files (88 images × ~2-5 MB each = ~300 MB+)
- Not suitable for version control
- Can be regenerated from raw data
- Models can be retrained

**What IS included:**
- All scripts (`*.py`, `*.sh`)
- Documentation (`*.md`)
- Metadata files (`COLLECTION_METADATA.md`)
- Configuration files
- Folder structure markers (`.gitkeep`, `README.md`)

---

## 💡 **Best Practices**

1. **Always use organized naming** (Phase 2) for ML training
2. **Keep ImageSet/ as backup** until confirmed organized correctly
3. **Document any new naming conventions** in this file
4. **Use hours in filename** for automatic day calculation
5. **Maintain consistent angle naming** (top_down, angled_45)

---

## 📝 **Notes**

- Original `ImageSet/` directory contains unorganized source images
- Can be safely deleted after verification of organized images
- Organized images are in `first_collection_oct2025/`
- All future collections should follow Phase 2 naming convention
