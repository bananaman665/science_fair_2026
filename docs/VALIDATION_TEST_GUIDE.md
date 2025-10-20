# 🧪 Single Apple Validation Test Guide

## Test the Model with Real-Time Daily Photos

### 🎯 **Goal:**
Take photos of a fresh apple over several days and compare the model's predictions to actual time elapsed.

---

## 📅 **Daily Testing Protocol**

### **Day 0 - Fresh Cut (Today)**

1. **Cut the apple:**
   - Cut one fresh apple horizontally in half
   - Note the exact time you cut it

2. **Take photo:**
   - Place on white background
   - Take photo of cut surface (top-down view)
   - Save as `validation_day0.jpg`

3. **Add to test:**
   ```bash
   source backend/.venv/bin/activate
   python test_single_apple.py add validation_day0.jpg 0 gala
   ```
   (Change `gala` to your apple type)

4. **Leave at room temperature**
   - Same conditions as training data
   - Don't refrigerate!

---

### **Day 1 - Next Day**

1. **Take photo (same time as Day 0):**
   - Same apple, same setup
   - Save as `validation_day1.jpg`

2. **Add to test:**
   ```bash
   source backend/.venv/bin/activate
   python test_single_apple.py add validation_day1.jpg 1
   ```

3. **Expected result:**
   - Model should predict ~0.8-1.2 days
   - Error should be <0.5 days for good prediction

---

### **Day 2, 3, 4... Continue Daily**

Repeat the same process each day:
```bash
python test_single_apple.py add validation_day2.jpg 2
python test_single_apple.py add validation_day3.jpg 3
python test_single_apple.py add validation_day4.jpg 4
```

---

## 📊 **View Results**

### **See Summary:**
```bash
python test_single_apple.py summary
```

**Output example:**
```
Date         |  Actual | Predicted |   Error |       Status
--------------------------------------------------------------
2025-10-19   |    0.0d |      0.12d |   0.12d | ✅ Excellent
2025-10-20   |    1.0d |      0.89d |   0.11d | ✅ Excellent
2025-10-21   |    2.0d |      1.78d |   0.22d | ✅ Excellent
2025-10-22   |    3.0d |      2.65d |   0.35d | ✅ Excellent

Mean Absolute Error: 0.20 days (4.8 hours)
```

### **Visualize Results:**
```bash
python test_single_apple.py plot
```

Creates a graph showing actual vs predicted days over time.

---

## 📁 **Photo Storage**

Create a validation folder for your test photos:
```
data_repository/
└── validation_test/
    ├── validation_day0.jpg
    ├── validation_day1.jpg
    ├── validation_day2.jpg
    ├── test_results.json       (auto-generated)
    └── test_results_plot.png   (auto-generated)
```

**Note:** These validation photos are also excluded from git (in .gitignore)

---

## 🎯 **What You're Testing:**

1. **Real-world performance:**
   - Does the model work on NEW apples?
   - Not just the training data

2. **Generalization:**
   - Can it handle different lighting?
   - Different camera angles?
   - Different oxidation patterns?

3. **Accuracy over time:**
   - Is it better at fresh apples or old ones?
   - Where does it struggle?

---

## 📊 **Success Criteria:**

| Error Range | Performance | What It Means |
|-------------|-------------|---------------|
| <0.5 days | ✅ Excellent | Within ~12 hours |
| 0.5-1.0 days | ✅ Good | Within ~24 hours |
| 1.0-1.5 days | ⚠️ Fair | Needs improvement |
| >1.5 days | ❌ Poor | Model needs retraining |

---

## 💡 **Tips for Best Results:**

1. **Consistent timing:**
   - Take photos at same time each day
   - Same lighting conditions if possible

2. **Same setup:**
   - White background
   - Similar camera angle
   - Same distance from apple

3. **Multiple photos:**
   - Take 2-3 photos each day
   - Test all of them
   - See if results are consistent

4. **Document observations:**
   - Note visible oxidation changes
   - Compare to model predictions
   - Great for Science Fair presentation!

---

## 🔬 **Science Fair Presentation:**

This validation test is **perfect** for your presentation:

1. **Show the process:**
   - "We tested the model on a completely new apple"
   - "Photos taken daily over X days"

2. **Show the results:**
   - Display the prediction vs actual graph
   - Highlight accuracy (Mean Absolute Error)

3. **Discuss findings:**
   - "Model predicts within ±0.X days"
   - "Most accurate for [fresh/aged] apples"
   - "Real-world validation confirms training"

---

## 📝 **Quick Reference Commands:**

```bash
# Day 0 - Fresh cut
python test_single_apple.py add photo.jpg 0 gala

# Day 1, 2, 3...
python test_single_apple.py add photo.jpg 1
python test_single_apple.py add photo.jpg 2
python test_single_apple.py add photo.jpg 3

# View results
python test_single_apple.py summary

# Create graph
python test_single_apple.py plot
```

---

**Start your validation test today and track the model's performance over the coming days!** 🍎📊
