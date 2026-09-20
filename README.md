# App Store Submissions

A Codex skill for auditing a mobile app project and preparing Apple App Store Connect and Google Play Console submissions.

Point the skill to a project folder and it reads relevant source, manifests, dependencies, privacy files, store assets, and project documentation. It reports submission blockers, declaration questions, review-access gaps, metadata issues, and missing assets with evidence from the project.

## What it covers

- Apple App Store and Google Play listing fields, assets, release details, and reviewer instructions.
- iOS and Android permissions, entitlements, build configuration, SDKs, privacy declarations, account deletion, and restricted features.
- Relevant project docs, including Markdown product, privacy, support, release, and security material.
- A project-local `assets/screenshots/` workspace with a tickable capture checklist and a validator for App Store and Google Play image dimensions.
- A non-destructive renderer that converts user-provided, real app captures into exact-size RGB PNG or JPEG exports for Apple and Google targets.
- Optional marketing compositions with a truthful headline and branded canvas. The renderer preserves the real captured UI, rejects material aspect-ratio mismatches by default, and does not fabricate app interfaces or device frames.
- Draft generation for supporting store graphics such as a Google Play feature graphic, while requiring real app captures for all store screenshots.
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

To create the screenshot workspace and checklist, use:

```text
Use $app-store-submissions to create and validate the required App Store and Google Play asset folders for /path/to/my-app.
```

The skill creates `assets/screenshots/CHECKLIST.md` and `assets/screenshots/source/`. Save original captures in `source/`, then render upload-ready files into the store-specific subfolders. It verifies dimensions and formats before upload, and only marks a checkbox complete after verifying its file. Screenshots must depict the current, real app experience.

## Render store-ready screenshots

Install the renderer dependency once:

```bash
python3 -m pip install -r scripts/requirements.txt
```

Create a faithful, direct-upload iPhone export from a real capture:

```bash
python3 scripts/render_store_screenshots.py /path/to/my-app \
  --source /path/to/my-app/assets/screenshots/source/home.png \
  --target apple-iphone-6.9-portrait --name 01 --style direct
```

Create a Google Play marketing composition when the copy accurately reflects the captured app:

```bash
python3 scripts/render_store_screenshots.py /path/to/my-app \
  --source /path/to/my-app/assets/screenshots/source/home.png \
  --target google-phone-portrait --name 01 --style marketing \
  --headline "Plan your day in one place" --background "#123047"
```

The renderer preserves the source, flattens final files to RGB, and refuses to overwrite an existing export unless `--replace` is supplied. It requires a new capture when the source aspect ratio is materially different, unless the user has explicitly checked and authorized `--allow-crop`.

The audit is evidence-based: a missing search result does not prove that a service, SDK, or backend does not collect or share data. Resolve any items marked as `Unresolved` or `Not evidenced` before completing store privacy declarations.

## Repository layout

```text
SKILL.md                         Core workflow
references/apple.md              Apple-specific guidance
references/google-play.md        Google Play-specific guidance
references/project-audit.md      Folder audit workflow
references/assets.md             Asset and screenshot requirements
scripts/prepare_store_assets.py  Asset workspace and dimension validator
scripts/render_store_screenshots.py  Screenshot renderer and marketing compositor
scripts/requirements.txt         Pillow dependency for rendering
agents/openai.yaml               Codex UI metadata
```

Store requirements change. The skill directs Codex to verify consequential requirements against current Apple and Google documentation for each submission.
