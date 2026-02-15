# Project Roadmap - Science Fair 2026

**Created:** February 15, 2026
**Last Updated:** February 16, 2026
**Status:** In Progress

## Completed

### 1. Create Google Cloud Project

- [x] Create GCP project (`science-fair-2026`, project #213429152907)
- [x] Enable billing
- [x] Enable required APIs (Cloud Run, Artifact Registry, Cloud Build)
- [x] Set up gcloud CLI locally
- [x] Configure default project and region (`us-central1`)

### 2. Deploy API to Google Cloud Run

- [x] Deploy to Cloud Run with 1Gi memory, 1 CPU, min 0 / max 2 instances
- [x] All 4 models loading and healthy
- [x] Test deployed API endpoints (health check + image analysis confirmed working)
- [x] Add Cloud Run URL to CORS config
- [ ] Update frontend API base URL to point to Cloud Run
- [ ] Set up custom domain (optional)

**Live URL:** https://apple-oxidation-api-213429152907.us-central1.run.app
**Docs:** https://apple-oxidation-api-213429152907.us-central1.run.app/docs

### 3. Firebase Setup (Project Owner Tasks)

All project owner setup steps complete. Frontend team can now proceed.

#### 3a. Create Firebase project

- [x] Firebase project created and attached to GCP project (`science-fair-2026`)

#### 3b. Enable Authentication providers

Firebase console > Authentication > Sign-in method:

- [x] Enable **Google** sign-in
- [ ] Enable **Apple** sign-in (for iOS - can be done later)

#### 3c. Create Firestore database

- [x] Firestore database created in **production mode**, location **us-central1**
- Database ID: `(default)`, type: `FIRESTORE_NATIVE`

#### 3d. Register a web app and get config

- [x] Web app registered (name: `apple-oxidation-web`)
- [x] Firebase config object saved (see below)

**Firebase Config (public/safe to commit):**

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyBXB_2D1LErMx5kBn028U9g_EKG6pqJsoI",
  authDomain: "science-fair-2026.firebaseapp.com",
  projectId: "science-fair-2026",
  storageBucket: "science-fair-2026.firebasestorage.app",
  messagingSenderId: "213429152907",
  appId: "1:213429152907:web:a03343f9dc7f31d35b788e"
};
```

#### 3e. Add frontend team as collaborators

- [x] Teammate added with **Editor** role in Firebase console

#### 3f. Share with frontend team

- [x] Firebase config object (saved in section 3d above)
- [x] Cloud Run API URL: `https://apple-oxidation-api-213429152907.us-central1.run.app`
- [x] Editor access to Firebase console

No service accounts or gcloud credentials needed for frontend work.

## Remaining (Frontend Team)

### 4. Migrate Frontend from Supabase to Firebase

Prerequisites: Firebase setup (section 3) must be complete.

- [ ] Install Firebase SDK: `npm install firebase`
- [ ] Create `frontend/src/lib/firebase.ts` with config from project owner
- [ ] Migrate auth logic (`auth.service.ts`, `authStore.ts`)
- [ ] Replace Supabase auth calls with Firebase Auth (`signInWithPopup`, etc.)
- [ ] Migrate data storage to Firestore (scan history, user data)
- [ ] Update environment variables / config
- [ ] Remove Supabase dependencies: `npm uninstall @supabase/supabase-js`
- [ ] Delete `frontend/src/lib/supabase.ts`
- [ ] Test auth flow end-to-end on web

### 5. Finish Mobile Apps

Prerequisites: Firebase migration (section 4) must be complete.

- [ ] Update API base URL in frontend to point to Cloud Run
- [ ] Configure Firebase SDK for iOS native (download `GoogleService-Info.plist`)
- [ ] Configure Firebase SDK for Android native (download `google-services.json`)
- [ ] Test OAuth flow on iOS (deep links, custom URL scheme)
- [ ] Test OAuth flow on Android
- [ ] Test camera capture + API upload flow on both platforms
- [ ] Handle offline/error states gracefully
- [ ] Replace app icons and splash screens (Capacitor defaults)
- [ ] Build and test release builds
- [ ] Prepare for distribution (TestFlight / internal testing)

## Notes

- Project owner must complete section 3 before frontend team can start
- Frontend team does NOT need gcloud credentials or service accounts
- Frontend team does NOT need to run the backend locally (Cloud Run API is public)
- Cloud Run scales to zero when idle — minimal cost for low traffic
