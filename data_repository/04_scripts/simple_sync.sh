#!/bin/bash
# Simple Google Drive Sync Script
# Science Fair 2025 - Apple Oxidation Detection

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_REPO_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$DATA_REPO_DIR")"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}📊 Repository Status:${NC}"
    echo "   Project Root: $PROJECT_ROOT"
    echo "   Data Repository: $DATA_REPO_DIR"
    echo "   Total directories: $(find "$DATA_REPO_DIR" -type d | wc -l | tr -d ' ')"
    echo "   Total files: $(find "$DATA_REPO_DIR" -type f | wc -l | tr -d ' ')"
    echo ""
    
    echo -e "${BLUE}📁 Raw Images Structure:${NC}"
    if [ -d "$DATA_REPO_DIR/01_raw_images" ]; then
        ls -la "$DATA_REPO_DIR/01_raw_images/" | head -10
    else
        echo "   No raw images directory found"
    fi
    echo ""
    
    echo -e "${BLUE}📄 Recent files:${NC}"
    find "$DATA_REPO_DIR" -type f -name "*.jpg" -o -name "*.png" -o -name "*.csv" -o -name "*.txt" | head -5
    echo ""
}

check_dependencies() {
    echo -e "${BLUE}🔍 Checking dependencies...${NC}"
    
    # Check Python
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✅ Python 3 found: $(python3 --version)${NC}"
    else
        echo -e "${RED}❌ Python 3 not found${NC}"
        return 1
    fi
    
    # Check pip packages
    if python3 -c "import googleapiclient" &> /dev/null; then
        echo -e "${GREEN}✅ Google API libraries installed${NC}"
    else
        echo -e "${YELLOW}⚠️  Google API libraries missing${NC}"
        echo "📦 Installing..."
        pip3 install google-api-python-client google-auth google-auth-oauthlib
    fi
    
    echo ""
}

setup_help() {
    echo -e "${BLUE}🔧 Google Drive API Setup Instructions:${NC}"
    echo ""
    echo "1. Go to: https://console.cloud.google.com"
    echo "2. Create a new project or select existing one"
    echo "3. Enable the Google Drive API"
    echo "4. Create OAuth 2.0 credentials (Desktop application)"
    echo "5. Download the credentials file"
    echo "6. Save it as: $SCRIPT_DIR/credentials.json"
    echo ""
    echo "Then run: $0 upload"
    echo ""
}

sync_upload() {
    echo -e "${BLUE}📤 Uploading to Google Drive...${NC}"
    
    if [ ! -f "$SCRIPT_DIR/credentials.json" ]; then
        echo -e "${RED}❌ credentials.json not found${NC}"
        setup_help
        return 1
    fi
    
    cd "$SCRIPT_DIR"
    python3 google_drive_sync.py --upload --repo-path "$DATA_REPO_DIR"
}

sync_download() {
    echo -e "${BLUE}📥 Downloading from Google Drive...${NC}"
    
    if [ ! -f "$SCRIPT_DIR/credentials.json" ]; then
        echo -e "${RED}❌ credentials.json not found${NC}"
        setup_help
        return 1
    fi
    
    cd "$SCRIPT_DIR"
    python3 google_drive_sync.py --download --repo-path "$DATA_REPO_DIR"
}

create_sample() {
    echo -e "${BLUE}📁 Creating sample structure...${NC}"
    
    # Create sample files for testing
    mkdir -p "$DATA_REPO_DIR/01_raw_images/round_1_sample/red_delicious/day_0"
    echo "Sample Red Delicious Day 0 data" > "$DATA_REPO_DIR/01_raw_images/round_1_sample/red_delicious/day_0/sample.txt"
    
    mkdir -p "$DATA_REPO_DIR/03_data_tracking"
    echo "Date,Apple_Type,Day,Notes" > "$DATA_REPO_DIR/03_data_tracking/sample_log.csv"
    echo "2025-09-21,Red Delicious,0,Sample entry" >> "$DATA_REPO_DIR/03_data_tracking/sample_log.csv"
    
    echo -e "${GREEN}✅ Sample structure created${NC}"
}

show_usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  status      Show repository status"
    echo "  check       Check dependencies"
    echo "  setup       Show Google Drive API setup instructions"
    echo "  upload      Upload local files to Google Drive"
    echo "  download    Download files from Google Drive"
    echo "  sample      Create sample folder structure"
    echo ""
}

# Main execution
case "$1" in
    "status")
        print_status
        ;;
    "check")
        check_dependencies
        ;;
    "setup")
        setup_help
        ;;
    "upload"|"sync")
        check_dependencies
        sync_upload
        ;;
    "download"|"pull")
        check_dependencies
        sync_download
        ;;
    "sample")
        create_sample
        ;;
    "")
        echo -e "${BLUE}🍎 Apple Oxidation Data Sync${NC}"
        echo -e "${BLUE}=============================${NC}"
        echo ""
        print_status
        echo ""
        show_usage
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        show_usage
        exit 1
        ;;
esac