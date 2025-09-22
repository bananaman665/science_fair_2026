#!/bin/bash
# Google Drive Sync Wrapper Script
# Science Fair 2025 - Apple Oxidation Detection

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}🍎 Apple Oxidation Data Sync${NC}"
    echo -e "${BLUE}=============================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_dependencies() {
    echo "🔍 Checking dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found. Please install Python 3."
        exit 1
    fi
    
    # Check pip packages
    python3 -c "import googleapiclient, google.auth" 2>/dev/null
    if [ $? -ne 0 ]; then
        print_warning "Google Drive API libraries not installed."
        echo "📦 Installing required packages..."
        pip3 install google-api-python-client google-auth google-auth-oauthlib
        if [ $? -ne 0 ]; then
            print_error "Failed to install required packages."
            exit 1
        fi
    fi
    
    print_success "Dependencies checked"
}

setup_credentials() {
    echo "🔧 Setting up Google Drive API credentials..."
    
    if [ ! -f "$SCRIPT_DIR/credentials.json" ]; then
        print_warning "credentials.json not found"
        echo ""
        echo "📋 To set up Google Drive API:"
        echo "1. Go to console.cloud.google.com"
        echo "2. Create a new project or select existing"
        echo "3. Enable Google Drive API"
        echo "4. Create OAuth 2.0 credentials (Desktop application)"
        echo "5. Download the credentials file"
        echo "6. Save it as: $SCRIPT_DIR/credentials.json"
        echo ""
        read -p "Press Enter when credentials.json is ready..."
    fi
    
    if [ -f "$SCRIPT_DIR/credentials.json" ]; then
        print_success "Credentials file found"
    else
        print_error "Credentials file still missing"
        exit 1
    fi
}

sync_to_drive() {
    echo "📤 Syncing local repository to Google Drive..."
    cd "$SCRIPT_DIR"
    python3 google_drive_sync.py --upload --repo-path "$REPO_DIR"
}

sync_from_drive() {
    echo "📥 Syncing from Google Drive to local repository..."
    cd "$SCRIPT_DIR"
    python3 google_drive_sync.py --download --repo-path "$REPO_DIR"
}

show_status() {
    echo "📊 Repository Status:"
    echo "   Local Path: $REPO_DIR"
    echo "   Total Files: $(find "$REPO_DIR" -type f | wc -l)"
    echo "   Total Folders: $(find "$REPO_DIR" -type d | wc -l)"
    echo ""
    
    # Show recent files
    echo "📁 Recent files (last 10):"
    find "$REPO_DIR" -type f -name "*.jpg" -o -name "*.png" -o -name "*.jpeg" | \
        head -10 | sed 's|'"$REPO_DIR"'/||'
        
    if [ $(find "$REPO_DIR" -type f -name "*.jpg" -o -name "*.png" -o -name "*.jpeg" | wc -l) -gt 10 ]; then
        echo "   ... and more"
    fi
}

create_sample_structure() {
    echo "📁 Creating sample folder structure..."
    
    # Create sample folders for demonstration
    mkdir -p "$REPO_DIR/01_raw_images/round_1_sample/red_delicious/day_0"
    mkdir -p "$REPO_DIR/01_raw_images/round_1_sample/red_delicious/day_1"
    mkdir -p "$REPO_DIR/01_raw_images/round_1_sample/granny_smith/day_0"
    mkdir -p "$REPO_DIR/01_raw_images/round_1_sample/gala/day_0"
    
    # Create sample README files
    echo "Red Delicious apple images for Round 1" > "$REPO_DIR/01_raw_images/round_1_sample/red_delicious/README.txt"
    echo "Granny Smith apple images for Round 1" > "$REPO_DIR/01_raw_images/round_1_sample/granny_smith/README.txt"
    echo "Gala apple images for Round 1" > "$REPO_DIR/01_raw_images/round_1_sample/gala/README.txt"
    
    # Create data tracking examples
    echo "Collection Date,Apple Type,Day,Slice,File Name,Oxidation Score,Notes" > "$REPO_DIR/03_data_tracking/sample_collection_log.csv"
    echo "2025-09-21,Red Delicious,0,1,RedDelicious_D0_S1_R1_Sample_20250921.jpg,0,Fresh baseline" >> "$REPO_DIR/03_data_tracking/sample_collection_log.csv"
    
    print_success "Sample structure created"
}

# Main menu
show_menu() {
    echo ""
    echo "Choose an option:"
    echo "1) Setup Google Drive API credentials"
    echo "2) Upload to Google Drive (sync local → cloud)"
    echo "3) Download from Google Drive (sync cloud → local)"
    echo "4) Show repository status"
    echo "5) Create sample folder structure"
    echo "6) Check dependencies"
    echo "7) Exit"
    echo ""
    echo -n "Enter choice [1-7]: "
}

# Main script
main() {
    print_header
    
    # Check if we're in the right directory
    if [ ! -d "$REPO_DIR/01_raw_images" ]; then
        print_error "Not in data repository directory"
        exit 1
    fi
    
    # If arguments provided, run non-interactive mode
    if [ $# -gt 0 ]; then
        case $1 in
            "setup"|"1")
                setup_credentials
                ;;
            "upload"|"sync"|"2")
                check_dependencies
                setup_credentials
                sync_to_drive
                ;;
            "download"|"pull"|"3")
                check_dependencies
                setup_credentials
                sync_from_drive
                ;;
            "status"|"4")
                show_status
                ;;
            "sample"|"5")
                create_sample_structure
                ;;
            "deps"|"check"|"6")
                check_dependencies
                ;;
            *)
                echo "Usage: $0 [setup|upload|download|status|sample|check]"
                exit 1
                ;;
        esac
        exit 0
    fi
    
    # Interactive mode
    while true; do
        show_menu
        read -r choice
        
        case $choice in
            1)
                setup_credentials
                ;;
            2)
                check_dependencies
                setup_credentials
                sync_to_drive
                ;;
            3)
                check_dependencies
                setup_credentials
                sync_from_drive
                ;;
            4)
                show_status
                ;;
            5)
                create_sample_structure
                ;;
            6)
                check_dependencies
                ;;
            7)
                echo "👋 Goodbye!"
                exit 0
                ;;
            "")
                print_warning "Please enter a number (1-7)"
                ;;
            *)
                print_error "Invalid option: $choice"
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..." -r
    done
}

# Run main function if script is executed directly
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi