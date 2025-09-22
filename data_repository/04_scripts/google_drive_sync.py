#!/usr/bin/env python3
"""
Google Drive Sync Script for Apple Oxidation Data Collection
Science Fair 2025

This script syncs the local data repository with Google Drive for team collaboration.
Requires Google Drive API setup and authentication.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
import argparse
import hashlib

# Google Drive API imports (install with: pip install google-api-python-client google-auth)
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("❌ Google Drive API libraries not installed.")
    print("📦 Install with: pip install google-api-python-client google-auth google-auth-oauthlib")
    sys.exit(1)

# Configuration
SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'
DRIVE_FOLDER_NAME = 'Apple_Oxidation_Detection_2025'

class GoogleDriveSync:
    def __init__(self, local_repo_path):
        self.local_repo_path = Path(local_repo_path)
        self.service = None
        self.drive_folder_id = None
        self.sync_log = []
        
    def authenticate(self):
        """Authenticate with Google Drive API"""
        creds = None
        
        # Load existing token
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    print(f"❌ Missing {CREDENTIALS_FILE}")
                    print("📋 Download from Google Cloud Console:")
                    print("   1. Go to console.cloud.google.com")
                    print("   2. Enable Google Drive API")
                    print("   3. Create OAuth 2.0 credentials")
                    print("   4. Download and save as credentials.json")
                    return False
                    
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save credentials for next run
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
                
        self.service = build('drive', 'v3', credentials=creds)
        print("✅ Authenticated with Google Drive")
        return True
        
    def find_or_create_main_folder(self):
        """Find or create the main project folder in Google Drive"""
        # Search for existing folder
        query = f"name='{DRIVE_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder'"
        results = self.service.files().list(q=query).execute()
        items = results.get('files', [])
        
        if items:
            self.drive_folder_id = items[0]['id']
            print(f"📁 Found existing folder: {DRIVE_FOLDER_NAME}")
        else:
            # Create new folder
            folder_metadata = {
                'name': DRIVE_FOLDER_NAME,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.service.files().create(body=folder_metadata).execute()
            self.drive_folder_id = folder.get('id')
            print(f"📁 Created new folder: {DRIVE_FOLDER_NAME}")
            
        return self.drive_folder_id
        
    def create_folder_structure(self, parent_id, local_path):
        """Recursively create folder structure in Google Drive"""
        folders_created = []
        
        for item in local_path.iterdir():
            if item.is_dir():
                # Check if folder exists
                query = f"name='{item.name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder'"
                results = self.service.files().list(q=query).execute()
                existing = results.get('files', [])
                
                if existing:
                    folder_id = existing[0]['id']
                    print(f"📂 Found: {item.name}")
                else:
                    # Create folder
                    folder_metadata = {
                        'name': item.name,
                        'parents': [parent_id],
                        'mimeType': 'application/vnd.google-apps.folder'
                    }
                    folder = self.service.files().create(body=folder_metadata).execute()
                    folder_id = folder.get('id')
                    folders_created.append(item.name)
                    print(f"📂 Created: {item.name}")
                    
                # Recursively create subfolders
                sub_folders = self.create_folder_structure(folder_id, item)
                folders_created.extend(sub_folders)
                
        return folders_created
        
    def get_file_hash(self, file_path):
        """Calculate MD5 hash of file for comparison"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
        
    def find_drive_folder_id(self, folder_name, parent_id):
        """Find folder ID in Google Drive"""
        query = f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder'"
        results = self.service.files().list(q=query).execute()
        items = results.get('files', [])
        return items[0]['id'] if items else None
        
    def upload_file(self, local_file_path, drive_folder_id):
        """Upload a file to Google Drive"""
        file_name = local_file_path.name
        
        # Check if file already exists
        query = f"name='{file_name}' and '{drive_folder_id}' in parents"
        results = self.service.files().list(q=query).execute()
        existing_files = results.get('files', [])
        
        # Calculate local file hash
        local_hash = self.get_file_hash(local_file_path)
        
        if existing_files:
            # File exists, check if update needed
            existing_file = existing_files[0]
            existing_hash = existing_file.get('md5Checksum', '')
            
            if local_hash != existing_hash:
                # Update existing file
                media = MediaFileUpload(str(local_file_path))
                updated_file = self.service.files().update(
                    fileId=existing_file['id'],
                    media_body=media
                ).execute()
                print(f"🔄 Updated: {file_name}")
                self.sync_log.append(f"Updated: {file_name}")
                return updated_file.get('id')
            else:
                print(f"✅ Unchanged: {file_name}")
                return existing_file['id']
        else:
            # Upload new file
            file_metadata = {
                'name': file_name,
                'parents': [drive_folder_id]
            }
            media = MediaFileUpload(str(local_file_path))
            uploaded_file = self.service.files().create(
                body=file_metadata,
                media_body=media
            ).execute()
            print(f"📤 Uploaded: {file_name}")
            self.sync_log.append(f"Uploaded: {file_name}")
            return uploaded_file.get('id')
            
    def sync_directory(self, local_dir, drive_parent_id):
        """Sync a directory recursively"""
        for item in local_dir.iterdir():
            if item.is_file():
                # Upload file
                self.upload_file(item, drive_parent_id)
            elif item.is_dir():
                # Find or create subfolder
                subfolder_id = self.find_drive_folder_id(item.name, drive_parent_id)
                if subfolder_id:
                    # Recursively sync subfolder
                    self.sync_directory(item, subfolder_id)
                    
    def sync_repository(self):
        """Sync entire local repository to Google Drive"""
        print(f"🚀 Starting sync: {self.local_repo_path}")
        start_time = time.time()
        
        # Authenticate
        if not self.authenticate():
            return False
            
        # Find or create main folder
        main_folder_id = self.find_or_create_main_folder()
        if not main_folder_id:
            print("❌ Failed to create main folder")
            return False
            
        # Create folder structure
        print("📁 Creating folder structure...")
        folders_created = self.create_folder_structure(main_folder_id, self.local_repo_path)
        
        # Sync files
        print("📤 Syncing files...")
        self.sync_directory(self.local_repo_path, main_folder_id)
        
        # Summary
        elapsed = time.time() - start_time
        print(f"\n✅ Sync completed in {elapsed:.1f} seconds")
        print(f"📂 Folders created: {len(folders_created)}")
        print(f"📄 Files processed: {len(self.sync_log)}")
        
        # Save sync log
        log_file = self.local_repo_path / '04_scripts' / 'sync_log.txt'
        with open(log_file, 'w') as f:
            f.write(f"Sync completed: {datetime.now()}\n")
            f.write(f"Duration: {elapsed:.1f} seconds\n")
            f.write(f"Files processed: {len(self.sync_log)}\n\n")
            for entry in self.sync_log:
                f.write(f"{entry}\n")
                
        return True
        
    def download_from_drive(self, drive_folder_id, local_path):
        """Download files from Google Drive to local repository"""
        # Get files in drive folder
        query = f"'{drive_folder_id}' in parents"
        results = self.service.files().list(q=query).execute()
        items = results.get('files', [])
        
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                # Create local folder
                local_subfolder = local_path / item['name']
                local_subfolder.mkdir(exist_ok=True)
                
                # Recursively download subfolder
                self.download_from_drive(item['id'], local_subfolder)
            else:
                # Download file
                local_file = local_path / item['name']
                
                # Check if local file exists and is different
                if local_file.exists():
                    local_hash = self.get_file_hash(local_file)
                    drive_hash = item.get('md5Checksum', '')
                    if local_hash == drive_hash:
                        print(f"✅ Unchanged: {item['name']}")
                        continue
                        
                # Download file
                request = self.service.files().get_media(fileId=item['id'])
                with open(local_file, 'wb') as f:
                    downloader = MediaIoBaseDownload(f, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        
                print(f"📥 Downloaded: {item['name']}")

def main():
    parser = argparse.ArgumentParser(description='Sync Apple Oxidation data with Google Drive')
    parser.add_argument('--upload', action='store_true', help='Upload local files to Google Drive')
    parser.add_argument('--download', action='store_true', help='Download files from Google Drive')
    parser.add_argument('--setup', action='store_true', help='Setup Google Drive API credentials')
    parser.add_argument('--repo-path', default='.', help='Path to local repository')
    
    args = parser.parse_args()
    
    # Default to upload if no action specified
    if not any([args.upload, args.download, args.setup]):
        args.upload = True
        
    repo_path = Path(args.repo_path).resolve()
    
    if args.setup:
        print("🔧 Google Drive API Setup Instructions:")
        print("1. Go to console.cloud.google.com")
        print("2. Create new project or select existing")
        print("3. Enable Google Drive API")
        print("4. Create OAuth 2.0 credentials")
        print("5. Download credentials.json to this directory")
        print("6. Run script again to authenticate")
        return
        
    if not repo_path.exists():
        print(f"❌ Repository path not found: {repo_path}")
        return
        
    sync = GoogleDriveSync(repo_path)
    
    if args.upload:
        print("📤 Uploading to Google Drive...")
        sync.sync_repository()
    elif args.download:
        print("📥 Downloading from Google Drive...")
        if sync.authenticate() and sync.find_or_create_main_folder():
            sync.download_from_drive(sync.drive_folder_id, repo_path)
        
if __name__ == "__main__":
    main()