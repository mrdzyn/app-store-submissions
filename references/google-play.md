# Google Play Console

Use for Android submissions. Inspect the app dashboard and publishing overview for the selected package, track, and account; conditional tasks there determine actual readiness.

## Field coverage

- App record: package identity, default language, app/game selection, free/paid status, category/tags, and developer contact details. Resolve new-record choices from the user's business intent; do not alter existing pricing as a convenience.
- Main store listing per locale: app name, short description, full description, and relevant contact/website fields. Google Play has no equivalent to Apple's separate keyword field.
- Assets: app icon, feature graphic, screenshots for applicable form factors, and optional video. For a project-local screenshot workspace and validation, read [assets.md](assets.md). Check current size, format, count, alpha channel, and content rules for each asset and locale.
- App content: privacy policy, ads declaration, app access instructions, content rating, target audience, Data safety, and applicable permissions or category-specific declarations. Include account-deletion details where applicable. Do not equate intended audience with the resulting content rating.
- Release: intended track, supplied build/version code, release name and localized release notes, countries, rollout, and publishing controls. Verify dashboard prerequisites, including applicable testing/production-access and target API requirements; do not hardcode thresholds that may change.

## Google-specific judgment

For Data safety, establish data types, collection, sharing, purposes, optionality, processing, security, and deletion practices using Google's current definitions and exceptions. Include SDK and backend behavior. Do not infer that no ads means no data collection, or that on-device permissions establish transmission off device. Reconcile the declaration's required scope across distributed versions rather than inspecting only a proposed build.

App access instructions should allow reviewers to reach all relevant restricted functionality using actual supplied access. Identify subscription, OTP, region, or organizational-login dependencies explicitly.

Inspect Publishing overview and managed-publishing behavior before sending changes. Saving a listing or release, sending changes for review, approval, and rollout are different states. Verify the resulting state and whether approval triggers publication under existing settings.

## Official sources

- [Create and set up your app](https://support.google.com/googleplay/android-developer/answer/9859152?hl=en) — listing fields and app setup.
- [Data safety form](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en) — disclosure scope and definitions.
- [Play Console Help](https://support.google.com/googleplay/android-developer/?hl=en) — find current preview-asset, app-content, app-access, account-deletion, testing, and publishing guidance.
- [Developer Policy Center](https://play.google.com/about/developer-content-policy/)

Reverify current requirements per submission.
