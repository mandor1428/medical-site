#!/usr/bin/env python3
"""Extract stable home-page artwork from the supplied 1086 x 1448 mockup.

The coordinates below are the exact regions previously rendered through CSS
sprite offsets.  Keeping them in one deterministic script makes the exported
assets reproducible while allowing the page to use ordinary responsive images.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reference" / "homepage.png"
OUTPUT_DIR = ROOT / "assets" / "img" / "home"
EXPECTED_SOURCE_SIZE = (1086, 1448)

# name: (left, top, width, height)
CROPS = {
    "hero-ospedale.webp": (566, 47, 520, 278),
    "fascicolo-tecnico.webp": (40, 618, 178, 175),
    "ente-scuole.webp": (34, 945, 193, 74),
    "ente-rsa.webp": (239, 945, 190, 74),
    "ente-asl-ospedali.webp": (440, 945, 191, 74),
    "ente-comuni.webp": (644, 945, 192, 74),
    "ente-uffici.webp": (848, 945, 204, 74),
    "prodotto-defibrillatore.webp": (35, 1107, 164, 82),
    "prodotto-lettino.webp": (207, 1107, 164, 82),
    "prodotto-carrozzina.webp": (379, 1107, 164, 82),
    "prodotto-monitor.webp": (551, 1107, 164, 82),
    "prodotto-pompa-infusione.webp": (723, 1107, 164, 82),
    "prodotto-elettrocardiografo.webp": (886, 1107, 164, 82),
}


def main() -> None:
    with Image.open(SOURCE) as source:
        source.load()
        if source.size != EXPECTED_SOURCE_SIZE:
            raise ValueError(
                f"Unexpected source size {source.size}; expected {EXPECTED_SOURCE_SIZE}"
            )

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        for filename, (left, top, width, height) in CROPS.items():
            box = (left, top, left + width, top + height)
            if box[2] > source.width or box[3] > source.height:
                raise ValueError(f"Crop {filename} exceeds the source bounds: {box}")

            artwork = source.crop(box)
            destination = OUTPUT_DIR / filename
            # Lossless WebP preserves the exact RGB pixels. Method 4 keeps the
            # build fast enough for repeatable local runs without changing them.
            artwork.save(destination, "WEBP", lossless=True, quality=100, method=4)
            print(f"{destination.relative_to(ROOT)} {artwork.width}x{artwork.height}")


if __name__ == "__main__":
    main()
