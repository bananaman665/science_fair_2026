# Data Repository Structure
## Science Fair 2025 - Apple Oxidation Detection

**Purpose:** Local repository for apple oxidation training data with Google Drive synchronization.

---

## Directory Structure

```
data_repository/
├── 01_raw_images/                    # Original collected images
│   ├── round_1_team_member/          # First collection round
│   │   ├── red_delicious/            # Red Delicious variety
│   │   │   ├── day_0/               # Fresh baseline images
│   │   │   ├── day_1/               # 24-hour oxidation
│   │   │   ├── day_2/               # 48-hour oxidation
│   │   │   ├── day_3/               # 72-hour oxidation
│   │   │   ├── day_4/               # 96-hour oxidation
│   │   │   ├── day_5/               # 120-hour oxidation
│   │   │   └── day_6/               # 144-hour oxidation
│   │   ├── granny_smith/            # Granny Smith variety
│   │   │   └── [same day structure]
│   │   └── gala/                    # Gala variety
│   │       └── [same day structure]
│   ├── round_2_team_member/          # Second collection round
│   ├── round_3_team_member/          # Third collection round
│   └── round_4_team_member/          # Fourth collection round
├── 02_processed_images/              # Curated training data
│   ├── approved_training_set/        # Approved images for model training
│   ├── validation_set/               # Images for model validation
│   └── test_set/                     # Images for final model testing
├── 03_data_tracking/                 # Data collection logs and metadata
│   ├── collection_logs.csv           # Master collection log
│   ├── quality_control.csv           # Quality control tracking
│   └── environment_data.csv          # Environmental conditions log
├── 04_scripts/                       # Automation and sync scripts
│   ├── google_drive_sync.py          # Python script for Google Drive sync
│   ├── sync_manager.sh               # Bash wrapper for easy sync management
│   ├── credentials.json              # Google Drive API credentials (not in git)
│   ├── token.json                    # Auth token (not in git)
│   └── sync_log.txt                  # Sync operation log
└── 05_archive/                       # Backup and rejected files
    ├── rejected_images/              # Images that didn't meet quality standards
    └── old_versions/                 # Previous versions of processed data
```

---

## File Naming Convention

### Image Files
```
[AppleType]_D[Day]_S[Slice]_R[Round]_[TeamMember]_[YYYYMMDD]_[HHMM].jpg
```

**Examples:**
- `RedDelicious_D0_S1_R1_Sarah_20250921_1030.jpg`
- `GrannySmith_D3_S2_R2_Mike_20250924_1445.jpg`
- `Gala_D6_S3_R1_Alex_20250927_0915.jpg`

### Data Files
```
[DataType]_[YYYYMMDD]_[Version].csv
```

**Examples:**
- `collection_log_20250921_v1.csv`
- `quality_control_20250924_v2.csv`
- `environment_data_20250921_v1.csv`

---

## Google Drive Synchronization

### Setup Requirements

1. **Google Cloud Console Setup:**
   - Create project at console.cloud.google.com
   - Enable Google Drive API
   - Create OAuth 2.0 credentials
   - Download credentials.json

2. **Local Setup:**
   - Install Python dependencies: `pip install google-api-python-client google-auth google-auth-oauthlib`
   - Place credentials.json in 04_scripts/ directory
   - Run initial authentication

### Sync Commands

**Interactive Menu:**
```bash
./04_scripts/sync_manager.sh
```

**Direct Commands:**
```bash
# Upload local changes to Google Drive
python3 04_scripts/google_drive_sync.py --upload

# Download changes from Google Drive
python3 04_scripts/google_drive_sync.py --download

# Setup API credentials
python3 04_scripts/google_drive_sync.py --setup
```

### Sync Features

- **Bidirectional sync** between local and Google Drive
- **File hash comparison** to avoid unnecessary uploads
- **Incremental updates** (only changed files)
- **Folder structure creation** on first sync
- **Conflict detection** and logging
- **Automatic retry** for failed operations

---

## Usage Workflows

### Data Collection Workflow

1. **Prepare Local Repository:**
   ```bash
   cd data_repository/01_raw_images/round_1_[your_name]
   ```

2. **Collect Images:**
   - Follow data collection guidelines
   - Save images with proper naming convention
   - Update data tracking files

3. **Sync to Cloud:**
   ```bash
   cd ../../04_scripts
   ./sync_manager.sh
   # Choose option 2: Upload to Google Drive
   ```

4. **Team Collaboration:**
   - Team members can download latest data
   - Real-time sharing of progress
   - Centralized backup and version control

### Model Training Workflow

1. **Download Latest Data:**
   ```bash
   ./04_scripts/sync_manager.sh
   # Choose option 3: Download from Google Drive
   ```

2. **Curate Training Set:**
   - Review images in 01_raw_images/
   - Copy approved images to 02_processed_images/approved_training_set/
   - Create validation and test sets

3. **Update and Sync:**
   - Upload processed datasets to share with team
   - Maintain synchronized training data across all team computers

---

## Data Management Best Practices

### Local Repository Management

- **Regular Backups:** Local repository acts as backup for Google Drive
- **Version Control:** Use git for tracking changes to scripts and documentation
- **Storage Management:** Monitor disk space, archive old data as needed
- **Quality Control:** Review images before syncing to shared storage

### Google Drive Management

- **Access Control:** Manage team member permissions appropriately
- **Storage Monitoring:** Monitor Google Drive storage usage
- **Folder Organization:** Maintain consistent folder structure
- **Sync Scheduling:** Regular sync to keep data current

### Security Considerations

- **Credentials Protection:** Never commit credentials.json or token.json to version control
- **Access Logging:** Monitor sync logs for unauthorized access
- **Data Privacy:** Ensure team-only access to sensitive project data
- **Backup Strategy:** Maintain multiple backup copies of critical data

---

## Troubleshooting

### Common Issues

**Sync Failures:**
- Check internet connection
- Verify Google Drive API quotas
- Review credentials and permissions
- Check available storage space

**Authentication Problems:**
- Delete token.json and re-authenticate
- Verify credentials.json is valid
- Check Google Drive API is enabled
- Ensure correct OAuth scopes

**File Organization Issues:**
- Verify file naming convention
- Check folder structure matches expected format
- Review sync logs for errors
- Manually organize misplaced files

### Recovery Procedures

**Lost Local Data:**
1. Use download sync to restore from Google Drive
2. Check 05_archive/ for backup copies
3. Review sync logs for recent changes

**Corrupted Sync:**
1. Clear local token.json
2. Re-authenticate with Google Drive
3. Perform fresh download sync
4. Compare file hashes to verify integrity

---

## Integration with Training Pipeline

### Data Path for AI Model

1. **Raw Images:** 01_raw_images/ → Quality review
2. **Processed Images:** 02_processed_images/ → Model training input
3. **Training Sets:** Organized by approved_training_set/, validation_set/, test_set/
4. **Metadata:** 03_data_tracking/ → Training labels and environmental context

### Automated Workflows

The repository structure is designed to integrate with:
- **Data preprocessing scripts** for model training
- **Automated quality control** pipelines
- **Model training workflows** using TensorFlow/PyTorch
- **Continuous integration** for model updates

---

## Team Collaboration Features

### Real-time Sharing
- Multiple team members can sync simultaneously
- Conflict detection and resolution
- Activity logging and notification

### Role-based Access
- Data collectors: Upload to assigned round folders
- Data managers: Full repository access
- Model developers: Access to processed datasets
- Advisors: Read-only access to final datasets

### Progress Tracking
- Sync logs show team activity
- File timestamps track collection progress
- Automated reports on data collection status

---

*This repository structure provides a professional-grade data management solution for the Apple Oxidation Detection project, enabling seamless collaboration and reliable data synchronization.*