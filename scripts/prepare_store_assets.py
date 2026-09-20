#!/usr/bin/env python3
"""Create and validate a project-local App Store and Google Play asset workspace."""

from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path


APPLE_IPHONE = (1320, 2868)
APPLE_IPAD = (2064, 2752)
APPLE_MAC_SIZES = {(1280, 800), (1440, 900), (2560, 1600), (2880, 1800)}
GOOGLE_RECOMMENDED_PHONE = (1080, 1920)
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("init", "validate"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("project", type=Path, help="App project folder")
        subparser.add_argument(
            "--stores",
            nargs="+",
            choices=("apple", "google"),
            default=("apple", "google"),
            help="Stores to include (default: both)",
        )
        subparser.add_argument("--apple-ipad", action="store_true", help="Include iPad assets")
        subparser.add_argument("--apple-mac", action="store_true", help="Include Mac screenshot guidance")
        subparser.add_argument("--google-tablet", action="store_true", help="Include tablet/Chromebook assets")

    return parser.parse_args()


def image_info(path: Path) -> tuple[int, int, bool]:
    """Return width, height, and whether a PNG has an alpha channel."""
    with path.open("rb") as image:
        header = image.read(32)
        if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) >= 26:
            width, height = struct.unpack(">II", header[16:24])
            color_type = header[25]
            has_alpha = color_type in {4, 6} or b"tRNS" in path.read_bytes()
            return width, height, has_alpha
        if header[:2] == b"\xff\xd8":
            image.seek(2)
            while True:
                marker_prefix = image.read(1)
                if not marker_prefix:
                    break
                if marker_prefix != b"\xff":
                    continue
                marker = image.read(1)
                while marker == b"\xff":
                    marker = image.read(1)
                if marker in {b"\xd8", b"\xd9"}:
                    continue
                length_data = image.read(2)
                if len(length_data) != 2:
                    break
                segment_length = struct.unpack(">H", length_data)[0]
                marker_value = marker[0]
                if marker_value in {
                    0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
                }:
                    data = image.read(5)
                    if len(data) != 5:
                        break
                    height, width = struct.unpack(">HH", data[1:5])
                    return width, height, False
                image.seek(segment_length - 2, 1)
    raise ValueError("not a readable PNG or JPEG")


def image_files(folder: Path) -> list[Path]:
    return sorted(path for path in folder.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES)


def checkbox(path: str, description: str) -> str:
    return f"- [ ] `{path}` — {description}"


def checklist(args: argparse.Namespace) -> str:
    sections = [
        "# Store asset checklist",
        "",
        "Save final images in the paths below. Screenshots must be real captures of the current app; do not use generated or fabricated UI.",
        "",
        "## Before capture",
        "",
        "- [ ] Confirm the selected stores, locale, supported device families, and orientation in the current store consoles.",
        "- [ ] Capture the signed-off build with representative content and no personal data, test markers, or debug controls.",
        "- [ ] Save original captures in `assets/screenshots/source/`; keep store-specific folders for final rendered exports only.",
        "",
    ]
    if "apple" in args.stores:
        sections.extend(["## Apple App Store", ""])
        for index in range(1, 6):
            sections.append(checkbox(
                f"apple/iphone-6.9/{index:02}.png",
                "real iPhone capture, 1320×2868 portrait (or 2868×1320 landscape), JPEG/PNG without alpha",
            ))
        if args.apple_ipad:
            sections.extend(["", "### iPad", ""])
            for index in range(1, 6):
                sections.append(checkbox(
                    f"apple/ipad-13/{index:02}.png",
                    "real iPad capture, 2064×2752 portrait (or 2752×2064 landscape), JPEG/PNG without alpha",
                ))
        if args.apple_mac:
            sections.extend([
                "", "### Mac", "",
                checkbox("apple/mac/01.png", "real Mac capture, 16:10 at 1280×800, 1440×900, 2560×1600, or 2880×1800"),
            ])
        sections.extend(["", "Apple permits one to ten screenshots per device family. Keep only verified final images in the folder.", ""])
    if "google" in args.stores:
        sections.extend(["## Google Play", "", "### Phone", ""])
        for index in range(1, 5):
            sections.append(checkbox(
                f"google-play/phone/{index:02}.png",
                "real phone capture, recommended 1080×1920 portrait (or 1920×1080 landscape), JPEG/24-bit PNG without alpha",
            ))
        sections.extend([
            "",
            checkbox("../store-graphics/google-play/icon-512.png", "512×512 32-bit PNG with alpha, 1 MB or smaller; use the approved app icon"),
            checkbox("../store-graphics/google-play/feature-graphic.png", "1024×500 JPEG or 24-bit PNG without alpha; generated artwork is allowed only when it does not misrepresent the app"),
        ])
        if args.google_tablet:
            sections.extend(["", "### Tablet / Chromebook", ""])
            for index in range(1, 5):
                sections.append(checkbox(
                    f"google-play/tablet/{index:02}.png",
                    "real large-screen capture, 1080–7680px, 9:16 portrait or 16:9 landscape, JPEG/24-bit PNG without alpha",
                ))
        sections.extend([
            "",
            "Google requires at least two screenshots across device types and accepts up to eight per type. Four current app screenshots are recommended for phone placement.",
            "",
        ])
    sections.extend([
        "## Final verification",
        "",
        "- [ ] Render each original from `assets/screenshots/source/` with `scripts/render_store_screenshots.py`; use direct mode for faithful exports or marketing mode only with accurate copy and a real, fully visible app capture.",
        "- [ ] Run `python3 scripts/prepare_store_assets.py validate /path/to/project` from this skill's folder.",
        "- [ ] Review every image for truthful UI, legibility, localization, and store content-policy compliance.",
        "- [ ] Confirm the current App Store Connect and Play Console accept the selected files before upload.",
        "",
    ])
    return "\n".join(sections)


def init_workspace(args: argparse.Namespace) -> int:
    project = args.project.resolve()
    if not project.is_dir():
        print(f"Project folder does not exist: {project}", file=sys.stderr)
        return 2

    screenshots = project / "assets" / "screenshots"
    folders = [screenshots / "source"]
    if "apple" in args.stores:
        folders.append(screenshots / "apple" / "iphone-6.9")
        if args.apple_ipad:
            folders.append(screenshots / "apple" / "ipad-13")
        if args.apple_mac:
            folders.append(screenshots / "apple" / "mac")
    if "google" in args.stores:
        folders.extend([
            screenshots / "google-play" / "phone",
            project / "assets" / "store-graphics" / "google-play",
        ])
        if args.google_tablet:
            folders.append(screenshots / "google-play" / "tablet")
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

    checklist_path = screenshots / "CHECKLIST.md"
    if checklist_path.exists():
        print(f"Preserved existing checklist: {checklist_path}")
    else:
        checklist_path.write_text(checklist(args), encoding="utf-8")
        print(f"Created checklist: {checklist_path}")
    print(f"Asset workspace ready: {screenshots}")
    return 0


def report(status: str, message: str) -> bool:
    print(f"{status}: {message}")
    return status == "PASS"


def valid_non_alpha_image(path: Path, expected: tuple[int, int] | None = None) -> bool:
    try:
        width, height, alpha = image_info(path)
    except ValueError as error:
        return report("FAIL", f"{path}: {error}")
    if alpha:
        return report("FAIL", f"{path}: image has a detectable alpha channel")
    if expected and (width, height) not in {expected, expected[::-1]}:
        return report("FAIL", f"{path}: {width}×{height}; expected {expected[0]}×{expected[1]} or landscape equivalent")
    return report("PASS", f"{path}: {width}×{height}")


def valid_apple_mac_image(path: Path) -> bool:
    try:
        width, height, alpha = image_info(path)
    except ValueError as error:
        return report("FAIL", f"{path}: {error}")
    if alpha or (width, height) not in APPLE_MAC_SIZES:
        allowed = ", ".join(f"{item[0]}×{item[1]}" for item in sorted(APPLE_MAC_SIZES))
        return report("FAIL", f"{path}: requires a non-alpha 16:10 image at {allowed}")
    return report("PASS", f"{path}: {width}×{height}")


def validate_google_phone(folder: Path) -> bool:
    files = image_files(folder)
    valid = True
    if not 2 <= len(files) <= 8:
        valid = report("FAIL", f"{folder}: found {len(files)} images; Google Play phone needs 2–8") and valid
    elif len(files) < 4:
        report("WARN", f"{folder}: four images are recommended for phone placement")
    for path in files:
        try:
            width, height, alpha = image_info(path)
            if alpha or min(width, height) < 320 or max(width, height) > 3840 or max(width, height) > min(width, height) * 2:
                valid = report("FAIL", f"{path}: {width}×{height} does not meet Google Play phone rules") and valid
            else:
                report("PASS", f"{path}: {width}×{height}")
        except ValueError as error:
            valid = report("FAIL", f"{path}: {error}") and valid
    return valid


def validate_google_tablet(folder: Path) -> bool:
    files = image_files(folder)
    valid = True
    if len(files) < 4:
        valid = report("FAIL", f"{folder}: found {len(files)} images; four are expected for a tablet listing") and valid
    for path in files:
        try:
            width, height, alpha = image_info(path)
            if alpha or min(width, height) < 1080 or max(width, height) > 7680:
                valid = report("FAIL", f"{path}: {width}×{height} does not meet Google Play large-screen rules") and valid
            else:
                report("PASS", f"{path}: {width}×{height}")
        except ValueError as error:
            valid = report("FAIL", f"{path}: {error}") and valid
    return valid


def validate_workspace(args: argparse.Namespace) -> int:
    project = args.project.resolve()
    screenshots = project / "assets" / "screenshots"
    graphics = project / "assets" / "store-graphics" / "google-play"
    valid = True
    if "apple" in args.stores:
        apple_phone = screenshots / "apple" / "iphone-6.9"
        files = image_files(apple_phone) if apple_phone.is_dir() else []
        if not 1 <= len(files) <= 10:
            valid = report("FAIL", f"{apple_phone}: found {len(files)} images; Apple needs 1–10") and valid
        for path in files:
            valid = valid_non_alpha_image(path, APPLE_IPHONE) and valid
        if args.apple_ipad:
            apple_ipad = screenshots / "apple" / "ipad-13"
            files = image_files(apple_ipad) if apple_ipad.is_dir() else []
            if not 1 <= len(files) <= 10:
                valid = report("FAIL", f"{apple_ipad}: found {len(files)} images; Apple needs 1–10") and valid
            for path in files:
                valid = valid_non_alpha_image(path, APPLE_IPAD) and valid
        if args.apple_mac:
            apple_mac = screenshots / "apple" / "mac"
            files = image_files(apple_mac) if apple_mac.is_dir() else []
            if not 1 <= len(files) <= 10:
                valid = report("FAIL", f"{apple_mac}: found {len(files)} images; Apple needs 1–10") and valid
            for path in files:
                valid = valid_apple_mac_image(path) and valid
    if "google" in args.stores:
        google_phone = screenshots / "google-play" / "phone"
        if google_phone.is_dir():
            valid = validate_google_phone(google_phone) and valid
        else:
            valid = report("FAIL", f"Missing folder: {google_phone}") and valid
        if args.google_tablet:
            google_tablet = screenshots / "google-play" / "tablet"
            if google_tablet.is_dir():
                valid = validate_google_tablet(google_tablet) and valid
            else:
                valid = report("FAIL", f"Missing folder: {google_tablet}") and valid
        icon = graphics / "icon-512.png"
        feature = next((path for path in (graphics / "feature-graphic.png", graphics / "feature-graphic.jpg", graphics / "feature-graphic.jpeg") if path.exists()), None)
        if not icon.exists():
            valid = report("FAIL", f"Missing Google Play icon: {icon}") and valid
        else:
            try:
                width, height, alpha = image_info(icon)
                if (width, height) != (512, 512) or not alpha or icon.stat().st_size > 1024 * 1024:
                    valid = report("FAIL", f"{icon}: requires 512×512 PNG with alpha and file size of 1 MB or less") and valid
                else:
                    report("PASS", f"{icon}: 512×512 PNG with alpha")
            except ValueError as error:
                valid = report("FAIL", f"{icon}: {error}") and valid
        if feature is None:
            valid = report("FAIL", f"Missing Google Play feature graphic in {graphics}") and valid
        else:
            valid = valid_non_alpha_image(feature, (1024, 500)) and valid
    return 0 if valid else 1


def main() -> int:
    args = parse_args()
    return init_workspace(args) if args.command == "init" else validate_workspace(args)


if __name__ == "__main__":
    raise SystemExit(main())
