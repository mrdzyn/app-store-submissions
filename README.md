# App Store Submissions

A Codex skill for auditing a mobile app project and preparing Apple App Store Connect and Google Play Console submissions.

Point the skill to a project folder and it reads relevant source, manifests, dependencies, privacy files, store assets, and project documentation. It reports submission blockers, declaration questions, review-access gaps, metadata issues, and missing assets with evidence from the project.

## What it covers

- Apple App Store and Google Play listing fields, assets, release details, and reviewer instructions.
- iOS and Android permissions, entitlements, build configuration, SDKs, privacy declarations, account deletion, and restricted features.
- Relevant project docs, including Markdown product, privacy, support, release, and security material.
- A submission-readiness report that distinguishes confirmed restrictions from missing evidence and follow-up questions.

## Install

Clone this repository into your Codex skills folder:

```bash
git clone https://github.com/mrdzyn/app-store-submissions.git ~/.codex/skills/app-store-submissions
```

Then use it in Codex:

```text
Use $app-store-submissions to audit /path/to/my-app for Apple App Store and Google Play submission restrictions, then prepare the missing submission fields.
```

The audit is evidence-based: a missing search result does not prove that a service, SDK, or backend does not collect or share data. Resolve any items marked as `Unresolved` or `Not evidenced` before completing store privacy declarations.

## Repository layout

```text
SKILL.md                         Core workflow
references/apple.md              Apple-specific guidance
references/google-play.md        Google Play-specific guidance
references/project-audit.md      Folder audit workflow
agents/openai.yaml               Codex UI metadata
```

Store requirements change. The skill directs Codex to verify consequential requirements against current Apple and Google documentation for each submission.
