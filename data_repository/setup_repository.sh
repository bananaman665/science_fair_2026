#!/bin/bash
# Initialize Data Repository
# Science Fair 2025 - Apple Oxidation Detection

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$SCRIPT_DIR"

echo "🍎 Initializing Apple Oxidation Data Repository"
echo "=============================================="

# Create additional team member folders
echo "📁 Creating team member folders..."
for i in {2..4}; do
    for apple_type in red_delicious granny_smith gala; do
        for day in {0..6}; do
            mkdir -p "$REPO_DIR/01_raw_images/round_${i}_team_member/${apple_type}/day_${day}"
        done
    done
done

# Create sample data tracking files
echo "📊 Creating sample data tracking files..."

# Collection log header
cat > "$REPO_DIR/03_data_tracking/collection_log_template.csv" << EOF
Date,Time,Round,Team_Member,Apple_Type,Day,Slice,File_Name,Oxidation_Score,Quality_Check,Notes
EOF

# Quality control header
cat > "$REPO_DIR/03_data_tracking/quality_control_template.csv" << EOF
File_Name,Date_Reviewed,Reviewer,Quality_Rating,Issues_Found,Action_Taken,Approved,Notes
EOF

# Environment data header
cat > "$REPO_DIR/03_data_tracking/environment_data_template.csv" << EOF
Date,Round,Team_Member,Room_Temperature_F,Lighting_Type,Time_of_Day,Camera_Model,Background_Used,Notes
EOF

# Create README files for each major directory
echo "📄 Creating README files..."

cat > "$REPO_DIR/01_raw_images/README.md" << EOF
# Raw Images Directory

This directory contains all original images collected during data collection rounds.

## Structure:
- round_[X]_team_member/ - Collection rounds by team member
- Each round contains apple variety folders (red_delicious, granny_smith, gala)
- Each variety contains day folders (day_0 through day_6)

## File Naming:
Use format: [AppleType]_D[Day]_S[Slice]_R[Round]_[Member]_[Date]_[Time].jpg
Example: RedDelicious_D0_S1_R1_Sarah_20250921_1030.jpg
EOF

cat > "$REPO_DIR/02_processed_images/README.md" << EOF
# Processed Images Directory

This directory contains curated and processed images ready for model training.

## Structure:
- approved_training_set/ - Images approved for model training
- validation_set/ - Images for model validation during training
- test_set/ - Images for final model testing

## Quality Standards:
- Sharp focus and proper lighting
- Consistent background and positioning
- Proper file naming convention
- Quality control review completed
EOF

cat > "$REPO_DIR/03_data_tracking/README.md" << EOF
# Data Tracking Directory

This directory contains all data collection logs and metadata.

## Files:
- collection_log_*.csv - Master collection logs
- quality_control_*.csv - Quality control reviews
- environment_data_*.csv - Environmental conditions during collection

## Templates:
Use the *_template.csv files as starting points for new data collection rounds.
EOF

cat > "$REPO_DIR/05_archive/README.md" << EOF
# Archive Directory

This directory contains backup and rejected files.

## Structure:
- rejected_images/ - Images that didn't meet quality standards
- old_versions/ - Previous versions of processed datasets

## Purpose:
Maintains backup copies and provides recovery options for data management.
EOF

# Initialize git repository
echo "🔧 Initializing git repository..."
cd "$REPO_DIR"
if [ ! -d ".git" ]; then
    git init
    git add README.md .gitignore */README.md 04_scripts/*.py 04_scripts/*.sh 03_data_tracking/*_template.csv
    git commit -m "Initial repository setup for Apple Oxidation Detection data collection"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Set permissions
echo "🔐 Setting script permissions..."
chmod +x "$REPO_DIR/04_scripts/"*.sh
chmod +x "$REPO_DIR/setup_repository.sh"

# Summary
echo ""
echo "✅ Repository initialization complete!"
echo ""
echo "📁 Directory structure created:"
echo "   - 4 collection rounds with apple variety folders"
echo "   - Processing pipeline directories"
echo "   - Data tracking templates"
echo "   - Archive and backup directories"
echo ""
echo "🔧 Scripts ready:"
echo "   - Google Drive sync: ./04_scripts/sync_manager.sh"
echo "   - Python sync tool: ./04_scripts/google_drive_sync.py"
echo ""
echo "📋 Next steps:"
echo "1. Set up Google Drive API credentials"
echo "2. Run ./04_scripts/sync_manager.sh to configure sync"
echo "3. Begin data collection following the guidelines"
echo "4. Use sync tools to share data with team"
echo ""
echo "🚀 Ready for data collection!"