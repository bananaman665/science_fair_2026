# 🧪 Combined Pilot Study & Algorithm Development Plan
## Dual-Purpose: Oxidation Testing + Initial ML Training

**Start Date:** October 6, 2025  
**Duration:** 3-4 days (compressed pilot)  
**Goals:** 
1. 📊 Test oxidation rates for schedule planning
2. 🤖 Collect initial photos for algorithm refinement

---

## 🍎 **Materials for Pilot**
- **3 apples** (1 Gala, 1 Granny Smith, 1 Red Delicious)
- Camera/phone with consistent settings
- White background setup
- Labels and markers
- Data collection sheet

---

## 📅 **Intensive 4-Day Pilot Schedule**

### **Day 0 - Fresh Baseline (October 6)**
**Morning (9:00 AM):**
1. **Set up photo station** (consistent lighting/background)
2. **Photograph whole apples** (2 angles each)
3. **Cut apples horizontally** (note exact time)
4. **Photograph cut surfaces immediately** (4 photos per apple)
5. **Label and leave at room temperature**

**Evening (9:00 PM - 12 hours later):**
- Photograph cut surfaces (4 photos per apple)
- Rate oxidation level (0-10 scale)
- Note any visible changes

### **Days 1-3 - Monitoring & Data Collection**
**Every 8 hours** (9 AM, 5 PM, 1 AM if awake):
- Photograph cut surfaces (4 photos per apple)
- Rate oxidation level (0-10 scale)  
- Note color/texture changes
- **Save photos with consistent naming**

### **Day 4 - Final Assessment**
- Final photo session
- Analyze oxidation progression
- **Organize photos for ML training**

---

## 📸 **Photo Collection for ML Training**

### **Naming Convention:**
```
pilot_[apple_type]_[hours_since_cut]_[angle]_[date].jpg

Examples:
pilot_gala_00h_surface1_oct06.jpg
pilot_gala_08h_surface1_oct06.jpg  
pilot_granny_smith_24h_surface2_oct07.jpg
```

### **Photo Organization:**
```
data_repository/
├── 01_raw_images/
    └── pilot_study_oct2025/
        ├── gala/
        │   ├── fresh/ (0-8 hours)
        │   ├── light_oxidation/ (8-24 hours) 
        │   └── medium_oxidation/ (24+ hours)
        ├── granny_smith/
        └── red_delicious/
```

---

## 📊 **Dual Data Collection Sheet**

| Time | Hours Since Cut | Gala Score | Granny Score | Red Del Score | ML Category | Notes |
|------|----------------|------------|---------------|---------------|-------------|--------|
| Oct 6 - 9 AM | 0h | 0 | 0 | 0 | Fresh | Baseline |
| Oct 6 - 9 PM | 12h | ? | ? | ? | Fresh/Light? | |
| Oct 7 - 9 AM | 24h | ? | ? | ? | Light? | |
| Oct 7 - 5 PM | 32h | ? | ? | ? | Light/Med? | |
| Oct 8 - 9 AM | 48h | ? | ? | ? | Medium? | |
| Oct 8 - 5 PM | 56h | ? | ? | ? | Medium/Heavy? | |
| Oct 9 - 9 AM | 72h | ? | ? | ? | Heavy? | Final |

---

## 🤖 **Algorithm Development During Pilot**

### **Phase 1: Initial Model Testing (Day 1-2)**
- **Collect 20-30 pilot photos**
- **Test with current synthetic model**
- **Identify where model fails on real photos**

### **Phase 2: Model Refinement (Day 2-3)**
- **Manual labeling** of pilot photos (fresh/light/medium/heavy)
- **Quick retraining** with mixed synthetic + real data
- **Test improved model accuracy**

### **Phase 3: Schedule Optimization (Day 4)**
- **Analyze oxidation progression**
- **Plan optimal photo timing for main collection**
- **Estimate total photos needed for robust training**

---

## 🎯 **Expected Pilot Outcomes**

### **Oxidation Rate Discovery:**
- **Fast oxidation (good progression in 48h):** Plan 3-day main collection
- **Moderate oxidation (needs 72h+):** Plan 4-5 day main collection  
- **Slow oxidation (minimal change):** Extend to 7-day collection

### **Algorithm Insights:**
- Which apple types work best with current model
- What photo angles/lighting produce best results
- How to improve preprocessing for real apple photos
- Estimated accuracy improvement from pilot data

### **Main Collection Planning:**
- **Optimal photo frequency** (every 8h? 12h? 24h?)
- **Best apple varieties** for consistent results
- **Equipment/setup improvements** needed
- **Total photos needed** for robust training set

---

## 📋 **Pilot Study Checklist**

### **Setup (October 6 morning):**
- [ ] Buy 3 apples (different varieties)
- [ ] Set up consistent photo station  
- [ ] Create data collection sheet
- [ ] Set phone alarms for 8-hour intervals
- [ ] Create pilot photo folders

### **Daily Tasks:**
- [ ] Take photos every 8 hours
- [ ] Rate oxidation consistently
- [ ] Save photos with proper naming
- [ ] Update data collection sheet
- [ ] Note any observations

### **Analysis (October 9):**
- [ ] Review all photos chronologically
- [ ] Test photos with current ML model
- [ ] Plan optimal main collection schedule
- [ ] Document lessons learned

---

## 💡 **Smart Pilot Strategy Benefits**

1. **Risk Reduction:** Test before committing to large collection
2. **Algorithm Improvement:** Real photo training data
3. **Evidence-Based Planning:** Data-driven main collection schedule  
4. **Efficiency:** Only 3 apples vs 9+ for testing
5. **Science Fair Story:** Shows proper experimental methodology

**This compressed pilot gives us the best of both worlds - oxidation data AND algorithm development!** 🚀

---

## 🔄 **Next Steps After Pilot**
1. **Analyze pilot results** (oxidation rates + ML performance)
2. **Plan main collection** (timing, quantity, setup)
3. **Execute optimized data collection** (week 2-3)
4. **Train production model** with full dataset
5. **Science Fair presentation** with complete methodology story