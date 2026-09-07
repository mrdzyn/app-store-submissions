---
name: app-store-submissions
description: Audit an app project folder and prepare, check, or fill Apple App Store Connect and Google Play Console submissions, including store assets, screenshot checklists, review instructions, privacy questionnaires, and release metadata. Use for repository-based submission readiness checks, new apps, version updates, incomplete store forms, or rejection-related metadata fixes.
---

# App Store Submissions

Turn app evidence into accurate, ready-to-paste store fields and compliant submission assets, then enter them in the correct store record when requested. Support either store independently or both together. Preparing a submission does not itself include building the app or publishing a release.

## Establish scope and evidence

Identify the app, requested stores, new listing versus update, locales, version/build, and intended outcome: draft copy, fill/save forms, submit for review, or release. Infer these from supplied materials and the existing console when possible. Ask only for missing facts that affect the requested work; continue drafting independent fields while awaiting answers.

Inspect the app brief, website, existing listing, supplied assets, release notes, and relevant repository files when available. Record a compact app fact sheet: audience, implemented features, monetization, account/login behavior, support/privacy URLs, SDKs and data handling, platform identifiers, and release scope. Distinguish user-confirmed facts, observed evidence, proposed wording, and unresolved questions. Website marketing alone does not establish what the submitted build implements.

Keep app facts in the task's output, never in this reusable skill. Do not copy credentials or personal data into the skill or public listing copy.

## Audit a pointed project folder

When the user points to a project folder, treat the folder as the primary evidence source and read [references/project-audit.md](references/project-audit.md). Audit it before drafting declarations or claiming submission readiness. Include relevant documentation and Markdown files; do not limit the review to source code.

Start from the supplied folder, respect repository instructions such as `AGENTS.md`, and avoid scanning unrelated parent or sibling directories. Use fast file discovery and targeted searches. Exclude generated output, caches, vendored dependencies, binaries, secrets, and large unrelated assets unless a specific question requires them.

The audit is read-only unless the user asks for fixes. Report evidence with file paths and line numbers when practical. Separate confirmed restrictions, likely submission questions, missing evidence, and ordinary recommendations. A code search can prove a feature or SDK is present; it rarely proves that data collection, server behavior, retention, deletion, or production configuration is absent.

## Prepare store assets and screenshots

When the user asks for submission assets, screenshots, or a complete submission package, read [references/assets.md](references/assets.md). Create the project-local `assets/screenshots/` workspace and its tickable `CHECKLIST.md` with [scripts/prepare_store_assets.py](scripts/prepare_store_assets.py). Use the app's detected targets to include only relevant device families. Do not overwrite an existing checklist or any existing asset.

Prompt the user to save real app captures in the checklist's named folders. If a running build, emulator, or device is available, help capture the real flows and save them there. Otherwise, identify the exact screens to capture and wait for actual captures. Do not generate or submit synthetic screenshots, invented UI, or edited screenshots that misrepresent the app's current experience.

Use image generation for missing supporting marketing artwork when the user has asked for assets and sufficient app/brand evidence exists. In particular, it can draft a Google Play feature graphic or non-app screenshot background treatment. Base prompts on verified app facts and provided brand materials, inspect the result, then save the selected final artifact in the checklist's destination without overwriting user work. Use image processing as needed to make the saved file match the required dimensions, format, and alpha-channel rules. Never use image generation to replace the actual app interface in a store screenshot.

Run the helper's `validate` command before uploading assets. It verifies required folder content, common formats, pixel dimensions, count limits, and detectable PNG alpha channels. Treat current console validation as decisive, and resolve its errors before uploading. Codex may change only completed checklist rows to `[x]` after it has verified the corresponding file; the user may tick rows manually as captures are saved.

## Prepare the relevant store fields

- For Apple, read [references/apple.md](references/apple.md).
- For Google Play, read [references/google-play.md](references/google-play.md).
- For asset requirements and the screenshot workspace, read [references/assets.md](references/assets.md).

Check current official documentation and the actual console for field names, length/count rules, asset specifications, policy questions, and conditional requirements. References are navigation aids, not frozen policy. Record the source URL and check date for consequential requirements. If current verification is unavailable, label the affected requirement unverified and prepare the rest.

Draft separate store-native copy for each requested locale. Describe real benefits and features; avoid fabricated capabilities, awards, rankings, prices, testimonials, or unverified claims. Preserve approved brand terminology. For updates, derive release notes from verified changes rather than inventing improvements. Translate only requested locales and recheck their lengths independently.

Give each field its exact console label, locale, proposed value, status, and relevant evidence. Put pasteable prose in its own block; keep counts and commentary outside the field text. Measure lengths programmatically using the documented unit, including punctuation, spaces, and line breaks. For Unicode or ambiguous counting rules, treat console validation as decisive. Never silently truncate copy.

Map existing assets to store, locale, device/form factor, order, dimensions, and file path. Verify against current specifications. Report missing assets precisely. Screenshots must represent the app; do not fabricate UI or imply an unimplemented feature. Create or edit assets only when needed and authorized.

## Answer declarations from evidence

Privacy, tracking, data collection/sharing, age/content ratings, ads, account deletion, encryption, permissions, and regulated-feature answers require evidence about actual behavior, including embedded SDKs and backend services. Absence of evidence is not a negative answer. Repository inspection can identify questions but may not establish production configuration or retention practices.

For an unresolved declaration, show the exact question, the missing fact, and who or what could resolve it. Ask focused factual questions rather than requesting blanket approval of a questionnaire. Do not invent a privacy policy URL, reviewer login, deletion mechanism, encryption exemption, or legal/business status. Use each store's definitions separately; do not mechanically copy Apple privacy answers into Google's Data safety form.

## Fill and verify

Use available purpose-built store tools or authenticated browser controls. Inspect the current account/team, app identifier, version, locale, and release track before editing. Use observed UI controls or documented APIs; do not guess selectors, endpoints, or success states. If access or a capability is unavailable, finish a paste-ready packet and identify the exact remaining action. User login or two-factor authentication may require user interaction; never request account passwords in ordinary chat.

Honor the user's existing authorization. A request to fill forms authorizes the relevant edits and saves; it does not by itself authorize sending the app for review or releasing it. An explicit request to submit or publish authorizes that action within its stated scope; do not ask again simply because the action is consequential. Before execution, ensure the actual app/build, destination, release behavior, and declarations are resolved. If additional authorization is needed, first complete the concrete draft and validation so the user can review it.

Preserve unrelated existing fields and release settings. Distinguish save, submit for review, approval, and public availability. Check whether a control can publish immediately or release automatically after approval. Never broaden requested countries, pricing, tracks, rollout percentages, or timing. Do not accept unrelated agreements or change account/banking settings as an incidental step.

After saving, read back the values or reopen the relevant section and check persistence, asset order, and validation errors. After submission, confirm the displayed status and any submission identifier. For an uncertain write, inspect current state before retrying; stop dependent actions if persistence or destination remains ambiguous.

## Deliver

Return a concise status for each requested store: drafted, saved, submitted, or released, only as verified. Include the submission packet or console link, unresolved fields/assets, and the next action if blocked. A local packet should contain store/locale field values, asset mapping, declaration evidence/questions, and a readiness checklist scaled to the task. Keep review credentials out of general reports; reference their secure location. Do not claim store approval or live availability from a successful save or submission.
