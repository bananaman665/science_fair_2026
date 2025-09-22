# Google Drive Folder Structure & File Management
## Science Fair 2025 - Cloud Storage Organization

**Purpose:** Centralized, organized storage for all apple oxidation images and data with team collaboration.

---

## Google Drive Folder Structure

### Main Project Folder
```
📁 Apple_Oxidation_Detection_2025/
├── 📁 01_Raw_Images/
│   ├── 📁 Round_1_[TeamMember]/
│   │   ├── 📁 Red_Delicious/
│   │   │   ├── 📁 Day_0/
│   │   │   ├── 📁 Day_1/
│   │   │   ├── 📁 Day_2/
│   │   │   ├── 📁 Day_3/
│   │   │   ├── 📁 Day_4/
│   │   │   ├── 📁 Day_5/
│   │   │   └── 📁 Day_6/
│   │   ├── 📁 Granny_Smith/
│   │   │   └── [same day structure]
│   │   └── 📁 Gala/
│   │       └── [same day structure]
│   ├── 📁 Round_2_[TeamMember]/
│   ├── 📁 Round_3_[TeamMember]/
│   └── 📁 Round_4_[TeamMember]/
├── 📁 02_Processed_Images/
│   ├── 📁 Approved_Training_Set/
│   ├── 📁 Validation_Set/
│   └── 📁 Test_Set/
├── 📁 03_Data_Tracking/
│   ├── 📄 Master_Collection_Log.gsheet
│   ├── 📄 Quality_Control_Review.gsheet
│   └── 📁 Backup_Sheets/
├── 📁 04_Documentation/
│   ├── 📄 Collection_Guidelines.md
│   ├── 📄 Team_Training_Materials.md
│   └── 📄 Troubleshooting_Guide.md
└── 📁 05_Archive/
    ├── 📁 Rejected_Images/
    └── 📁 Old_Versions/
```

---

## File Naming Convention

### Format
```
[AppleType]_D[DayNumber]_S[SliceNumber]_R[RoundNumber]_[TeamMember]_[YYYYMMDD]_[Time].jpg
```

### Examples
```
RedDelicious_D0_S1_R1_Sarah_20250921_1030.jpg
GrannySmith_D3_S2_R2_Mike_20250924_1445.jpg
Gala_D6_S3_R1_Alex_20250927_0915.jpg
```

### Component Breakdown
- **AppleType:** RedDelicious, GrannySmith, Gala
- **DayNumber:** 0, 1, 2, 3, 4, 5, 6
- **SliceNumber:** 1, 2, 3
- **RoundNumber:** 1, 2, 3, 4 (collection round)
- **TeamMember:** FirstName or initials
- **Date:** YYYYMMDD format
- **Time:** HHMM (24-hour format, optional)

---

## Folder Permissions & Access

### Team Roles & Permissions

**Project Lead (Owner):**
- Full access to all folders
- Can manage sharing permissions
- Responsible for folder organization

**Data Manager (Editor):**
- Edit access to all folders
- Manages file organization
- Quality control review authority

**Team Members (Editor):**
- Edit access to assigned round folders
- View access to other rounds
- Can upload and organize their own images

**Advisors (Viewer):**
- View-only access to processed images
- Access to documentation
- No access to raw collection folders

---

## Upload Workflow

### Daily Collection Process

1. **Capture Images** using standardized protocol
2. **Connect to WiFi** for upload
3. **Open Google Drive app** on phone/camera
4. **Navigate to your round folder** (e.g., Round_1_Sarah)
5. **Select apple variety folder** (RedDelicious/GrannySmith/Gala)
6. **Select day folder** (Day_0 through Day_6)
7. **Upload images** with proper naming
8. **Update Google Sheet** with file names and notes
9. **Verify upload** completed successfully

### Batch Upload from Computer

1. **Transfer images** from camera/phone to computer
2. **Rename files** according to convention
3. **Open Google Drive** in browser
4. **Navigate to appropriate folder**
5. **Drag and drop** images
6. **Verify organization** and naming
7. **Update tracking sheet**

---

## Quality Control Process

### Image Review Workflow

1. **Daily Review:** Team member checks their own uploads
2. **Weekly Review:** Data manager reviews all new images
3. **Quality Assessment:** Use standardized criteria
4. **Action Items:** Move rejected images to archive
5. **Documentation:** Update quality control sheet

### Quality Criteria Checklist

**Technical Quality:**
- [ ] Sharp focus and clear details
- [ ] Proper lighting (no over/under exposure)
- [ ] Consistent background
- [ ] Correct file naming
- [ ] Appropriate file size (2-10MB)

**Content Quality:**
- [ ] Apple slice clearly visible
- [ ] Oxidation state appropriate for day
- [ ] No foreign objects in frame
- [ ] Consistent positioning
- [ ] Core pattern visible

---

## Backup & Sync Strategy

### Automatic Sync Settings

**Google Drive Desktop App:**
- Sync main project folder to local computer
- Enable offline access for critical folders
- Set up automatic backup from phone camera roll

**Mobile App Settings:**
- Enable camera upload for designated folder
- Use WiFi-only for large uploads
- Enable notifications for shared folder updates

### Manual Backup Schedule

**Daily:** 
- Verify all images uploaded successfully
- Check Google Sheets are updated
- Confirm file naming consistency

**Weekly:**
- Download complete backup to external drive
- Verify folder organization
- Review and archive old versions

---

## Storage Management

### File Size Guidelines

**Image Quality Settings:**
- High quality JPEG (not RAW)
- Target file size: 2-5MB per image
- Resolution: 8MP minimum, 12MP optimal

**Storage Estimates:**
- Per image: ~3MB average
- Per day (9 images): ~27MB
- Per round (7 days): ~189MB
- Total project (4 rounds): ~756MB

### Storage Optimization

**Google Drive Storage:**
- Monitor storage usage regularly
- Compress older images if needed
- Use Google Photos integration for overflow
- Upgrade storage plan if necessary

---

## Collaboration Features

### Real-time Collaboration

**Folder Comments:**
- Add comments to folders for team communication
- Tag team members for notifications
- Track discussion threads

**File Sharing:**
- Share specific folders with external advisors
- Create shareable links for presentations
- Set expiration dates for temporary access

### Activity Tracking

**Version History:**
- Track all file uploads and changes
- Restore previous versions if needed
- Monitor team member activity

**Notifications:**
- Set up alerts for new uploads
- Email summaries of daily activity
- Mobile push notifications for urgent updates

---

## Mobile Access Optimization

### Google Drive App Setup

**Essential Settings:**
- Enable offline access for guidelines
- Set up automatic camera upload
- Configure data usage limits
- Enable file compression for mobile uploads

**Field Collection Tips:**
- Pre-download folder structure for offline access
- Use airplane mode to prevent interruptions during photography
- Batch upload when on WiFi
- Keep phone charged and have backup power

---

## Security & Privacy

### Access Control

**Team Member Guidelines:**
- Use school/project Google accounts only
- Don't share login credentials
- Log out from shared computers
- Report any unauthorized access

**Data Protection:**
- Regular password updates
- Two-factor authentication enabled
- Shared device logout procedures
- Privacy settings review

---

## Troubleshooting Common Issues

### Upload Problems

**Slow Upload Speeds:**
- Use WiFi instead of cellular data
- Upload during off-peak hours
- Compress images if file size too large
- Check available storage space

**File Organization Issues:**
- Double-check folder navigation before upload
- Use drag-and-drop instead of bulk upload
- Verify file names before uploading
- Create missing folders as needed

### Access Problems

**Permission Denied:**
- Verify team member email addresses
- Check sharing settings with project lead
- Clear browser cache and cookies
- Try incognito/private browsing mode

### Sync Issues

**Files Not Appearing:**
- Refresh browser or restart app
- Check internet connection
- Verify correct folder location
- Wait for sync to complete (may take few minutes)

---

## Setup Instructions

### For Project Lead:

1. **Create main folder** structure in Google Drive
2. **Set up sharing permissions** for team members
3. **Create master Google Sheets** for data tracking
4. **Test upload process** with sample images
5. **Share folder links** with team
6. **Provide training** on folder structure and naming

### For Team Members:

1. **Accept folder sharing invitation**
2. **Install Google Drive** mobile app
3. **Test upload process** with practice images
4. **Bookmark frequently used folders**
5. **Set up mobile notifications**
6. **Practice file naming convention**

---

*This cloud-based system eliminates the need for printed forms and provides real-time collaboration and backup capabilities*