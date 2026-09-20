#!/usr/bin/env python3
"""Render non-destructive, store-sized exports from real app screenshots."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps
except ImportError as error:
    raise SystemExit(
        "Pillow is required. Install it with: python3 -m pip install -r scripts/requirements.txt"
    ) from error


@dataclass(frozen=True)
class Target:
    width: int
    height: int
    folder: str
    google: bool = False


TARGETS = {
    "apple-iphone-6.9-portrait": Target(1320, 2868, "apple/iphone-6.9"),
    "apple-iphone-6.9-landscape": Target(2868, 1320, "apple/iphone-6.9"),
    "apple-ipad-13-portrait": Target(2064, 2752, "apple/ipad-13"),
    "apple-ipad-13-landscape": Target(2752, 2064, "apple/ipad-13"),
    "apple-mac": Target(1440, 900, "apple/mac"),
    "google-phone-portrait": Target(1080, 1920, "google-play/phone", google=True),
    "google-phone-landscape": Target(1920, 1080, "google-play/phone", google=True),
    "google-tablet-portrait": Target(1080, 1920, "google-play/tablet", google=True),
    "google-tablet-landscape": Target(1920, 1080, "google-play/tablet", google=True),
    "google-feature-graphic": Target(1024, 500, "../store-graphics/google-play", google=True),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="App project folder")
    parser.add_argument("--source", required=True, type=Path, help="Original user-provided screenshot")
    parser.add_argument("--target", required=True, choices=sorted(TARGETS), help="Required store asset target")
    parser.add_argument("--name", required=True, help="Output base name, for example 01 or onboarding")
    parser.add_argument("--style", choices=("direct", "marketing"), default="direct")
    parser.add_argument("--headline", help="Accurate optional marketing headline")
    parser.add_argument("--subheadline", help="Accurate optional supporting copy")
    parser.add_argument("--background", default="#101828", help="Canvas color for marketing mode")
    parser.add_argument("--text-color", help="Headline color for marketing mode")
    parser.add_argument("--font", type=Path, help="Optional TrueType or OpenType font file")
    parser.add_argument("--format", choices=("png", "jpg"), default="png")
    parser.add_argument("--allow-crop", action="store_true", help="Allow direct mode to crop a mismatched source")
    parser.add_argument("--replace", action="store_true", help="Replace an existing output file")
    return parser.parse_args()


def safe_name(name: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
        raise ValueError("--name may use only letters, numbers, dots, underscores, and hyphens")
    return name


def resample() -> int:
    return Image.Resampling.LANCZOS


def load_font(size: int, requested: Path | None) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [requested] if requested else []
    candidates.extend(
        Path(path)
        for path in (
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        )
    )
    for path in candidates:
        if path and path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines() or [text]:
        words = paragraph.split()
        current = ""
        for word in words:
            proposed = f"{current} {word}".strip()
            if current and draw.textbbox((0, 0), proposed, font=font)[2] > max_width:
                lines.append(current)
                current = word
            else:
                current = proposed
        if current:
            lines.append(current)
    return lines or [""]


def draw_copy(
    image: Image.Image,
    headline: str | None,
    subheadline: str | None,
    color: tuple[int, int, int],
    max_header_height: int,
    requested_font: Path | None,
) -> int:
    if not headline:
        return 0
    draw = ImageDraw.Draw(image)
    max_width = int(image.width * 0.84)
    x = int(image.width * 0.08)
    headline_font = load_font(max(28, int(image.width * 0.06)), requested_font)
    headline_lines = wrap(draw, headline, headline_font, max_width)
    y = int(image.height * 0.055)
    for line in headline_lines:
        bounds = draw.textbbox((0, 0), line, font=headline_font)
        draw.text((x, y), line, font=headline_font, fill=color)
        y += bounds[3] - bounds[1] + int(image.height * 0.012)
    if subheadline:
        sub_font = load_font(max(20, int(image.width * 0.03)), requested_font)
        for line in wrap(draw, subheadline, sub_font, max_width):
            bounds = draw.textbbox((0, 0), line, font=sub_font)
            draw.text((x, y), line, font=sub_font, fill=color)
            y += bounds[3] - bounds[1] + int(image.height * 0.008)
    if y > max_header_height:
        raise ValueError("Headline and supporting copy exceed the permitted header area")
    return y + int(image.height * 0.025)


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *size), radius=radius, fill=255)
    return mask


def render_direct(source: Image.Image, target: Target, allow_crop: bool) -> Image.Image:
    source_ratio = source.width / source.height
    target_ratio = target.width / target.height
    difference = abs(source_ratio - target_ratio) / target_ratio
    if difference > 0.01 and not allow_crop:
        raise ValueError(
            f"Source aspect ratio differs by {difference:.1%}. Re-capture at {target.width}×{target.height} "
            "or rerun with --allow-crop after confirming no UI will be concealed."
        )
    if difference > 0.0001:
        return ImageOps.fit(source, (target.width, target.height), method=resample(), centering=(0.5, 0.5))
    return source.resize((target.width, target.height), resample())


def render_marketing(source: Image.Image, target: Target, args: argparse.Namespace) -> Image.Image:
    background = ImageColor.getrgb(args.background)
    text_color = ImageColor.getrgb(args.text_color) if args.text_color else (255, 255, 255)
    canvas = Image.new("RGB", (target.width, target.height), background)
    max_header = int(target.height * (0.20 if target.google else 0.28))
    content_top = draw_copy(canvas, args.headline, args.subheadline, text_color, max_header, args.font)
    content_top = max(content_top, int(target.height * 0.06))
    margin_x = int(target.width * 0.07)
    margin_bottom = int(target.height * 0.05)
    available = (target.width - margin_x * 2, target.height - content_top - margin_bottom)
    if available[0] <= 0 or available[1] <= 0:
        raise ValueError("Marketing copy leaves no room for the screenshot")
    screenshot = ImageOps.contain(source, available, method=resample())
    x = (target.width - screenshot.width) // 2
    y = content_top + (available[1] - screenshot.height) // 2
    mask = rounded_mask(screenshot.size, max(12, int(min(screenshot.size) * 0.025)))
    canvas.paste(screenshot, (x, y), mask)
    return canvas


def main() -> int:
    args = parse_args()
    project = args.project.resolve()
    source_path = args.source.resolve()
    target = TARGETS[args.target]
    if not project.is_dir():
        raise SystemExit(f"Project folder does not exist: {project}")
    if not source_path.is_file():
        raise SystemExit(f"Source image does not exist: {source_path}")
    try:
        name = safe_name(args.name)
        output_dir = (project / "assets" / "screenshots" / target.folder).resolve()
        extension = ".jpg" if args.format == "jpg" else ".png"
        output = output_dir / f"{name}{extension}"
        if output.resolve() == source_path:
            raise ValueError("Output must be separate from the original source capture")
        if output.exists() and not args.replace:
            raise ValueError(f"Output exists: {output}; use a new name or --replace")
        with Image.open(source_path) as opened:
            source = ImageOps.exif_transpose(opened).convert("RGB")
        final = render_direct(source, target, args.allow_crop) if args.style == "direct" else render_marketing(source, target, args)
        output_dir.mkdir(parents=True, exist_ok=True)
        if args.format == "jpg":
            final.save(output, "JPEG", quality=95, optimize=True)
        else:
            final.save(output, "PNG", optimize=True)
        print(f"Rendered {args.style} export: {output}")
        print(f"Target: {target.width}×{target.height}; source preserved: {source_path}")
        return 0
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
