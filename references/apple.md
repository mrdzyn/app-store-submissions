# Apple App Store Connect

Use for Apple submissions. Inspect the selected platform and version; required fields vary by app, locale, feature set, region, and submission state.

## Field coverage

- App record: name, subtitle, primary language, bundle ID, SKU where applicable, categories, and content rights. Preserve established identifiers; resolve missing identifiers before creating a record.
- Version listing: promotional text, description, keywords, support URL, optional marketing URL, copyright, and What's New for updates. Keep reviewer notes separate from public copy.
- Assets: screenshots and optional previews for applicable devices/locales. For a project-local screenshot workspace and validation, read [assets.md](assets.md). Inspect dimensions, format, alpha channel, and app representation before uploading.
- Review: selected processed build, contact information, sign-in requirement, reviewer access, and steps for reaching gated features. Identify OTP, paywall, location, hardware, or backend dependencies that could prevent review. Use supplied dedicated review access; do not invent credentials.
- Declarations: app privacy, privacy policy, age-rating questionnaire, content rights, export compliance/encryption, and feature/region-specific questions. Assess accessibility claims only for features actually verified.
- Release: pricing, territories, release option, and rollout settings within scope. Check applicable in-app purchases/subscriptions and account prerequisites without silently changing them.

## Apple-specific judgment

Use Apple's definitions for collected data, purposes, linkage to identity, and tracking. Include relevant third-party partner behavior. Do not infer privacy answers solely from permissions or a privacy manifest. Resolve mismatches between the app, SDK configuration, disclosures, and privacy policy before submitting affected declarations.

Check whether the selected metadata can be edited in its current status and whether a new version is required. Do not assume saving a version sends it for review. Inspect the complete review submission and configured release option before the final action.

## Official sources

Open the relevant current page when executing the workflow; follow its links for specific limits and conditional forms.

- [App information](https://developer.apple.com/help/app-store-connect/create-an-app-record/view-and-edit-app-information)
- [Platform version fields](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information)
- [App privacy details](https://developer.apple.com/app-store/app-privacy-details/)
- [App Store Connect Help](https://developer.apple.com/help/app-store-connect/) — screenshot specifications, age rating, encryption, build selection, submission, and release controls.
- [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)

Reverify current requirements per submission.
