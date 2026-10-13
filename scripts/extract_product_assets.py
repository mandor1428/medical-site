#!/usr/bin/env python3
"""Extract reusable product imagery from the approved page mockups.

The coordinates below mirror the ``--crop-x``, ``--crop-y``, ``--crop-w`` and
``--crop-h`` values that previously positioned a complete page screenshot in
each image frame.  Running this script turns every region into an independent,
lossless WebP asset so the browser no longer has to scale and translate an
entire screenshot for each product.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


# output path: (source screenshot, x, y, width, height)
CROPS = {
    # Catalog listing cards (inline crop variables in catalogo.html).
    "assets/images/catalogo/monitor-multiparametrico-gima-20000.webp": ("assets/screens/catalogo.png", 255, 252, 165, 90),
    "assets/images/catalogo/defibrillatore-semiautomatico-def-001.webp": ("assets/screens/catalogo.png", 431, 252, 164, 90),
    "assets/images/catalogo/pompa-infusione-bba-973554.webp": ("assets/screens/catalogo.png", 605, 252, 165, 90),
    "assets/images/catalogo/carrozzina-gima-43210.webp": ("assets/screens/catalogo.png", 781, 252, 164, 90),
    "assets/images/catalogo/lettino-visita-gima-27500.webp": ("assets/screens/catalogo.png", 255, 455, 165, 90),
    "assets/images/catalogo/pulsossimetro-omr-501.webp": ("assets/screens/catalogo.png", 431, 455, 164, 90),
    "assets/images/catalogo/elettrocardiografo-mir-ecg12.webp": ("assets/screens/catalogo.png", 605, 455, 165, 90),
    "assets/images/catalogo/aspiratore-chirurgico-fis-7305.webp": ("assets/screens/catalogo.png", 781, 455, 164, 90),
    "assets/images/catalogo/guanti-chirurgici-mol-118500.webp": ("assets/screens/catalogo.png", 255, 663, 165, 90),
    "assets/images/catalogo/sfigmomanometro-omr-705.webp": ("assets/screens/catalogo.png", 431, 663, 164, 90),
    "assets/images/catalogo/lampada-scialitica-rim-led50.webp": ("assets/screens/catalogo.png", 605, 663, 165, 90),
    "assets/images/catalogo/disinfettante-ecol-1000.webp": ("assets/screens/catalogo.png", 781, 663, 164, 90),
    "assets/images/catalogo/aerosol-omr-neb01.webp": ("assets/screens/catalogo.png", 255, 871, 165, 90),
    "assets/images/catalogo/garze-sterili-hart-42105.webp": ("assets/screens/catalogo.png", 431, 871, 164, 90),
    "assets/images/catalogo/letto-ospedaliero-gima-44700.webp": ("assets/screens/catalogo.png", 605, 871, 165, 90),
    "assets/images/catalogo/contenitore-taglienti-inr-001.webp": ("assets/screens/catalogo.png", 781, 871, 164, 90),
    "assets/images/catalogo/deambulatore-gima-43100.webp": ("assets/screens/catalogo.png", 255, 1078, 165, 90),
    "assets/images/catalogo/sollevatore-mop-150.webp": ("assets/screens/catalogo.png", 431, 1078, 164, 90),
    "assets/images/catalogo/stetoscopio-lit-3200.webp": ("assets/screens/catalogo.png", 605, 1078, 165, 90),
    "assets/images/catalogo/termometro-bra-nte300.webp": ("assets/screens/catalogo.png", 781, 1078, 164, 90),

    # Category hero variants and listing cards (categoria.html).
    "assets/images/categoria/diagnostica-hero-wide.webp": ("assets/screens/categoria.png", 656, 60, 880, 180),
    "assets/images/categoria/diagnostica-hero-desktop.webp": ("assets/screens/categoria.png", 936, 60, 600, 180),
    "assets/images/categoria/diagnostica-hero-mobile.webp": ("assets/screens/categoria.png", 1050, 60, 486, 189),
    "assets/images/categoria/ecografo-gima-20000.webp": ("assets/screens/categoria.png", 351, 455, 174, 110),
    "assets/images/categoria/elettrocardiografo-gima-20001.webp": ("assets/screens/categoria.png", 537, 455, 176, 110),
    "assets/images/categoria/monitor-gima-20002.webp": ("assets/screens/categoria.png", 724, 455, 176, 110),
    "assets/images/categoria/sistema-rx-gima-20003.webp": ("assets/screens/categoria.png", 911, 455, 176, 110),
    "assets/images/categoria/spirometro-gima-20004.webp": ("assets/screens/categoria.png", 1099, 455, 177, 110),
    "assets/images/categoria/defibrillatore-gima-20005.webp": ("assets/screens/categoria.png", 1288, 455, 178, 110),
    "assets/images/categoria/centrifuga-gima-20006.webp": ("assets/screens/categoria.png", 351, 711, 174, 110),
    "assets/images/categoria/microscopio-gima-20007.webp": ("assets/screens/categoria.png", 537, 711, 176, 110),
    "assets/images/categoria/analizzatore-gima-20008.webp": ("assets/screens/categoria.png", 724, 711, 176, 110),
    "assets/images/categoria/pulsossimetro-gima-20009.webp": ("assets/screens/categoria.png", 911, 711, 176, 110),
    "assets/images/categoria/sfigmomanometro-gima-20010.webp": ("assets/screens/categoria.png", 1099, 711, 177, 110),
    "assets/images/categoria/pompa-infusione-gima-20011.webp": ("assets/screens/categoria.png", 1288, 711, 178, 110),

    # Product gallery and alternatives (class and inline crop variables in prodotto.html).
    "assets/images/prodotto/gima-49876-vista-principale.webp": ("assets/screens/prodotto.png", 35, 101, 55, 55),
    "assets/images/prodotto/gima-49876-bracciale.webp": ("assets/screens/prodotto.png", 35, 164, 55, 55),
    "assets/images/prodotto/gima-49876-custodia.webp": ("assets/screens/prodotto.png", 35, 228, 55, 55),
    "assets/images/prodotto/gima-49876-confezione.webp": ("assets/screens/prodotto.png", 35, 291, 55, 55),
    "assets/images/prodotto/gima-49876-video.webp": ("assets/screens/prodotto.png", 35, 355, 55, 55),
    "assets/images/prodotto/sfigmomanometro-gima-49876.webp": ("assets/screens/prodotto.png", 102, 98, 281, 291),
    "assets/images/prodotto/sfigmomanometro-aneroide-gima-32750.webp": ("assets/screens/prodotto.png", 49, 1203, 68, 45),
    "assets/images/prodotto/sfigmomanometro-polso-gima-32912.webp": ("assets/screens/prodotto.png", 49, 1251, 68, 45),
    "assets/images/prodotto/sfigmomanometro-stativo-gima-32760.webp": ("assets/screens/prodotto.png", 49, 1304, 68, 45),

    # Quote-list thumbnails (class crop variables in lista-quotazione.html).
    "assets/images/lista-quotazione/defibrillatore-gima-35340.webp": ("assets/screens/lista-quotazione.png", 40, 328, 80, 80),
    "assets/images/lista-quotazione/lettino-gima-27441.webp": ("assets/screens/lista-quotazione.png", 40, 445, 80, 80),
    "assets/images/lista-quotazione/carrozzina-gima-43210.webp": ("assets/screens/lista-quotazione.png", 40, 563, 80, 80),
    "assets/images/lista-quotazione/monitor-gima-20000.webp": ("assets/screens/lista-quotazione.png", 40, 680, 80, 80),
}


def main() -> None:
    opened: dict[Path, Image.Image] = {}

    for output_name, (source_name, x, y, width, height) in CROPS.items():
        source = ROOT / source_name
        output = ROOT / output_name
        image = opened.setdefault(source, Image.open(source).convert("RGB"))
        right, bottom = x + width, y + height

        if x < 0 or y < 0 or right > image.width or bottom > image.height:
            raise ValueError(
                f"Crop {output_name} ({x}, {y}, {right}, {bottom}) exceeds "
                f"{source_name} ({image.width}x{image.height})"
            )

        output.parent.mkdir(parents=True, exist_ok=True)
        image.crop((x, y, right, bottom)).save(
            output,
            "WEBP",
            lossless=True,
            quality=100,
            method=6,
            exact=True,
        )
        print(f"{output.relative_to(ROOT)} ({width}x{height})")


if __name__ == "__main__":
    main()
