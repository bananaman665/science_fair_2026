# Google Sheets Data Collection Template
## Science Fair 2025 - Digital Data Tracking

**Setup Instructions:** Copy the table below into a new Google Sheet for real-time data collection.

---

## Google Sheets Setup

### Sheet 1: "Collection Overview"

| Collection Round | Team Member | Start Date | End Date | Total Images | Status | Notes |
|------------------|-------------|------------|----------|--------------|--------|-------|
| Round 1 | | | | | In Progress | |
| Round 2 | | | | | Not Started | |
| Round 3 | | | | | Not Started | |
| Round 4 | | | | | Not Started | |

### Sheet 2: "Daily Collection Log"

| Date | Day # | Team Member | Apple Variety | Slice # | File Name | Oxidation Score (0-10) | Quality Check | Notes |
|------|-------|-------------|---------------|---------|-----------|------------------------|---------------|-------|
| | Day 0 | | Red Delicious | 1 | | 0 | ✓ Pass | Fresh baseline |
| | Day 0 | | Red Delicious | 2 | | 0 | ✓ Pass | |
| | Day 0 | | Red Delicious | 3 | | 0 | ✓ Pass | |
| | Day 0 | | Granny Smith | 1 | | 0 | ✓ Pass | |
| | Day 0 | | Granny Smith | 2 | | 0 | ✓ Pass | |
| | Day 0 | | Granny Smith | 3 | | 0 | ✓ Pass | |
| | Day 0 | | Gala | 1 | | 0 | ✓ Pass | |
| | Day 0 | | Gala | 2 | | 0 | ✓ Pass | |
| | Day 0 | | Gala | 3 | | 0 | ✓ Pass | |
| | Day 1 | | Red Delicious | 1 | | | | |
| | Day 1 | | Red Delicious | 2 | | | | |
| | Day 1 | | Red Delicious | 3 | | | | |
| | Day 1 | | Granny Smith | 1 | | | | |
| | Day 1 | | Granny Smith | 2 | | | | |
| | Day 1 | | Granny Smith | 3 | | | | |
| | Day 1 | | Gala | 1 | | | | |
| | Day 1 | | Gala | 2 | | | | |
| | Day 1 | | Gala | 3 | | | | |

*Continue this pattern for Days 2-6*

### Sheet 3: "Environmental Conditions"

| Collection Round | Team Member | Room Temperature (°F) | Lighting Type | Time of Day | Camera/Phone Model | Background Used | Notes |
|------------------|-------------|----------------------|---------------|-------------|-------------------|-----------------|-------|
| Round 1 | | | Natural/Artificial | | | White plate | |
| Round 2 | | | | | | | |
| Round 3 | | | | | | | |
| Round 4 | | | | | | | |

### Sheet 4: "Quality Control"

| File Name | Date Taken | Quality Rating | Issues Found | Action Taken | Approved By | Notes |
|-----------|------------|----------------|--------------|--------------|-------------|-------|
| | | Excellent/Good/Poor | None/Blur/Lighting/Other | Keep/Retake/Reject | | |
| | | | | | | |
| | | | | | | |

---

## Google Sheets Formulas (Optional Enhancements)

### Auto-generate File Names (Column I in Daily Log):
```
=CONCATENATE(E2,"_Day",B2,"_Slice",F2,"_",C2,"_",TEXT(A2,"YYYYMMDD"))
```

### Count Total Images per Variety:
```
=COUNTIF(E:E,"Red Delicious")
=COUNTIF(E:E,"Granny Smith") 
=COUNTIF(E:E,"Gala")
```

### Calculate Average Oxidation Score:
```
=AVERAGE(G:G)
```

### Progress Tracking:
```
=COUNTIF(H:H,"✓ Pass")/COUNTA(H:H)*100&"%"
```

---

## Data Validation Setup

### Drop-down Lists (Data > Data Validation):

**Apple Variety Column:**
- Red Delicious
- Granny Smith
- Gala

**Quality Check Column:**
- ✓ Pass
- ⚠ Needs Review
- ✗ Reject

**Day Number Column:**
- Day 0
- Day 1
- Day 2
- Day 3
- Day 4
- Day 5
- Day 6

**Quality Rating Column:**
- Excellent
- Good
- Poor

---

## Conditional Formatting Rules

### Oxidation Score Color Coding:
- **0-2:** Green (Fresh)
- **3-5:** Yellow (Light oxidation)
- **6-8:** Orange (Medium oxidation)  
- **9-10:** Red (Heavy oxidation)

### Quality Check Status:
- **✓ Pass:** Green background
- **⚠ Needs Review:** Yellow background
- **✗ Reject:** Red background

---

## Sharing and Collaboration Settings

### Recommended Share Settings:
- **Team Members:** Editor access
- **Project Lead:** Owner
- **Advisors:** Viewer access

### Real-time Collaboration Features:
- Comments for questions/issues
- Revision history for tracking changes
- Automatic save (no data loss)
- Mobile access for field collection

---

## Copy-Paste Instructions

1. **Create New Google Sheet**
2. **Copy tables above** into separate sheets
3. **Set up data validation** for consistency
4. **Apply conditional formatting** for visual feedback
5. **Share with team** with appropriate permissions
6. **Test on mobile** for field use compatibility

---

*This template replaces the need for printed data sheets and provides real-time collaboration capabilities*