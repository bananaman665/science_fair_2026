# Project Roadmap - Science Fair 2026

**Created:** February 15, 2026
**Last Updated:** February 15, 2026
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

## Remaining

### 3. Migrate Frontend from Supabase to Firebase

- [ ] Set up Firebase project (attach to existing GCP project)
- [ ] Configure Firebase Authentication (Google Sign-In, Apple Sign-In)
- [ ] Set up Firestore database (replace Supabase tables)
- [ ] Migrate auth logic (`auth.service.ts`, `authStore.ts`, `supabase.ts`)
- [ ] Migrate data storage (scan history, user data)
- [ ] Update environment variables / config
- [ ] Remove Supabase dependencies from `package.json`
- [ ] Test auth flow end-to-end on web

### 4. Finish Mobile Apps

- [ ] Update Capacitor config for production API URL (Cloud Run)
- [ ] Configure Firebase SDK for iOS and Android native
- [ ] Test OAuth flow on iOS (deep links, custom URL scheme)
- [ ] Test OAuth flow on Android
- [ ] Test camera capture + API upload flow on both platforms
- [ ] Handle offline/error states gracefully
- [ ] App icons and splash screens (replace Capacitor defaults)
- [ ] Build and test release builds
- [ ] Prepare for distribution (TestFlight / internal testing)

## Notes

- Firebase migration can be done in parallel with mobile app work
- Mobile app finalization depends on Firebase migration being done
- Cloud Run scales to zero when idle — minimal cost for low traffic
