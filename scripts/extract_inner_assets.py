#!/usr/bin/env python3
"""Extract stable page artwork from the supplied full-page mockups.

The public pages must render ordinary responsive images, not reposition an
entire screenshot behind every image frame.  Crops stay reproducible here and
are exported as lossless WebP files so their pixels match the mockups.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]

# source: {output path: (left, top, width, height)}
SOURCES = {
    "assets/screens/soluzioni.png": {
        "assets/img/soluzioni/hero-pa.webp": (448, 45, 500, 345),
        "assets/img/soluzioni/hero-pa-mobile.webp": (500, 45, 448, 260),
        "assets/img/soluzioni/scuole.webp": (27, 485, 294, 139),
        "assets/img/soluzioni/rsa.webp": (334, 485, 280, 132),
        "assets/img/soluzioni/asl-ospedali.webp": (627, 485, 296, 140),
        "assets/img/soluzioni/comuni.webp": (27, 867, 294, 139),
        "assets/img/soluzioni/uffici.webp": (334, 867, 280, 132),
        "assets/img/soluzioni/altri-enti.webp": (627, 867, 296, 140),
    },
    "assets/screens/mepa.png": {
        "assets/img/mepa/hero.webp": (437, 54, 587, 356),
        "assets/img/mepa/hero-mobile.webp": (555, 54, 469, 300),
        "assets/img/mepa/step-catalogo.webp": (50, 635, 275, 159),
        "assets/img/mepa/step-codice.webp": (376, 636, 275, 159),
        "assets/img/mepa/codice-unico.webp": (468, 934, 532, 246),
    },
    "assets/screens/come-acquistare.png": {
        "assets/img/come-acquistare/hero.webp": (492, 54, 532, 189),
    },
    "assets/screens/chi-siamo.png": {
        "assets/img/chi-siamo/hero.webp": (484, 54, 540, 204),
        "assets/img/chi-siamo/hero-mobile.webp": (600, 54, 400, 106),
        "assets/img/chi-siamo/enti-serviti.webp": (33, 665, 959, 399),
    },
    "assets/screens/contatti.png": {
        "assets/img/contatti/hero.webp": (686, 60, 850, 303),
        "assets/img/contatti/hero-mobile.webp": (850, 60, 686, 303),
        "assets/img/come-acquistare/hero-mobile.webp": (850, 60, 686, 303),
    },
    "assets/screens/faq.png": {
        "assets/img/faq/hero.webp": (768, 58, 768, 270),
        "assets/img/faq/hero-mobile.webp": (850, 58, 686, 270),
    },
    "assets/screens/referenze.png": {
        "assets/img/referenze/hero.webp": (493, 54, 531, 307),
        "assets/img/referenze/hero-mobile.webp": (590, 54, 434, 260),
        "assets/img/referenze/caso-fornitura-sanitaria.webp": (48, 888, 287, 157),
        "assets/img/referenze/caso-procedura-gara.webp": (377, 896, 274, 149),
        "assets/img/referenze/caso-documentazione.webp": (694, 901, 289, 150),
    },
}


def main() -> None:
    for source_name, crops in SOURCES.items():
        source_path = ROOT / source_name
        with Image.open(source_path) as source:
            source.load()
            for output_name, (left, top, width, height) in crops.items():
                box = (left, top, left + width, top + height)
                if left < 0 or top < 0 or box[2] > source.width or box[3] > source.height:
                    raise ValueError(
                        f"Crop {output_name} exceeds {source_name} {source.size}: {box}"
                    )

                output_path = ROOT / output_name
                output_path.parent.mkdir(parents=True, exist_ok=True)
                artwork = source.crop(box)
                # Method 4 keeps lossless output deterministic without making the
                # full extraction needlessly slow on the large source mockups.
                artwork.save(output_path, "WEBP", lossless=True, quality=100, method=4)
                print(f"{output_path.relative_to(ROOT)} {width}x{height}")


if __name__ == "__main__":
    main()
