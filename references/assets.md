# Store asset workspace and checklist

Use this reference when the user asks for screenshots, icons, feature graphics, preview assets, or a complete submission package. Check the current official source and selected console fields before creating or uploading assets; supported device families and requirements can change.

## Create the workspace

Run the helper from the skill folder before requesting captures. For an iPhone and Android phone app:

```bash
python3 scripts/prepare_store_assets.py init /path/to/project
```

Add `--apple-ipad`, `--apple-mac`, or `--google-tablet` only when those targets are supported. The command creates this project-local structure without overwriting existing files:

```text
assets/
  screenshots/
    CHECKLIST.md
    source/                       # original user-provided captures
    apple/iphone-6.9/
    apple/ipad-13/                 # when selected
    google-play/phone/
    google-play/tablet/            # when selected
  store-graphics/
    google-play/
```

`CHECKLIST.md` contains individual Markdown checkboxes, exact filename suggestions, required or recommended dimensions, and a short capture plan. Save original captures in `source/`; the render helper writes direct-upload exports to the store-specific folders. The user can tick boxes while saving captures. Codex can tick a row only after the corresponding file passes verification.

## Screenshot rules

Screenshots must accurately show the current app. They can be captured from real devices or emulators and may be lightly prepared for store presentation only when the visible interface remains truthful. Do not use generated or fabricated UI. Keep source captures and any composed final images separately when that aids traceability.

The helper's initial checklist uses these current baseline targets:

| Store / target | Checklist target | Capture count | Format and dimensions |
| --- | --- | --- | --- |
| Apple iPhone | 6.9-inch display | 1–10 | JPEG or PNG, no alpha; `1320×2868` portrait or `2868×1320` landscape |
| Apple iPad | 13-inch display, only for iPad apps | 1–10 | JPEG or PNG, no alpha; `2064×2752` portrait or `2752×2064` landscape |
| Google Play phone | phone | 2–8; 4 recommended | JPEG or 24-bit PNG, no alpha; each side `320–3840px`, long side no more than twice the short side. The checklist recommends `1080×1920` portrait or `1920×1080` landscape. |
| Google Play tablet / Chromebook | only when supported | 4 recommended | JPEG or 24-bit PNG, `1080–7680px`; use 9:16 portrait or 16:9 landscape. |

Apple accepts one to ten screenshots and scales some newer device screenshots for smaller displays. The currently selected 6.9-inch iPhone and 13-inch iPad targets cover the required categories for ordinary iPhone/iPad submissions, but console requirements control for the submitted app. Google Play supports up to eight screenshots per device type and requires at least two across device types to publish; its recommendation surfaces have stricter screenshot counts and resolutions.

## Render and validate user-provided captures

The render helper uses Pillow. Install it in the active Python environment once when needed:

```bash
python3 -m pip install -r scripts/requirements.txt
```

Create a direct iPhone export from a real source capture. The source remains unchanged:

```bash
python3 scripts/render_store_screenshots.py /path/to/project \
  --source /path/to/project/assets/screenshots/source/home.png \
  --target apple-iphone-6.9-portrait --name 01 --style direct
```

For a marketing composition, supply only accurate copy that is already supported by the app and its listing. The whole captured interface stays visible on a branded canvas; Google Play copy occupies no more than 20% of the image.

```bash
python3 scripts/render_store_screenshots.py /path/to/project \
  --source /path/to/project/assets/screenshots/source/home.png \
  --target google-phone-portrait --name 01 --style marketing \
  --headline "Plan your day in one place" --background "#123047"
```

Direct mode rejects captures whose aspect ratio differs from the target by more than 1%. Re-capture on the required simulator/device or use `--allow-crop` only after confirming that the crop does not conceal or change any interface content. The helper flattens the final screenshot to a non-alpha RGB PNG or JPEG as required. It never overwrites an export without `--replace`.

Run this after rendering the asset set:

```bash
python3 scripts/prepare_store_assets.py validate /path/to/project
```

The renderer and validator cannot determine visual truthfulness, embedded-text policy, runtime state, or current console-specific conditions. Inspect those manually and use the console's final validation.

## Generate supporting graphics

Use image generation only for graphics that do not claim to be a direct app capture, such as a Google Play feature graphic, illustrated background, or other non-UI artwork. It may provide a background for a marketing composition, but must never modify, extend, or fabricate the captured app interface. Do not generate a new brand icon if the project already has an approved editable logo or icon source; adapt that source instead.

For a missing Google Play feature graphic, create a `1024×500` JPEG or 24-bit PNG with no alpha and save it as `assets/store-graphics/google-play/feature-graphic.png` or `.jpg`. Keep focal content near the centre, avoid store badges, ranking/award/price claims, calls to action, and unlicensed third-party marks. For the app icon, use the app's approved icon source; Google Play requires a `512×512` 32-bit PNG with alpha and a maximum size of 1 MB.

Generated artwork is a draft until the user reviews it. Do not overwrite a provided graphic. If the image generator's output is not the exact required size or format, resize/export it before final validation rather than claiming it is upload-ready.

## Official sources

- [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications) — formats, alpha-channel rule, device sizes, and counts.
- [Google Play preview assets](https://support.google.com/googleplay/android-developer/answer/9866151?hl=en) — icon, feature graphic, screenshot formats, counts, dimensions, and content guidance.
- [Google Play icon design specifications](https://developer.android.com/distribute/google-play/resources/icon-design-specifications) — dynamic masking, shadows, and keyline guidance.

Source starting points checked on 2026-09-07. Reverify requirements at submission time.
