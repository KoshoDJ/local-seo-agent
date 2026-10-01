#!/usr/bin/env python3
"""Make the review QR code.

Encodes the /review FILTER FORM on our own site - never the Google review link
directly. That is the whole point: a QR on a truck or an invoice is scanned by
someone we cannot identify (no ?cid=), and if it went straight to Google then an
unhappy customer would land on the public review box with nothing in between.
Pointing it at /review means 4-5 stars still flow through to Google in one tap,
while 1-3 stars route to the owner instead. Writes two files:

    website/public/review-qr.png   - for print: invoices, counter cards, trucks
    website/public/review-qr.svg   - vector, scales to any size without blurring

Run it:
    Code/.venv/bin/python Code/make_review_qr.py

Or point it at any URL directly:
    Code/.venv/bin/python Code/make_review_qr.py https://automatable.co/review

Error correction is set to H (30% recoverable). That is deliberate - a QR on a
truck door or a greasy invoice gets scratched, wet and partly covered, and H is
the level that still scans when a chunk of it is gone.
"""

import re
import sys
from pathlib import Path

try:
    import segno
except ImportError:
    sys.exit(
        "segno is not installed. Run:\n"
        "  python3 -m venv Code/.venv && Code/.venv/bin/pip install segno\n"
        "then re-run this with Code/.venv/bin/python"
    )

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "website" / "lib" / "review.config.ts"
OUT_DIR = ROOT / "website" / "public"

# Ink from design/kit/tokens/colors.css (--ink-900). Deliberately NOT the kit's
# lime accent: lime on white is a light-on-light QR and phone scanners fail it.
# The rule for any QR is contrast first, brand second.
DARK = "#0e0f0c"
LIGHT = "#ffffff"  # white, not parchment: print needs maximum contrast


def url_from_config() -> str | None:
    """Build the /review URL from the site's own domain in site.config.ts.

    Deliberately NOT googleReviewUrl. The QR is the no-cid path from the spec:
    an anonymous scanner has to pass through our filter form, not skip it. It
    also means the printed sticker never goes stale - swap the Google link in
    review.config.ts and every QR already in the wild keeps working.
    """
    site = ROOT / "website" / "lib" / "site.config.ts"
    if not site.exists():
        return None
    match = re.search(r'url:\s*["\']([^"\']+)["\']', site.read_text(encoding="utf-8"))
    return match.group(1).rstrip("/") + "/review" if match else None


def main() -> int:
    url = sys.argv[1] if len(sys.argv) > 1 else url_from_config()

    if not url:
        print(
            "Could not work out the site URL.\n\n"
            "Fix it one of two ways:\n"
            "  1. Check `url:` is set in website/lib/site.config.ts, then re-run.\n"
            "  2. Or pass it straight in:  make_review_qr.py https://yoursite.com/review"
        )
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    qr = segno.make(url, error="h")

    png = OUT_DIR / "review-qr.png"
    svg = OUT_DIR / "review-qr.svg"

    # Scale is worked out from the code's own size so the PNG always lands
    # around 1,200px wide - that prints crisp at 4 inches / 300dpi, whatever
    # length of URL Google hands you.
    border = 4
    modules = qr.symbol_size(scale=1, border=border)[0]
    scale = max(8, round(1200 / modules))

    qr.save(png, scale=scale, border=border, dark=DARK, light=LIGHT)
    qr.save(svg, scale=scale, border=border, dark=DARK, light=LIGHT)

    print(f"QR code points at: {url}\n")
    print(f"  {png.relative_to(ROOT)}")
    print(f"  {svg.relative_to(ROOT)}")
    print("\nScan it with your own phone before printing anything.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
