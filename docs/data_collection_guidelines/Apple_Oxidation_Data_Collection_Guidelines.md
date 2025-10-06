# Apple Oxidation Data Collection Guidelines
## Science Fair 2025 - Team Protocol

**Project:** Apple Oxidation Detection AI Model  
**Date Created:** September 20, 202- **Team Member:** ________________  
- **Apple Collection Date:** ___________ 
**Version:** 1.0

---

## Overview

This document provides standardized procedures for collecting apple oxidation data to train our machine learning model. **Consistency is critical** - all team members must follow these guidelines exactly to ensure our dataset is reliable and our model performs well.

---

## Apple Varieties (Multi-Species Approach)

### Primary Target Varieties
We will collect data from **3 different apple varieties** to improve model robustness:

1. **Red Delicious** 
   - Reason: Most common variety, predictable oxidation pattern
   - Oxidation characteristics: Browns moderately, clear color progression

2. **Granny Smith**
   - Reason: Different baseline color (green), slower oxidation rate
   - Oxidation characteristics: Takes longer to brown, different color changes

3. **Gala**
   - Reason: Fast oxidation rate, good for time-lapse data
   - Oxidation characteristics: Browns quickly, dramatic color changes

### Why Multiple Varieties?
- **Model Robustness:** Handles different apple types in real-world usage
- **Color Variation:** Different baseline colors improve detection accuracy
- **Oxidation Rates:** Various browning speeds provide diverse training data
- **Real-World Application:** Users will photograph different apple types

---

## Equipment Checklist

### Required Items (per collection session)
- [ ] Fresh apples (3 varieties, 2 apples per variety)
- [ ] Sharp knife for consistent cutting
- [ ] Cutting board (white or light colored)
- [ ] Camera/smartphone with good quality
- [ ] Ruler or measuring tape
- [ ] Labels/markers for identification
- [ ] Timer/stopwatch
- [ ] Data collection sheet (see template below)
- [ ] Clean white plate or background
- [ ] Consistent lighting source

---

## Pre-Collection Setup

### Environment Preparation
1. **Location:** Choose a location with consistent lighting (near window with natural light OR consistent artificial lighting)
2. **Background:** Use white or light gray background for all photos
3. **Temperature:** Room temperature (68-72°F / 20-22°C)
4. **Timing:** Plan for 7-day collection period per apple set

### Apple Preparation
1. **Selection:** Choose apples that are:
   - Similar size within each variety
   - No visible bruises or dark spots
   - Firm texture
   - Fresh appearance

---

## Cutting Protocol

### Standardized Cutting Procedure
1. **Slice Thickness:** 0.5 inches (1.3 cm) thick
2. **Cut Direction:** Cut perpendicular to core (showing star pattern)
3. **Slice Position:** Use center slices (avoid end pieces)
4. **Number of Slices:** 3 slices per apple
5. **Core Removal:** Leave core visible in photos (natural reference point)

### Safety Guidelines
- Always cut away from your body
- Use sharp knife for clean cuts
- Adult supervision required for younger team members
- Clean knife between different apple varieties

---

## Photography Protocol

### Camera Settings
- **Resolution:** Minimum 8MP (smartphone quality acceptable)
- **Focus:** Ensure apple slice is in sharp focus
- **Flash:** NO flash - use natural/ambient lighting only
- **Format:** JPEG or PNG (avoid heavily compressed formats)

### Photo Composition
- **Distance:** 12-18 inches from apple slice
- **Angle:** Directly above (90-degree angle) for consistency
- **Background:** White plate or paper, no patterns
- **Framing:** Apple slice fills 60-80% of frame
- **Multiple Shots:** Take 3 photos per slice, use best quality image

### Lighting Requirements
- **Consistency:** Same lighting conditions for entire 7-day period
- **Quality:** Bright enough to see color details clearly
- **Shadows:** Minimize shadows on apple surface
- **Time of Day:** If using natural light, photograph at same time daily (recommend 10 AM - 2 PM)

---

## 🧪 **IMPORTANT: Start with Pilot Study First**

**Before beginning full data collection, complete the 7-day Pilot Study** (see `Apple_Oxidation_Pilot_Study.md`). This will determine:
- Actual oxidation rates for each apple type at room temperature
- Optimal photo timing intervals (every 12 hours? 24 hours? 48 hours?)
- Whether oxidation is sufficient in 2-3 days or if we need 5-7 days
- Which apple varieties show the clearest oxidation progression

---

## Data Collection Schedule
*Note: This timeline should be adjusted based on pilot study results*

### Planned Timeline: Multi-Day Collection Period
- **Day 0:** Fresh cut (baseline photos within 15 minutes)
- **Day 1:** 24 hours after cutting
- **Day 2:** 48 hours after cutting
- **Day 3:** 72 hours after cutting *(may extend based on pilot)*
- **Day 4:** 96 hours after cutting *(if needed)*
- **Day 5:** 120 hours after cutting *(if needed)*
- **Day 6:** 144 hours after cutting *(if needed)*

### Daily Collection Time
- **Consistency:** Same time each day (± 1 hour)
- **Duration:** 15-30 minutes per variety
- **Order:** Photograph in same variety order each day

---

## File Naming Convention

### Standard Format
```
AppleType_Day_SliceNumber_TeamMember_Date
```

### Examples
```
RedDelicious_Day0_Slice1_Sarah_20250920.jpg
GrannySmith_Day3_Slice2_Mike_20250923.jpg
Gala_Day6_Slice1_Alex_20250926.jpg
```

### Folder Structure
```
Apple_Oxidation_Dataset/
├── RedDelicious/
│   ├── Day0/
│   ├── Day1/
│   └── ...
├── GrannySmith/
│   ├── Day0/
│   ├── Day1/
│   └── ...
└── Gala/
    ├── Day0/
    ├── Day1/
    └── ...
```

---

## Data Collection Sheet Template

### Session Information
- **Date Started:** ___________
- **Team Member:** ___________
- **Apple Purchase Date:** ___________
- **Storage Method:** ___________
- **Room Temperature:** ___________

### Daily Tracking (copy for each day)

**Day _____ Date: ___________**

| Apple Variety | Slice 1 | Slice 2 | Slice 3 | Notes |
|---------------|---------|---------|---------|-------|
| Red Delicious | ☐ Photo | ☐ Photo | ☐ Photo | _____ |
| Granny Smith  | ☐ Photo | ☐ Photo | ☐ Photo | _____ |
| Gala          | ☐ Photo | ☐ Photo | ☐ Photo | _____ |

**Observations:**
- Oxidation Level (0-10 scale): _____
- Color Changes Noted: _____
- Texture Changes: _____
- Other Observations: _____

---

## Quality Control Guidelines

### Photo Quality Checklist
- [ ] In focus and sharp
- [ ] Proper lighting (no dark/bright spots)
- [ ] Consistent background
- [ ] Apple slice clearly visible
- [ ] No camera shake or blur
- [ ] Correct file naming

### Data Validation
- [ ] All 3 varieties photographed each day
- [ ] Photos taken at consistent time
- [ ] Data sheet completed
- [ ] Files organized correctly
- [ ] Backup photos taken (recommended)

### Common Mistakes to Avoid
- ❌ Inconsistent lighting between days
- ❌ Different camera angles
- ❌ Varying slice thickness
- ❌ Incorrect file naming
- ❌ Missing days in sequence
- ❌ Using flash photography
- ❌ Poor focus or blurry images

---

## Storage and Handling

### Apple Storage Between Photos
1. **Location:** Refrigerator (consistent temperature)
2. **Container:** Open container or plate (allow air exposure)
3. **Separation:** Keep varieties separate
4. **Labeling:** Clear labels on containers
5. **Daily Removal:** Remove only for photography, return immediately

### Data Backup
1. **Primary Storage:** Organized folders on computer
2. **Backup:** Cloud storage (Google Drive, iCloud, etc.)
3. **File Verification:** Check file integrity daily
4. **Team Sharing:** Upload to shared drive within 24 hours

---

## Team Coordination

### Collection Assignments
**Week 1:** Team Member A - Red Delicious focus  
**Week 2:** Team Member B - Granny Smith focus  
**Week 3:** Team Member C - Gala focus  
**Week 4:** Team Member D - All varieties (validation set)

### Communication Protocol
- **Daily Updates:** Share progress in team chat
- **Problem Reporting:** Immediately report any issues
- **File Sharing:** Upload photos within 24 hours
- **Quality Review:** Weekly team review of collected data

---

## Expected Outcomes

### Target Dataset Size
- **Total Images:** 500+ high-quality photos
- **Per Variety:** ~165 photos each (3 varieties × 7 days × 3 slices × multiple rounds)
- **Collection Rounds:** Minimum 3 complete rounds per variety
- **Quality Control:** 10% buffer for rejected/poor quality images

### Oxidation Progression Documentation
- **Day 0:** Fresh baseline (white/cream color)
- **Days 1-2:** Initial yellowing/slight browning
- **Days 3-4:** Moderate browning, texture changes
- **Days 5-6:** Heavy oxidation, significant color change

---

## Troubleshooting Common Issues

### Lighting Problems
- **Issue:** Photos too dark or inconsistent lighting
- **Solution:** Use consistent artificial lighting or photograph at same time daily

### Focus Issues
- **Issue:** Blurry or out-of-focus photos
- **Solution:** Use camera's macro mode, ensure stable hands

### Color Accuracy
- **Issue:** Colors look different between photos
- **Solution:** Use same camera/phone, consistent lighting, manual camera settings if possible

### Storage Problems
- **Issue:** Apples developing mold or unexpected changes
- **Solution:** Ensure proper air circulation, consistent refrigeration

### File Organization
- **Issue:** Confused file naming or lost photos
- **Solution:** Follow naming convention exactly, create backup immediately

---

## Scientific Considerations

### Variables to Control
- **Apple Variety:** Exact type used
- **Cut Size:** Consistent thickness and surface area
- **Environment:** Same room, temperature, humidity
- **Timing:** Exact timing of photo collection

### Variables to Document
- **Apple Variety:** Exact type used
- **Environmental Factors:** Room temperature, lighting conditions

---

## Safety Reminders

### Knife Safety
- Always cut away from body
- Use cutting board on stable surface
- Adult supervision for team members under 16
- Clean knife between varieties to prevent cross-contamination

### Food Safety
- Wash hands before handling apples
- Use clean cutting surfaces
- Don't consume apples after Day 2
- Dispose of moldy or spoiled apple slices immediately

---

## Contact Information

**Project Lead:** [Name] - [Phone/Email]  
**Data Manager:** [Name] - [Phone/Email]  
**Questions/Issues:** [Team communication channel]

---

## Version History

- **v1.0 (Sept 20, 2025):** Initial guidelines created
- **v1.1 (TBD):** Updates based on first collection round feedback

---

*Remember: Consistency is key to building a successful AI model. When in doubt, document everything and ask for team guidance!*